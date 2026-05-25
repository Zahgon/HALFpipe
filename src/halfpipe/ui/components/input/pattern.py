# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

import logging
import os
from operator import attrgetter
from os import path as op
from threading import Event, Thread
from typing import Any

import inflect

from ....ingest.glob import (
    _scan_files_and_collect_tags,
    remove_tag_remainder_match,
    resolve,
    show_tag_suggestion_check,
    tag_parse,
    tokenize,
)
from ..keyboard import Key
from ..text import Text, TextElement, TextElementCollection
from ..view import CallableView
from .choice import SingleChoiceInputView
from .text import TextInputView, common_chars

logger = logging.getLogger("halfpipe.ui")
p = inflect.engine()


class NestedTextInputView(TextInputView):
    def __init__(self, parent_view: CallableView, *args, **kwargs):
        self.parent_view = parent_view
        super().__init__(*args, **kwargs)

    def update(self):
        self.parent_view.update()


class NestedSingleChoiceInputView(SingleChoiceInputView):
    def __init__(self, parent_view: CallableView, *args, **kwargs):
        self.parent_view = parent_view
        super().__init__(*args, **kwargs)

    def update(self):
        self.parent_view.update()


class FilePatternInputView(CallableView):
    def __init__(
        self,
        entities: list[str],
        required_entities: list[str] | None = None,
        entity_colors_list: list[str] | None = None,
        dironly=False,
        base_path=None,
        **kwargs,
    ):
        super(FilePatternInputView, self).__init__(**kwargs)
        self.text_input_view = NestedTextInputView(
            self,
            base_path,
            tokenizefun=self._tokenize,
            nchr_prepend=1,
            messagefun=self._messagefun,
            forbidden_chars="'\"'",
            maxlen=256,
        )
        self.suggestion_view = NestedSingleChoiceInputView(self, [], is_vertical=True, add_brackets=False)

        self.message: Text = TextElement("")
        self.message_is_dirty = False

        self.matching_files: list[Text] = []
        self.cur_dir = None
        self.cur_dir_files: list[str] = []
        self.dironly = dironly
        self.is_ok = False

        self.entities = entities
        if required_entities is None:
            required_entities = list()
        self.required_entities = required_entities
        if entity_colors_list is None:
            entity_colors_list = ["ired", "igreen", "imagenta", "icyan", "iyellow"]
        self.entity_colors_list = entity_colors_list
        self.color_by_tag: dict[str, Any] | None = None
        self.tag_suggestions: list[Text] = []
        self.is_suggesting_entities = False
        self.tab_pressed = False

        self._scan_thread: Thread | None = None
        self._is_scanning = True
        self._scan_requested_event = Event()
        self._scan_complete_event = Event()



    def show_message(self, msg):
        if isinstance(msg, Text):
            self.message = msg
        else:
            self.message = self._tokenize(msg, add_brackets=False)
        self.message_is_dirty = True




    def _tokenize(self, text, add_brackets=True):
        if add_brackets:
            text = f"[{text}]"

        tokens = tokenize.split(text)
        tokens = [token for token in tokens if token is not None]

        text_element_collection = TextElementCollection()

        for token in tokens:
            color = None

            matchobj = tag_parse.fullmatch(token)
            if matchobj is not None:
                tag_name = matchobj.group("tag_name")
                assert self.color_by_tag is not None
                color = self.color_by_tag.get(tag_name, self.highlight_color)

            text_element_collection.append(TextElement(token, color=color))

        return text_element_collection


    def setup(self):
        super(FilePatternInputView, self).setup()

        self.text_input_view._layout = self.layout
        self.text_input_view.setup()

        self.suggestion_view._layout = self.layout
        self.suggestion_view.setup()

        self.color_by_tag = {
            entity: self.layout.color.from_string(color_str)
            for entity, color_str in zip(self.entities, self.entity_colors_list, strict=False)
        }








    def draw_at(self, y):
        if y is not None:
            size: int = 0

            text_input_view_draw_size = self.text_input_view.draw_at(y + size)
            if isinstance(text_input_view_draw_size, int):
                size += text_input_view_draw_size

            suggestion_view_draw_size = self.suggestion_view.draw_at(y + size)
            if isinstance(suggestion_view_draw_size, int):
                size += suggestion_view_draw_size

            self._view_width = max(
                self._view_width,
                self.text_input_view._view_width,
                self.suggestion_view._view_width,
            )

            return size

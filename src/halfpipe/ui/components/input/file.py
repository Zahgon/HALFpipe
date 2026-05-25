# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

""" """

import os
from os import path as op

from ..file import get_dir, resolve
from ..keyboard import Key
from ..view import CallableView
from .choice import SingleChoiceInputView
from .text import TextInputView, common_chars


class FileInputView(CallableView):
    def __init__(self, base_path=None, exists=True, messagefun=None, **kwargs):
        super(FileInputView, self).__init__(**kwargs)
        self.text_input_view = TextInputView(base_path, messagefun=messagefun, forbidden_chars="'\"'", maxlen=256)
        self.text_input_view.update = self.update  # type: ignore
        self.suggestion_view = SingleChoiceInputView([], is_vertical=True, add_brackets=False)
        self.suggestion_view.update = self.update  # type: ignore

        self.matching_files = []
        self.cur_dir = None
        self.cur_dir_files = []
        self.exists = exists



    def setup(self):
        super(FileInputView, self).setup()
        self.text_input_view._layout = self.layout
        self.text_input_view.setup()
        self.suggestion_view._layout = self.layout
        self.suggestion_view.setup()







    def draw_at(self, y: int | None) -> int | None:
        if y is None:
            return None
        size = 0

        text_size = self.text_input_view.draw_at(y + size)
        if text_size is not None:
            size += text_size

        suggestion_size = self.suggestion_view.draw_at(y + size)
        if suggestion_size is not None:
            size += suggestion_size

        if self.text_input_view._view_width > self._view_width:
            self._view_width = self.text_input_view._view_width
        if self.suggestion_view._view_width > self._view_width:
            self._view_width = self.suggestion_view._view_width

        return size


class DirectoryInputView(FileInputView):


# -*- coding: utf-8 -*-


import copy
from abc import abstractmethod

import inflect
from textual import on
from textual.app import ComposeResult
from textual.containers import Grid, VerticalScroll
from textual.widget import Widget
from textual.widgets import (
    Button,
    Collapsible,
    ContentSwitcher,
)

from ...logging import logger
from ..data_analyzers.context import ctx
from ..general_widgets.custom_general_widgets import FocusLabel
from ..help_functions import widget_exists
from ..specialized_widgets.confirm_screen import Confirm
from .utils.name_input import NameInput

p = inflect.engine()


class TypeNameItem:
    """
    Represents an item with a type and a name.

    This class is a simple data structure used to store the type and name
    of an item, such as a feature or a model.

    Attributes
    ----------
    type : str
        The type of the item.
    name : str
        The name of the item.
    """

    def __init__(self, _type, name):
        self.type = _type
        self.name = name


class SelectionTemplate(Widget):
    """
    Base class for managing a selection of items (e.g., features, models).

    This widget provides a foundation for building user interface components
    that allow users to manage a list of items, including adding, deleting,
    renaming, and duplicating them. It uses a sidebar with collapsible
    sections to organize items by type and a content switcher to display
    the details of the selected item.

    Attributes
    ----------
    ITEM_MAP : dict[str, str]
        A dictionary mapping item types (keys) to their display names (values).
        This should be defined in subclasses.
    BINDINGS : list[tuple[str, str, str]]
        A list of key bindings for the widget.
    current_order : list[str]
        The current order of sorting for the items.
    ITEM_KEY : str | None
        The key used to access item-specific data in the cache.
        This should be defined in subclasses.
    SETTING_KEY : str | None
        An optional key used to access settings-specific data in the cache.
        This is only used in some subclasses.
    _id_counter : int
        A counter used to generate unique IDs for new items.
    feature_items : dict[str, TypeNameItem]
        A dictionary mapping item IDs to `TypeNameItem` objects.
    """

    ITEM_MAP: dict[str, str] = {}
    BINDINGS = [("a", "add_item", "Add"), ("d", "delete_feature", "Delete")]
    current_order = ["name", "type"]
    ITEM_KEY: None | str = None  # To be defined in child classes
    SETTING_KEY: None | str = None  # Optional, only used in some child classes

    def __init__(self, disabled=False, **kwargs) -> None:
        """
        Initializes the SelectionTemplate widget.

        This constructor sets up the widget's internal state, including the
        ID counter and the dictionary for tracking items.

        Note
        ----
        Each created widget needs to have a unique id, even after deletion it cannot be recycled.
        The id_counter takes care of this and feature_items dictionary keeps track of the id
        and number and feature name.

        Parameters
        ----------
        disabled : bool, optional
            Whether the widget is initially disabled, by default False.
        **kwargs
            Additional keyword arguments passed to the base class constructor.
        """

        super().__init__(disabled=disabled, **kwargs)

        self._id_counter = 0
        self.feature_items: dict = {}

    def compose(self) -> ComposeResult:
        """
        Creates the child widgets of the SelectionTemplate.

        This method constructs the layout of the widget, including the
        sidebar with buttons and collapsible sections, and the content
        switcher.

        Returns
        -------
        ComposeResult
            The result of composing the child widgets.
        """
        pass

    @on(Button.Pressed, "#sidebar .add_button")
    async def add(self) -> None:
        """
        Handles the "Add" button press event.

        This method is called when the user presses the "Add" button. It
        runs the `add_item` action.
        """
        await self.run_action("add_item")

    @on(Button.Pressed, "#sidebar .delete_button")
    async def delete(self) -> None:
        """
        Handles the "Delete" button press event.

        This method is called when the user presses the "Delete" button.
        It runs the `delete_item` action.
        """
        pass

    @on(Button.Pressed, "#sidebar .duplicate_button")
    async def duplicate(self) -> None:
        """
        Handles the "Duplicate" button press event.

        This method is called when the user presses the "Duplicate"
        button. It runs the `duplicate_item` action.
        """
        pass

    @on(Button.Pressed, "#sidebar .sort_button")
    async def sort(self) -> None:
        """
        Handles the "Sort" button press event.

        This method is called when the user presses the "Sort" button. It
        runs the `sort_features` action.
        """
        await self.run_action("sort_features")

    def _delete_item(self, respond: bool, check_aggregate: bool = False) -> None:
        """
        Deletes an item and its associated data.

        This method is called to delete an item from the widget and remove
        its data from the cache. It is called after the user confirms the
        deletion in the `Confirm` modal.

        Parameters
        ----------
        respond : bool
            Whether the user confirmed the deletion.
        check_aggregate : bool, optional
            Whether to check for and delete associated aggregate models,
            by default False.
        """
        pass

    def action_delete_item(self) -> None:
        """
        Deletes the currently selected item.

        This method is called to delete the currently selected item. It
        pushes a `Confirm` modal to the screen to ask the user for
        confirmation before deleting the item. It unmount the item widget and
        delete its entry from dictionaries.
        """
        pass

    @abstractmethod
    def action_add_item(self) -> None:
        raise NotImplementedError()

    async def add_new_item(self, new_item: tuple | bool) -> None:
        """
        Adds a new item to the widget.

        This method adds a new item to the widget, either by creating a
        new entry or by loading an existing one from the cache. It
        mounts a new widget for the item and updates the sidebar and
        content switcher.

        Note
        ----
        Principle of adding a new feature lies in mounting a new widget while creating a
        new entry in the dictionary to keep track of the selections which are later dumped
        into the Context object. If this is a load or a duplication, then new entry is
        not created but read from the dictionary. The dictionary entry was created elsewhere.

        Parameters
        ----------
        new_item : tuple[str, str] | list[str, str] | bool
            A tuple or list containing the item type and name, or False if
            the item creation was canceled.
        """
        if isinstance(new_item, tuple) or isinstance(new_item, list):
            item_type, item_name = new_item
            content_switcher_item_new_id = p.singular_noun(self.ITEM_KEY) + "_item_" + str(self._id_counter)
            collapsible_item_new_id = content_switcher_item_new_id + "_flabel"
            logger.debug(
                f"UI->SelectionTemplate.add_new_item: item_type:{item_type}, item_name:{item_name}, \
content_switcher_item_new_id:{content_switcher_item_new_id}, collapsible_item_new_id:{collapsible_item_new_id}"
            )

            self.feature_items[content_switcher_item_new_id] = TypeNameItem(item_type, item_name)
            item_key = self.feature_items[content_switcher_item_new_id].type

            new_content_item = self.fill_cache_and_create_new_content_item(new_item)
            # Deselect previous FocusLabel if exists
            content_switcher_item_old_id = self.get_widget_by_id("content_switcher").current
            if content_switcher_item_old_id is not None:
                collapsible_item_old_id = content_switcher_item_old_id + "_flabel"
                if widget_exists(self, collapsible_item_old_id):
                    self.get_widget_by_id(collapsible_item_old_id).deselect()

            new_list_item = FocusLabel(item_name, id=collapsible_item_new_id)  # classes="labels " + item_type)
            if not widget_exists(self, "list_" + item_key):
                await self.get_widget_by_id("sidebar").mount(
                    Collapsible(title=self.ITEM_MAP[item_key], id="list_" + item_key, classes="list", collapsed=False)
                )
                await self.reorder_collapsibles()
            await self.get_widget_by_id("list_" + item_key).query_one(Collapsible.Contents).mount(new_list_item)
            self.get_widget_by_id("list_" + item_key).collapsed = False
            self.get_widget_by_id("list_" + item_key).styles.visibility = "visible"
            await self.get_widget_by_id("content_switcher").mount(new_content_item)
            self.get_widget_by_id("content_switcher").current = content_switcher_item_new_id
            self.get_widget_by_id("content_switcher").border_title = "{}: {}".format(
                self.ITEM_MAP[item_key].replace("\n", " "),
                self.feature_items[content_switcher_item_new_id].name,
            )
            self._id_counter += 1

    async def reorder_collapsibles(self):
        container = self.get_widget_by_id("sidebar")
        # Get all Collapsible children
        collapsibles: list[Collapsible] = container.walk_children(Collapsible)

        unsorted_id_list = [w.id for w in collapsibles]
        sorted_ids_template = ["list_" + f for f in self.ITEM_MAP]

        index = {val: i for i, val in enumerate(sorted_ids_template)}

        def position(val):
            return index[val]

        for i in range(1, len(unsorted_id_list)):
            for j in range(i):
                # If the current element is "earlier" in sorted_ids_template than the one before it in unsorted_id_list
                if position(unsorted_id_list[i]) < position(unsorted_id_list[j]):
                    container.move_child(collapsibles[i], before=collapsibles[j])
                    break

    async def action_duplicate_item(self):
        """
        Duplicates the currently selected item.

        This method duplicates the currently selected item, including its
        data in the cache. It then adds the duplicated item to the widget.
        It prompts the user for a new name for the duplicated item using a
        `NameInput` modal.
        """
        pass

    @on(Button.Pressed, "#sidebar .rename_button")
    async def action_rename_item(self) -> None:
        """
        Renames the currently selected item.

        This method renames the currently selected item, including its
        data in the cache. It pushes a `NameInput` modal to the screen to
        get the new name from the user.
        """
        pass

    def on_focus_label_selected(self, message: FocusLabel.Selected) -> None:
        """Changes border title color according to the feature type."""
        pass

    def fill_cache_and_create_new_content_item(self, new_item: tuple[str, str] | list[tuple[str, str]]) -> Widget:
        """
        Fills the cache and creates a new content item.

        This method is a placeholder for subclasses to implement. It
        should fill the cache with the data for the new item and create
        the corresponding widget to display the item's content.

        Parameters
        ----------
        new_item : tuple[str, str] | list[str, str]
            A tuple or list containing the item type and name.

        Returns
        -------
        Widget
        """

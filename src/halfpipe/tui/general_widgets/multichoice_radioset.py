# -*- coding: utf-8 -*-
from dataclasses import dataclass

import numpy as np
from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal, ScrollableContainer
from textual.message import Message
from textual.widget import Widget
from textual.widgets import Button, Label, RadioButton

from ..specialized_widgets.confirm_screen import Confirm
from .draggable_modal_screen import DraggableModalScreen

# !!!This must be before importing the RadioSet to override the RadioButton imported by the RadioSet!!!
RadioButton.BUTTON_INNER = "X"
from textual.widgets import RadioSet  # noqa: E402


class MultipleRadioSet(Widget):
    """
    A widget that creates a set of radio buttons arranged in a table format.

    This widget arranges radio buttons in a table-like structure, with
    options specified by horizontal and vertical label sets. It allows
    users to select one radio button per row.

    Attributes
    ----------
    horizontal_label_set : list[str]
        The list of labels for the horizontal radio button groups.
    vertical_label_set : list[str]
        The list of labels for the vertical radio button groups.
    default_value_column : int
        The index of the column that should be selected by default.
    unique_first_column : bool
        If True, ensures that only one radio button in the first column
        can be selected across all rows.
    last_unique_selection : str
        The ID of the last selected row when `unique_first_column` is True.

    Events
    ------
    Changed
        Posted when a radio button selection changes.

    Methods
    -------
    __init__(id, classes, horizontal_label_set, vertical_label_set, default_value_column, unique_first_column)
        Initializes the widget with optional ID, classes, horizontal and
        vertical label sets.
    compose() -> ComposeResult
        Composes the widget by generating a table of radio buttons labeled
        by the horizontal and vertical labels provided.
    on_mount()
        Called when the widget is initialized to set the widths and
        alignment of radio buttons.
    get_selections() -> dict[str, list[bool]]
        Retrieves the currently selected radio buttons for each row.
    on_radio_set_changed(message)
        Handles the event when a radio button selection changes.
    """

    @dataclass
    class Changed(Message):
        multiple_radio_set: "MultipleRadioSet"
        row: int
        column: int

        @property
        def control(self):
            """Alias for self.file_browser."""
            pass

    def __init__(
        self,
        id: str | None = None,
        classes: str | None = None,
        horizontal_label_set: None | list = None,
        vertical_label_set: None | list = None,
        default_value_column: int = 0,
        unique_first_column=False,
        default_values: list[int] | None = None,
    ):
        """
        Initializes the MultipleRadioSet widget.

        Parameters
        ----------
        id : str, optional
            An identifier for the widget instance, by default None.
        classes : str, optional
            Space-separated list of style class names, by default None.
        horizontal_label_set : list[str], optional
            List of labels for the horizontal radio buttons, by default
            pre-defined labels.
        vertical_label_set : list[str], optional
            List of labels for the vertical radio buttons, by default
            pre-defined labels.
        default_value_column : int, optional
            The index of the column that should be selected by default,
            by default 0.
        unique_first_column : bool, optional
            If True, ensures that only one radio button in the first
            column can be selected across all rows, by default False.
        """
        super().__init__(id=id, classes=classes)
        self.horizontal_label_set = (
            horizontal_label_set
            if horizontal_label_set is not None
            else ["h_label1", "h_lab2", "h_long_label3", "4", "h_label5"]
        )
        self.horizontal_label_set[-1] = self.horizontal_label_set[-1] + "  "
        self.vertical_label_set = (
            vertical_label_set if vertical_label_set is not None else ["v_label1", "v_long_label2", "v_label3", "v_label4"]
        )
        self.default_value_column = default_value_column
        self.unique_first_column = unique_first_column
        self.last_unique_selection = "row_radio_sets_0"
        self.default_values = default_values

    def compose(self) -> ComposeResult:
        """
        Constructs the layout of the widget with horizontal and vertical labels.

        This method creates the table structure by adding horizontal and
        vertical labels and the corresponding radio buttons.

        Yields
        ------
        ComposeResult
            The composed widgets for the `MultipleRadioSet`.
        """
        pass

    def on_mount(self):
        """
        Configures the width and content alignment of each radio button.

        This method is called after the widget is mounted to set the
        width and content alignment of each radio button based on the
        length of the horizontal labels.
        """
        pass

    def get_selections(self):
        """
        Retrieves the currently selected radio buttons for each row.

        Returns
        -------
        dict[str, list[bool]]
            A dictionary mapping each vertical label to its selected radio
            button values.
        """
        pass

    @on(RadioSet.Changed)
    def on_radio_set_changed(self, message):
        """
        Handles the event when a radio button selection changes.

        This method is called when a radio button within a `RadioSet` is
        selected. It manages the logic for `unique_first_column` and
        posts a `Changed` message.

        Parameters
        ----------
        message : RadioSet.Changed
            The message object containing information about the radio
            button selection change.
        """
        pass


class MultipleRadioSetModal(DraggableModalScreen):
    """
    A modal dialog that allows the user to assign field maps to functional images.

    This modal dialog uses a set of horizontally and vertically labeled
    radio buttons to allow the user to make selections. It includes an
    'OK' button to submit the selections.

    Attributes
    ----------
    CSS_PATH : list[str]
        List of CSS files to be used for styling.
    title : str
        The title of the modal dialog.
    horizontal_label_set : list[str]
        The labels to be used for the horizontal radio button set.
    vertical_label_set : list[str]
        The labels to be used for the vertical radio button set.

    Methods
    -------
    __init__(title, id, classes, width, horizontal_label_set, vertical_label_set)
        Initializes the modal with a title, ID, classes, width, and label sets.
    on_mount()
        Asynchronously mounts the main content and UI elements in the modal.
    ok()
        Event handler for the 'OK' button which captures the selections made
        by the user and then dismisses the modal.
    """

    def __init__(
        self,
        title="Field maps to functional images",
        id: str | None = None,
        classes: str | None = None,
        width=None,
        horizontal_label_set: None | list = None,
        vertical_label_set: None | list = None,
    ) -> None:
        """
        Initializes the modal with a title, ID, classes, width, and label sets.

        Parameters
        ----------
        title : str, optional
            The title of the modal dialog, by default "Field maps to
            functional images".
        id : str | None, optional
            The unique identifier for this modal instance, by default None.
        classes : str | None, optional
            Additional CSS classes to style this modal, by default None.
        width : int | None, optional
            The width of the modal, by default None.
        horizontal_label_set : list[str] | None, optional
            The labels to be used for the horizontal radio button set,
            by default None.
        vertical_label_set : list[str] | None, optional
            The labels to be used for the vertical radio button set,
            by default None.
        """
        super().__init__(id=id, classes=classes)
        self.title_bar.title = title
        self.horizontal_label_set = (
            horizontal_label_set
            if horizontal_label_set is not None
            else ["h_label1", "h_lab2", "h_long_label3", "4", "h_label5"]
        )
        self.vertical_label_set = (
            vertical_label_set if vertical_label_set is not None else ["v_label1", "v_long_label2", "v_label3", "v_label4"]
        )




# """Example for testing"""
# from textual.app import App, ComposeResult
#
# class Main(App):
#     """
#     Class for testing.
#
#     Attributes
#     ----------
#     CSS_PATH : str
#         Path to the CSS file to be used for styling.
#
#     Methods
#     -------
#     compose():
#         Defines the components to be rendered by the application.
#
#     on_button_show_modal_pressed(self):
#         Event handler for the button with id 'show_modal' to display a modal with multiple radio sets.
#
#     on_button_pressed(self):
#         Event handler for the button with id 'ok' to query and process the current radio set selections.
#     """
#
#     CSS_PATH = "tcss/radio_set_changed.tcss"
#
#     def compose(self):
#         yield Button("OK", id="ok")
#         yield Button("Mount modal", id="show_modal")
#         yield MultipleRadioSet(default_values=[0,1,2,3])
#
#     @on(Button.Pressed, "#show_modal")
#     def on_button_show_modal_pressed(self):
#         self.app.push_screen(
#             MultipleRadioSetModal(
#                 horizontal_label_set=[
#                     "h_label1",
#                     "h_lab2",
#                     "h_long_label3\n_long_label3----\n_long_label3",
#                     "4",
#                     "h_label5",
#                     "h_label5",
#                     "4",
#                     "h_label5",
#                     "h_label5",
#                     "h_label5",
#                 ],
#                 vertical_label_set=["v_label1", "v_long_label2", "v_label3", "v_label4", "v_label222222222222222224"],
#             )
#         )
#
#     @on(Button.Pressed, "#ok")
#     def on_button_pressed(self):
#         selections = self.query_one(MultipleRadioSet).get_selections()
#         print(selections)
#
# if __name__ == "__main__":
#     app = Main()
#     app.run()

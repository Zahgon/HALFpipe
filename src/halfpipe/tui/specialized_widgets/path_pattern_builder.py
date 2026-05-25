# -*- coding: utf-8 -*-

import re
from typing import Any

from rich.text import Text
from textual import events, on, work
from textual.containers import Container, Grid, Horizontal
from textual.widgets import Button, Static

from ...ingest.glob import resolve_path_wildcards, tag_glob
from ...logging import logger
from ..data_analyzers.context import ctx
from ..data_analyzers.file_pattern_steps import AddAtlasImageStep, AddBinarySeedMapStep, AddSpatialMapStep, EventsStep
from ..general_widgets.draggable_modal_screen import DraggableModalScreen
from ..general_widgets.list_of_files_modal import ListOfFiles
from ..specialized_widgets.file_browser_modal import FileBrowserModal, path_test_with_isfile_true
from ..templates.utils.name_input import NameInput
from .confirm_screen import Confirm
from .pattern_suggestor import InputSegmentHighlightingWithUpDownArrows, InputWithColoredSuggestions, SegmentHighlighting


# utilities for the widget
def convert_validation_error_to_string(error: Any) -> str:
    """
    Converts a validation error object to a string.

    This function takes a validation error object (typically from a
    library like Marshmallow) and converts it into a human-readable
    string. It extracts the field names and their associated error
    messages and formats them into a single string.

    Parameters
    ----------
    error : Any
        The validation error object.

    Returns
    -------
    str
        A string containing the formatted validation error messages.
    """
    pass


def check_wrapped_tags(path: str, tags: list[str]) -> bool:
    """
    Checks if any of the specified tags are wrapped in curly braces in the given path.

    This function uses a regular expression to search for any of the
    provided tags within curly braces in the input path.

    Parameters
    ----------
    path : str
        The path string to search within.
    tags : list[str]
        A list of tags to search for.

    Returns
    -------
    bool
        True if any of the tags are found wrapped in curly braces,
        False otherwise.
    """
    pass


class ColorButton(Button):
    """
    A button widget that sets the current highlighting color.

    This class extends the `Button` widget to provide a button that,
    when clicked, sets the highlight color of a specified widget.

    Attributes
    ----------
    color : str
        The color associated with the button, used for styling the
        background.

    Methods
    -------
    __init__(color, *args, **kwargs)
        Initializes the ColorButton with a specified color.
    on_click(event)
        Handles the click event and sets the highlight color of a
        specific widget.
    """

    def __init__(self, color: str, *args: Any, **kwargs: Any) -> None:
        """
        Initializes the ColorButton with a specified color.

        Parameters
        ----------
        color : str
            The color associated with the button.
        *args : Any
            Additional positional arguments passed to the base class
            constructor.
        **kwargs : Any
            Additional keyword arguments passed to the base class
            constructor.
        """
        super().__init__(*args, **kwargs)
        self.color = color
        self.styles.background = color
        self.status = "on"

    async def on_click(self, event: events.Click) -> None:
        """
        Handles the click event and sets the highlight color of a specific widget.

        This method is called when the button is clicked. It retrieves
        the widget with the ID "input_prompt" and sets its `highlight_color`
        attribute to the color associated with this button.

        Parameters
        ----------
        event : events.Click
            The click event.
        """
        pass
        #     self.status = 'on'
        # elif self.status == 'on':
        #     self.status = 'off'
        #     path_widget.change_highlight_color('default')


class PathPatternBuilder(DraggableModalScreen):
    """
    A modal screen for interactively building file path patterns.

    This class provides a modal screen that allows users to interactively
    specify file path patterns. It includes color buttons to switch
    between highlight colors, an input field for the path, edit buttons,
    and "Ok" and "Cancel" buttons. The key component is the
    `InputWithColoredSuggestions` widget, which allows for string
    highlighting and pattern suggestions.

    Attributes
    ----------
    title_bar : TitleBar
        The title bar of the modal screen.
    path : str
        The initial file path provided.
    highlight_colors : list[str]
        A list of colors available for highlighting.
    labels : list[str]
        A list of labels used for tagging and identifying segments of the
        path.
    pattern_match_results : dict[str, Any]
        A dictionary that stores the current pattern, feedback message,
        and matched files.
    original_value : str
        The original file path value before user modifications.
    mandatory_tag : str
        A mandatory tag that needs to be present in the path pattern.
    pattern_class : Any
        The class used for creating file pattern steps.

    Methods
    -------
    __init__(path, highlight_colors, labels, title, pattern_class, *args, **kwargs)
        Initializes the PathPatternBuilder.
    on_mount()
        Called when the modal is mounted.
    deactivate_pressed_button()
        Deactivates the currently active button.
    activate_pressed_button(_id)
        Activates the button with the given ID.
    open_browse_window()
        Opens a file browser modal window.
    update_input(selected_path)
        Updates the input prompt with the selected path.
    reset_highlights()
        Resets all highlights in the input prompt.
    reset_all()
        Resets all data and highlights in the input prompt.
    submit_highlights()
        Submits the highlighted path for processing.
    _segment_highlighting_submitted(event)
        Updates pattern_match_results based on the output of various
        methods.
    activate_and_deactivate_press(event)
        Activates and deactivates buttons based on the pressed event.
    _ok(event)
        Confirms the selected pattern and dismisses the modal if valid.
    _ok_part_two()
        Confirms the selected pattern and dismisses the modal if valid.
    _close(event)
        Closes the modal without taking action.
    _remove_self()
        Displays a list of files matching the current pattern.
    on_key(event)
        Handles keyboard input to navigate and toggle highlights.
    key_enter()
        Submits the current path pattern when Enter is pressed.
    key_escape()
        Dismisses the modal when Escape is pressed.
    """

    def __init__(
        self,
        path: str | Text,
        highlight_colors=None,
        labels=None,
        title="X",
        pattern_class=None,
        *args,
        **kwargs,
    ) -> None:
        """
        Initializes the PathPatternBuilder.

        Parameters
        ----------
        path : str | Text
            The initial file path.
        highlight_colors : list[str], optional
            A list of colors available for highlighting, by default None.
        labels : list[str], optional
            A list of labels used for tagging, by default None.
        title : str, optional
            The title of the modal, by default "X".
        pattern_class : Any, optional
            The class used for creating file pattern steps, by default
            None.
        *args : Any
            Additional positional arguments passed to the base class
            constructor.
        **kwargs : Any
            Additional keyword arguments passed to the base class
            constructor.
        """
        super().__init__(*args, **kwargs)
        self.title_bar.title = title
        self.path = path.plain if isinstance(path, Text) else path
        self.highlight_colors = ["red", "green", "blue", "yellow", "magenta"] if highlight_colors is None else highlight_colors
        self.labels = ["subject", "Session", "Run", "Acquisition", "task"] if labels is None else labels

        self.pattern_match_results: dict = {
            "file_pattern": self.path,
            "message": "Found 0 files.",
            "files": [],
            "file_tag": None,
        }
        self.original_value = path
        # TODO: since now we are always passing the particular pattern_class to the path_pattern_builder, we do not need
        # to pass colors and labels separately, thus this needs to be cleaned through the whole code
        self.pattern_class = pattern_class
        self.mandatory_tags = [f"{{{label}}}" for label in pattern_class.required_entities]  # f"{{{self.labels[0]}}}"
        self.manual_tag_entity = pattern_class.tag_entity

        self.active_button_id = None

    def on_mount(self) -> None:
        """
        Called when the modal is mounted.

        This method is called when the modal is mounted. It initializes
        the UI components, including color buttons, the path input field,
        and action buttons.
        """
        pass

    @on(Button.Pressed, "#browse_button")
    def open_browse_window(self) -> None:
        """Opens a file browser modal window."""
        pass

    def update_input(self, selected_path: str) -> None:
        """
        Updates the input prompt with the selected path.

        Parameters
        ----------
        selected_path : str
            The selected path.
        """
        if selected_path is not None:
            self.get_widget_by_id("input_prompt").value = str(selected_path)
            self.get_widget_by_id("input_prompt").original_value = str(selected_path)

    @on(Button.Pressed, "#reset_button")
    def reset_highlights(self) -> None:
        """Resets all highlights in the input prompt."""
        pass

    @on(Button.Pressed, "#reset_all")
    def reset_all(self) -> None:
        """Resets all data and highlights in the input prompt."""
        pass

    @on(Button.Pressed, "#clear_all")
    def clear_all(self) -> None:
        """Clears the input prompt."""
        pass

    @on(Button.Pressed, "#submit_button")
    def submit_highlights(self) -> None:
        """Submits the highlighted path for processing."""
        pass

    @on(InputWithColoredSuggestions.Changed)
    @on(SegmentHighlighting.Submitted)
    @on(SegmentHighlighting.Changed)
    def _segment_highlighting_submitted(self, event) -> None:
        """
        Updates pattern_match_results based on the output of various methods.

        This method is called when the input value changes or when a
        segment is highlighted and submitted. It updates the
        `pattern_match_results` dictionary with the new file pattern,
        feedback message, and list of files.

        Parameters
        ----------
        event : InputWithColoredSuggestions.Changed | SegmentHighlighting.Submitted | SegmentHighlighting.Changed
            The event object containing information about the change.
        """
        pass

    @on(Button.Pressed, ".color_buttons")
    def activate_and_deactivate_press(self, event: Button.Pressed) -> None:
        """
        Activates and deactivates buttons based on the pressed event.

        This method is called when a color button is pressed. It
        deactivates the currently active button and activates the pressed
        button.

        Parameters
        ----------
        event : Button.Pressed
            The button pressed event.
        """
        pass

    @on(Button.Pressed, "#ok_button")
    async def _ok(self, event: Button.Pressed) -> None:
        """
        Confirms the selected pattern and dismisses the modal if valid.

        This method is called when the user presses the "Ok" button. It
        validates the selected file pattern and dismisses the modal if
        the pattern is valid. If the pattern is invalid, it displays an
        error message.

        Parameters
        ----------
        event : Button.Pressed
            The button pressed event.
        """
        pass

    @work(exclusive=True, name="fill_ctx_spec")
    async def _ok_part_two(self) -> None:
        """
        Confirms the selected pattern and dismisses the modal if valid.

        This method is called after the initial validation in `_ok`. It
        checks if the mandatory tag is present in the file pattern and
        dismisses the modal if the pattern is valid. If the mandatory
        tag is missing, it displays an error message.
        """
        pass


    @on(Button.Pressed, "#cancel_button")
    def _close(self, event: Button.Pressed) -> None:
        """
        Closes the modal without taking action.

        This method is called when the user presses the "Cancel" button. It
        dismisses the modal without taking any action.

        Parameters
        ----------
        event : Button.Pressed
            The button pressed event.
        """
        pass

    @on(Button.Pressed, "#show_button")
    def _remove_self(self) -> None:
        """
        Displays a list of files matching the current pattern.

        This method is called when the user presses the "Show" button. It
        opens the `ListOfFiles` modal to display the list of files found
        using the current file pattern.
        """
        pass

    #
    # async def on_key(self, event: events.Key) -> None:
    #     """
    #     Handles keyboard input to navigate and toggle highlights.
    #
    #     This method is called when a key is pressed. It handles keyboard
    #     input to navigate and toggle highlights in the input prompt.
    #
    #     Parameters
    #     ----------
    #     event : events.Key
    #         The key pressed event.
    #     """
    #     path_widget = self.get_widget_by_id("input_prompt")
    #     if event.key in ["1", "2", "3", "4", "5"]:
    #         # Set highlight color based on key pressed.
    #         index = int(event.key) - 1
    #         path_widget.highlight_color = self.highlight_colors[index]
    #         self.deactivate_pressed_button()
    #         self.activate_pressed_button("button_" + self.labels[index])

    def key_enter(self) -> None:
        """
        Submits the current path pattern when Enter is pressed.

        This method is called when the user presses the Enter key. It
        submits the current path pattern for processing.
        """
        pass

    def key_escape(self) -> None:
        """
        Dismisses the modal when Escape is pressed.

        This method is called when the user presses the Escape key. It
        dismisses the modal.
        """
        pass

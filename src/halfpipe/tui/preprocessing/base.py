# -*- coding: utf-8 -*-

from copy import deepcopy

from textual import on, work
from textual.app import ComposeResult
from textual.containers import Container, Grid, Horizontal, Vertical
from textual.message import Message
from textual.widget import Widget
from textual.widgets import Button, Input, Static, Switch

from ...model.file.base import File
from ..data_analyzers.context import ctx
from ..data_analyzers.meta_data_steps import CheckBoldSliceEncodingDirectionStep
from ..general_widgets.custom_general_widgets import LabelledSwitch, SwitchWithInputBox
from ..general_widgets.custom_switch import TextSwitch
from ..help_functions import widget_exists
from ..standards import global_settings_defaults


class Preprocessing(Widget):
    """
    A widget for configuring preprocessing settings.

    This widget provides a user interface for configuring various
    preprocessing steps, including anatomical and functional settings. Moreover,
    an advanced settings are available if needed.

    Attributes
    ----------
    default_settings : dict[str, Any]
        Default settings for preprocessing operations.

    Methods
    -------
    __init__(id, classes)
        Initializes the Preprocessing widget.
    compose() -> ComposeResult
        Composes the widget's components.
    _on_advanced_settings_switch_switch_changed(message)
        Handles changes in the advanced settings switch.
    _on_via_algorithm_switch_changed(message)
        Handles changes in the "Detect non-steady-state via algorithm" switch.
    on_run_reconall_switch_changed(message)
        Handles changes in the "Run recon all" switch.
    on_time_slicing_switch_changed(message)
        Handles changes in the "Turn on slice timing" switch.
    callback_func(message_dict)
        Callback function to handle messages from the FilePattern or
        CheckMetaData classes.
    _add_slice_timing_from_file(path)
        Adds slice timing information from a file (currently a TODO).
    _on_edit_vols_to_remove_button_pressed()
        Handles the "Edit" button press for setting initial volumes to remove.
    """

    def __init__(self, id: str | None = None, classes: str | None = None) -> None:
        """
        Initializes the Preprocessing widget.

        Parameters
        ----------
        id : str, optional
            An optional identifier for the widget, by default None.
        classes : str, optional
            An optional string of classes for applying styles to the
            widget, by default None.
        """
        super().__init__(id=id, classes=classes)
        # To overriding the default settings is done only when loading from a spec file. To do this, this attribute needs
        # firstly to be redefined and then the widget recomposed as is done in the working_directory widget.
        self._global_settings_defaults = deepcopy(global_settings_defaults)

        ctx.spec.global_settings.setdefault(self._global_settings_defaults["dummy_scans"])
        ctx.spec.global_settings.setdefault(self._global_settings_defaults["run_reconall"])
        ctx.spec.global_settings.setdefault(self._global_settings_defaults["slice_timing"])
        ctx.spec.global_settings.setdefault(self._global_settings_defaults["skull_strip_algorithm"])

        # self.default_settings = {"run_reconall": False, "slice_timing": False,
        # "via_algorithm_switch": False, "dummy_scans": 0}

    def compose(self) -> ComposeResult:
        """
        Composes the widget's components.

        This method defines the layout and components of the widget,
        including anatomical settings, functional settings, advanced
        settings, and debug settings.

        Yields
        ------
        ComposeResult
            The composed widgets.
        """
        pass




    @on(Switch.Changed, "#advanced_settings_switch")
    async def _on_advanced_settings_switch_switch_changed(self, message):
        """
        Handles changes in the advanced settings switch.

        This method is called when the state of the advanced settings
        switch changes. It shows or hides the advanced settings panels
        based on the switch state.

        Parameters
        ----------
        message : Switch.Changed
            The message object containing information about the switch
            state change.
        """
        pass
            # self.get_widget_by_id("workflowgroup_settings").styles.visibility = "hidden"
            # self.get_widget_by_id("debuggroup_settings").styles.visibility = "hidden"
            # self.get_widget_by_id("rungroup_settings").styles.visibility = "hidden"

    @on(Switch.Changed, "#via_algorithm_switch")
    def _on_via_algorithm_switch_changed(self, message):
        """
        Handles changes in the "Detect non-steady-state via algorithm" switch.

        This method is called when the state of the "Detect non-steady-state
        via algorithm" switch changes. It updates the UI and the
        application's context based on the switch state. For manual option,
        an input modal is raised.

        Parameters
        ----------
        message : Switch.Changed
            The message object containing information about the switch
            state change.
        """
        pass
            # raise imedietely the modal
            # self._on_edit_vols_to_remove_button_pressed()

    @on(Switch.Changed, "#run_reconall")
    def on_run_reconall_switch_changed(self, message: Message):
        """
        Handles changes in the "Turn on slice timing" switch.

        This method is called when the state of the "Turn on slice timing"
        switch changes. It updates the UI and the application's context
        based on the switch state.
        Parameters
        ----------

        message : Switch.Changed
            The message object containing information about the switch
            state change.
        """
        pass

    @on(Switch.Changed, "#skull_strip_algorithm")
    def on_skull_strip_algorithm_switch_changed(self, message: Message):
        """
        Handles changes in the "Skull strip algorithm" switch.

        This method is called when the state of the "Skull strip algorithm"
        switch changes. It updates the UI and the application's context
        based on the switch state.

        Parameters
        ----------

        message : Switch.Changed
            The message object containing information about the switch
            state change.
        """
        pass



    def callback_func(self, message_dict: dict):
        """
        The callback function is passed to the FilePattern or CheckMetaData classes where they gather all of the messages
        so that the user can view them again.

        Parameters
        ----------
        message_dict : dict
            Dictionary containing key-value pairs where keys are strings
            and values are lists of strings. This dictionary is used to
            generate a formatted string with the key and concatenated
            values for each entry.
        """
        pass

    def _add_slice_timing_from_file(self, path: str):
        """
        Adds slice timing information from a file (currently a TODO).

        This method is intended to allow users to specify slice timing
        information from a file, but it is currently not implemented.

        Parameters
        ----------
        path : str
            The path to the file containing slice timing information.
        """
        pass


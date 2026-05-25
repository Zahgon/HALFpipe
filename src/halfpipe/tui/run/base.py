# -*- coding: utf-8 -*-
# ok (more-less) to review

import json
import os
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from textual import on, work
from textual.app import ComposeResult
from textual.containers import Horizontal, HorizontalScroll, ScrollableContainer
from textual.message import Message
from textual.widget import Widget
from textual.widgets import Button, Input, Label, Pretty, RadioButton, Select, Static, TextArea
from textual.worker import Worker, WorkerState

from ...cli.run import run_stage_workflow
from ...model.spec import SpecSchema, save_spec
from ..data_analyzers.context import ctx
from ..general_widgets.custom_switch import TextSwitch
from ..general_widgets.draggable_modal_screen import DraggableModalScreen
from ..help_functions import with_loading_modal
from ..save import dump_dict_to_contex
from ..specialized_widgets.confirm_screen import Confirm
from ..specialized_widgets.quit_modal import quit_modal

# from ..standards import opts

# !!!This must be before importing the RadioSet to override the RadioButton imported by the RadioSet!!!
RadioButton.BUTTON_INNER = "X"


@dataclass
class BatchOptions:
    workdir: Path | None | str = None
    use_cluster: bool = True
    nipype_omp_nthreads: int = 1
    nipype_n_procs: int = 1
    # choose which intermediate files to keep
    keep: list[str] = field(default_factory=lambda: ["some"])
    # exclude subjects that match
    subject_exclude: list[str] = field(default_factory=list)
    # include only subjects that match
    subject_include: list[str] = field(default_factory=list)
    # select subjects that match
    subject_list: str | None = None
    fs_license_file: Path | None = None
    nipype_resource_monitor: bool = False
    watchdog: bool = False
    verbose: bool = False
    fs_root: str | None = None
    spec_path: str | None = None
    bids_database_dir: str | None = None

    def validate(self):
        valid_keep = ["all", "some"]
        for val in self.keep:
            if val not in valid_keep:
                raise ValueError(f"Invalid value for keep: {val}")


class IntOnlyInput(Input):
    async def validate(self) -> bool | str:
        return True if self.value.strip().isdigit() else "Must be an integer."


class PathOnlyInput(Input):
    async def validate(self) -> bool | str:
        return True if (isinstance(self.value, str) and self.value != "") else "Must be a string."


class CSVTextArea(TextArea):
    async def validate(self) -> bool | str:
        raw = self.text.strip()

        if not raw:
            return True

        # Split by comma and strip spaces
        items = [item.strip() for item in raw.split(",")]

        # Allow trailing comma → last item may be empty
        if items[-1] == "":
            items = items[:-1]  # drop empty last item

        # Ensure at least one non-empty string
        if not items or any(i == "" for i in items):
            return "Must be a single string or comma-separated strings."

        return True


class BatchOptionModal(DraggableModalScreen):
    def __init__(self) -> None:
        """
        Initializes the ContrastTableInputWindow instance.

        Parameters
        ----------
        table_row_index : dict[str, str]
            A dictionary representing the row index of the contrast table,
            where keys are condition names and values are their initial values.
        current_col_labels : list[str]
            A list of current column labels in the contrast table.
        """
        super().__init__()
        self.title_bar.title = "Batch script values"
        humanize_option_labels = {
            #   "nipype_omp_nthreads": "nipype number of threads",
            "nipype_n_procs": "nipype number of processes",
            "nipype_resource_monitor": "Use nipype resource monitor",
            # "watchdog": "watchdog",
            # "verbose": "verbose",
            #  "keep":"choose which intermediate files to keep",
            "subject_list": "subject list (leave empty if all, separate subjects by comma)",
            # "subject_exclude": "exclude subjects that match",
            # "subject_include": "include only subjects that match",
            # "fs_license_file": 'dddd/ddd/'
        }
        self.batch_options_values: dict[str, str] = {"nipype_n_procs": "1"}
        self.batch_options_bools: dict[str, bool] = {"nipype_resource_monitor": False}
        self.batch_options_lists: dict[str, str | None] = {"subject_list": None}
        # self.batch_options_choices = {'keep': ['some']}

        widgets_option_values = []
        for key, int_val in self.batch_options_values.items():
            input_box = IntOnlyInput(
                placeholder="Value",
                value=int_val,
                name=key,
                validate_on="none",  # only validate when we call it manually
                id=key,
                classes="input_number_values",
            )
            label = Label(humanize_option_labels[key], classes="labels")
            # label.tooltip = int_val
            widgets_option_values.append(Horizontal(label, input_box, classes="option_values options"))

        widgets_option_bools = []
        for key, _ in self.batch_options_bools.items():
            label = Label(humanize_option_labels[key], classes="labels")
            # label.tooltip = bool_val
            text_switch = TextSwitch(value=True)
            widgets_option_bools.append(Horizontal(label, text_switch, id=key, classes="option_bools options"))

        widgets_option_lists = []
        for key, _ in self.batch_options_lists.items():
            input_box = CSVTextArea(
                name=key,
                soft_wrap=True,
                id=key,
                classes="input_list_values",
            )
            label = Label(humanize_option_labels[key], classes="labels")
            # label.tooltip = list_val
            widgets_option_lists.append(Horizontal(label, input_box, classes="option_lists options"))

        # if the singularity path is already set via flag then this should retrieve the path
        singularity_container_path = os.environ.get("SINGULARITY_CONTAINER", None)
        singularity_path_widget = Horizontal(
            Label("Singularity container path", classes="labels"),
            HorizontalScroll(
                PathOnlyInput(
                    value=singularity_container_path,
                    validate_on="none",
                    id="singularity_path_input",
                    classes="input_list_values",
                ),
                id="singularity_path_input_horizontal_wrapper",
            ),
            id="singularity_top_panel",
            classes="option_lists options",
        )

        self.widgets_to_mount = [*widgets_option_values, *widgets_option_bools, *widgets_option_lists, singularity_path_widget]



    @on(Button.Pressed, ".cancel_button")
    def cancel_window(self):
        """
        Cancels the window and dismisses it without saving user input.

        This method is called when the "Cancel" button is pressed. It
        triggers the `_cancel_window` method to dismiss the modal.
        """
        pass

    def key_escape(self):
        """
        Cancels the window and dismisses it when the escape key is pressed.

        This method is called when the escape key is pressed. It triggers
        the `_cancel_window` method to dismiss the modal.
        """
        pass

    def _confirm_window(self):
        """
        Validates the user inputs and updates the table row index if inputs are valid.

        This method checks if the contrast name is unique and if all input
        values are filled. If the inputs are valid, it updates the
        `table_row_index` and dismisses the modal. Otherwise, it displays
        an error message.
        """
        pass

    def _cancel_window(self):
        """
        Dismisses the window without saving any user inputs.

        This method dismisses the modal window without making any changes.
        """
        self.dismiss(False)


class Run(Widget):
    """
    A widget for managing the dumping the cached data to create the spec.json file,
    saving it and finally run the pipeline.

    This class provides a user interface for refreshing the spec data, saving the
    configuration to a spec file, and running the pipeline. It also
    manages the conversion of cached data to the context format and gives a preview
    of the generated spec.json file.

    Attributes
    ----------
    old_cache : defaultdict[str, defaultdict[str, dict[str, Any]]] | None
        A cache of old data, structured as a defaultdict of defaultdicts
        containing dictionaries.
    json_data : str | None
        A JSON string representation of the current configuration.

    Methods
    -------
    __init__(id, classes)
        Initializes the Run widget.
    compose() -> ComposeResult
        Composes the widget's components.
    on_run_button_pressed()
        Handles the event when the "Run" button is pressed.
    on_save_button_pressed()
        Handles the event when the "Save" button is pressed.
    on_refresh_button_pressed()
        Handles the event when the "Refresh" button is pressed.
    refresh_context()
        Refreshes the context by dumping the cached data and updating the UI.
    """

    def __init__(
        self,
        id: str | None = None,
        classes: str | None = None,
    ) -> None:
        """
        Initializes the Run widget.

        Parameters
        ----------
        id : str, optional
            An optional identifier for the widget, by default None.
        classes : str, optional
            An optional string of classes for applying styles to the
            widget, by default None.
        """
        super().__init__(id=id, classes=classes)
        self.old_cache: defaultdict[str, defaultdict[str, dict[str, Any]]] | None = None
        self.json_data = None

    def compose(self) -> ComposeResult:
        """
        Composes the widget's components.

        This method defines the layout and components of the widget,
        including the "Refresh", "Save", and "Run" buttons, and the output
        area.

        Yields
        ------
        ComposeResult
            The composed widgets.
        """
        pass


    @on(Button.Pressed, "#run_button")
    def on_run_button_pressed(self):
        """
        Handles the event when the "Run" button is pressed.

        This method is called when the user presses the "Run" button. It
        exits the application and returns the working directory.
        """
        pass

    # @on(Button.Pressed, "#save_button")
    async def on_save_button_pressed(self):
        """
        Handles the event when the "Save" button is pressed.

        This method is called when the user presses the "Save" button. It
        refreshes the context, saves the spec file to the working
        directory, and success modal is raised.
        """
        pass


    @on(Button.Pressed, "#generate_batch_script_button")
    def on_generate_batch_script_button_pressed(self):
        """
        Handles the event when the "Refresh" button is pressed.

        This method is called when the user presses the "Refresh" button.
        It refreshes the context and updates the UI spec preview with the new data.
        """
        pass


    def on_worker_state_changed(self, event: Worker.StateChanged) -> None:
        """
        Handles state changes in the pattern matching worker.

        This method is called when the state of the `update_worker`
        changes. If the worker is successful, it updates the
        `pattern_match_results` with the callback message and posts a
        `PathPatternChanged` message.

        Parameters
        ----------
        event : Worker.StateChanged
            The event object containing information about the worker state
            change.
        """
        pass

    @on(Button.Pressed, "#exit_button")
    async def on_exit_button_pressed(self):
        """
        Handles the event when the "Refresh" button is pressed.

        This method is called when the user presses the "Refresh" button.
        It refreshes the context and updates the UI spec preview with the new data.
        """
        pass

    @on(Button.Pressed, "#refresh_button")
    async def on_refresh_button_pressed(self):
        """
        Handles the event when the "Refresh" button is pressed..

        This method is called when the user presses the "Refresh" button.
        It refreshes the context and updates the UI spec preview with the new data.
        """
        pass


    async def refresh_context(self):
        """
        Refreshes the context by dumping the cached data and updating the spec preview.

        This method dumps the cached data to the context, converts it to a
        JSON string, and updates the output widget with the JSON data.
        """
        pass

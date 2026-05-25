# -*- coding: utf-8 -*-


from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal, ScrollableContainer, Vertical
from textual.message import Message
from textual.widgets import RadioButton, SelectionList, Static

from ...logging import logger
from ..general_widgets.custom_general_widgets import SwitchWithSelect
from ..general_widgets.custom_switch import TextSwitch
from ..help_functions import extract_conditions, widget_exists
from ..specialized_widgets.confirm_screen import Confirm
from ..specialized_widgets.event_file_widget import EventFilePanel
from ..standards import task_based_defaults
from ..templates.feature_template import FeatureTemplate
from .utils.model_conditions_and_contrasts import ModelConditionsAndContrasts

RadioButton.BUTTON_INNER = "X"


class TaskBased(FeatureTemplate):
    """
    Manages task-based features.

    This class extends `FeatureTemplate` to encapsulate and manage user selections
    related to task-based features,
    selecting relevant tasks, defining model conditions, and specifying
    contrasts (with integrated `ModelConditionsAndContrasts` class). In case of
    non-bids data, it uses `EventFilePanel` to handle event file selection.

    Attributes
    ----------
    entity : str
        The entity used to describe task-based features, set to "desc".
    filters : dict[str, str]
        Filters used to identify event files.
        - datatype : str
            The data type of the event files, set to "func".
        - suffix : str
            The suffix of the event files, set to "event".
    featurefield : str
        The name of the field in the features dictionary that holds the event
        file information, set to "events".
    type : str
        A string indicating the type of the feature, which is "task_based".
    file_panel_class : type[EventFilePanel]
        The class used to manage the file selection panel for event files,
        set to `EventFilePanel`.
    model_conditions_and_contrast_table : ModelConditionsAndContrasts
        The widget for managing model conditions and contrast.

    Methods
    -------
    __init__(this_user_selection_dict, id, classes)
        Initializes the TaskBased instance.
    compose() -> ComposeResult
        Composes the UI elements for the task-based feature.
    on_mount() -> None
        Performs actions when the TaskBased feature is mounted.
    mount_tasks()
        Mounts task selection and event file panels.
    _on_tasks_to_use_selection_changed(message)
        Handles changes in the task selection.
    _on_selection_list_changed_tasks_to_use_selection(message)
        Updates conditions when task selection changes.
    update_conditions_table()
        Updates the conditions table based on selected images.
    """

    entity = "desc"
    filters = {"datatype": "func", "suffix": "event"}
    featurefield = "events"
    type = "task_based"
    file_panel_class = EventFilePanel
    defaults = task_based_defaults

    def __init__(self, this_user_selection_dict, id: str | None = None, classes: str | None = None) -> None:
        """
        Initializes the TaskBased instance.

        This method initializes the TaskBased object by calling the constructor
        of the parent class (`FeatureTemplate`). Moreover, it sets up the conditions
        list, and creating the `ModelConditionsAndContrasts` widget.

        Parameters
        ----------
        this_user_selection_dict : dict
            A dictionary containing the user's selection for this feature.
        id : str, optional
            The ID of the widget, by default None.
        classes : str, optional
            CSS classes for the widget, by default None.
        """

        super().__init__(this_user_selection_dict=this_user_selection_dict, defaults=self.defaults, id=id, classes=classes)
        self.feature_dict.setdefault("conditions", [])
        self.feature_dict.setdefault("model_serial_correlations", True)
        self.feature_dict.setdefault(self.featurefield, [])
        self.feature_dict.setdefault("estimation", "multiple_trial")

        self.trial_estimation_default_switch_value = False if self.feature_dict["estimation"] == "multiple_trial" else True

        self.estimation_types = {
            "single trial least squares single": "single_trial_least_squares_single",
            "single trial least squares all": "single_trial_least_squares_all",
            "multiple trial": "multiple_trial",
        }
        # Reverse mapping
        self.estimation_labels = {v: k for k, v in self.estimation_types.items()}
        self.feature_dict.setdefault("estimation", "multiple_trial")

        self.estimation_type_panel = Vertical(
            SwitchWithSelect(
                "Single trial estimation",
                options=[
                    ("least-squares all", "single_trial_least_squares_all"),
                    ("least-squares single", "single_trial_least_squares_single"),
                ],
                switch_value=self.trial_estimation_default_switch_value,
                default_option=self.feature_dict["estimation"]
                if self.feature_dict["estimation"] != "multiple_trial"
                else "single_trial_least_squares_single",
                id="estimation_type",
            ),
            id="estimation_types_selection_panel",
            classes="components",
        )

        self.estimation_type_panel.border_title = "Estimation Type"
        self.on_init = True



    @on(SwitchWithSelect.Changed, "#estimation_type")
    def _on_estimation_type_changed(self, message) -> None:
        """
        Handles changes in the bandpass filter type.

        This method is called when the value of the `SwitchWithSelect`
        widget with the ID "bandpass_filter_type" changes. It updates the
        bandpass filter settings in `setting_dict` based on the selected
        filter type (Gaussian or frequency-based).

        Parameters
        ----------
        message : SwitchWithSelect.Changed
            The message object containing information about the change.
        """
        pass





    @on(SelectionList.SelectionToggled, "#tasks_to_use_selection")
    def _on_tasks_to_use_selection_changed(self, message):
        """
        Handles changes in the task selection.

        This method displays an error message if no tasks are selected
        and reselects the last selected task to ensure that at least one
        task is always selected.

        Parameters
        ----------
        message : SelectionList.SelectionToggled
            The message object containing information about the task selection change.
        """
        pass

    @on(file_panel_class.Changed, "#top_file_panel")
    @on(SelectionList.SelectionToggled, "#tasks_to_use_selection")
    def _on_selection_list_changed_tasks_to_use_selection(self, message):
        """
        Updates conditions when task selection changes.

        This method updates the list of possible conditions based on the
        currently selected images (`update_conditions_table`). Also, it
        provides list of all available conditions to the
        ModelConditionsAndContrasts table (`update_all_possible_conditions`).
        This is can change for examople when user load an event file. We need to know all possible conditions
        even though we are not showing them all to the user. For more see class
        `ModelConditionsAndContrasts`.

        Parameters
        ----------
        message : SelectionList.SelectionToggled | EventFilePanel.Changed
            The message object containing information about the selection change.
        """
        pass


    def update_conditions_table(self):
        """
        Updates the conditions table based on selected images.

        This method updates the condition values in the
        `ModelConditionsAndContrasts` widget to reflect the conditions
        associated with the currently selected images.
        """
        pass

    @on(TextSwitch.Changed, "#model_serial_correlations_switch")
    def _on_model_serial_correlations_switch_changed(self, message: Message) -> None:
        """
        Handles changes in the grand mean scaling switch.

        This method is called when the switch state of the
        `SwitchWithInputBox` widget with the ID "grand_mean_scaling"
        changes. If the switch is turned off, it sets the grand mean
        scaling value in `setting_dict` to None.

        Parameters
        ----------
        message : SwitchWithInputBox.SwitchChanged
            The message object containing information about the change.
        """
        pass

# -*- coding: utf-8 -*-

import copy
from copy import deepcopy

import inflect
from textual import on
from textual.containers import Horizontal, Vertical
from textual.message import Message
from textual.widget import Widget
from textual.widgets import Select, SelectionList, Static
from textual.widgets.selection_list import Selection

from ...model.tags import entity_longnames as entity_display_aliases
from ..data_analyzers.context import ctx
from ..data_analyzers.summary_steps import BoldSummaryStep
from ..data_input.base import DataSummaryLine
from ..general_widgets.custom_general_widgets import SwitchWithInputBox, SwitchWithSelect
from ..specialized_widgets.event_file_widget import FilePanelTemplate
from ..standards import bandpass_filter_defaults

entity_label_dict = {"dir": "Directions", "run": "Runs", "task": "Tasks", "ses": "Sessions"}

p = inflect.engine()


class FeatureTemplate(Widget):
    """
    Base class for creating and managing feature-based settings and selections.

    This widget provides a foundation for building user interface components that
    allow users to configure and select various settings related to a specific
    feature. It handles the initialization of new widgets, loading settings from
    specification files, and managing preprocessing options.

    Attributes
    ----------
    entity : str
        An identifier for the type of entity the widget interacts with (e.g., "task", "run").
    filters : dict
        A dictionary specifying the datatype and suffix to filter database queries.
        Example: `{"datatype": "func", "suffix": "bold"}`.
    featurefield : str
        The specific feature field in the settings (e.g., "atlases", "seeds").
    type : str
        The type of the feature (e.g., "atlas_based_connectivity", "reho").
    file_panel_class : type
        The class used for the file panel within this widget. Defaults to `FilePanelTemplate`.
    feature_dict : dict
        A dictionary containing feature-specific settings and values.
    setting_dict : dict
        A dictionary containing general settings and configuration values.
    event_file_pattern_counter : int
        A counter for file patterns, used when creating new file patterns.
    tagvals : list
        A list of available tags for selection.
    images_to_use : dict | None
        A dictionary specifying which images to use, keyed by entity (e.g., "task").
        Values are dictionaries mapping tag names to boolean values (True if selected).
    confounds_options : dict
        Available options for confounds removal, with their descriptions and default states.
        Keys are confound names, values are lists: `[description, default_state]`.
    preprocessing_panel : Vertical
        A panel containing pre-processing options such as smoothing, mean scaling, and temporal filtering.
    tasks_to_use_selection_panel : Vertical | None
        A panel containing the selection list of images to use.
    """

    entity: str = ""
    filters: dict = {"datatype": "", "suffix": ""}
    featurefield: str = ""
    type: str = ""
    file_panel_class = FilePanelTemplate

    def __init__(
        self, this_user_selection_dict: dict, defaults: dict, id: str | None = None, classes: str | None = None
    ) -> None:
        """
        Initializes the FeatureTemplate widget.

        This constructor sets up the widget's internal state, including feature
        and general settings, preprocessing options, and image selection. It
        handles both the creation of new widgets and the loading of settings
        from a specification file.

        Note
        ----
        At the beginning there is a bunch of 'if not in'. If a new widget is created the pass
        this_user_selection_dict is empty and the nested keys need some initialization. On the other
        hand, if a new widget is created automatically on spec file load then this dictionary is not empty and these
        values are then used for the various widgets within this widget.

        Parameters
        ----------
        this_user_selection_dict : dict
            A dictionary containing user selections and settings. It should have
            keys "features" and "settings".
        defaults : dict
            A dictionary containing default settings for features.
        id : str, optional
            An optional identifier for the widget, by default None.
        classes : str, optional
            An optional string of classes for applying styles to the widget, by
            default None.
        """
        super().__init__(id=id, classes=classes)
        _defaults = deepcopy(defaults)
        self._bandpass_filter_defaults = deepcopy(bandpass_filter_defaults)

        self.feature_dict = this_user_selection_dict["features"]
        self.setting_dict = this_user_selection_dict["settings"]
        self.event_file_pattern_counter = 0

        self.temp_bandpass_filter_selection: dict
        self.feature_dict.setdefault("contrasts", [])
        self.feature_dict.setdefault("type", self.type)

        self.bandpass_filter_default_switch_value = True
        self.setting_dict.setdefault("space", "standard")
        self.setting_dict.setdefault("bandpass_filter", _defaults["bandpass_filter"])

        # if self.type in ["reho", "falff", "atlas_based_connectivity"]:
        #     self.setting_dict.setdefault("bandpass_filter", {"type": "frequency_based", "high": "0.1", "low": "0.01"})
        # else:
        #     self.setting_dict.setdefault("bandpass_filter", {"type": "gaussian", "hp_width": "125", "lp_width": None})

        if self.setting_dict["bandpass_filter"]["type"] is None:
            self.bandpass_filter_default_switch_value = False

        self.setting_dict.setdefault("smoothing", _defaults["smoothing"])

        self.grand_mean_scaling_default_switch_value = True
        self.setting_dict.setdefault("grand_mean_scaling", _defaults["grand_mean_scaling"])
        if self.setting_dict["grand_mean_scaling"]["mean"] is None:
            self.grand_mean_scaling_default_switch_value = False

        self.setting_dict.setdefault(
            "filters",
            [
                {"type": "tag", "action": "include", "entity": entity, "values": []}
                for entity, tags in ctx.get_available_images.items()
                if entity == "task"
            ],
        )

        self.images_to_use: dict | None
        # if images exists, i.e., bold files with task tags were correctly given
        if ctx.get_available_images != {}:
            # In "Features" we use only "Tasks" !
            # loop around available tasks to create a selection dictionary for the selection widget
            # if empty setting_dict["filters"] (meaning to loading or duplicating is happening) assign True to all images
            # Case 1) filters is an empty list. Meaning: we are loading from a file and there are no filters so we assign
            # all values as True
            if self.setting_dict["filters"] == []:
                # self.images_to_use = {"task": {task: True for task in ctx.get_available_images["task"]}}
                self.images_to_use = {
                    entity: {tag: True for tag in tags}
                    for entity, tags in ctx.get_available_images.items()
                    if entity == "task"
                }
            # Case 2) filters is not an empty list but the values are empty. Meaning: there are two possibilities. Either this
            # is fresh new feature or we are making a duplicate from a feature that we
            # previously have created. We assign all values to False
            else:
                self.images_to_use = {
                    entity: {tag: False for tag in tags}
                    for entity, tags in ctx.get_available_images.items()
                    if entity == "task"
                }
                # Case 3) We are loading or duplicating and some tasks are on and some are off. This means some filters are on
                # and some off. Based on what is present in the filters dictionary under values, we assign True.
                if self.setting_dict["filters"][0]["values"] != []:
                    for image in self.setting_dict["filters"][0]["values"]:
                        self.images_to_use["task"][image] = True
        else:
            self.images_to_use = None

        confounds_options = _defaults["confounds_options"]
        for confound in self.setting_dict.get("confounds_removal", []):
            confounds_options[confound][1] = True

        # ica-aroma is separated from the rest in the spec.json file
        confounds_options["ICA-AROMA"][1] = self.setting_dict.get("ica_aroma", False)

        self.confounds_options = confounds_options
        self.create_preprocessing_panel(self.setting_dict["smoothing"]["fwhm"])

        if self.images_to_use is not None:
            self.tasks_to_use_selection_panel = Vertical(
                SelectionList[str](
                    *[Selection(image, image, self.images_to_use["task"][image]) for image in self.images_to_use["task"]],
                    id="tasks_to_use_selection",
                ),
                DataSummaryLine(id="feedback_task_filtered_bold"),
                id="tasks_to_use_selection_panel",
                classes="components",
            )

    def create_preprocessing_panel(self, default_smoothing_value):
        """
        Creates the preprocessing panel with the given default smoothing value.

        This method constructs the preprocessing panel, which includes options
        for smoothing, grand mean scaling, and temporal filtering. The panel is
        created dynamically to accommodate different smoothing settings (e.g.,
        smoothing in settings vs. smoothing in features).

        Parameters
        ----------
        default_smoothing_value : Any
            The default smoothing value (FWHM in mm).
        """
        # We need to create preprocessing panel via a separate function because from reho and falff the smoothing is in
        # features not in settings. Hence to override the default value when we for example load from a spec file, we need
        # to refresh the preprocessing panel after we switch from smoothing in settings to smoothing in features. For more
        # look for example at init at the reho.py
        if default_smoothing_value is None:
            smoothing_default_switch_value = False
        else:
            smoothing_default_switch_value = True
        # update low and high pass filter is done automatically at start, the SwitchWithSelect.Changed
        # "#bandpass_filter_type") automatically triggers def _on_bandpass_filter_type_change
        self.preprocessing_panel = Vertical(
            Horizontal(
                Static("Specify space", id="space_label"),
                Select(
                    options=[("Standard space (MNI ICBM 2009c Nonlinear Asymmetric)", "standard"), ("Native space", "native")],
                    value=self.setting_dict["space"],
                    allow_blank=False,
                    id="space_selection",
                ),
                id="space_selection_panel",
            ),
            SwitchWithInputBox(
                label="Smoothing (FWHM in mm)",
                value=str(default_smoothing_value) if default_smoothing_value is not None else default_smoothing_value,
                switch_value=smoothing_default_switch_value,
                classes="switch_with_input_box",
                id="smoothing",
            ),
            SwitchWithInputBox(
                label="Grand mean scaling",
                value=str(self.setting_dict["grand_mean_scaling"]["mean"])
                if self.setting_dict["grand_mean_scaling"]["mean"] is not None
                else self.setting_dict["grand_mean_scaling"]["mean"],
                switch_value=self.grand_mean_scaling_default_switch_value,
                classes="switch_with_input_box additional_preprocessing_settings",
                id="grand_mean_scaling",
            ),
            SwitchWithSelect(
                "Temporal filter",
                options=[("Gaussian-weighted", "gaussian"), ("Frequency-based", "frequency_based")],
                switch_value=self.bandpass_filter_default_switch_value,
                default_option=self.setting_dict["bandpass_filter"]["type"],
                id="bandpass_filter_type",
                classes="additional_preprocessing_settings",
            ),
            SwitchWithInputBox(
                label="Low-pass temporal filter width \n(in seconds)",
                value=None,
                classes="switch_with_input_box bandpass_filter_values",
                id="bandpass_filter_lp_width",
            ),
            SwitchWithInputBox(
                label="High-pass temporal filter width \n(in seconds)",
                value=None,
                classes="switch_with_input_box bandpass_filter_values",
                id="bandpass_filter_hp_width",
            ),
            SelectionList[str](
                *[
                    Selection(self.confounds_options[key][0], key, self.confounds_options[key][1])
                    for key in self.confounds_options
                ],
                #       classes="components",
                id="confounds_selection",
            ),
            id="preprocessing",
            classes="components",
        )

    async def on_mount(self) -> None:
        """
        Handles actions to be taken when the component is mounted in the UI.

        This method is called when the widget is mounted to the
        application. It sets the border titles for the input box, tag
        selection list, and file panel.
        """
        pass

    @on(SelectionList.SelectedChanged, "#tasks_to_use_selection")
    def _on_selection_list_changed(self, message) -> None:
        """
        Handles changes in the selection list of tasks to use.

        This method is called when the selection in the `SelectionList`
        widget with the ID "tasks_to_use_selection" changes. It updates
        the filters in `setting_dict` based on the selected tasks.

        Parameters
        ----------
        message : SelectionList.SelectedChanged
            The message object containing information about the change.
        """
        pass

    def update_dataline(self) -> None:
        """
        Updates the data line with the current selection.

        This method updates the data line with the current selection of
        tasks and other settings.
        """
        pass

    @on(SwitchWithSelect.SwitchChanged, "#bandpass_filter_type")
    def _on_bandpass_filter_type_switch_changed(self, message):
        """
        Handles changes in the bandpass filter type switch.

        This method is called when the switch state of the
        `SwitchWithSelect` widget with the ID "bandpass_filter_type"
        changes. It toggles the visibility of the low-pass and high-pass
        filter widgets and updates the `setting_dict` accordingly.

        Parameters
        ----------
        message : SwitchWithSelect.SwitchChanged
            The message object containing information about the change.
        """
        pass

    @on(SwitchWithSelect.Changed, "#bandpass_filter_type")
    def _on_bandpass_filter_type_changed(self, message) -> None:
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

    def set_bandpass_filter_values_after_toggle(self, bandpass_filter_type) -> None:
        """
        Sets the bandpass filter values after toggling the filter type.

        This method is called after the bandpass filter type is toggled.
        It updates the labels and values of the low-pass and high-pass
        filter widgets based on the selected filter type. It also updates
        the `setting_dict` with the new filter values.

        Parameters
        ----------
        bandpass_filter_type : str
            The selected bandpass filter type ("gaussian" or
            "frequency_based").
        """
        pass

    @on(SwitchWithInputBox.Changed, "#grand_mean_scaling")
    def _on_grand_mean_scaling_changed(self, message: Message) -> None:
        """
        Handles changes in the grand mean scaling value.

        This method is called when the value of the `SwitchWithInputBox`
        widget with the ID "grand_mean_scaling" changes. It updates the
        `setting_dict` with the new grand mean scaling value.

        Parameters
        ----------
        message : SwitchWithInputBox.Changed
            The message object containing information about the change.
        """
        pass

    @on(SwitchWithInputBox.SwitchChanged, "#grand_mean_scaling")
    def _on_grand_mean_scaling_switch_changed(self, message: Message) -> None:
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

    def _update_bandpass_filter_setting(self, control, switch_value, value=None):
        """
        Shared logic for updating bandpass filter settings.
        """
        pass

    @on(SwitchWithInputBox.Changed, ".bandpass_filter_values")
    def _on_bandpass_filter_xp_width_changed(self, message: Message) -> None:
        """
        Handles value changes in bandpass filter input box.
        """
        pass

    @on(SwitchWithInputBox.SwitchChanged, ".bandpass_filter_values")
    def _on_bandpass_filter_xp_width_switch_changed(self, message: Message) -> None:
        """
        Handles switch state changes in bandpass filter input box.
        """
        pass

    def _update_smoothing_setting(self, switch_value: bool, value: str | None) -> None:
        """
        Shared logic for updating smoothing settings.

        Parameters
        ----------
        switch_value : bool
            The state of the smoothing switch (True = enabled, False = disabled).
        value : str | None
            The current smoothing value from the input box.
        """
        pass

    @on(SwitchWithInputBox.Changed, "#smoothing")
    def _on_smoothing_changed(self, message: Message) -> None:
        """
        Handles input value changes in the smoothing control.
        """
        pass

    @on(SwitchWithInputBox.SwitchChanged, "#smoothing")
    def _on_smoothing_switch_changed(self, message: Message) -> None:
        """
        Handles switch state changes in the smoothing control.
        """
        pass

    @on(SelectionList.SelectedChanged, "#confounds_selection")
    def feed_feature_dict_confounds(self) -> None:
        """
        Feeds the feature dictionary with confounds.

        This method is called when the selection in the `SelectionList`
        widget with the ID "confounds_selection" changes. It updates the
        `setting_dict` with the selected confounds.
        """
        pass

    #############################
    #
    # def set_file_tag_defaults(self):
    #     self.get_widget_by_id("file_tag_selection").deselect_all()
    #     if self.feature_dict[self.featurefield] == []:
    #         self.get_widget_by_id("file_tag_selection").select_all()
    #     else:
    #         for file_tag in self.feature_dict[self.featurefield]:
    #             self.get_widget_by_id("file_tag_selection").select(file_tag)

    @on(FilePanelTemplate.FileTagsChanged)
    def on_file_tag_selection_changed(self, message) -> None:
        """
        Handles changes in the tag selection list.

        This method is called when the selection in the `SelectionList`
        widget changes. It updates the corresponding value in the
        `feature_dict`.

        Parameters
        ----------
        selection_list : SelectionList
            The selection list widget.
        """
        pass


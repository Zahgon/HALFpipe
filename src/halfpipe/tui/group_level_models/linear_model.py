# -*- coding: utf-8 -*-

import asyncio
from itertools import chain, combinations

from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Grid, Horizontal, ScrollableContainer, Vertical
from textual.widgets import Button, Select, SelectionList, Static
from textual.widgets._select import NULL
from textual.widgets.selection_list import Selection

from ...ingest.spreadsheet import read_spreadsheet
from ...model.file.base import File
from ..data_analyzers.context import ctx
from ..general_widgets.custom_general_widgets import SwitchWithSelect
from ..general_widgets.custom_switch import TextSwitch
from ..help_functions import widget_exists
from ..specialized_widgets.confirm_screen import SimpleMessageModal
from ..templates.model_template import ModelTemplate
from .utils.add_spreadsheet_modal import AddSpreadsheetModal
from .utils.additional_contrasts_table import AdditionalContrastsCategoricalVariablesTable


class LinearModel(ModelTemplate):
    """
    A model representing a linear group-level model.

    This class extends `ModelTemplate` to provide a specific type of
    group-level model that includes an intercept term and allows for
    the inclusion of additional variables and interaction terms. It
    allows users to select tasks to use, set aggregation levels, define
    cutoff values, and specify a spreadsheet file for covariates and
    group data.

    Attributes
    ----------
    type : str
        The type of the model, set to "lme" for linear model.
    spreadsheet_filepaths : dict[str, str]
        A dictionary mapping spreadsheet cache IDs to their file paths.
    model_dict : dict[str, Any]
        A dictionary containing the model's configuration, including
        contrasts, filters, and the selected spreadsheet.
    spreadsheet_panel : Vertical
        A panel containing widgets for selecting and managing the
        spreadsheet file.
    metadata_variables : list[dict[str, Any]]
        A list of metadata dictionaries for the variables in the
        selected spreadsheet.
    spreadsheet_df : pd.DataFrame
        A pandas DataFrame containing the data from the selected
        spreadsheet.
    variables : list[str]
        A list of variable names from the selected spreadsheet.
    is_new : bool
        A flag indicating whether the model is newly created or loaded
        from existing data.
    has_type_t : bool
        A flag indicating whether the model has type 't' contrasts.

    Methods
    -------
    __init__(this_user_selection_dict, id, classes)
        Initializes the model with optional user selections, ID, and classes.
    compose() -> ComposeResult
        Composes the widget's components.
    _on_button_select_spreadsheet_pressed()
        Handles the event when the "Add" button for the spreadsheet is pressed.
    _on_spreadsheet_selection_changed(message)
        Handles changes in the selected spreadsheet.
    _on_switch_with_select_switch_changed(message)
        Handles changes in the switch state of a SwitchWithSelect widget.
    _on_switch_with_select_changed(message)
        Handles changes in the selected option of a SwitchWithSelect widget.
    _on_level_sub_panels_selection_list_changed(message)
        Handles changes in the selection of levels for a categorical variable.
    _on_interaction_variables_selection_list_changed(message)
        Handles changes in the selected interaction variables.
    _on_interaction_terms_selection_list_changed(message)
        Handles changes in the selected interaction terms.
    _on_contrast_switch_changed(message)
        Handles changes in the state of the contrast switch.
    _on_additional_contrasts_categorical_variables_table_changed(message)
        Handles changes in the additional contrasts table.
    """

    # Type of the model, set to "lme" for linear model.
    type = "lme"

    def __init__(self, this_user_selection_dict=None, id: str | None = None, classes: str | None = None) -> None:
        """
        Initializes the model with optional user selections, ID, and classes.

        Parameters
        ----------
        this_user_selection_dict : dict | None, optional
            A dictionary containing user-specified selections for the model,
            by default None.
        id : str | None, optional
            An optional identifier for the model, by default None.
        classes : str | None, optional
            An optional string of classes for applying styles to the model,
            by default None.
        """
        super().__init__(this_user_selection_dict=this_user_selection_dict, id=id, classes=classes)
        # A dictionary mapping spreadsheet cache IDs to their file paths.
        self.spreadsheet_filepaths: dict[str, str] = {}
        self.model_dict.setdefault("contrasts", [])
        self.model_dict.setdefault("filters", [])
        self.model_dict.setdefault("spreadsheet", None)
        # In case loading or duplicating, the spreadsheet field is not None. So we need to find matching fileobject in the
        # ctx.cache and assign it in this widget.
        for key in ctx.cache:
            if key.startswith("__spreadsheet_file_"):
                self.spreadsheet_filepaths[key] = ctx.cache[key]["files"].path  # type: ignore

        # there has to be button to Add new spreadsheet
        spreadsheet_selection = Select(
            [(i[1], i[0]) for i in self.spreadsheet_filepaths.items()],
            value=next(
                (key for key, value in self.spreadsheet_filepaths.items() if value == self.model_dict["spreadsheet"]), NULL
            )
            if self.model_dict["spreadsheet"] is not None
            else NULL,
            id="spreadsheet_selection",
        )

        self.spreadsheet_panel = Vertical(
            # Static('No spreadsheet selected!', id='spreadsheet_path_label'),
            spreadsheet_selection,
            Horizontal(
                Button("Add", id="add_spreadsheet"),
                Button("Delete", id="delete_spreadsheet"),
                Button("Details", id="details_spreadsheet"),
            ),
            id="spreadsheet_selection_panel",
            classes="components",
        )
        self.spreadsheet_panel.border_title = "Covariates/group data spreadsheet file"


    @on(Button.Pressed, "#add_spreadsheet")
    async def _on_button_select_spreadsheet_pressed(self):
        """
        Handles the event when the "Add" button for the spreadsheet is pressed.

        This method pushes the `AddSpreadsheetModal` onto the screen to
        allow the user to select a spreadsheet file. It then updates the
        spreadsheet selection widget with the newly selected file.
        """
        pass


    @on(Select.Changed, "#spreadsheet_selection")
    async def _on_spreadsheet_selection_changed(self, message):
        """
        Handles changes in the selected spreadsheet.

        This method is called when the user selects a different
        spreadsheet from the `Select` widget. It updates the model's
        configuration based on the selected spreadsheet, including
        loading metadata, setting up filters, and creating widgets for
        variable selection and interaction terms.

        Parameters
        ----------
        message : Select.Changed
            The message object containing information about the selection
            change.
        """
        pass

    @on(SwitchWithSelect.SwitchChanged, ".additional_preprocessing_settings")
    def _on_switch_with_select_switch_changed(self, message):
        """
        Handles changes in the switch state of a SwitchWithSelect widget.

        This method is called when the switch state changes in a
        `SwitchWithSelect` (Additional preprocessing settings) widget.
        It adds or removes variables from the model based on the switch state.

        Parameters
        ----------
        message : SwitchWithSelect.SwitchChanged
            The message object containing information about the switch
            state change.
        """
        pass

    @on(SwitchWithSelect.Changed, ".additional_preprocessing_settings")
    def _on_switch_with_select_changed(self, message):
        """
        Handles changes in the selected option of a SwitchWithSelect
        (Additional preprocessing settings) widget.

        This method is called when the selected option changes in a
        `SwitchWithSelect` widget. It selects am action for missing values
        based on the selected option.

        Parameters
        ----------
        message : SwitchWithSelect.Changed
            The message object containing information about the option
            change.
        """
        pass

    @on(SelectionList.SelectedChanged, ".level_selection")
    def _on_level_sub_panels_selection_list_changed(self, message):
        """
        Handles changes in the selection of subjects (types) levels for a categorical variable.

        This method is called when the selection changes in a
        `SelectionList` widget representing the levels of a categorical
        variable. It updates the model's filters to reflect the selected
        levels.

        Parameters
        ----------
        message : SelectionList.SelectedChanged
            The message object containing information about the selection
            change.
        """
        pass

    @on(SelectionList.SelectedChanged, "#interaction_variables_selection_panel")
    def _on_interaction_variables_selection_list_changed(self, message):
        """
        Handles changes in the selected interaction variables.

        This method is called when the selection changes in the
        `SelectionList` widget for interaction variables. It updates the
        available interaction terms based on the selected variables.

        Parameters
        ----------
        message : SelectionList.SelectedChanged
            The message object containing information about the selection
            change.
        """
        pass

    @on(SelectionList.SelectedChanged, "#interaction_terms_selection_panel")
    def _on_interaction_terms_selection_list_changed(self, message):
        """
        Handles changes in the selected interaction terms.

        This method is called when the selection changes in the
        `SelectionList` widget for interaction terms. It updates the
        model's contrasts to reflect the selected interaction terms.

        Parameters
        ----------
        message : SelectionList.SelectedChanged
            The message object containing information about the selection
            change.
        """
        pass

    @on(TextSwitch.Changed, "#contrast_switch")
    async def _on_contrast_switch_changed(self, message):
        """
        Handles changes in the state of the contrast switch.

        This method is called when the state of the contrast switch
        changes. It dynamically adds or removes `AdditionalContrastsCategoricalVariablesTable`
        widgets for each categorical variable based on the switch state.

        Parameters
        ----------
        message : TextSwitch.Changed
            The message object containing information about the switch
            state change.
        """
        pass

    @on(AdditionalContrastsCategoricalVariablesTable.Changed)
    def _on_additional_contrasts_categorical_variables_table_changed(self, message):
        """
        Handles changes in the additional contrasts table.

        This method is called when the `AdditionalContrastsCategoricalVariablesTable`
        widget changes. It updates the model's contrasts to reflect the
        changes made in the table.

        Parameters
        ----------
        message : AdditionalContrastsCategoricalVariablesTable.Changed
            The message object containing information about the table
            change.
        """
        pass

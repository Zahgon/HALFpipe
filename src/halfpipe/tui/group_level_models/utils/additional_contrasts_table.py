# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

from dataclasses import dataclass
from itertools import cycle

import pandas as pd
from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal, HorizontalScroll
from textual.message import Message
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Button, DataTable

from ...features.utils.model_conditions_and_contrasts import ContrastTableInputWindow


class AdditionalContrastsCategoricalVariablesTable(Widget):
    """With some exceptions, this is very similar to ModelConditionsAndContrasts class.
    As a future TODO, one can make a abstract class for this and the above mentioned class.
    For now, for more information just look at the ModelConditionsAndContrasts class.
    """

    @dataclass
    class Changed(Message):
        additional_contrasts_categorical_variables_table: "AdditionalContrastsCategoricalVariablesTable"
        value: str

        @property
        def control(self):
            """Alias for self.file_browser."""
            pass

    BINDINGS = [
        ("a", "add_column", "Add column"),
        ("r", "remove_column", "Add column"),
        ("s", "submit", "Submit"),
    ]

    sort_type_cycle = cycle(
        [
            "alphabetically",
            "reverse_alphabetically",
            "by_group",
            "reverse_by_group",
        ]
    )

    # if so, the selection and the table need an update
    condition_values: reactive[list] = reactive([], init=False)

    def __init__(
        self,
        all_possible_conditions: list,
        feature_contrasts_dict: list,
        feature_conditions_list: list,
        id: str | None = None,
        classes: str | None = None,
    ) -> None:
        """The pandas dataframe is to remember all choices even when some images or conditions are turned off.
        This is because when they are turned on, the condition values will be also back.
        The feature_contrasts_dict is used when the widget is created either from read-in (from existing json file) or
        when duplicated.
        The tricky part in this widget is to keep sync between the selection list and the table and on top of  that
        with the images selection list from the upper widget. Also one needs to properly store and recover table values
        on change.
        The all_possible_conditions is a list of all conditions based on the available images (bold) files.
        The feature_contrasts_dict is reference to the list in the ctx.cache!
        """
        super().__init__(id=id, classes=classes)
        self.feature_contrasts_dict = feature_contrasts_dict
        self.feature_conditions_list = feature_conditions_list
        # This means now all possible levels, because if user change subjects to use, then we should get more rows and there
        # should be also memory of the previous choice.
        self.all_possible_conditions = all_possible_conditions
        self.row_dict: dict = {}
        self.update_all_possible_conditions(all_possible_conditions)

    def update_all_possible_conditions(self, all_possible_conditions: list) -> None:
        self.df = pd.DataFrame()
        # This here assign the row incides, so in our case these are all possible values of categorical variables,
        # or in other words the 'levels'.
        self.df["condition"] = all_possible_conditions
        self.df.set_index("condition", inplace=True)
        # if there are dict entries then set defaults
        # if self.feature_contrasts_dict is not None:  # Ensure it is not None
        if self.feature_contrasts_dict != []:
            # convert dict to pandas
            for contrast_dict in self.feature_contrasts_dict:
                #   for row_index in self.df.index:
                for condition_name in contrast_dict["values"]:
                    self.df.loc[condition_name, contrast_dict["name"]] = contrast_dict["values"][condition_name]
            self.table_row_index = dict.fromkeys(list(self.feature_contrasts_dict[0]["values"].keys()))


    def action_add_column(self):
        """Add column with new contrast values to te table."""
        pass






    def sort_by_row_label(self, default: str | None = None):
        """
        Parameters
        ----------
        default : str, optional
            Custom sort type to override the default cycling sort types.
        """
        pass


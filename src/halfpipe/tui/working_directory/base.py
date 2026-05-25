# -*- coding: utf-8 -*-
# ok to review

import os
from pathlib import Path

from niworkflows.utils.misc import check_valid_fs_license
from textual import on, work
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.message import Message
from textual.widget import Widget
from textual.widgets import Button, Static, Tabs
from textual.worker import Worker, WorkerState

from ...model.spec import load_spec
from ...workdir import init_workdir
from ..data_analyzers.context import ctx
from ..help_functions import copy_and_rename_file
from ..load import cache_file_patterns, fill_ctx_spec, mount_features, mount_file_panels, mount_models
from ..specialized_widgets.confirm_screen import Confirm
from ..specialized_widgets.file_browser_modal import path_test_with_isfile_true
from ..specialized_widgets.filebrowser import FileBrowser


class WorkDirectory(Widget):
    """
    Manages the working directory selection and initialization for the application.

    This widget provides the user interface for selecting a working directory,
    which serves as the root for storing all output files and loading
    configurations from existing 'spec.json' files. It handles the
    interaction with the file browser, validation of the selected directory,
    and the loading or overriding of existing configurations.

    Attributes
    ----------
    existing_spec : Spec | None
        The loaded specification object from 'spec.json', or None if no
        specification file is found.
    data_input_success : bool
        A flag indicating whether the data input process was successful.
    event_file_objects : list[File]
        A list of event file objects loaded from the specification.
    atlas_file_objects : list[File]
        A list of atlas file objects loaded from the specification.
    seed_map_file_objects : list[File]
        A list of seed map file objects loaded from the specification.
    spatial_map_file_objects : list[File]
        A list of spatial map file objects loaded from the specification.
    feature_widget : Widget
        The feature selection widget.
    model_widget : Widget
        The model selection widget.

    Methods
    -------
    compose()
        Composes the widgets for the working directory interface.
    _on_file_browser_changed(message)
        Handles file browser's changed event, including verifying selected directory and loading configuration
        from 'spec.json'.
    working_directory_override(override)
        Manages overriding an existing spec file, if one is found in the selected directory.
    existing_spec_file_decision(load)
        Manages user decision whether to load an existing spec file or override it.
    load_from_spec()
        Loads settings from 'spec.json' and updates the context cache.
    cache_file_patterns()
        Caches data from 'spec.json' into context and creates corresponding widgets.
    mount_features()
        Mounts feature selection widgets based on the spec file.
    on_worker_state_changed(event)
        Handles state change events for workers, progressing through stages of loading.
    mount_file_panels()
        Initializes file panels for various file types (events, atlas, seed, spatial maps).
    mount_models()
        Initializes the model selection widgets based on the spec file.
    """

    def __init__(
        self,
        id: str | None = None,
        classes: str | None = None,
    ) -> None:
        """
        Initializes the WorkDirectory widget.

        Parameters
        ----------
        id : str | None, optional
            Identifier for the widget, by default None.
        classes : str | None, optional
            Classes for CSS styling, by default None.
        """
        super().__init__(id=id, classes=classes)
        self.fs_license_file_found = False

    def compose(self) -> ComposeResult:
        """
        Composes the widgets for the working directory interface.

        This method creates the layout for the working directory selection,
        including a descriptive static text and a file browser.

        Returns
        -------
        ComposeResult
            The result of composing the child widgets.
        """
        pass





    @work(exclusive=False, name="work_dir_path_passed_worker")
    async def _working_dir_path_passed(self, selected_path: str | Path):
        """
        Handles the FileBrowser's Changed event.

        This method is called when the user selects a directory in the
        FileBrowser. It validates the selected directory, updates the UI,
        and checks for an existing 'spec.json' file. If a 'spec.json' file
        is found, it prompts the user to decide whether to load or override
        the existing configuration.

        Note
        ----
        The FileBrowser itself makes checks over the selected working directory
        validity. If it passes then we get here and no more checks are needed.

        Parameters
        ----------
        message : Message
            The message object containing information about the change.
        """
        pass

    async def on_worker_state_changed(self, event: Worker.StateChanged) -> None:
        """
        Handles state change events for workers.

        This method is called when the state of a worker changes. If the worker
        ended with SUCCESS, it manages the progression through different stages
        of loading, such as filling the spec context object, caching file patterns,
        mounting features, mounting file panels,and mounting models.

        Parameters
        ----------
        event : Worker.StateChanged
            The event object containing information about the worker's
            state change.
        """
        pass









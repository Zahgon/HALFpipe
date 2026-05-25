# -*- coding: utf-8 -*-


import functools
import os
from pathlib import Path
from typing import Iterable

from textual import on
from textual.containers import Horizontal
from textual.message import Message
from textual.widgets import Button, DirectoryTree, Input
from textual.widgets._directory_tree import DirEntry
from textual.widgets._tree import Tree, TreeNode

from ..general_widgets.draggable_modal_screen import DraggableModalScreen
from ..general_widgets.select_or_input_path import SelectOrInputPath, create_path_option_list
from ..help_functions import with_loading_modal
from .confirm_screen import Confirm


def path_test(path: str, isfile: bool = False) -> str:
    """
    Checks if a given path is valid and accessible.

    This function checks if a given path exists, is writable, and
    matches the expected type (file or directory).

    Parameters
    ----------
    path : str
        The path to the file or directory to be checked.
    isfile : bool, optional
        If True, the function expects the path to be a file. If False, it
        expects the path to be a directory. Default is False.

    Returns
    -------
    str
        A message indicating the result of the path check. Possible
        values are:
        - "OK" if the path corresponds to the expected type (file or
          directory) and is writable.
        - "A directory was selected instead of a file!" if isfile is
          True, but the path is a directory.
        - "A file was selected instead of a directory!" if isfile is
          False, but the path is a file.
        - "Permission denied." if the path is not writable.
        - "File not found." if the path does not exist.
    """
    pass


# Partially apply path_test with isfile=True
path_test_with_isfile_true = functools.partial(path_test, isfile=True)


class FilteredDirectoryTree(DirectoryTree):
    """
    A directory tree widget that filters out hidden files and directories.

    This class extends `DirectoryTree` to provide a directory tree that
    filters out paths with names starting with a period, which are
    typically hidden files or directories.

    Methods
    -------
    filter_paths(paths)
        Filters out paths that have names starting with a period,
        indicating hidden files or directories.
    """

    class NodeChanged(Message):
        """Posted when a directory is selected.

        Can be handled using `on_directory_tree_directory_selected` in a
        subclass of `DirectoryTree` or in a parent widget in the DOM.
        """

        def __init__(self, node: TreeNode[DirEntry], path: Path) -> None:
            """Initialise the DirectorySelected object.

            Args:
                node: The tree node for the directory that was selected.
                path: The path of the directory that was selected.
            """
            super().__init__()
            self.node: TreeNode[DirEntry] = node
            """The tree node of the directory that was selected."""
            self.path: Path = path
            """The path of the directory that was selected."""

        @property
        def control(self) -> Tree[DirEntry]:
            """The `Tree` that had a directory selected."""
            pass

    def filter_paths(self, paths: Iterable[Path]) -> Iterable[Path]:
        """
        Filters out paths that have names starting with a period.

        This method filters out paths that have names starting with a
        period, indicating hidden files or directories.

        Parameters
        ----------
        paths : Iterable[Path]
            A list of file and directory paths to filter.

        Returns
        -------
        Iterable[Path]
            A list of paths excluding those with names starting with a
            period.
        """
        pass


    def scroll_to_line(self, line: int, animate: bool = True) -> None:
        """Scroll to the given line.

        Args:
            line: A line number.
            animate: Enable animation.
        """
        pass


class FileBrowserModal(DraggableModalScreen):
    """
    A modal dialog for browsing directories and selecting paths.

    This class provides a modal dialog that allows users to browse
    directories, select a path, and validate the selected path. It
    includes a directory tree, a path input box, and "Ok" and "Cancel"
    buttons. The path input box is given by the SelectOrInputPath widget
    which makes path string suggestion selection.

    Attributes
    ----------
    CSS_PATH : list[str]
        Path to the CSS file for styling the file browser.

    Methods
    -------
    __init__(title, path_test_function, **kwargs)
        Initializes the FileBrowserModal.
    on_mount()
        Executed when the modal is mounted. Mounts the directory tree and
        path input components.
    _select_or_input_path_changed(message)
        Event handler for changes in the path selection or input. Manages
        the expansion and collapse of directory nodes.
    on_filtered_directory_tree_directory_or_file_selected(message)
        Event handler for directory or file selection changes. Updates the
        selected directory and path input prompt.
    update_from_input()
        Updates the selected directory based on input value from the path
        input box.
    ok()
        Confirms the selected path and calls the confirm window function.
    cancel()
        Cancels the file browsing and calls the cancel window function.
    key_escape()
        Cancels the file browsing when the escape key is pressed.
    _confirm_window()
        Validates the selected path and dismisses the modal if valid,
        otherwise shows an error message.
    _cancel_window()
        Dismisses the modal without selecting any path.
    """

    CSS_PATH = ["tcss/file_browser.tcss"]

    def __init__(self, title="Browse", path_test_function=None, **kwargs) -> None:
        """
        Initializes the FileBrowserModal.

        Parameters
        ----------
        title : str, optional
            The title of the modal window, by default "Browse".
        path_test_function : callable, optional
            A function to test the validity of the selected path, by
            default None. If None, the `path_test` function is used.
        **kwargs : dict
            Additional keyword arguments passed to the base class
            constructor.
        """
        super().__init__(**kwargs)
        # A list of expanded nodes in the directory tree.
        self.expanded_nodes: list = []
        # The title of the modal window.
        self.title_bar.title = title
        # The function used to test the validity of the selected path.
        self.path_test_function = path_test if path_test_function is None else path_test_function

    def on_mount(self) -> None:
        """
        Executed when the modal is mounted.

        This method is called when the modal is mounted. It mounts the
        directory tree, path input box (SelectOrInputPath), and action buttons to the modal
        content.
        """
        pass

    @on(SelectOrInputPath.PromptChanged)
    def _select_or_input_path_changed(self, message):
        """
        Event handler for changes in the path selection or input.

        This method is called when the path selection or input changes. It
        manages the expansion and collapse of directory nodes in the
        directory tree based on the selected path.

        Parameters
        ----------
        message : SelectOrInputPath.PromptChanged
            The message object containing information about the path
            change.
        """
        pass

    @on(FilteredDirectoryTree.DirectorySelected, ".browse_tree")
    @on(FilteredDirectoryTree.FileSelected, ".browse_tree")
    # @on(FilteredDirectoryTree.NodeChanged, ".browse_tree")
    def on_filtered_directory_tree_directory_or_file_selected(self, message):
        """
        Event handler for directory or file selection changes.

        This method is called when a directory or file is selected in the
        directory tree. It updates the selected directory and the path
        input prompt.

        Parameters
        ----------
        message : FilteredDirectoryTree.DirectorySelected | FilteredDirectoryTree.FileSelected
            The message object containing information about the selection.
        """
        pass

    @on(Input.Submitted, "#path_input_box2")
    def update_from_input(self):
        """
        Updates the selected directory based on input value.

        This method is called when the user submits a value in the path
        input box. It updates the `selected_directory` attribute with the
        new value.
        """
        pass

    @on(Button.Pressed, ".ok")
    async def ok(self):
        """
        Confirms the selected path.

        This method is called when the user presses the "Ok" button. It
        calls `_confirm_window` to validate the selected path and dismiss
        the modal.
        """
        pass

    @on(Button.Pressed, ".cancel")
    def cancel(self):
        """
        Cancels the file browsing.

        This method is called when the user presses the "Cancel" button. It
        calls `_cancel_window` to dismiss the modal without selecting any
        path.
        """
        self._cancel_window()

    def key_escape(self):
        """
        Cancels the file browsing when the escape key is pressed.

        This method is called when the user presses the Escape key. It
        calls `_cancel_window` to dismiss the modal without selecting any
        path.
        """
        pass


    async def _confirm_window(self):
        """
        Validates the selected path and dismisses the modal.

        This method validates the selected path using the
        `path_test_function`. If the path is valid, it dismisses the
        modal with the selected path. If the path is not found, it
        prompts the user to create a new directory. If the path is
        invalid for other reasons, it displays an error message.
        """
        pass

    def _cancel_window(self):
        """
        Dismisses the modal without selecting any path.

        This method dismisses the modal window without making any changes.
        """
        self.dismiss("")

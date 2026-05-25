from dataclasses import dataclass
from pathlib import Path

from rich.text import Text
from textual import on, work
from textual.containers import VerticalScroll
from textual.message import Message
from textual.widget import Widget
from textual.widgets import Button, SelectionList
from textual.widgets.selection_list import Selection

from ...logging import logger
from ..data_analyzers.file_pattern_steps import (
    MatEventsStep,
    TsvEventsStep,
    TxtEventsStep,
)
from ..help_functions import extract_name_part
from ..specialized_widgets.non_bids_file_itemization import FileItem


class FilePanelTemplate(Widget):
    """
    A template class for creating panels that manage a collection of files.

    This class provides a base structure for creating panels that allow
    users to add, manage, and interact with a list of files. It includes
    functionality for adding new file items, handling file item deletion,
    and updating the panel's state.

    Attributes
    ----------
    _counter : ClassVar[int]
        A class-level counter to keep track of the number of file patterns.
    class_name : ClassVar[str | None]
        The name of the class, used for identification.
    id_string : ClassVar[str]
        The ID string used to identify the panel in the UI.
    file_item_id_base : ClassVar[str]
        The base ID used for generating unique IDs for file items.
    the_class : ClassVar[Type["FilePanelTemplate"] | None]
        A reference to the class itself.
    pattern_class : ClassVar[Type[Any] | None]
        The class used for creating file pattern steps.
    current_file_pattern_id : str | None
        The ID of the currently FilePanelTemplateactive file pattern.
    value : reactive[bool]
        A reactive attribute that indicates whether the panel's state has changed.

    Methods
    -------
    __init__(id, classes)
        Initializes the FilePanelTemplate instance.
    callback_func(message_dict)
        Processes a message dictionary and formats text messages for callback.
    watch_value()
        Posts a message when the value changes.
    compose() -> ComposeResult
        Composes the widget's components.
    _on_button_add_file_item_pressed()
        Handles the event when the add file item button is pressed.
    add_file_item_pressed()
        Initiates the creation of a new file item.
    create_file_item(load_object, message_dict)
        Creates and mounts a new file item widget.
    on_mount()
        Handles actions upon mounting the panel to the application.
    _on_file_item_is_deleted(message)
        Handles the event when a file item is deleted.
    _on_update_all_instances(event)
        Updates instances when a file item is finished or its path pattern changes.
    reset_all_counters()
        Recursively reset counters for all subclasses.
    """

    # A class-level counter to keep track of the number of file patterns.
    _counter = 0
    # The name of the class, used for identification.
    class_name: None | str = None
    # The ID string used to identify the panel in the UI.
    id_string: str = ""
    # The base ID used for generating unique IDs for file items.
    file_item_id_base: str = ""
    # A reference to the class itself.
    the_class = None
    # The class used for creating file pattern steps.
    pattern_class: type | None = None
    # The ID of the currently active file pattern.
    current_file_pattern_id = None
    # # A reactive attribute that indicates whether the panel's state has changed.
    # value: reactive[bool] = reactive(None, init=False)
    filters: dict

    @dataclass
    class FileItemIsDeleted(Message):
        file_panel: Widget
        deleted_id: str
        value: str | Path

        @property
        def control(self):
            """Alias for self.file_browser."""
            pass

    @dataclass
    class Changed(Message):
        file_panel: Widget
        value: str

        @property
        def control(self):
            """Alias for self.file_browser."""
            pass

    @dataclass
    class FileTagsChanged(Message):
        file_tag_selection: Widget
        value: list

        @property
        def control(self):
            """Alias for self.file_browser."""
            pass

    def __init__(self, default_file_tags=None, file_tagging=False, id: str | None = None, classes: str | None = None) -> None:
        """
        Initializes the FilePanelTemplate instance.

        Parameters
        ----------
        id : str, optional
            An optional identifier for the widget, by default None.
        classes : str, optional
            An optional string of classes for applying styles to the
            widget, by default None.
        """
        super().__init__(id=id, classes=classes)
        type(self).the_class = self.__class__  # Sets the_class at the class level
        self.the_app = self.app

        cls = type(self)  # Get the actual class of the instance
        if not hasattr(cls, "_counter"):  # Ensure each child class has its own counter
            cls._counter = 0
        self.file_pattern_counter = cls._counter
        self.value = None
        self.default_file_tags: list[str] = default_file_tags if default_file_tags is not None else []
        if not hasattr(cls, "filters") or cls.filters is None:
            raise TypeError(f"Class {cls.__name__} must define a class attribute 'filters'")
        self.file_tagging = file_tagging

    def callback_func(self, message_dict):
        """
        Processes a message dictionary and formats text messages for callback.

        This method takes a dictionary of messages, formats them into a
        rich text string, and stores the result in the `callback_message`
        attribute.

        Parameters
        ----------
        message_dict : dict[str, list[str]]
            A dictionary where keys are message categories and values are
            lists of messages.
        """
        pass

    def compose(self):
        """
        Composes the widget's components.

        This method defines the layout and components of the widget,
        including a vertical scroll container and an "Add" button.

        Yields
        ------
        VerticalScroll
            The composed widgets.
        """
        pass

    @on(Button.Pressed, "#add_file_button")
    async def _on_button_add_file_item_pressed(self):
        """
        Handles the event when the add file item button is pressed.

        This method is called when the user presses the "Add" button. It
        calls `add_file_item_pressed` to initiate the creation of a new
        file item.
        """
        pass

    async def add_file_item_pressed(self):
        """
        Initiates the creation of a new file item.

        This method is called when the user wants to add a new file item.
        It calls `create_file_item` to create and mount the new file item
        widget.
        """
        pass

    async def create_file_item(self, load_object=None, message_dict=None):
        """
        Creates and mounts a new file item widget.

        This method creates a new `FileItem` widget, mounts it to the
        panel, and updates the panel's state. It handles both the case
        where a new file item is being added and the case where a file
        item is being loaded from existing data.

        Parameters
        ----------
        load_object : Any, optional
            An object containing data to load into the file item, by
            default None.
        message_dict : dict[str, list[str]] | None, optional
            A dictionary of messages to display in the file item, by
            default None.

        Returns
        -------
        str | None
            The ID of the newly created file item, or None if the file
            item could not be created.
        """

        async def mount_file_item_widget():
            if self.the_class is not None and self.pattern_class is not None:
                the_file_item = FileItem(
                    id=self.file_item_id_base + str(self.file_pattern_counter),
                    classes="file_patterns",
                    pattern_class=self.pattern_class(app=self.app, callback=self.callback_func),
                    edit_button=False,
                )
                # regular FileItem mount when user clicks "Add" and creates the file pattern
                await self.get_widget_by_id(self.id_string).mount(the_file_item)
                self.current_file_pattern_id = self.file_item_id_base + str(self.file_pattern_counter)

                self.file_pattern_counter += 1
                self.refresh()

        if load_object is None:
            await mount_file_item_widget()
        else:
            # Mounting, for example, when loading the spec file
            if self.the_class is not None:
                # EventFilePanel has pattern_class=None by default, since when user is adding it, he/she is prompt to
                # specify the type. However, if loading from a spec file, we need to determine this by the extension of the
                # item in the spec file
                if self.pattern_class is None:
                    extension_mapping = {".tsv": TsvEventsStep, ".mat": MatEventsStep, ".txt": TxtEventsStep}
                    self.pattern_class = extension_mapping.get(load_object.__dict__["extension"])

                if self.pattern_class is not None:
                    await self.get_widget_by_id(self.id_string).mount(
                        FileItem(
                            id=self.file_item_id_base + str(self.file_pattern_counter),
                            classes="file_patterns",
                            load_object=load_object,
                            message_dict=message_dict,
                            pattern_class=self.pattern_class(app=self.app, callback=self.callback_func),
                            execute_pattern_class_on_mount=False,
                            edit_button=False,
                        )
                    )

                self.current_file_pattern_id = self.file_item_id_base + str(self.file_pattern_counter)
                self.file_pattern_counter += 1

        return self.current_file_pattern_id

    def on_mount(self):
        """
        Handles actions upon mounting the panel to the application.

        This method is called when the panel is mounted to the application.
        It handles the case where a new feature is added and copies the
        file items from the first feature's panel to the new panel.
        """
        pass

    @on(FileItem.IsDeleted)
    async def _on_file_item_is_deleted(self, message):
        """
        Handles the event when a file item is deleted.

        This method is called when a `FileItem.IsDeleted` message is
        received. It removes the deleted file item from the panel and
        posts a `FileItemIsDeleted` message to notify other parts of the
        application.

        Parameters
        ----------
        message : FileItem.IsDeleted
            The message object containing information about the deleted
            file item.
        """
        pass

    @classmethod
    def reset_all_counters(cls):
        """
        Recursively reset counters for all subclasses.

        This method resets the `_counter` attribute for the class and all
        its subclasses. It is used to ensure that file item IDs are
        unique across different instances of the panel.
        """
        pass

    @on(FileItem.PathPatternChanged)
    def on_file_panel_changed(self, message: Message) -> None:
        """
        Handles changes in the file panel.

        This method is called when the file panel changes. It extracts
        tags from the file paths based on the file pattern and updates
        the file tag selection list.

        Parameters
        ----------
        message : Message
            The message object containing information about the change.
        """
        pass

    @work(exclusive=False, name="update_file_tag_selection")
    async def update_file_tag_selection(self, file_tags: set, remove=False) -> None:
        """
        Updates the tag selection list based on the provided tag values.

        This method updates the tag selection list with the provided tag
        values. It handles the initial selection of tags and subsequent
        updates.

        Parameters
        ----------
        file_tags : set
            A set of tag values to update the selection list with.
        """
        pass


    def _extract_file_tags(self, file_pattern, files, file_tag=None):
        """
        Extract file tags based on the given file pattern, file paths, and optional file_tag.
        Falls back to 'desc' suffix if no tags are found with the main suffix.

        Parameters
        ----------
        file_pattern : str
            The pattern used to extract tags.
        files : list[str]
            List of file paths.
        file_tag : str | None
            A provided file tag. If given, it's used directly.

        Returns
        -------
        set[str | None]
            A set of extracted file tags.
        """
        pass

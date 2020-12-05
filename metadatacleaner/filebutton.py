"""Button representing the file state."""

from gi.repository import Gtk

from metadatacleaner.file import File, FileState
from metadatacleaner.filepopover import FilePopover
from metadatacleaner.metadatawindow import MetadataWindow


@Gtk.Template(
    resource_path="/fr/romainvigier/MetadataCleaner/ui/FileButton.ui"
)
class FileButton(Gtk.Button):
    """Button representing the file state."""

    __gtype_name__ = "FileButton"

    _state_stack: Gtk.Stack = Gtk.Template.Child()

    def __init__(self, f: File, *args, **kwargs) -> None:
        """Button initialization.

        Args:
            f (File): The file the button will represent.
        """
        super().__init__(*args, **kwargs)
        self._file = f
        self._file.connect("state-changed", self._on_file_state_changed)

    def _sync_file_button_to_state(self) -> None:
        page = {
            FileState.INITIALIZING: "working",
            FileState.ERROR_WHILE_INITIALIZING: "error",
            FileState.UNSUPPORTED: "error",
            FileState.SUPPORTED: "working",
            FileState.CHECKING_METADATA: "working",
            FileState.ERROR_WHILE_CHECKING_METADATA: "error",
            FileState.HAS_NO_METADATA: "warning",
            FileState.HAS_METADATA: "has-metadata",
            FileState.REMOVING_METADATA: "working",
            FileState.ERROR_WHILE_REMOVING_METADATA: "error",
            FileState.CLEANED: "clean",
            FileState.SAVING: "working",
            FileState.ERROR_WHILE_SAVING: "error",
            FileState.SAVED: "clean"
        }
        self._state_stack.set_visible_child_name(page[self._file.state])

    @Gtk.Template.Callback()
    def _on_file_button_clicked(self, button: Gtk.Button) -> None:
        if self._file.state is FileState.HAS_METADATA:
            self.show_metadata_window()
        else:
            self.show_popover()

    def _on_file_state_changed(self, file: File, new_state: FileState) -> None:
        self._sync_file_button_to_state()

    def show_popover(self) -> None:
        """Show the popover with details about the file's state."""
        popover = FilePopover(self._file)
        popover.set_relative_to(self)
        popover.popup()

    def show_metadata_window(self) -> None:
        """Show the window with the details about the file's metadata."""
        window = MetadataWindow(
            transient_for=self.get_toplevel(),
            f=self._file
        )
        window.show()

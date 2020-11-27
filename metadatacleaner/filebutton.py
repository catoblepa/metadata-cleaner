from gi.repository import Gtk
from typing import Optional

from metadatacleaner.file import File, FileState
from metadatacleaner.filepopover import FilePopover


@Gtk.Template(
    resource_path="/fr/romainvigier/MetadataCleaner/ui/FileButton.ui"
)
class FileButton(Gtk.Button):

    __gtype_name__ = "FileButton"

    # _button: Gtk.Button = Gtk.Template.Child()
    _state_stack: Gtk.Stack = Gtk.Template.Child()

    _popover: Optional[FilePopover] = None

    def __init__(self, app: Gtk.Application, f: File) -> None:
        super().__init__()
        self._app = app
        self._file = f
        self._setup_popover()
        self._file.connect("state-changed", self._on_file_state_changed)

    @Gtk.Template.Callback()
    def _on_file_button_clicked(self, button) -> None:
        self.show_popover()

    def _on_file_state_changed(self, file, new_state) -> None:
        self._sync_file_button_to_state()

    def _setup_popover(self) -> None:
        self._popover = FilePopover(self._app, self._file)
        self._popover.set_relative_to(self)

    def _sync_file_button_to_state(self) -> None:
        page = {
            FileState.INITIALIZING: "working",
            FileState.ERROR_WHILE_INITIALIZING: "error",
            FileState.UNSUPPORTED: "error",
            FileState.SUPPORTED: "working",
            FileState.CHECKING_METADATA: "working",
            FileState.ERROR_WHILE_CHECKING_METADATA: "error",
            FileState.HAS_NO_METADATA: "clean",
            FileState.HAS_METADATA: "has-metadata",
            FileState.REMOVING_METADATA: "working",
            FileState.ERROR_WHILE_REMOVING_METADATA: "error",
            FileState.CLEANED: "clean",
            FileState.SAVING: "working",
            FileState.ERROR_WHILE_SAVING: "error",
            FileState.SAVED: "clean"
        }
        self._state_stack.set_visible_child_name(page[self._file.state])

    def show_popover(self) -> None:
        if self._popover:
            self._popover.popup()

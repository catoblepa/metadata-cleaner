"""Row representing a file."""

from gi.repository import Gio, Gtk, Handy
from typing import Optional

from metadatacleaner.file import File, FileState
from metadatacleaner.filebutton import FileButton


@Gtk.Template(
    resource_path="/fr/romainvigier/MetadataCleaner/ui/FileRow.ui"
)
class FileRow(Handy.ActionRow):
    """Row representing a file."""

    __gtype_name__ = "FileRow"

    def __init__(self, f: File, *args, **kwargs) -> None:
        """Row initialization.

        Args:
            f (File): The file the row will represent.
        """
        super().__init__(*args, **kwargs)
        self._window: Optional[Gtk.Widget] = None
        self._file = f
        self._setup_title()
        self._setup_file_button()
        self.connect("hierarchy-changed", self._on_hierarchy_changed)
        self._file.connect("state-changed", self._on_file_state_changed)
        self._file.connect("removed", self._on_file_removed)

    def _on_hierarchy_changed(
        self,
        widget: Gtk.Widget,
        previous_toplevel: Optional[Gtk.Widget]
    ) -> None:
        self._window = self.get_toplevel()
        if not hasattr(self._window, "files_manager"):
            self._window = None

    @Gtk.Template.Callback()
    def _on_remove_file_button_clicked(self, button: Gtk.Button) -> None:
        if not self._window:
            return
        self._window.files_manager.remove_file(self._file)

    def _on_file_state_changed(self, file: File, new_state: FileState) -> None:
        self._sync_icon()

    def _on_file_removed(self, file: File) -> None:
        self.destroy()

    def _setup_title(self) -> None:
        self.set_title(self._file.filename)

    def _setup_file_button(self) -> None:
        self._file_button = FileButton(self._file)
        self.add(self._file_button)
        self.set_activatable_widget(self._file_button)

    def _sync_icon(self) -> None:
        icon_name = Gio.content_type_get_generic_icon_name(self._file.mimetype)
        self.set_icon_name(icon_name)

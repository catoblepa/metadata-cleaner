from gettext import gettext as _
from gi.repository import Gdk, Gio, GLib, Gtk, Handy
from typing import Optional

from metadatacleaner.filebutton import FileButton
from metadatacleaner.filesmanager import File, FileState


@Gtk.Template(
    resource_path="/fr/romainvigier/MetadataCleaner/ui/FileRow.ui"
)
class FileRow(Handy.ActionRow):

    __gtype_name__ = "FileRow"

    _file_button: Optional[FileButton] = None

    def __init__(self, app: Gtk.Application, f: File) -> None:
        super().__init__()
        self._app = app
        self._file = f
        self._setup_title()
        self._setup_file_button()
        self._file.connect("state-changed", self._on_file_state_changed)
        self._file.connect("removed", self._on_file_removed)

    @Gtk.Template.Callback()
    def _on_remove_file_button_clicked(self, button) -> None:
        self._app.files_manager.remove(self._file)

    def _on_file_state_changed(self, file, new_state) -> None:
        self._sync_icon()

    def _on_file_removed(self, file) -> None:
        self.destroy()

    def _setup_title(self) -> None:
        self.set_title(self._file.filename)

    def _setup_file_button(self) -> None:
        self._file_button = FileButton(self._app, self._file)
        self.add(self._file_button)
        self.set_activatable_widget(self._file_button)

    def _sync_icon(self) -> None:
        icon_name = Gio.content_type_get_generic_icon_name(self._file.mimetype)
        self.set_icon_name(icon_name)

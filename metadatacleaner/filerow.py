from gettext import gettext as _
from gi.repository import Gdk, Gio, GLib, Gtk
from typing import Optional

from metadatacleaner.filebutton import FileButton
from metadatacleaner.filesmanager import File, FileState


@Gtk.Template(
    resource_path="/fr/romainvigier/MetadataCleaner/ui/FileRow.ui"
)
class FileRow(Gtk.ListBoxRow):

    __gtype_name__ = "FileRow"

    _box: Gtk.Box = Gtk.Template.Child()
    _file_label: Gtk.Label = Gtk.Template.Child()

    _file_button: Optional[FileButton] = None

    def __init__(self, app: Gtk.Application, f: File) -> None:
        super().__init__()
        self._app = app
        self._file = f
        self._setup_file_label()
        self._setup_file_button()

    def _setup_file_label(self) -> None:
        self._file_label.set_label(self._file.filename)
        self._file_label.set_tooltip_text(self._file.filename)

    def _setup_file_button(self) -> None:
        self._file_button = FileButton(self._app, self._file)
        self._box.pack_end(self._file_button, False, True, 0)

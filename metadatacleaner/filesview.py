from gi.repository import Gtk, Handy
from typing import Optional

from metadatacleaner.cleanmetadatabutton import CleanMetadataButton
from metadatacleaner.filerow import FileRow
from metadatacleaner.savefilesbutton import SaveFilesButton
from metadatacleaner.statusindicator import StatusIndicator


@Gtk.Template(resource_path="/fr/romainvigier/MetadataCleaner/ui/FilesView.ui")
class FilesView(Gtk.Box):

    __gtype_name__ = "FilesView"

    _files_list_box: Gtk.ListBox = Gtk.Template.Child()
    _actionbar: Gtk.ActionBar = Gtk.Template.Child()

    def __init__(self) -> None:
        super().__init__()
        self._window: Optional[Gtk.Window] = None
        self.connect("realize", self._on_realize)

    def _on_realize(self, widget) -> None:
        self._window = self.get_toplevel()
        self._window.files_manager.connect("file-added", self._on_file_added)
        self._setup_actionbar()

    def _on_file_added(self, files_manager, new_file_index) -> None:
        f = files_manager.get_file(new_file_index)
        self._files_list_box.add(FileRow(f))

    def _setup_actionbar(self) -> None:
        self._actionbar.pack_start(StatusIndicator())
        self._actionbar.pack_end(SaveFilesButton())
        self._actionbar.pack_end(CleanMetadataButton())

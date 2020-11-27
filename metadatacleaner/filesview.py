from gi.repository import Gtk, Handy

from metadatacleaner.cleanmetadatabutton import CleanMetadataButton
from metadatacleaner.filerow import FileRow
from metadatacleaner.savefilesbutton import SaveFilesButton
from metadatacleaner.statusindicator import StatusIndicator


@Gtk.Template(resource_path="/fr/romainvigier/MetadataCleaner/ui/FilesView.ui")
class FilesView(Gtk.Box):

    __gtype_name__ = "FilesView"

    _files_list_box: Gtk.ListBox = Gtk.Template.Child()
    _actionbar: Gtk.ActionBar = Gtk.Template.Child()

    def __init__(self, app: Gtk.Application) -> None:
        super().__init__()
        self._app = app
        self._setup_actionbar()
        self._app.files_manager.connect("file-added", self._on_file_added)

    def _on_file_added(self, file_manager, new_file_index) -> None:
        f = self._app.files_manager.get_file(new_file_index)
        self._files_list_box.add(FileRow(self._app, f))

    def _setup_actionbar(self) -> None:
        self._actionbar.pack_start(StatusIndicator(self._app))
        self._actionbar.pack_end(SaveFilesButton(self._app))
        self._actionbar.pack_end(CleanMetadataButton(self._app))

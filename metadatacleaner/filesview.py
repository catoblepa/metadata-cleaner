from gi.repository import Gtk, Handy

from metadatacleaner.addfilesbutton import AddFilesButton
from metadatacleaner.filerow import FileRow
from metadatacleaner.cleanmetadatabutton import CleanMetadataButton


@Gtk.Template(resource_path="/fr/romainvigier/MetadataCleaner/ui/FilesView.ui")
class FilesView(Gtk.Box):

    __gtype_name__ = "FilesView"

    _headerbar: Handy.HeaderBar = Gtk.Template.Child()
    _files_list_box: Gtk.ListBox = Gtk.Template.Child()

    def __init__(self, app: Gtk.Application) -> None:
        super().__init__()
        self._app = app
        self._setup_headerbar()
        self._app.files_manager.connect("file-added", self._on_file_added)

    def _on_file_added(self, file_manager, new_file_index):
        f = self._app.files_manager.get_file(new_file_index)
        self._files_list_box.add(FileRow(self._app, f))

    def _setup_headerbar(self) -> None:
        self._headerbar.pack_start(AddFilesButton(self._app))
        self._headerbar.pack_end(CleanMetadataButton(self._app))

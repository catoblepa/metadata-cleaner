"""View showing all the files."""

from gi.repository import Gtk
from typing import Optional

from metadatacleaner.cleanmetadatabutton import CleanMetadataButton
from metadatacleaner.filerow import FileRow
from metadatacleaner.filesmanager import FilesManager
from metadatacleaner.savefilesbutton import SaveFilesButton
from metadatacleaner.statusindicator import StatusIndicator


@Gtk.Template(resource_path="/fr/romainvigier/MetadataCleaner/ui/FilesView.ui")
class FilesView(Gtk.Box):
    """View showing all the files."""

    __gtype_name__ = "FilesView"

    _files_list_box: Gtk.ListBox = Gtk.Template.Child()
    _actionbar: Gtk.ActionBar = Gtk.Template.Child()

    def __init__(self, *args, **kwargs) -> None:
        """View initialization."""
        super().__init__(*args, **kwargs)
        self._window: Optional[Gtk.Widget] = None
        self.connect("hierarchy-changed", self._on_hierarchy_changed)

    def _on_hierarchy_changed(
        self,
        widget: Gtk.Widget,
        previous_toplevel: Optional[Gtk.Widget]
    ) -> None:
        self._window = self.get_toplevel()
        if not hasattr(self._window, "files_manager"):
            self._window = None
            return
        self._window.files_manager.connect("file-added", self._on_file_added)
        self._setup_actionbar()

    def _on_file_added(
        self,
        files_manager: FilesManager,
        new_file_index: int
    ) -> None:
        f = files_manager.get_file(new_file_index)
        self._files_list_box.add(FileRow(f))

    def _setup_actionbar(self) -> None:
        self._actionbar.pack_start(StatusIndicator())
        self._actionbar.pack_end(SaveFilesButton())
        self._actionbar.pack_end(CleanMetadataButton())

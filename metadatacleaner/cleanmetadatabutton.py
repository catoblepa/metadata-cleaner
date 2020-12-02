"""Button to clean metadata of all added files."""

from gi.repository import Gtk
from typing import Optional

from metadatacleaner.filesmanager import FilesManager, FilesManagerState


@Gtk.Template(
    resource_path="/fr/romainvigier/MetadataCleaner/ui/CleanMetadataButton.ui"
)
class CleanMetadataButton(Gtk.Bin):
    """Button to clean metadata of all added files."""

    __gtype_name__ = "CleanMetadataButton"

    _button: Gtk.Button = Gtk.Template.Child()

    def __init__(self, *args, **kwargs) -> None:
        """Button initialization."""
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
        self._window.files_manager.connect(
            "file-removed",
            self._on_file_removed
        )
        self._window.files_manager.connect(
            "file-state-changed",
            self._on_file_state_changed
        )
        self._window.files_manager.connect(
            "state-changed",
            self._on_files_manager_state_changed
        )
        self._sync_button_sensitivity()

    def _on_file_added(
        self,
        files_manager: FilesManager,
        file_index: int
    ) -> None:
        self._sync_button_sensitivity()

    def _on_file_removed(self, files_manager: FilesManager) -> None:
        self._sync_button_sensitivity()

    def _on_file_state_changed(
        self,
        files_manager: FilesManager,
        file_index: int
    ) -> None:
        self._sync_button_sensitivity()

    def _on_files_manager_state_changed(
        self,
        files_manager: FilesManager,
        new_state: FilesManagerState
    ) -> None:
        self._sync_button_sensitivity()

    def _sync_button_sensitivity(self) -> None:
        if not self._window:
            return
        if self._window.files_manager.state == FilesManagerState.WORKING \
                or len(self._window.files_manager.get_cleanable_files()) == 0:
            self._button.set_sensitive(False)
        else:
            self._button.set_sensitive(True)

from gi.repository import Gtk

from metadatacleaner.filesmanager import FilesManager, FilesManagerState


@Gtk.Template(
    resource_path="/fr/romainvigier/MetadataCleaner/ui/SaveFilesButton.ui"
)
class SaveFilesButton(Gtk.Bin):

    __gtype_name__ = "SaveFilesButton"

    _button: Gtk.Button = Gtk.Template.Child()

    def __init__(self, app):
        super().__init__()
        self._app = app
        self._sync_button_sensitivity()
        self._app.files_manager.connect("file-added", self._on_file_added)
        self._app.files_manager.connect("file-removed", self._on_file_removed)
        self._app.files_manager.connect(
            "file-state-changed",
            self._on_file_state_changed
        )
        self._app.files_manager.connect(
            "state-changed",
            self._on_files_manager_state_changed
        )

    @Gtk.Template.Callback()
    def _on_save_files_button_clicked(self, button):
        self._app.save_cleaned_files()

    def _on_file_added(self, files_manager, file_index) -> None:
        self._sync_button_sensitivity()

    def _on_file_removed(self, files_manager) -> None:
        self._sync_button_sensitivity()

    def _on_file_state_changed(self, files_manager, file_index) -> None:
        self._sync_button_sensitivity()

    def _on_files_manager_state_changed(
        self,
        files_manager: FilesManager,
        new_state: FilesManagerState
    ) -> None:
        self._sync_button_sensitivity()

    def _sync_button_sensitivity(self) -> None:
        if self._app.files_manager.state == FilesManagerState.WORKING \
                or len(self._app.files_manager.get_cleaned_files()) == 0:
            self._button.set_sensitive(False)
        else:
            self._button.set_sensitive(True)

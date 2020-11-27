from gi.repository import Gtk


@Gtk.Template(
    resource_path="/fr/romainvigier/MetadataCleaner/ui/CleanMetadataButton.ui"
)
class CleanMetadataButton(Gtk.Bin):

    __gtype_name__ = "CleanMetadataButton"

    _button: Gtk.Button = Gtk.Template.Child()

    def __init__(self, app) -> None:
        super().__init__()
        self._app = app
        self._sync_button_sensitivity()
        self._app.files_manager.connect("file-added", self._on_file_added)
        self._app.files_manager.connect("file-removed", self._on_file_removed)
        self._app.files_manager.connect(
            "file-state-changed",
            self._on_file_state_changed
        )

    @Gtk.Template.Callback()
    def _on_clean_metadata_button_clicked(self, button) -> None:
        self._app.clean_metadata()

    def _on_file_added(self, files_manager, file_index) -> None:
        self._sync_button_sensitivity()

    def _on_file_removed(self, files_manager) -> None:
        self._sync_button_sensitivity()

    def _on_file_state_changed(self, files_manager, file_index) -> None:
        self._sync_button_sensitivity()

    def _sync_button_sensitivity(self) -> None:
        if len(self._app.files_manager.get_cleanable_files()) == 0:
            self._button.set_sensitive(False)
        else:
            self._button.set_sensitive(True)

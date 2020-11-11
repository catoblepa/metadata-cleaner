from gi.repository import Gtk


@Gtk.Template(
    resource_path="/fr/romainvigier/MetadataCleaner/ui/AddFilesButton.ui"
)
class AddFilesButton(Gtk.Bin):

    __gtype_name__ = "AddFilesButton"

    def __init__(self, app):
        super().__init__()
        self._app = app

    @Gtk.Template.Callback()
    def _on_add_files_button_clicked(self, button):
        self._app.add_files()

from gi.repository import Gtk


@Gtk.Template(
    resource_path="/fr/romainvigier/MetadataCleaner/ui/AddFilesButton.ui"
)
class AddFilesButton(Gtk.Button):

    __gtype_name__ = "AddFilesButton"

    def __init__(self):
        super().__init__()

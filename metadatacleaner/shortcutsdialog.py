from gi.repository import Gtk


@Gtk.Template(
    resource_path="/fr/romainvigier/MetadataCleaner/ui/ShortcutsDialog.ui"
)
class ShortcutsDialog(Gtk.ShortcutsWindow):

    __gtype_name__ = "ShortcutsDialog"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

from gi.repository import Gtk


@Gtk.Template(
    resource_path="/fr/romainvigier/MetadataCleaner/ui/AboutDialog.ui"
)
class AboutDialog(Gtk.AboutDialog):

    __gtype_name__ = "AboutDialog"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

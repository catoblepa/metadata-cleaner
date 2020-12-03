"""About dialog giving informations about the application."""

from gi.repository import Gtk


@Gtk.Template(
    resource_path="/fr/romainvigier/MetadataCleaner/ui/AboutDialog.ui"
)
class AboutDialog(Gtk.AboutDialog):
    """About dialog."""

    __gtype_name__ = "AboutDialog"

    def __init__(self, *args, **kwargs) -> None:
        """About dialog initialization."""
        super().__init__(*args, **kwargs)

"""Dialog showing keyboard shortcuts."""

from gi.repository import Gtk


@Gtk.Template(
    resource_path="/fr/romainvigier/MetadataCleaner/ui/ShortcutsDialog.ui"
)
class ShortcutsDialog(Gtk.ShortcutsWindow):
    """Dialog showing keyboard shortcuts."""

    __gtype_name__ = "ShortcutsDialog"

    def __init__(self, *args, **kwargs):
        """Dialog initialization."""
        super().__init__(*args, **kwargs)

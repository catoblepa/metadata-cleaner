"""View when no files are added."""

from gi.repository import Gtk


@Gtk.Template(resource_path="/fr/romainvigier/MetadataCleaner/ui/EmptyView.ui")
class EmptyView(Gtk.Box):
    """View when no files are added."""

    __gtype_name__ = "EmptyView"

    def __init__(self, *args, **kwargs) -> None:
        """View initialization."""
        super().__init__(*args, **kwargs)

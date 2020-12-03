"""Menu Popover."""

from gi.repository import Gtk


@Gtk.Template(
    resource_path="/fr/romainvigier/MetadataCleaner/ui/MenuPopover.ui"
)
class MenuPopover(Gtk.PopoverMenu):
    """Menu Popover."""

    __gtype_name__ = "MenuPopover"

    def __init__(self, *args, **kwargs) -> None:
        """Popover initialization."""
        super().__init__(*args, **kwargs)

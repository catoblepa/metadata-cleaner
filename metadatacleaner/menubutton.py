"""Menu button."""

from gi.repository import Gtk

from metadatacleaner.menupopover import MenuPopover


@Gtk.Template(
    resource_path="/fr/romainvigier/MetadataCleaner/ui/MenuButton.ui"
)
class MenuButton(Gtk.MenuButton):
    """Menu button."""

    __gtype_name__ = "MenuButton"

    def __init__(self, *args, **kwargs) -> None:
        """Menu button initialization."""
        super().__init__(*args, **kwargs)
        self._setup_popover()

    def _setup_popover(self) -> None:
        self._popover = MenuPopover()
        self.set_popover(self._popover)

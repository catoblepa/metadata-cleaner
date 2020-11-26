from gi.repository import Gtk
from typing import Optional

from metadatacleaner.menupopover import MenuPopover


@Gtk.Template(
    resource_path="/fr/romainvigier/MetadataCleaner/ui/MenuButton.ui"
)
class MenuButton(Gtk.MenuButton):

    __gtype_name__ = "MenuButton"

    _popover: Optional[MenuPopover] = None

    def __init__(self, app):
        super().__init__()
        self._app = app
        self._setup_popover()

    def _setup_popover(self) -> None:
        self._popover = MenuPopover(self._app)
        self.set_popover(self._popover)

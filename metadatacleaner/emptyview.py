from gi.repository import Gtk, Handy

from metadatacleaner.addfilesbutton import AddFilesButton
from metadatacleaner.menubutton import MenuButton


@Gtk.Template(resource_path="/fr/romainvigier/MetadataCleaner/ui/EmptyView.ui")
class EmptyView(Gtk.Box):

    __gtype_name__ = "EmptyView"

    _headerbar: Handy.HeaderBar = Gtk.Template.Child()
    _box: Gtk.Box = Gtk.Template.Child()

    def __init__(self, app: Gtk.Application) -> None:
        super().__init__()
        self._app = app
        self._setup_headerbar()
        self._setup_box()

    def _setup_headerbar(self) -> None:
        self._headerbar.pack_start(AddFilesButton(self._app))
        self._headerbar.pack_end(MenuButton(self._app))

    def _setup_box(self) -> None:
        pass

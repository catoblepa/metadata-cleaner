from gi.repository import Gtk, Handy

from metadatacleaner.addfilesbutton import AddFilesButton


@Gtk.Template(resource_path="/fr/romainvigier/MetadataCleaner/ui/EmptyView.ui")
class EmptyView(Gtk.Box):

    __gtype_name__ = "EmptyView"

    _headerbar: Handy.HeaderBar = Gtk.Template.Child()
    _box: Gtk.Box = Gtk.Template.Child()

    def __init__(self, app: Gtk.Application) -> None:
        super().__init__()
        self._app = app
        self._box.pack_end(AddFilesButton(self._app), False, True, 0)

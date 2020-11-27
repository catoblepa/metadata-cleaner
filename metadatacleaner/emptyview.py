from gi.repository import Gtk


@Gtk.Template(resource_path="/fr/romainvigier/MetadataCleaner/ui/EmptyView.ui")
class EmptyView(Gtk.Box):

    __gtype_name__ = "EmptyView"

    def __init__(self, app: Gtk.Application) -> None:
        super().__init__()
        self._app = app

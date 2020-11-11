from gettext import gettext as _
from gi.repository import Gdk, Gio, GLib, Gtk

from metadatacleaner.filesmanager import File, FilesManager
from metadatacleaner.window import Window


class MetadataCleaner(Gtk.Application):

    _window = None
    files_manager = None

    def __init__(self, app_id):
        super().__init__(
            application_id=app_id
        )
        self.name = _("Metadata Cleaner")
        self.settings = Gio.Settings.new(
            app_id
        )
        self.files_manager = FilesManager()
        GLib.set_application_name(self.name)
        GLib.set_prgname(self.name)

    def do_activate(self):
        if not self._window:
            self._window = Window(self)
            self._window.set_application(self)
            self._window.show_all()
        self._window.show_empty_view()
        self._window.present()

    def do_startup(self):
        Gtk.Application.do_startup(self)

    def add_files(self):
        if not self._window:
            return
        files = self._window.get_files_from_filechooser()
        if not files:
            return
        for f in files:
            self.files_manager.add(File(f))

    def clean_metadata(self) -> None:
        if not self._window:
            return
        if self.settings.get_boolean("warn-before-removing"):
            response = self._window.show_remove_warning_dialog()
            if response != Gtk.ResponseType.OK:
                return
        for f in self.files_manager.get_cleanable_files():
            f.remove_metadata()

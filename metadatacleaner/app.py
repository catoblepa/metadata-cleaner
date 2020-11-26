import logging

from gettext import gettext as _
from gi.repository import Gdk, Gio, GLib, Gtk

from metadatacleaner.filesmanager import File, FilesManager
from metadatacleaner.window import Window


class MetadataCleaner(Gtk.Application):

    _window = None
    files_manager = None

    def __init__(self, app_id: str, version: str) -> None:
        super().__init__(
            application_id=app_id
        )
        self.name = _("Metadata Cleaner")
        self.version = version
        self.settings = Gio.Settings.new(
            app_id
        )
        self.files_manager = FilesManager()
        GLib.set_application_name(self.name)
        GLib.set_prgname(self.name)

    def do_activate(self) -> None:
        if not self._window:
            self._window = Window(self)
            self._window.set_application(self)
            self._window.show_all()
        self._window.show_empty_view()
        self._window.present()

    def do_startup(self) -> None:
        Gtk.Application.do_startup(self)
        self._setup_actions()

    def add_files(self) -> None:
        if not self._window or not self.files_manager:
            return
        gfiles = self._window.get_files_from_filechooser()
        if not gfiles:
            return
        files = []
        for gfile in gfiles:
            f = File(gfile)
            self.files_manager.add(f)
            files.append(f)
        for f in files:
            f.initialize_parser()
            f.check_metadata()

    def clean_metadata(self) -> None:
        if not self._window or not self.files_manager:
            return
        if self.settings.get_boolean("warn-before-removing"):
            response = self._window.show_remove_warning_dialog()
            if response != Gtk.ResponseType.OK:
                return
        for f in self.files_manager.get_cleanable_files():
            f.remove_metadata(
                lightweight_mode=self.settings.get_boolean("lightweight-mode")
            )

    def _setup_actions(self) -> None:
        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", self._on_about_action)
        self.add_action(about_action)
        quit_action = Gio.SimpleAction.new("quit", None)
        quit_action.connect("activate", self._on_quit_action)
        self.add_action(quit_action)
        lightweight_setting_action = Gio.SimpleAction.new_stateful(
            "lightweight-setting",
            None,
            self.settings.get_value("lightweight-mode")
        )
        lightweight_setting_action.connect(
            "activate",
            self.on_lightweight_setting_action
        )
        self.add_action(lightweight_setting_action)

    def _on_about_action(self, action, parameters) -> None:
        if not self._window:
            return
        self._window.show_about_dialog()

    def _on_quit_action(self, action, parameters) -> None:
        self.quit()

    def on_lightweight_setting_action(self, action, parameters) -> None:
        self.settings.set_boolean(
            "lightweight-mode",
            not self.settings.get_boolean("lightweight-mode")
        )
        action.set_state(self.settings.get_value("lightweight-mode"))

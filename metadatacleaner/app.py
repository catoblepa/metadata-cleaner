import logging

from gettext import gettext as _
from gi.repository import Gdk, Gio, GLib, Gtk

from metadatacleaner.file import File
from metadatacleaner.filesmanager import FilesManager
from metadatacleaner.window import Window


class MetadataCleaner(Gtk.Application):

    _window = None
    files_manager = None

    def __init__(self, app_id: str, version: str) -> None:
        super().__init__(
            application_id=app_id,
            flags=Gio.ApplicationFlags.FLAGS_NONE
        )
        self.name = _("Metadata Cleaner")
        self.version = version
        self.settings = Gio.Settings.new(app_id)
        self.files_manager = FilesManager()
        GLib.set_application_name(self.name)
        GLib.set_prgname(self.name)
        Gtk.Window.set_default_icon_name(app_id)

    def do_activate(self) -> None:
        if not self._window:
            self._window = Window(self)
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
        self.files_manager.add_gfiles(gfiles)

    def clean_metadata(self) -> None:
        if not self.files_manager:
            return
        self.files_manager.clean_files(
            lightweight_mode=self.settings.get_boolean("lightweight-mode")
        )

    def save_cleaned_files(self) -> None:
        if not self._window or not self.files_manager:
            return
        if self.settings.get_boolean("warn-before-saving"):
            response = self._window.show_save_warning_dialog()
            if response != Gtk.ResponseType.OK:
                return
        self.files_manager.save_cleaned_files()

    def _setup_actions(self) -> None:
        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", self._on_about_action)
        self.add_action(about_action)
        about_metadata_privacy_action = Gio.SimpleAction.new(
            "about-metadata-privacy",
            None
        )
        about_metadata_privacy_action.connect(
            "activate",
            self._on_about_metadata_privacy_action
        )
        self.add_action(about_metadata_privacy_action)
        about_removing_metadata_action = Gio.SimpleAction.new(
            "about-removing-metadata",
            None
        )
        about_removing_metadata_action.connect(
            "activate",
            self._on_about_removing_metadata_action
        )
        self.add_action(about_removing_metadata_action)
        add_files_action = Gio.SimpleAction.new("add-files", None)
        add_files_action.connect("activate", self._on_add_files_action)
        self.add_action(add_files_action)
        clean_metadata_action = Gio.SimpleAction.new("clean-metadata", None)
        clean_metadata_action.connect(
            "activate",
            self._on_clean_metadata_action
        )
        self.add_action(clean_metadata_action)
        save_cleaned_files_action = Gio.SimpleAction.new(
            "save-cleaned-files",
            None
        )
        save_cleaned_files_action.connect(
            "activate",
            self._on_save_cleaned_files_action
        )
        self.add_action(save_cleaned_files_action)
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

    def _on_about_metadata_privacy_action(self, action, parameters) -> None:
        if not self._window:
            return
        self._window.show_about_metadata_privacy_dialog()

    def _on_about_removing_metadata_action(self, action, parameters) -> None:
        if not self._window:
            return
        self._window.show_about_removing_metadata_dialog()

    def _on_add_files_action(self, action, parameters) -> None:
        self.add_files()

    def _on_clean_metadata_action(self, action, parameters) -> None:
        self.clean_metadata()

    def _on_save_cleaned_files_action(self, action, parameters) -> None:
        self.save_cleaned_files()

    def on_lightweight_setting_action(self, action, parameters) -> None:
        self.settings.set_boolean(
            "lightweight-mode",
            not self.settings.get_boolean("lightweight-mode")
        )
        action.set_state(self.settings.get_value("lightweight-mode"))

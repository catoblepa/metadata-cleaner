import logging

from gettext import gettext as _
from gi.repository import Gdk, Gio, GLib, Gtk
from typing import List

from metadatacleaner.file import File
from metadatacleaner.filesmanager import FilesManager
from metadatacleaner.window import Window


class MetadataCleaner(Gtk.Application):

    def __init__(self, app_id: str, version: str) -> None:
        super().__init__(
            application_id=app_id,
            flags=Gio.ApplicationFlags.FLAGS_NONE
        )
        self.name = _("Metadata Cleaner")
        self.version = version
        self.settings = Gio.Settings.new(app_id)
        self._windows: List[Window] = list()
        GLib.set_application_name(self.name)
        GLib.set_prgname("metadata-cleaner")
        Gtk.Window.set_default_icon_name(app_id)

    def do_activate(self) -> None:
        self.new_window()

    def do_startup(self) -> None:
        Gtk.Application.do_startup(self)
        self._setup_actions()
        self._setup_accels()

    def _setup_actions(self) -> None:
        new_window_action = Gio.SimpleAction.new("new-window", None)
        new_window_action.connect("activate", self._on_new_window_action)
        self.add_action(new_window_action)
        quit_action = Gio.SimpleAction.new("quit", None)
        quit_action.connect("activate", self._on_quit_action)
        self.add_action(quit_action)

    def _setup_accels(self) -> None:
        self.add_accelerator("<Primary>n", "app.new-window", None)
        self.add_accelerator("<Primary>q", "app.quit", None)
        self.add_accelerator("<Primary>o", "win.add-files", None)
        self.add_accelerator("<Primary>m", "win.clean-metadata", None)
        self.add_accelerator("<Primary>w", "win.close", None)
        self.add_accelerator("<Primary>s", "win.save-cleaned-files", None)
        self.add_accelerator("<Primary>question", "win.shortcuts", None)

    def _on_new_window_action(self, action, parameters) -> None:
        self.new_window()

    def _on_quit_action(self, action, parameters) -> None:
        self.quit()

    def _on_window_destroyed(self, window) -> None:
        self._windows.remove(window)
        if len(self._windows) == 0:
            self.quit()

    def new_window(self) -> None:
        window = Window(self)
        window.show_empty_view()
        window.show()
        window.connect("destroy", self._on_window_destroyed)
        self._windows.append(window)

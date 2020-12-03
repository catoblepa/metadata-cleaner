"""Application for Metadata Cleaner."""

import logging

from gettext import gettext as _
from gi.repository import Gio, GLib, Gtk, Handy
from typing import List, Optional

from metadatacleaner.file import File
from metadatacleaner.filesmanager import FilesManager
from metadatacleaner.window import Window


logger = logging.getLogger(__name__)


class MetadataCleaner(Gtk.Application):
    """Application for Metadata Cleaner."""

    def __init__(
        self,
        app_id: str,
        version: str,
        flatpak: bool = False,
        *args,
        **kwargs
    ) -> None:
        """Application initialization.

        Args:
            app_id (str): Application ID
            version (str): Version string
            flatpak (bool, optional): If the application is running in a
                Flatpak sandbox. Defaults to False.
        """
        super().__init__(
            application_id=app_id,
            flags=Gio.ApplicationFlags.HANDLES_OPEN,
            *args,
            **kwargs
        )
        self.name = _("Metadata Cleaner")
        self.version = version
        self.flatpak = flatpak
        self.settings = Gio.Settings.new(app_id)
        self._windows: List[Window] = list()
        GLib.set_application_name(self.name)
        GLib.set_prgname("metadata-cleaner")
        Gtk.Window.set_default_icon_name(app_id)
        Handy.init()

    # APPLICATION METHODS #

    def do_activate(self) -> None:
        """Run on application activation."""
        self.new_window()

    def do_startup(self) -> None:
        """Run on application startup."""
        Gtk.Application.do_startup(self)
        self._setup_actions()
        self._setup_accels()

    def do_open(self, gfiles: List[Gio.File], n_files: int, hint: str) -> None:
        """Run when files are passed to the command line."""
        if self.flatpak:
            logger.warning(
                "Opening files from the command line is not supported in the "
                "Flatpak sandbox. Please open them directly from the "
                "application window."
            )
            self.new_window()
            return
        self.new_window(gfiles=gfiles)

    # SETUP #

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

    # SIGNAL HANDLERS #

    def _on_new_window_action(self, action, parameters) -> None:
        self.new_window()

    def _on_quit_action(self, action, parameters) -> None:
        self.quit()

    def _on_window_destroyed(self, window) -> None:
        self._windows.remove(window)
        if len(self._windows) == 0:
            self.quit()

    # PUBLIC #

    def new_window(self, gfiles: List[Gio.File] = None) -> None:
        """Create a new window.

        Args:
            gfiles (List[Gio.File], optional): List of files to be added to the
                new window. Defaults to None.
        """
        window = Window(app=self, gfiles=gfiles)
        window.show_empty_view()
        window.show()
        window.connect("destroy", self._on_window_destroyed)
        self._windows.append(window)

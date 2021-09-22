# SPDX-FileCopyrightText: 2020, 2021 Romain Vigier <contact AT romainvigier.fr>
# SPDX-License-Identifier: GPL-3.0-or-later

"""About dialog giving information about the application."""

from gettext import gettext as _
from gi.repository import Adw, GObject, Gtk
from typing import Optional

from metadatacleaner.ui.creditsrole import CreditsRole
from metadatacleaner.ui.outbutton import OutButton


@Gtk.Template(
    resource_path="/fr/romainvigier/MetadataCleaner/ui/AboutDialog.ui"
)
class AboutDialog(Adw.Window):
    """About dialog."""

    __gtype_name__ = "AboutDialog"

    version = GObject.Property(type=str)

    _artists = ""
    _authors = ""
    _copyright = ""
    _documenters = ""
    _translator_credits = ""

    _copyright_label: OutButton = Gtk.Template.Child()
    _credits_artwork: OutButton = Gtk.Template.Child()
    _credits_code: OutButton = Gtk.Template.Child()
    _credits_documentation: OutButton = Gtk.Template.Child()
    _credits_translation: OutButton = Gtk.Template.Child()
    _stack: Gtk.Stack = Gtk.Template.Child()

    def __init__(self, *args, **kwargs) -> None:
        """About dialog initialization."""
        super().__init__(*args, **kwargs)

    @GObject.Property(type=str)
    def artists(self) -> str:
        """Get the artists string.

        Returns:
            str: The artists string.
        """
        return self._artists

    @artists.setter  # type: ignore
    def artists(self, value: str) -> None:
        self._artists = value
        self._credits_artwork.persons = value
        self._credits_artwork.set_visible(bool(value))

    @GObject.Property(type=str)
    def authors(self) -> str:
        """Get the authors string.

        Returns:
            str: The authors string.
        """
        return self._authors

    @authors.setter  # type: ignore
    def authors(self, value: str) -> None:
        self._authors = value
        self._credits_code.persons = value
        self._credits_code.set_visible(bool(value))

    @GObject.Property(type=str)
    def copyright(self) -> str:
        """Get the copyright string.

        Returns:
            str: The copyright string.
        """
        return self._copyright

    @copyright.setter  # type: ignore
    def copyright(self, value: str) -> None:
        self._copyright = value
        self._copyright_label.set_label(value)
        self._copyright_label.set_visible(bool(value))

    @GObject.Property(type=str)
    def documenters(self) -> str:
        """Get the documenters string.

        Returns:
            str: The documenters string.
        """
        return self._documenters

    @documenters.setter  # type: ignore
    def documenters(self, value: str) -> None:
        self._documenters = value
        self._credits_documentation.persons = value
        self._credits_documentation.set_visible(bool(value))

    @GObject.Property(type=str, nick="translator-credits")
    def translator_credits(self) -> str:
        """Get the translator-credits string.

        Returns:
            str: The translator-credits string.
        """
        return self._translator_credits

    @translator_credits.setter  # type: ignore
    def translator_credits(self, value: str) -> None:
        self._translator_credits = value
        if value in ["translator-credits", "translator_credits"]:
            value = None
        self._credits_translation.persons = value
        self._credits_translation.set_visible(bool(value))

    @Gtk.Template.Callback()
    def _on_close_request(self, window: Adw.Window) -> None:
        self._stack.set_visible_child_name("about")

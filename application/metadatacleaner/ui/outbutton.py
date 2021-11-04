# SPDX-FileCopyrightText: 2021 Romain Vigier <contact AT romainvigier.fr>
# SPDX-License-Identifier: GPL-3.0-or-later

"""Fancy link button."""

from gi.repository import Gdk, GObject, Gtk


@Gtk.Template(
    resource_path="/fr/romainvigier/MetadataCleaner/ui/OutButton.ui"
)
class OutButton(Gtk.Button):
    """Fancy link button."""

    __gtype_name__ = "OutButton"

    icon_name = GObject.Property(type=str, nick="icon-name")
    label = GObject.Property(type=str)
    uri = GObject.Property(type=str)

    def __init__(self, *args, **kwargs) -> None:
        """Button initialization."""
        super().__init__(*args, **kwargs)
        self.set_cursor(Gdk.Cursor.new_from_name("pointer"))

    @Gtk.Template.Callback()
    def _on_clicked(self, button) -> None:
        Gtk.show_uri(self.get_root(), self.uri, Gdk.CURRENT_TIME)

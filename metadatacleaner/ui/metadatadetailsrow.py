# SPDX-FileCopyrightText: 2021 Romain Vigier <contact AT romainvigier.fr>
# SPDX-License-Identifier: GPL-3.0-or-later

"""List of a file's metadata."""

from gi.repository import GObject, Gtk


@Gtk.Template(
    resource_path="/fr/romainvigier/MetadataCleaner/ui/MetadataDetailsRow.ui"
)
class MetadataDetailsRow(Gtk.Box):
    """List of a file's metadata."""

    __gtype_name__ = "MetadataDetailsRow"

    key = GObject.Property(type=str, default="")
    value = GObject.Property(type=str, default="")
    buffer = GObject.Property(type=Gtk.TextBuffer, nick="buffer")

    def __init__(self, *args, **kwargs) -> None:
        """Widget initialization."""
        super().__init__(*args, **kwargs)
        self.buffer = Gtk.TextBuffer()

    @Gtk.Template.Callback()
    def _on_value_changed(self, widget, p_spec: GObject.ParamSpec) -> None:
        self.buffer.set_text(self.value)

# SPDX-FileCopyrightText: 2020, 2021 Romain Vigier <contact AT romainvigier.fr>
# SPDX-License-Identifier: GPL-3.0-or-later

"""List of a file's metadata."""

from gettext import gettext as _
from gi.repository import GObject, Gtk


@Gtk.Template(
    resource_path="/fr/romainvigier/MetadataCleaner/ui/InfoDetails.ui"
)
class InfoDetails(Gtk.Box):
    """Informations about a file."""

    __gtype_name__ = "InfoDetails"

    title = GObject.Property(type=str)
    details = GObject.Property(type=str)
    has_details = GObject.Property(
        type=bool,
        default=False,
        nick="has-details")

    def __init__(
            self,
            *args,
            **kwargs) -> None:
        """Widget initialization."""
        super().__init__(*args, **kwargs)

    @Gtk.Template.Callback()
    def _on_details_changed(self, widget, p_spec: GObject.ParamSpec) -> None:
        self.has_details = bool(self.details)

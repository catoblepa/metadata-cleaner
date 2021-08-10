# SPDX-FileCopyrightText: 2020, 2021 Romain Vigier <contact AT romainvigier.fr>
# SPDX-License-Identifier: GPL-3.0-or-later

"""List of a file's metadata."""

from gi.repository import GObject, Gtk

from metadatacleaner.modules.metadata import MetadataList

from metadatacleaner.ui.metadatadetailsrow import MetadataDetailsRow


@Gtk.Template(
    resource_path="/fr/romainvigier/MetadataCleaner/ui/MetadataDetails.ui"
)
class MetadataDetails(Gtk.Box):
    """List of a file's metadata."""

    __gtype_name__ = "MetadataDetails"

    filename = GObject.Property(type=str)
    metadata_list = GObject.Property(type=MetadataList, nick="metadata-list")

    def __init__(self, *args, **kwargs) -> None:
        """Widget initialization."""
        super().__init__(*args, **kwargs)

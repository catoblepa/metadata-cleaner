# SPDX-FileCopyrightText: 2021 Romain Vigier <contact AT romainvigier.fr>
# SPDX-License-Identifier: GPL-3.0-or-later

"""Metadata classes."""

from gi.repository import Gio, GObject


class Metadata(GObject.GObject):
    """Metadata object."""

    __gtype_name__ = "Metadata"

    key = GObject.Property(type=str)
    value = GObject.Property(type=str)

    def __init__(self, *args, **kwargs) -> None:
        """Metadata object initialization."""
        super().__init__(**kwargs)


class MetadataList(Gio.ListStore):
    """Metadata List object."""

    __gtype_name__ = "MetadataList"

    def __init__(self, *args, **kwargs) -> None:
        """Metadata List initialization."""
        Gio.ListStore.__init__(self, item_type=Metadata)


class MetadataFile(GObject.GObject):
    """Metadata File object."""

    __gtype_name__ = "MetadataFile"

    filename = GObject.Property(type=str)
    metadata = GObject.Property(type=MetadataList)

    def __init__(self, *args, **kwargs) -> None:
        """Metadata File initialization."""
        super().__init__(**kwargs)


class MetadataStore(Gio.ListStore):
    """Metadata Store object."""

    __gtype_name__ = "MetadataStore"

    def __init__(self, *args, **kwargs) -> None:
        """Metadata Store initialization."""
        Gio.ListStore.__init__(self, item_type=MetadataFile)

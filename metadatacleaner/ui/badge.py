# SPDX-FileCopyrightText: 2021 Romain Vigier <contact AT romainvigier.fr>
# SPDX-License-Identifier: GPL-3.0-or-later

"""Badge to display informations."""

from gi.repository import Adw, Gtk


@Gtk.Template(resource_path="/fr/romainvigier/MetadataCleaner/ui/Badge.ui")
class Badge(Adw.Bin):
    """Badge to display informations."""

    __gtype_name__ = "Badge"

    def __init__(self, *args, **kwargs) -> None:
        """Badge initialization."""
        super().__init__(*args, **kwargs)

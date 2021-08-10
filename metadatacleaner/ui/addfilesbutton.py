# SPDX-FileCopyrightText: 2020 Romain Vigier <contact AT romainvigier.fr>
# SPDX-License-Identifier: GPL-3.0-or-later

"""Button allowing to add files."""

from gi.repository import Gtk


@Gtk.Template(
    resource_path="/fr/romainvigier/MetadataCleaner/ui/AddFilesButton.ui"
)
class AddFilesButton(Gtk.Button):
    """Button allowing to add files."""

    __gtype_name__ = "AddFilesButton"

    def __init__(self, *args, **kwargs) -> None:
        """Button initialization."""
        super().__init__(*args, **kwargs)

# SPDX-FileCopyrightText: 2020, 2021 Romain Vigier <contact AT romainvigier.fr>
# SPDX-License-Identifier: GPL-3.0-or-later

"""Settings button."""

from gi.repository import Gtk


@Gtk.Template(
    resource_path="/fr/romainvigier/MetadataCleaner/ui/SettingsButton.ui"
)
class SettingsButton(Gtk.MenuButton):
    """Settings button."""

    __gtype_name__ = "SettingsButton"

    def __init__(self, *args, **kwargs) -> None:
        """Initialize Settings button."""
        super().__init__(*args, **kwargs)

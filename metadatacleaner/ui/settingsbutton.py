# SPDX-FileCopyrightText: 2020, 2021 Romain Vigier <contact AT romainvigier.fr>
# SPDX-License-Identifier: GPL-3.0-or-later

"""Settings button."""

from gi.repository import Gio, GObject, Gtk


@Gtk.Template(
    resource_path="/fr/romainvigier/MetadataCleaner/ui/SettingsButton.ui"
)
class SettingsButton(Gtk.MenuButton):
    """Settings button."""

    __gtype_name__ = "SettingsButton"

    settings = GObject.Property(type=Gio.Settings)

    _lightweight_switch: Gtk.Switch = Gtk.Template.Child()

    def __init__(self, *args, **kwargs) -> None:
        """Initialize Settings button."""
        super().__init__(*args, **kwargs)

    @Gtk.Template.Callback()
    def _on_settings_changed(
            self,
            widget: Gtk.Widget,
            pspec: GObject.ParamSpec) -> None:
        self.settings.bind(
            "lightweight-cleaning",
            self._lightweight_switch,
            "active",
            Gio.SettingsBindFlags.DEFAULT)

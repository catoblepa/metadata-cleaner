# SPDX-FileCopyrightText: 2020, 2021 Romain Vigier <contact AT romainvigier.fr>
# SPDX-License-Identifier: GPL-3.0-or-later

"""Dialog warning the user of possible data loss on saving."""

from gi.repository import Gio, GObject, Gtk


@Gtk.Template(
    resource_path="/fr/romainvigier/MetadataCleaner/ui/SaveWarningDialog.ui"
)
class SaveWarningDialog(Gtk.MessageDialog):
    """Dialog warning the user of possible data loss on saving."""

    __gtype_name__ = "SaveWarningDialog"

    settings = GObject.Property(type=Gio.Settings)

    _checkbutton: Gtk.CheckButton = Gtk.Template.Child()

    def __init__(self, *args, **kwargs) -> None:
        """Dialog initialization."""
        super().__init__(*args, **kwargs)

    @Gtk.Template.Callback()
    def _on_settings_changed(self, dialog, p_spec: GObject.ParamSpec) -> None:
        if not self.settings:
            return
        self.settings.bind(
            "warn-before-saving",
            self._checkbutton,
            "active",
            Gio.SettingsBindFlags.INVERT_BOOLEAN)

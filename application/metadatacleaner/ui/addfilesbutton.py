# SPDX-FileCopyrightText: 2020 Romain Vigier <contact AT romainvigier.fr>
# SPDX-License-Identifier: GPL-3.0-or-later

"""Button allowing to add files."""

from gi.repository import Adw, Gtk


@Gtk.Template(
    resource_path="/fr/romainvigier/MetadataCleaner/ui/AddFilesButton.ui"
)
class AddFilesButton(Gtk.Widget):
    """Button allowing to add files."""

    __gtype_name__ = "AddFilesButton"

    _split_button: Adw.SplitButton = Gtk.Template.Child()

    @Gtk.Template.Callback()
    def _on_add_folders_button_clicked(self, button: Gtk.Button) -> None:
        self._split_button.popdown()

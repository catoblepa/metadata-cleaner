"""Dialog warning the user of possible data loss on saving."""

from gi.repository import Gio, Gtk


@Gtk.Template(
    resource_path="/fr/romainvigier/MetadataCleaner/ui/SaveWarningDialog.ui"
)
class SaveWarningDialog(Gtk.MessageDialog):
    """Dialog warning the user of possible data loss on saving."""

    __gtype_name__ = "SaveWarningDialog"

    _checkbutton: Gtk.CheckButton = Gtk.Template.Child()

    def __init__(self, settings: Gio.Settings, *args, **kwargs) -> None:
        """Dialog initialization."""
        super().__init__(
            buttons=Gtk.ButtonsType.OK_CANCEL,
            *args,
            **kwargs
        )
        self._setup_checkbutton(settings)

    def _setup_checkbutton(self, settings: Gio.Settings) -> None:
        settings.bind(
            "warn-before-saving",
            self._checkbutton,
            "active",
            Gio.SettingsBindFlags.INVERT_BOOLEAN
        )

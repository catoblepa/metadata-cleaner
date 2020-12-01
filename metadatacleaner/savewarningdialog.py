from gi.repository import Gio, Gtk


@Gtk.Template(
    resource_path="/fr/romainvigier/MetadataCleaner/ui/SaveWarningDialog.ui"
)
class SaveWarningDialog(Gtk.MessageDialog):

    __gtype_name__ = "SaveWarningDialog"

    _checkbutton: Gtk.CheckButton = Gtk.Template.Child()

    def __init__(self, settings: Gio.Settings, *args, **kwargs) -> None:
        super().__init__(
            buttons=Gtk.ButtonsType.OK_CANCEL,
            *args,
            **kwargs
        )
        self._setup_checkbutton(settings)

    def _setup_checkbutton(self, settings) -> None:
        settings.bind(
            "warn-before-saving",
            self._checkbutton,
            "active",
            Gio.SettingsBindFlags.INVERT_BOOLEAN
        )

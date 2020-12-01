from gettext import gettext as _
from gi.repository import Gtk

from metadatacleaner.filesmanager import SUPPORTED_FORMATS


class FileChooserDialog(Gtk.FileChooserNative):

    __gtype_name__ = "FileChooserDialog"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(
            modal=True,
            title=_("Choose files"),
            action=Gtk.FileChooserAction.OPEN,
            select_multiple=True,
            *args,
            **kwargs
        )
        self._setup_file_filter()

    def _setup_file_filter(self) -> None:
        file_filter = Gtk.FileFilter()
        file_filter.set_name(_("All supported files"))
        for mimetype, extensions in SUPPORTED_FORMATS.items():
            for extension in extensions:
                file_filter.add_pattern(f"*{extension}")
        self.add_filter(file_filter)

from gettext import gettext as _
from gi.repository import Gio, Gtk, Handy
from typing import List, Optional

from metadatacleaner.emptyview import EmptyView
from metadatacleaner.filesview import FilesView
from metadatacleaner.filesmanager import SUPPORTED_FORMATS


@Gtk.Template(resource_path="/fr/romainvigier/MetadataCleaner/ui/Window.ui")
class Window(Handy.ApplicationWindow):

    __gtype_name__ = "Window"

    _stack: Gtk.Stack = Gtk.Template.Child()

    def __init__(self, app: Gtk.Application) -> None:
        super().__init__(
            application=app,
            title=app.name
        )
        self._app = app
        self._setup_views()
        # TODO: Add about dialog
        # TODO: Add lightweight setting
        # TODO: Check accessibility
        # TODO: Add a ScrolledWindow to prevent window growing out of control
        self._app.files_manager.connect("file-added", self._on_file_added)

    def _on_file_added(self, file_manager, new_file_index):
        if self._stack.get_visible_child_name() != "files_view":
            self.show_files_view()

    @Gtk.Template.Callback()
    def _on_destroy(self, window: Gtk.Window) -> None:
        self._app.quit()

    def _setup_views(self) -> None:
        self._empty_view = EmptyView(self._app)
        self._files_view = FilesView(self._app)
        self._stack.add_named(self._empty_view, "empty_view")
        self._stack.add_named(self._files_view, "files_view")

    def show_empty_view(self) -> None:
        self._stack.set_visible_child_name("empty_view")

    def show_files_view(self) -> None:
        self._stack.set_visible_child_name("files_view")

    def get_files_from_filechooser(self) -> Optional[List[Gio.File]]:
        files: Optional[List[Gio.File]] = None
        file_chooser = Gtk.FileChooserNative(
            title=_("Choose files"),
            action=Gtk.FileChooserAction.OPEN,
            select_multiple=True,
            modal=True,
            transient_for=self
        )
        file_filter = Gtk.FileFilter()
        file_filter.set_name(_("All supported files"))
        for mimetype, extensions in SUPPORTED_FORMATS.items():
            for extension in extensions:
                file_filter.add_pattern(f"*{extension}")
        file_chooser.add_filter(file_filter)
        response = file_chooser.run()
        if response == Gtk.ResponseType.ACCEPT:
            files = file_chooser.get_files()
        file_chooser.destroy()
        return files

    def show_remove_warning_dialog(self) -> Gtk.ResponseType:
        dialog = Gtk.MessageDialog(
            text=_("Make sure you backed up your files!"),
            secondary_text=_(
                "Once you remove metadata, there's no going back."
            ),
            flags=0,
            modal=True,
            message_type=Gtk.MessageType.WARNING,
            buttons=Gtk.ButtonsType.OK_CANCEL,
            transient_for=self
        )
        dont_warn_again_checkbox = Gtk.CheckButton(
            visible=True,
            label=_("Don't tell me again"),
            halign="center"
        )
        self._app.settings.bind(
            "warn-before-removing",
            dont_warn_again_checkbox,
            "active",
            Gio.SettingsBindFlags.INVERT_BOOLEAN
        )
        dialog.get_message_area().pack_end(
            dont_warn_again_checkbox,
            False,
            True,
            12
        )
        response = dialog.run()
        dialog.destroy()
        return response

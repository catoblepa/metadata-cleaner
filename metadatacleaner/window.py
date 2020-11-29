from gettext import gettext as _
from gi.repository import Gio, Gtk, Handy
from typing import List, Optional

from metadatacleaner.addfilesbutton import AddFilesButton
from metadatacleaner.emptyview import EmptyView
from metadatacleaner.filesview import FilesView
from metadatacleaner.filesmanager import SUPPORTED_FORMATS
from metadatacleaner.menubutton import MenuButton


@Gtk.Template(resource_path="/fr/romainvigier/MetadataCleaner/ui/Window.ui")
class Window(Handy.ApplicationWindow):

    __gtype_name__ = "Window"

    _headerbar: Handy.HeaderBar = Gtk.Template.Child()
    _stack: Gtk.Stack = Gtk.Template.Child()

    def __init__(self, app: Gtk.Application) -> None:
        super().__init__(
            application=app,
            title=app.name
        )
        self._app = app
        self._setup_headerbar()
        self._setup_views()
        # TODO: Check accessibility
        self._app.files_manager.connect("file-added", self._on_file_added)
        self._app.files_manager.connect("file-removed", self._on_file_removed)

    def _on_file_added(self, file_manager, new_file_index):
        if self._stack.get_visible_child_name() != "files_view":
            self.show_files_view()

    def _on_file_removed(self, file_manager):
        if len(self._app.files_manager.get_files()) == 0:
            self.show_empty_view()

    @Gtk.Template.Callback()
    def _on_destroy(self, window: Gtk.Window) -> None:
        self._app.quit()

    def _setup_headerbar(self) -> None:
        self._headerbar.pack_start(AddFilesButton(self._app))
        self._headerbar.pack_end(MenuButton(self._app))
        self._headerbar.set_title(self._app.name)

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

    def show_save_warning_dialog(self) -> Gtk.ResponseType:
        dialog = Gtk.MessageDialog(
            text=_("Make sure you backed up your files!"),
            secondary_text=_(
                "Once you replace your files, there's no going back."
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
            "warn-before-saving",
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

    def show_about_dialog(self) -> None:
        about_dialog = Gtk.AboutDialog(
            transient_for=self,
            modal=True,
            version=self._app.version,
            logo_icon_name=self._app.get_application_id(),
            license_type=Gtk.License.GPL_3_0,
            copyright="© 2020 Romain Vigier",
            authors=["Romain Vigier"],
            website="https://gitlab.com/rmnvgr/metadata-cleaner/"
        )
        about_dialog.present()

    def show_about_metadata_privacy_dialog(self) -> None:
        dialog = Gtk.MessageDialog(
            text=_("Note about metadata and privacy"),
            secondary_text=_(
                "Metadata consist of information that characterizes data. "
                "Metadata are used to provide documentation for data "
                "products. In essence, metadata answer who, what, when, "
                "where, why, and how about every facet of the data that are "
                "being documented.\n\n"
                "Metadata within a file can tell a lot about you. Cameras "
                "record data about when a picture was taken and what camera "
                "was used. Office documents like PDF or Office automatically "
                "adds author and company information to documents and "
                "spreadsheets. Maybe you don't want to disclose those "
                "informations.\n\n"
                "This tool will get rid, as much as possible, of metadata."
            ),
            flags=0,
            modal=True,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            transient_for=self
        )
        dialog.run()
        dialog.destroy()

    def show_about_removing_metadata_dialog(self) -> None:
        dialog = Gtk.MessageDialog(
            text=_("Note about removing metadata"),
            secondary_text=_(
                "While this tool is doing its very best to display metadata, "
                "it doesn't mean that a file is clean from any metadata if "
                "it doesn't show any. There is no reliable way to detect "
                "every single possible metadata for complex file formats.\n\n"
                "This is why you shouldn't rely on metadata's presence to "
                "decide if your file must be cleaned or not."
            ),
            flags=0,
            modal=True,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            transient_for=self
        )
        dialog.run()
        dialog.destroy()

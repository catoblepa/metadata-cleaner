from gettext import gettext as _
from gi.repository import Gio, GLib, Gtk, Handy
from typing import List, Optional

from metadatacleaner.addfilesbutton import AddFilesButton
from metadatacleaner.emptyview import EmptyView
from metadatacleaner.filesview import FilesView
from metadatacleaner.filesmanager import FilesManager, FilesManagerState
from metadatacleaner.filesmanager import SUPPORTED_FORMATS
from metadatacleaner.menubutton import MenuButton
from metadatacleaner.shortcutsdialog import ShortcutsDialog


@Gtk.Template(resource_path="/fr/romainvigier/MetadataCleaner/ui/Window.ui")
class Window(Handy.ApplicationWindow):

    __gtype_name__ = "Window"

    _headerbar: Handy.HeaderBar = Gtk.Template.Child()
    _stack: Gtk.Stack = Gtk.Template.Child()

    files_manager: Optional[FilesManager] = None

    def __init__(self, app: Gtk.Application) -> None:
        super().__init__(
            application=app,
            title=app.name
        )
        self._app = app
        self._setup_files_manager()
        self._setup_headerbar()
        self._setup_views()
        self._setup_actions()
        # TODO: Check accessibility
        # TODO: Move dialogs to UI files
        # TODO: Clean UI files
        # TODO: Clean unused imports, commented code
        # TODO: Resize window when a lot of files are added?

    # SETUP #

    def _setup_files_manager(self) -> None:
        self.files_manager = FilesManager()
        self.files_manager.connect("file-added", self._on_file_added)
        self.files_manager.connect("file-removed", self._on_file_removed)

    def _setup_headerbar(self) -> None:
        self._headerbar.pack_start(AddFilesButton())
        self._headerbar.pack_end(MenuButton())
        self._headerbar.set_title(self._app.name)

    def _setup_views(self) -> None:
        self._empty_view = EmptyView()
        self._files_view = FilesView()
        self._stack.add_named(self._empty_view, "empty_view")
        self._stack.add_named(self._files_view, "files_view")

    def _setup_actions(self) -> None:
        if not self.files_manager:
            return
        close_action = Gio.SimpleAction.new("close", None)
        close_action.connect("activate", self._on_close_action)
        self.add_action(close_action)
        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", self._on_about_action)
        self.add_action(about_action)
        shortcuts_action = Gio.SimpleAction.new("shortcuts", None)
        shortcuts_action.connect("activate", self._on_shortcuts_action)
        self.add_action(shortcuts_action)
        about_metadata_privacy_action = Gio.SimpleAction.new(
            "about-metadata-privacy",
            None
        )
        about_metadata_privacy_action.connect(
            "activate",
            self._on_about_metadata_privacy_action
        )
        self.add_action(about_metadata_privacy_action)
        about_removing_metadata_action = Gio.SimpleAction.new(
            "about-removing-metadata",
            None
        )
        about_removing_metadata_action.connect(
            "activate",
            self._on_about_removing_metadata_action
        )
        self.add_action(about_removing_metadata_action)
        add_files_action = Gio.SimpleAction.new("add-files", None)
        add_files_action.connect("activate", self._on_add_files_action)
        self.add_action(add_files_action)
        clean_metadata_action = Gio.SimpleAction.new("clean-metadata", None)
        clean_metadata_action.connect(
            "activate",
            self._on_clean_metadata_action
        )
        self.add_action(clean_metadata_action)
        save_cleaned_files_action = Gio.SimpleAction.new(
            "save-cleaned-files",
            None
        )
        save_cleaned_files_action.connect(
            "activate",
            self._on_save_cleaned_files_action
        )
        self.add_action(save_cleaned_files_action)
        lightweight_mode_action = Gio.SimpleAction.new_stateful(
            "lightweight-mode",
            None,
            GLib.Variant.new_boolean(self.files_manager.lightweight_mode)
        )
        lightweight_mode_action.connect(
            "activate",
            self.on_lightweight_mode_action
        )
        self.add_action(lightweight_mode_action)

    # SIGNAL HANDLERS #

    def _on_file_added(self, file_manager, new_file_index):
        if self._stack.get_visible_child_name() != "files_view":
            self.show_files_view()

    def _on_file_removed(self, file_manager):
        if len(self._app.files_manager.get_files()) == 0:
            self.show_empty_view()

    def _on_close_action(self, action, parameters) -> None:
        self.destroy()

    def _on_about_action(self, action, parameters) -> None:
        self.show_about_dialog()

    def _on_shortcuts_action(self, action, parameters) -> None:
        self.show_shortcuts_dialog()

    def _on_about_metadata_privacy_action(self, action, parameters) -> None:
        self.show_about_metadata_privacy_dialog()

    def _on_about_removing_metadata_action(self, action, parameters) -> None:
        self.show_about_removing_metadata_dialog()

    def _on_add_files_action(self, action, parameters) -> None:
        if not self.files_manager:
            return
        if self.files_manager.state == FilesManagerState.WORKING:
            return
        self.add_files()

    def _on_clean_metadata_action(self, action, parameters) -> None:
        if not self.files_manager:
            return
        if self.files_manager.state == FilesManagerState.WORKING \
                or len(self.files_manager.get_cleanable_files()) == 0:
            return
        self.clean_metadata()

    def _on_save_cleaned_files_action(self, action, parameters) -> None:
        if not self.files_manager:
            return
        if self.files_manager.state == FilesManagerState.WORKING \
                or len(self.files_manager.get_cleaned_files()) == 0:
            return
        self.save_cleaned_files()

    def on_lightweight_mode_action(self, action, parameters) -> None:
        if not self.files_manager:
            return
        self.files_manager.lightweight_mode = \
            not self.files_manager.lightweight_mode
        action.set_state(
            GLib.Variant.new_boolean(self.files_manager.lightweight_mode)
        )

    # VIEWS #

    def show_empty_view(self) -> None:
        self._stack.set_visible_child_name("empty_view")

    def show_files_view(self) -> None:
        self._stack.set_visible_child_name("files_view")

    # ACTIONS #

    def add_files(self) -> None:
        if not self.files_manager:
            return
        gfiles = self.get_files_from_filechooser()
        if not gfiles:
            return
        self.files_manager.add_gfiles(gfiles)

    def clean_metadata(self) -> None:
        if not self.files_manager:
            return
        self.files_manager.clean_files()

    def save_cleaned_files(self) -> None:
        if not self.files_manager:
            return
        if self._app.settings.get_boolean("warn-before-saving"):
            response = self.show_save_warning_dialog()
            if response != Gtk.ResponseType.OK:
                return
        self.files_manager.save_cleaned_files()

    # DIALOGS #

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
        about_dialog.show()

    def show_shortcuts_dialog(self) -> None:
        shortcuts_dialog = ShortcutsDialog(
            transient_for=self
        )
        shortcuts_dialog.show()

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

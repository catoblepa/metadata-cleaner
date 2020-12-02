"""Application window of Metadata Cleaner."""

from gi.repository import Gio, GLib, Gtk, Handy
from typing import Any, List, Optional

from metadatacleaner.aboutdialog import AboutDialog
from metadatacleaner.aboutmetadataprivacydialog \
    import AboutMetadataPrivacyDialog
from metadatacleaner.aboutremovingmetadatadialog \
    import AboutRemovingMetadataDialog
from metadatacleaner.addfilesbutton import AddFilesButton
from metadatacleaner.emptyview import EmptyView
from metadatacleaner.filechooserdialog import FileChooserDialog
from metadatacleaner.filesview import FilesView
from metadatacleaner.filesmanager import FilesManager, FilesManagerState
from metadatacleaner.menubutton import MenuButton
from metadatacleaner.savewarningdialog import SaveWarningDialog
from metadatacleaner.shortcutsdialog import ShortcutsDialog


@Gtk.Template(resource_path="/fr/romainvigier/MetadataCleaner/ui/Window.ui")
class Window(Handy.ApplicationWindow):
    """Application window of Metadata Cleaner."""

    __gtype_name__ = "Window"

    _headerbar: Handy.HeaderBar = Gtk.Template.Child()
    _stack: Gtk.Stack = Gtk.Template.Child()

    def __init__(
        self,
        app: Gtk.Application,
        gfiles: List[Gio.File] = None,
        *args,
        **kwargs
    ) -> None:
        """Window initialization.

        Args:
            app (Gtk.Application): The parent application.
            gfiles (List[Gio.File], optional): List of files to add. Defaults
                to None.
        """
        super().__init__(
            application=app,
            title=app.name,
            *args,
            **kwargs
        )
        self._app = app
        self._setup_files_manager()
        self._setup_headerbar()
        self._setup_views()
        self._setup_actions()
        if gfiles:
            self.files_manager.add_gfiles(gfiles)

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
            self._on_lightweight_mode_action
        )
        self.add_action(lightweight_mode_action)

    # SIGNAL HANDLERS #

    def _on_file_added(self, file_manager: FilesManager, new_file_index: int):
        if self._stack.get_visible_child_name() != "files_view":
            self.show_files_view()

    def _on_file_removed(self, file_manager: FilesManager):
        if len(self.files_manager.get_files()) == 0:
            self.show_empty_view()

    def _on_close_action(self, action: Gio.Action, parameters: Any) -> None:
        self.destroy()

    def _on_about_action(self, action: Gio.Action, parameters: Any) -> None:
        self.show_about_dialog()

    def _on_shortcuts_action(
        self,
        action: Gio.Action,
        parameters: Any
    ) -> None:
        self.show_shortcuts_dialog()

    def _on_about_metadata_privacy_action(
        self,
        action: Gio.Action,
        parameters: Any
    ) -> None:
        self.show_about_metadata_privacy_dialog()

    def _on_about_removing_metadata_action(
        self,
        action: Gio.Action,
        parameters: Any
    ) -> None:
        self.show_about_removing_metadata_dialog()

    def _on_add_files_action(
        self,
        action: Gio.Action,
        parameters: Any
    ) -> None:
        self.add_files()

    def _on_clean_metadata_action(
        self,
        action: Gio.Action,
        parameters: Any
    ) -> None:
        if self.files_manager.state == FilesManagerState.WORKING \
                or len(self.files_manager.get_cleanable_files()) == 0:
            return
        self.clean_metadata()

    def _on_save_cleaned_files_action(
        self,
        action: Gio.Action,
        parameters: Any
    ) -> None:
        if self.files_manager.state == FilesManagerState.WORKING \
                or len(self.files_manager.get_cleaned_files()) == 0:
            return
        self.save_cleaned_files()

    def _on_lightweight_mode_action(
        self,
        action: Gio.Action,
        parameters: Any
    ) -> None:
        self.files_manager.lightweight_mode = \
            not self.files_manager.lightweight_mode
        action.set_state(
            GLib.Variant.new_boolean(self.files_manager.lightweight_mode)
        )

    # VIEWS #

    def show_empty_view(self) -> None:
        """Show an empty view."""
        self._stack.set_visible_child_name("empty_view")

    def show_files_view(self) -> None:
        """Show the files."""
        self._stack.set_visible_child_name("files_view")

    # ACTIONS #

    def add_files(self) -> None:
        """Add files."""
        gfiles = self.get_files_from_filechooser()
        if not gfiles:
            return
        self.files_manager.add_gfiles(gfiles)

    def clean_metadata(self) -> None:
        """Remove metadata from files."""
        self.files_manager.clean_files()

    def save_cleaned_files(self) -> None:
        """Save cleaned files."""
        if self._app.settings.get_boolean("warn-before-saving"):
            response = self.show_save_warning_dialog()
            if response != Gtk.ResponseType.OK:
                return
        self.files_manager.save_cleaned_files()

    # DIALOGS #

    def get_files_from_filechooser(self) -> Optional[List[Gio.File]]:
        """Get files from a file chooser.

        Returns:
            Optional[List[Gio.File]]: List of Gio Files choosed by the user.
        """
        files: Optional[List[Gio.File]] = None
        file_chooser = FileChooserDialog(
            transient_for=self
        )
        response: Gtk.ResponseType = file_chooser.run()
        if response == Gtk.ResponseType.ACCEPT:
            files = file_chooser.get_files()
        file_chooser.destroy()
        return files

    def show_save_warning_dialog(self) -> Gtk.ResponseType:
        """Show a warning about data loss before saving.

        Returns:
            Gtk.ResponseType: The action choosed by the user.
        """
        dialog = SaveWarningDialog(
            settings=self._app.settings,
            transient_for=self
        )
        response: Gtk.ResponseType = dialog.run()
        dialog.destroy()
        return response

    def show_about_dialog(self) -> None:
        """Show a dialog with informations about the application."""
        about_dialog = AboutDialog(
            transient_for=self,
            version=self._app.version
        )
        about_dialog.show()

    def show_shortcuts_dialog(self) -> None:
        """Show a dialog with keyboard shortcuts."""
        shortcuts_dialog = ShortcutsDialog(
            transient_for=self
        )
        shortcuts_dialog.show()

    def show_about_metadata_privacy_dialog(self) -> None:
        """Show a message dialog teaching users about metadata and privacy."""
        dialog = AboutMetadataPrivacyDialog(
            transient_for=self
        )
        dialog.run()
        dialog.destroy()

    def show_about_removing_metadata_dialog(self) -> None:
        """Show a message dialog teaching users about removing metadata."""
        dialog = AboutRemovingMetadataDialog(
            transient_for=self
        )
        dialog.run()
        dialog.destroy()

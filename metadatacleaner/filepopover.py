"""Popover with details about the file's metadata."""

from gettext import gettext as _
from gi.repository import Gtk
from typing import Optional

from metadatacleaner.file import File, FileState
from metadatacleaner.metadataview import MetadataView


@Gtk.Template(
    resource_path="/fr/romainvigier/MetadataCleaner/ui/FilePopover.ui"
)
class FilePopover(Gtk.Popover):
    """Popover with details about the file's metadata."""

    __gtype_name__ = "FilePopover"

    _box: Gtk.Box = Gtk.Template.Child()
    _title: Gtk.Label = Gtk.Template.Child()

    def __init__(self, f: File, *args, **kwargs) -> None:
        """Popover initialization.

        Args:
            f (File): The file the popover will give details about.
        """
        super().__init__(*args, **kwargs)
        self._file = f
        self._content: Optional[Gtk.Widget] = None
        self._sync_title_to_file()
        self._sync_content_to_file()
        self._file.connect("state-changed", self._on_file_state_changed)

    def _sync_title_to_file(self) -> None:
        title = {
            FileState.INITIALIZING: _("Initializing…"),
            FileState.ERROR_WHILE_INITIALIZING: _(
                "Error while initializing the file parser."
            ),
            FileState.UNSUPPORTED: _("File type not supported."),
            FileState.SUPPORTED: _("File type supported."),
            FileState.CHECKING_METADATA: _("Checking metadata…"),
            FileState.ERROR_WHILE_CHECKING_METADATA: _(
                "Error while checking metadata:"
            ),
            FileState.HAS_NO_METADATA: _(
                "No metadata have been found.\n"
                "The file will be cleaned anyway, better safe than sorry."
            ),
            FileState.HAS_METADATA: _("These metadata have been found:"),
            FileState.REMOVING_METADATA: _("Removing metadata…"),
            FileState.ERROR_WHILE_REMOVING_METADATA: _(
                "Error while removing metadata:"
            ),
            FileState.CLEANED: _("The file has been cleaned."),
            FileState.SAVING: _("Saving the cleaned file…"),
            FileState.ERROR_WHILE_SAVING: _("Error while saving the file:"),
            FileState.SAVED: _("The cleaned file has been saved.")
        }
        self._title.set_label(title[self._file.state])

    def _sync_content_to_file(self) -> None:
        if self._content:
            self._content.destroy()
            self._content = None
        if self._file.state == FileState.HAS_METADATA:
            self._content = MetadataView(self._file.metadata) \
                if self._file.metadata \
                else None
        elif self._file.state in [
            FileState.ERROR_WHILE_CHECKING_METADATA,
            FileState.ERROR_WHILE_REMOVING_METADATA,
            FileState.ERROR_WHILE_SAVING
        ]:
            self._content = Gtk.Label(
                visible=True,
                label=str(self._file.error),
                selectable=True
            )
        if self._content:
            self._box.pack_end(self._content, False, True, 0)

    def _on_file_state_changed(self, file: File, new_state: FileState) -> None:
        self._sync_title_to_file()
        self._sync_content_to_file()

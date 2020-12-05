"""Popover with details about the file's state."""

from gettext import gettext as _
from gi.repository import Gtk
from typing import Optional

from metadatacleaner.file import File, FileState


@Gtk.Template(
    resource_path="/fr/romainvigier/MetadataCleaner/ui/FilePopover.ui"
)
class FilePopover(Gtk.Popover):
    """Popover with details about the file's state."""

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
        self._setup_title()
        self._setup_content()

    def _setup_title(self) -> None:
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

    def _setup_content(self) -> None:
        if self._file.state in [
            FileState.ERROR_WHILE_CHECKING_METADATA,
            FileState.ERROR_WHILE_REMOVING_METADATA,
            FileState.ERROR_WHILE_SAVING
        ]:
            content = Gtk.Label(
                visible=True,
                label=str(self._file.error),
                selectable=True,
                wrap=True
            )
            self._box.pack_end(content, False, True, 0)

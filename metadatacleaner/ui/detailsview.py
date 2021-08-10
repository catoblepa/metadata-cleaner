# SPDX-FileCopyrightText: 2020, 2021 Romain Vigier <contact AT romainvigier.fr>
# SPDX-License-Identifier: GPL-3.0-or-later

"""Window detailing the file's metadata."""

from gettext import gettext as _
from gi.repository import Gtk
from typing import Optional

from metadatacleaner.modules.file import File, FileState

from metadatacleaner.ui.infodetails import InfoDetails
from metadatacleaner.ui.metadatadetails import MetadataDetails


@Gtk.Template(
    resource_path="/fr/romainvigier/MetadataCleaner/ui/DetailsView.ui"
)
class DetailsView(Gtk.ScrolledWindow):
    """View details of a file."""

    __gtype_name__ = "DetailsView"

    _box: Gtk.Box = Gtk.Template.Child()

    def __init__(self, *args, **kwargs) -> None:
        """View initialization."""
        super().__init__(*args, **kwargs)
        self._file: Optional[File] = None

    def view_file(self, f: File) -> None:
        """Set the file to view.

        Args:
            f (File): The file to view.
        """
        self.clear()
        if f.state == FileState.HAS_METADATA:
            self._setup_metadata_details(f)
        elif f.state == FileState.CLEANED:
            self._setup_cleaned_details()
        elif f.state in [
                FileState.ERROR_WHILE_CHECKING_METADATA,
                FileState.ERROR_WHILE_INITIALIZING,
                FileState.ERROR_WHILE_REMOVING_METADATA,
                FileState.HAS_NO_METADATA,
                FileState.UNSUPPORTED]:
            self._setup_error_details(f)

    def clear(self) -> None:
        """Clear the view."""
        while self._box.get_first_child():
            self._box.remove(self._box.get_first_child())
        self.get_vadjustment().set_value(0)

    def _setup_cleaned_details(self) -> None:
        self._box.append(InfoDetails(
            info_title=_("The file has been cleaned.")))

    def _setup_metadata_details(self, f: File) -> None:
        for metadata_file in f.metadata:
            self._box.append(MetadataDetails(
                filename=metadata_file.filename,
                metadata_list=metadata_file.metadata
            ))

    def _setup_error_details(self, f: File) -> None:
        info_titles = {
            FileState.ERROR_WHILE_INITIALIZING: _("Unable to read the file."),
            FileState.UNSUPPORTED: _("File type not supported."),
            FileState.ERROR_WHILE_CHECKING_METADATA: _(
                "Unable to check metadata."),
            FileState.HAS_NO_METADATA: _(
                "No known metadata, the file will be cleaned to be sure."),
            FileState.ERROR_WHILE_REMOVING_METADATA: _(
                "Unable to remove metadata.")
        }
        info_details = str(f.error or "")
        self._box.append(InfoDetails(
            title=info_titles[f.state],
            details=info_details))

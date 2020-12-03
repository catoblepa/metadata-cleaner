"""Indicator showing the status of the files manager."""

from gettext import gettext as _
from gi.repository import GLib, Gtk
from typing import Optional

from metadatacleaner.filesmanager import FilesManager, FilesManagerState
from metadatacleaner.menupopover import MenuPopover


@Gtk.Template(
    resource_path="/fr/romainvigier/MetadataCleaner/ui/StatusIndicator.ui"
)
class StatusIndicator(Gtk.Stack):
    """Indicator showing the status of the files manager."""

    __gtype_name__ = "StatusIndicator"

    _progressbar: Gtk.ProgressBar = Gtk.Template.Child()

    def __init__(self, *args, **kwargs) -> None:
        """Status indicator initialization."""
        super().__init__(*args, **kwargs)
        self._window: Optional[Gtk.Widget] = None
        self.connect("hierarchy-changed", self._on_hierarchy_changed)

    def _sync_progressbar(self, current, total) -> None:
        self._progressbar.set_fraction(current / total)
        self._progressbar.set_text(
            _("Processing file {}/{}").format(current, total)
        )

    def _on_hierarchy_changed(
        self,
        widget: Gtk.Widget,
        previous_toplevel: Optional[Gtk.Widget]
    ) -> None:
        self._window = self.get_toplevel()
        if not hasattr(self._window, "files_manager"):
            self._window = None
            return
        self._window.files_manager.connect(
            "state-changed",
            self._on_files_manager_state_changed
        )
        self._window.files_manager.connect(
            "progress-changed",
            self._on_files_manager_progress_changed
        )
        self.show_idle()

    def _on_files_manager_state_changed(
        self,
        files_manager: FilesManager,
        new_state: FilesManagerState
    ) -> None:
        if new_state == FilesManagerState.WORKING:
            self.show_progressbar()

    def _on_files_manager_progress_changed(
        self,
        files_manager: FilesManager,
        current: int,
        total: int
    ) -> None:
        self._sync_progressbar(current, total)
        if current == total:
            self.show_done()

    def show_idle(self) -> None:
        """Show the idle state."""
        self.set_visible_child_name("idle")

    def show_progressbar(self) -> None:
        """Show a progress bar."""
        self.set_visible_child_name("working")

    def show_done(self) -> None:
        """Show a "Done" message."""
        self.set_visible_child_name("done")
        GLib.timeout_add_seconds(5, self._show_done_finished)

    def _show_done_finished(self) -> None:
        if not self._window:
            return
        if self._window.files_manager.state == FilesManagerState.IDLE:
            self.show_idle()

"""Vizualisation of metadata."""

from gettext import gettext as _
from gi.repository import Gtk
from typing import Dict, Optional


@Gtk.Template(
    resource_path="/fr/romainvigier/MetadataCleaner/ui/MetadataView.ui"
)
class MetadataView(Gtk.ScrolledWindow):
    """Vizualisation of metadata."""

    __gtype_name__ = "MetadataView"

    _tree_view: Gtk.TreeView = Gtk.Template.Child()

    def __init__(self, metadata: Dict, *args, **kwargs) -> None:
        """View initialization.

        Args:
            metadata (Dict): The metadata to visualize.
        """
        super().__init__(*args, **kwargs)
        self._metadata = metadata
        if isinstance(metadata[list(metadata)[0]], Dict):
            self._setup_multifile_list_store()
            self._setup_multifile_tree_view()
        else:
            self._setup_list_store()
            self._setup_tree_view()

    def _setup_list_store(self) -> None:
        self._list_store = Gtk.ListStore(str, str, str)
        for key, value in self._metadata.items():
            self._list_store.append(["", str(key), str(value)])

    def _setup_multifile_list_store(self) -> None:
        self._list_store = Gtk.ListStore(str, str, str)
        for f, metadata in self._metadata.items():
            for key, value in metadata.items():
                self._list_store.append([str(f), str(key), str(value)])

    def _setup_tree_view(self) -> None:
        self._tree_view.set_model(self._list_store)
        self._tree_view.append_column(
            Gtk.TreeViewColumn(_("Key"), Gtk.CellRendererText(), text=1)
        )
        self._tree_view.append_column(
            Gtk.TreeViewColumn(_("Value"), Gtk.CellRendererText(), text=2)
        )

    def _setup_multifile_tree_view(self) -> None:
        self._tree_view.set_model(self._list_store)
        self._tree_view.append_column(
            Gtk.TreeViewColumn(_("File"), Gtk.CellRendererText(), text=0)
        )
        self._tree_view.append_column(
            Gtk.TreeViewColumn(_("Key"), Gtk.CellRendererText(), text=1)
        )
        self._tree_view.append_column(
            Gtk.TreeViewColumn(_("Value"), Gtk.CellRendererText(), text=2)
        )

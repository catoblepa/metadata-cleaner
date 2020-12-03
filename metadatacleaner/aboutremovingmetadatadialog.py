"""Message dialog teaching users about removing metadata."""

from gi.repository import Gtk


@Gtk.Template(
    resource_path=(
        "/fr/romainvigier/MetadataCleaner/"
        "ui/AboutRemovingMetadataDialog.ui"
    )
)
class AboutRemovingMetadataDialog(Gtk.MessageDialog):
    """Message dialog teaching users about removing metadata."""

    __gtype_name__ = "AboutRemovingMetadataDialog"

    def __init__(self, *args, **kwargs) -> None:
        """Dialog initialization."""
        super().__init__(
            buttons=Gtk.ButtonsType.OK,
            *args,
            **kwargs
        )

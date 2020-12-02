"""Message dialog teaching users about metadata and privacy."""

from gi.repository import Gtk


@Gtk.Template(
    resource_path=(
        "/fr/romainvigier/MetadataCleaner/"
        "ui/AboutMetadataPrivacyDialog.ui"
    )
)
class AboutMetadataPrivacyDialog(Gtk.MessageDialog):
    """Message dialog teaching users about metadata and privacy."""

    __gtype_name__ = "AboutMetadataPrivacyDialog"

    def __init__(self, *args, **kwargs) -> None:
        """Dialog initialization."""
        super().__init__(
            buttons=Gtk.ButtonsType.OK,
            *args,
            **kwargs
        )

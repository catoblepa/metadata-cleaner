from gi.repository import Gtk


@Gtk.Template(
    resource_path=(
        "/fr/romainvigier/MetadataCleaner/"
        "ui/AboutRemovingMetadataDialog.ui"
    )
)
class AboutRemovingMetadataDialog(Gtk.MessageDialog):

    __gtype_name__ = "AboutRemovingMetadataDialog"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(
            buttons=Gtk.ButtonsType.OK,
            *args,
            **kwargs
        )

from gi.repository import Gtk


@Gtk.Template(
    resource_path="/fr/romainvigier/MetadataCleaner/ui/MenuPopover.ui"
)
class MenuPopover(Gtk.PopoverMenu):

    __gtype_name__ = "MenuPopover"

    def __init__(self) -> None:
        super().__init__()

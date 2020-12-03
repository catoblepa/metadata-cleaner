# Metadata Cleaner

![Welcome screen](./data/screenshots/1.png)
![Files view with metadata popover](./data/screenshots/2.png)

Metadata within a file can tell a lot about you. Cameras record data about when a picture was taken and what camera was used. Office applications automatically add author and company information to documents and spreadsheets. Maybe you don't want to disclose those informations.

This tool allows you to view metadata in your files and to get rid of them, as much as possible.

Under the hood, it relies on [mat2](https://0xacab.org/jvoisin/mat2) to parse and remove the metadata.

[![Donate using Liberapay](https://liberapay.com/assets/widgets/donate.svg)](https://liberapay.com/rmnvgr/donate)

---

[[_TOC_]]

---

## Building from source

Dependencies:

- `gtk3` >= 3.24
- `libhandy1`
- `python3`
- `python3-gobject`
- `python3-mat2` and [its dependencies](https://0xacab.org/jvoisin/mat2#requirements)

Metadata Cleaner uses the meson build system:

```sh
meson builddir
sudo ninja -C builddir install
```

Flatpak building is also available and requires the GNOME 3.38 platform and SDK:

```sh
flatpak-builder --force-clean --user --install build-dir data/fr.romainvigier.MetadataCleaner.yaml
```

## Contributing

See [`CONTRIBUTING.md`](./CONTRIBUTING.md).

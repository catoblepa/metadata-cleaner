# Contributing

---

[[_TOC_]]

---

## Code

Metadata Cleaner is written in Python 3. It follows the [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide, the [PEP 257](https://www.python.org/dev/peps/pep-0257/) doctring conventions and the [PEP 484](https://www.python.org/dev/peps/pep-0484/) type hints.

Open a new merge request with your changes, the CI will automatically check your code.

## Translations

If you want to add a new language, add its code in a new line in the [`./po/LINGUAS`](./po/LINGUAS) file.

Run these commands to update the `po` files:

```sh
meson builddir
cd builddir
meson compile fr.romainvigier.MetadataCleaner-pot
meson compile fr.romainvigier.MetadataCleaner-update-po
```

Edit your language file in the [`./po/`](./po) directory.

## Support

I've written this application for the benefit of everyone, if you want to help me in return, please consider [supporting me on Liberapay](https://liberapay.com/rmnvgr/)!

<!--
SPDX-FileCopyrightText: 2020 Romain Vigier <contact AT romainvigier.fr>
SPDX-License-Identifier: CC-BY-SA-4.0
-->

# Contributing

---

[[_TOC_]]

---

## Code

Before writing any code, please open a new issue to discuss your intented changes.

Metadata Cleaner is written in Python 3. It follows the [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide, the [PEP 257](https://www.python.org/dev/peps/pep-0257/) doctring conventions and the [PEP 484](https://www.python.org/dev/peps/pep-0484/) type hints.

If you add or modify strings, make your modification available to translation by updating the POT and PO files with these commands:

```bash
meson compile -C builddir fr.romainvigier.MetadataCleaner-pot
meson compile -C builddir fr.romainvigier.MetadataCleaner-update-po
```

Open a new merge request with your changes, the CI will automatically check your code.

## Translations

The project uses Weblate to manage translations. Head over [Metadata Cleaner's project page](https://hosted.weblate.org/projects/metadata-cleaner/) to start translating the application. If you need help, check out [Weblate's user documentation](https://docs.weblate.org/en/latest/user/translating.html).

Current translation status:

[![Translation status](https://hosted.weblate.org/widgets/metadata-cleaner/-/multi-auto.svg)](https://hosted.weblate.org/engage/metadata-cleaner/)

## Copyright notices

When you change or add files, add your copyright notice to the top of the file, or in a separate file (named `original-file.ext.license`), following the [SPDX specification](https://spdx.dev/).

The CI will warn you if you add a file without specifying its license.

## Commit messages

If you make a merge request with only one commit, specify in its message which part of the program you worked on, then what your changes do. If you make a merge request with multiple commits, they will be squashed into a single commit: you can change the commit message when making the merge request.

Message examples:

```
Status indicator: Add details about the current operation
```
or
```
Translation: Update French
```

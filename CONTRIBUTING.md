<!--
SPDX-FileCopyrightText: Metadata Cleaner contributors
SPDX-License-Identifier: CC-BY-SA-4.0
-->

# Contributing

## Documentation

The help pages are written in [Mallard](http://projectmallard.org/index.html) and are viewed in [GNOME Yelp](https://wiki.gnome.org/Apps/Yelp/).

The source of the help is in the `./help` directory. Only edit files in the `C` subdirectory, other subdirectoies are automatically generated. If you create new pages, add their path to the `./help/meson.build` file.

## Translations

The project uses Weblate to manage translations. Head over [Metadata Cleaner's project page](https://hosted.weblate.org/projects/metadata-cleaner/) to start translating the application. If you need help, check out [Weblate's user documentation](https://docs.weblate.org/en/latest/user/translating.html).

Current translation status:

[![Translation status](https://hosted.weblate.org/widgets/metadata-cleaner/-/multi-auto.svg)](https://hosted.weblate.org/engage/metadata-cleaner/)

## Code

The code of the application is in the `./application` directory.

Before writing any code, please open a new issue to discuss your intended changes.

### Conventions

Metadata Cleaner is written in Python 3. It follows the [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide, the [PEP 257](https://www.python.org/dev/peps/pep-0257/) doctring conventions and the [PEP 484](https://www.python.org/dev/peps/pep-0484/) type hints.

To check that your code follows these guidelines, have the programs `pycodestyle`, `pydocstyle` and `mypy` in your `PATH` and run this command:

```bash
meson test -C builddir
```

### New files

If you add new UI or Python files, add their path to the `./application/po/POTFILES` file. Add the UI files path to `./application/data/fr.romainvigier.MetadataCleaner.gresource.xml` and the Python files path to `./application/metadatacleaner/meson.build`.


### Licenses and copyright notices

When you add a file, add the copyright notice at the top of the file, or in a separate file (named `original-file.ext.license`), following the [SPDX specification](https://spdx.dev/). For instance:

```txt
SPDX-FileCopyrightText: Metadata Cleaner contributors
SPDX-License-Identifier: GPL-3.0-or-later
```

To check that you have no missing licenses or copyright notices, have the program `reuse` in your `PATH` and run this command:

```bash
meson test -C builddir
```

### Commit messages

If you make a merge request with only one commit, specify in its message which part of the program you worked on, then what your changes do. If you make a merge request with multiple commits, they can be squashed into a single commit: you can change the commit message when making the merge request.

Message example:

```
Status indicator: Add details about the current operation
```

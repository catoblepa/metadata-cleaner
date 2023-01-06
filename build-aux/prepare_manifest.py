#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2021 Romain Vigier <contact AT romainvigier.fr>
# SPDX-License-Identifier: GPL-3.0-or-later

"""Prepare the Flatpak manifest for a release build."""

import yaml


MANIFEST_FILE = "build-aux/fr.romainvigier.MetadataCleaner.yaml"


def rewrite_manifest() -> None:
    """Rewrite manifest to remove the devel flag."""
    print("Rewriting manifest for release...")

    with open(MANIFEST_FILE, "r") as f:
        manifest = yaml.safe_load(f)

    manifest["default-branch"] = "stable"

    try:
        opts = manifest["modules"][-1]["config-opts"]
    except KeyError:
        return
    opts = ["-Ddevel=false" if i == "-Ddevel=true" else i for i in opts]
    manifest["modules"][-1]["config-opts"] = opts

    with open(MANIFEST_FILE, "w") as f:
        yaml.dump(manifest, f)

    print("Finished rewriting manifest.")


rewrite_manifest()

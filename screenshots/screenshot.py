#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2021 Romain Vigier <contact AT romainvigier.fr>
# SPDX-License-Identifier: GPL-3.0-or-later

"""Run the screenshooter in a headless compositor."""

import os
import subprocess

from datetime import date
from langcodes import Language, LanguageTagError
from typing import Optional


PREFIX = os.path.join("/tmp", "screenshots")
DATA_DIR = os.path.join(PREFIX, "share")
LOCALE_DIR = os.path.join(DATA_DIR, "locale")

APP_ID = "fr.romainvigier.MetadataCleaner"
PACKAGE_NAME = "metadata-cleaner"
RESOURCE_DIR = os.path.join(DATA_DIR, PACKAGE_NAME)
RESOURCE_FILE = os.path.join(RESOURCE_DIR, f"{APP_ID}.gresource")
RESOURCE_PATH = "/fr/romainvigier/MetadataCleaner"
TEXTDOMAIN = APP_ID

SOCKET = "wayland-99"
SOCKET_2X = "wayland-100"


class Widget:
    """Base widget."""

    def __init__(
            self,
            ui_file: str,
            image_file: str,
            css_file: Optional[str] = None) -> None:
        """Create a new widget.

        Args:
            ui_file (str): Path to the UI file describing the widget.
            image_file (str): Path to the output image file.
            css_file (str, optional): Path to the stylesheet file to load for
                the widget. Defaults to None.
        """
        self.ui_file = ui_file
        self.image_file = image_file
        self.license_file = f"{image_file}.license"
        self.css_file: Optional[str] = css_file


class ApplicationWidget(Widget):
    """Application widget."""

    def __init__(self, number: int) -> None:
        """Create a new application widget.

        Args:
            number (int): Number of the screenshot.
        """
        ui_file = os.path.join("screenshots", f"application-{number}.ui")
        image_file = os.path.join("resources", "screenshots", f"{number}.png")
        css_file = os.path.join("screenshots", "application.css")
        super().__init__(ui_file, image_file, css_file)


class HelpWidget(Widget):
    """Help widget."""

    def __init__(self, name: str, langcode: str, css: bool) -> None:
        """Create a new help widget.

        Args:
            name (str): Name of the widget.
            lang (str): Language of the widget.
            css (bool): If the widget uses a custom stylesheet.
        """
        ui_file = os.path.join("screenshots", f"help-{name}.ui")
        image_file = os.path.join("help", langcode, "figures", f"{name}.png")
        css_file = os.path.join("screenshots", f"help-{name}.css") if css \
            else None
        super().__init__(ui_file, image_file, css_file)


def compile_translations() -> None:
    """Compile translations."""
    print("Compiling translations…")
    po_dir = os.path.join("application", "po")
    with open(os.path.join(po_dir, "LINGUAS")) as f:
        languages = [lang for lang in f.read().splitlines()
                     if lang != "" and lang[0] != "#"]
    languages.sort()
    for i, lang in enumerate(languages, 1):
        print(f"[{i}/{len(languages)}] Compiling {lang} translation…")
        in_file = os.path.join(po_dir, f"{lang}.po")
        out_dir = os.path.join(LOCALE_DIR, lang, "LC_MESSAGES")
        out_file = os.path.join(out_dir, f"{TEXTDOMAIN}.mo")
        os.makedirs(out_dir, exist_ok=True)
        subprocess.run([
            "msgfmt",
            f"--output-file={out_file}",
            in_file])


def compile_resources() -> None:
    """Compile resources."""
    print("Compiling resources…")
    source_dir = os.path.join("application", "data")
    source_file = os.path.join(source_dir, f"{APP_ID}.gresource.xml")
    os.makedirs(RESOURCE_DIR, exist_ok=True)
    subprocess.run([
        "glib-compile-resources",
        f"--target={RESOURCE_FILE}",
        f"--sourcedir={source_dir}",
        source_file])


def start_weston(
        scale: Optional[int] = None,
        socket: Optional[str] = None) -> subprocess.Popen[bytes]:
    """Start the Weston compositor in headless mode."""
    args = []
    if scale:
        args.append(f"--scale={scale}")
    if socket:
        args.append(f"--socket={socket}")
    return subprocess.Popen(
        ["weston", "--backend=headless-backend.so"] + args,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL)


def run_uishooter(
        ui_file: str,
        output: Optional[str] = None,
        resource_file: Optional[str] = None,
        resource_path: Optional[str] = None,
        textdomain: Optional[str] = None,
        locale: Optional[str] = None,
        locale_dir: Optional[str] = None,
        css: Optional[str] = None,
        scale: Optional[int] = None,
        dark: bool = False,
        libadwaita: bool = False) -> int:
    """Shoot the given UI file.

    Args:
        ui_file (str): Path to the UI file.
        output (str, optional): Path to the output image. Defaults to None.
        resource_file (str, optional): Path to a resource file to load.
            Defaults to None.
        resource_path (str, optional): Resource path to load. Defaults to None.
        textdomain (str, optional): Translation textdomain. Defaults to None.
        locale (str, optional): Locale to use. Defaults to None.
        locale_dir (str, optional): Path to a directory containing compiled
            translations. Defaults to None.
        css (str, optional): Path to a CSS file to load. Defaults to None.
        scale (int, optional): Integer scale factor of the output image.
            Defaults to 1.
        dark (bool, optional): Use dark color scheme. Defaults to False.
        libadwaita (bool, optional): Use libadwaita. Defaults to False.

    Returns:
        int: uishooter exit code
    """
    args = []
    env = os.environ.copy()
    if output:
        args.append(f"--output={output}")
    if resource_file:
        args.append(f"--resource-file={resource_file}")
    if resource_path:
        args.append(f"--resource-path={resource_path}")
    if textdomain:
        args.append(f"--textdomain={textdomain}")
    if locale:
        args.append(f"--locale={locale}")
    if locale_dir:
        args.append(f"--locale-dir={locale_dir}")
    if css:
        args.append(f"--css={css}")
    if scale:
        args.append(f"--scale={scale}")
    if dark:
        args.append(f"--dark")
    if libadwaita:
        args.append(f"--libadwaita")
    args.append(ui_file)
    env["WAYLAND_DISPLAY"] = SOCKET_2X if scale == 2 else SOCKET
    return subprocess.run(["uishooter"] + args, env=env).returncode


def shoot_application() -> None:
    """Shoot widgets for application metainfo."""
    print("Shooting application widgets…")
    total = 4
    for i in range(1, total + 1):
        widget = ApplicationWidget(i)
        print(f"[{i}/{total}] Shooting {widget.ui_file}…")
        exit_code = run_uishooter(
            ui_file=widget.ui_file,
            resource_path=RESOURCE_PATH,
            resource_file=RESOURCE_FILE,
            css=widget.css_file,
            output=widget.image_file,
            libadwaita=True)
        if exit_code != 0:
            raise RuntimeError(f"Error while shooting {widget.ui_file}.")
        write_license_file(widget.license_file)


def shoot_help() -> None:
    """Shoot widgets for the help pages."""
    print("Shooting help widgets…")
    with open(os.path.join("help", "LINGUAS")) as f:
        langcodes = [code for code in f.read().splitlines()
                     if code != "" and code[0] != "#"]
    langcodes.sort()
    total = len(langcodes) + 1
    for i, langcode in enumerate(langcodes, 1):
        for widget in [
                HelpWidget("add-files-button", langcode, True),
                HelpWidget("add-folders-button", langcode, True),
                HelpWidget("clean-button", langcode, False),
                HelpWidget("metadata-example", langcode, True)]:
            print(f"[{i}/{total}|{langcode}] Shooting {widget.ui_file}…")
            exit_code = run_uishooter(
                ui_file=widget.ui_file,
                locale=locale_from_langcode(langcode),
                locale_dir=LOCALE_DIR,
                textdomain=TEXTDOMAIN,
                resource_path=RESOURCE_PATH,
                resource_file=RESOURCE_FILE,
                css=widget.css_file,
                output=widget.image_file,
                libadwaita=True)
            if exit_code != 0:
                raise RuntimeError(f"Error while shooting {widget.ui_file}.")
            write_license_file(widget.license_file)


def shoot_website() -> None:
    """Shoot widgets for website."""
    print("Shooting website widgets…")
    for scale in [1, 2]:
        image_suffix = f"-{scale}x" if scale > 1 else ""
        widget = Widget(
            os.path.join("screenshots", "website.ui"),
            os.path.join("website", f"app{image_suffix}.png"),
            os.path.join("screenshots", "website.css"))
        print(f"[1/1|{scale}x] Shooting {widget.ui_file}…")
        exit_code = run_uishooter(
            ui_file=widget.ui_file,
            resource_path=RESOURCE_PATH,
            resource_file=RESOURCE_FILE,
            css=widget.css_file,
            scale=scale,
            output=widget.image_file,
            libadwaita=True)
        if exit_code != 0:
            raise RuntimeError(f"Error while shooting {widget.ui_file}.")
        write_license_file(widget.license_file)


def write_license_file(path: str) -> None:
    """Write a license file at the given path.

    Args:
        path (str): The path of the license file.
    """
    with open(path, "w") as f:
        f.writelines([
            f"SPDX-FileCopyrightText: {date.today().year} "
            "Romain Vigier <contact AT romainvigier.fr>\n",
            "SPDX-License-Identifier: CC-BY-SA-4.0"
        ])


def locale_from_langcode(langcode: str) -> str:
    """Get the locale string from a language code.

    Args:
        langcode (str): Language code.

    Returns:
        str: Locale string.
    """
    # Likely territory for "pt" is "BR", force "PT"
    if langcode == "pt":
        langcode = "pt-PT"
    try:
        language = Language.get(langcode)
        language = language.fill_likely_values()
        return f"{language.language}_{language.territory}.utf8"
    except LanguageTagError:
        return "C"


if __name__ == "__main__":
    weston = None
    weston_2x = None
    try:
        compile_translations()
        compile_resources()
        weston = start_weston(socket=SOCKET)
        weston_2x = start_weston(scale=2, socket=SOCKET_2X)
        shoot_application()
        shoot_help()
        shoot_website()
    finally:
        if weston:
            weston.terminate()
        if weston_2x:
            weston_2x.terminate()

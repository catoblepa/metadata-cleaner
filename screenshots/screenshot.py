#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2021 Romain Vigier <contact AT romainvigier.fr>
# SPDX-License-Identifier: GPL-3.0-or-later

"""Run the screenshooter in a headless compositor."""

import os
import subprocess

from datetime import date
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
            self, ui_file: str, image_file: str, css_file: str = None) -> None:
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

    def __init__(self, name: str, lang: str, css: bool) -> None:
        """Create a new help widget.

        Args:
            name (str): Name of the widget.
            lang (str): Language of the widget.
            css (bool): If the widget uses a custom stylesheet.
        """
        ui_file = os.path.join("screenshots", f"help-{name}.ui")
        image_file = os.path.join("help", lang, "figures", f"{name}.png")
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
        scale: int = None,
        socket: str = None) -> subprocess.Popen[bytes]:
    """Start the Weston compositor in headless mode."""
    args = []
    if scale:
        args.append(f"--scale={scale}")
    if socket:
        args.append(f"--socket={socket}")
    return subprocess.Popen(
        ["weston", "--backend=headless-backend.so"] + args)


def run_uishooter(
        ui_file: str,
        output: str = None,
        resource_file: str = None,
        resource_path: str = None,
        textdomain: str = None,
        locale: str = None,
        locale_dir: str = None,
        css: str = None,
        scale: int = None,
        dark: bool = False,
        libadwaita: bool = False,
        language: str = None) -> int:
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
    if language:
        env["LANGUAGE"] = language
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
        languages = [lang for lang in f.read().splitlines()
                     if lang != "" and lang[0] != "#"]
    languages.sort()
    total = len(languages) + 1
    for i, lang in enumerate(["C"] + languages, 1):
        for widget in [
                HelpWidget("add-files-button", lang, True),
                HelpWidget("clean-button", lang, False),
                HelpWidget("metadata-example", lang, True)]:
            print(f"[{i}/{total}|{lang}] Shooting {widget.ui_file}…")
            exit_code = run_uishooter(
                ui_file=widget.ui_file,
                locale=locale_from_lang(lang),
                locale_dir=LOCALE_DIR,
                textdomain=TEXTDOMAIN,
                resource_path=RESOURCE_PATH,
                resource_file=RESOURCE_FILE,
                css=widget.css_file,
                output=widget.image_file,
                libadwaita=True,
                language=lang)
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


def locale_from_lang(lang: str) -> str:
    """Get a locale string from a language code.

    Args:
        lang (str): The language code.

    Returns:
        str: The locale string.
    """
    try:
        return {
            "aa": "aa_DJ.utf-8",
            "af": "af_ZA.utf-8",
            "ak": "ak_GH.utf-8",
            "am": "am_ET.utf-8",
            "an": "an_ES.utf-8",
            "ar": "ar_TN.utf-8",
            "as": "as_IN.utf-8",
            "az": "az_AZ.utf-8",
            "be": "be_BY.utf-8",
            "bg": "BG.utf-8",
            "bho": "bho_IN.utf-8",
            "bi": "bi_VU.utf-8",
            "bn": "bn_IN.utf-8",
            "bo": "bo_CN.utf-8",
            "br": "br_FR.utf-8",
            "bs": "bs_BA.utf-8",
            "ca": "ca_ES.utf-8",
            "ce": "ce_RU.utf-8",
            "cs": "cs_CZ.utf-8",
            "cv": "cv_RU.utf-8",
            "cy": "cy_GB.utf-8",
            "da": "da_DK.utf-8",
            "de": "de_DE.utf-8",
            "doi": "doi_IN.utf-8",
            "dv": "dv_MV.utf-8",
            "dz": "dz_BT.utf-8",
            "el": "el_GR.utf-8",
            "en": "en_US.utf-8",
            "es": "es_ES.utf-8",
            "et": "et_EE.utf-8",
            "eu": "eu_ES.utf-8",
            "fa": "da_IR.utf-8",
            "ff": "ff_SN.utf-8",
            "fi": "fi_FI.utf-8",
            "fil": "fil_PH.utf-8",
            "fo": "fo_FO.utf-8",
            "fr": "fr_FR.utf-8",
            "fy": "fy_DE.utf-8",
            "ga": "ga_IE.utf-8",
            "gd": "gd_GB.utf-8",
            "gl": "gl_ES.utf-8",
            "gu": "gu_IN.utf-8",
            "gv": "gv_GB.utf-8",
            "ha": "ha_NG.utf-8",
            "he": "he_IL.utf-8",
            "hi": "hi_IN.utf-8",
            "hr": "hr_HR.utf-8",
            "ht": "ht_HT.utf-8",
            "hu": "hu_HU.utf-8",
            "hy": "hy_AM.utf-8",
            "ia": "ia_FR.utf-8",
            "id": "id_ID.utf-8",
            "ig": "ig_NG.utf-8",
            "ik": "ik_CA.utf-8",
            "is": "is_IS.utf-8",
            "it": "it_IT.utf-8",
            "iu": "iu_CA.utf-8",
            "ja": "ja_JP.utf-8",
            "kab": "kab_DZ.utf-8",
            "ka": "ka_GE.utf-8",
            "kk": "kk_KZ.utf-8",
            "kl": "kl_GL.utf-8",
            "km": "km_KH.utf-8",
            "kn": "kn_IN.utf-8",
            "ko": "ko_KR.utf-8",
            "ks": "ks_IN.utf-8",
            "ku": "ku_TR.utf-8",
            "kw": "kw_GB.utf-8",
            "ky": "ky_KG.utf-8",
            "lb": "lb_LU.utf-8",
            "lg": "lg_UG.utf-8",
            "li": "li_BE.utf-8",
            "ln": "ln_CS.utf-8",
            "lo": "lo_LA.utf-8",
            "lt": "lt_LT.utf-8",
            "lv": "lv_LV.utf-8",
            "mag": "mag_IN.utf-8",
            "mai": "mai_IN.utf-8",
            "mg": "mg_MG.utf-8",
            "mi": "mi_NZ.utf-8",
            "mk": "mk_MK.utf-8",
            "ml": "ml_IN.utf-8",
            "mni": "mni_IN.utf-8",
            "mn": "mn_MN.utf-8",
            "mr": "mr_IN.utf-8",
            "ms": "ms_MY.utf-8",
            "mt": "mt_MT.utf-8",
            "my": "my_MM.utf-8",
            "nb": "nb_NO.utf-8",
            "ne": "ne_NP.utf-8",
            "nl": "nl_NL.utf-8",
            "nn": "nn_NO.utf-8",
            "nr": "nr_ZA.utf-8",
            "nso": "nso_ZA.utf-8",
            "oc": "oc_FR.utf-8",
            "om": "om_ET.utf-8",
            "or": "or_IN.utf-8",
            "os": "os_RU.utf-8",
            "pa": "pa_IN.utf-8",
            "pl": "pl_PL.utf-8",
            "pt": "pt_PT.utf-8",
            "raj": "raj_IN.utf-8",
            "ro": "ro_RO.utf-8",
            "ru": "ru_RU.utf-8",
            "rw": "rw_RW.utf-8",
            "sa": "sa_IN.utf-8",
            "sc": "sc_IT.utf-8",
            "sd": "sd_IN.utf-8",
            "se": "se_NO.utf-8",
            "shn": "shn_MM.utf-8",
            "sid": "sid_ET.utf-8",
            "si": "si_LK.utf-8",
            "sk": "sk_SK.utf-8",
            "sl": "sl_SI.utf-8",
            "sm": "sm_WS.utf-8",
            "so": "so_SO.utf-8",
            "sq": "sq_AL.utf-8",
            "sr": "sr_RS.utf-8",
            "ss": "ss_ZA.utf-8",
            "st": "st_ZA.utf-8",
            "sv": "sv_SE.utf-8",
            "sw": "sw_TZ.utf-8",
            "ta": "ta_IN.utf-8",
            "te": "te_IN.utf-8",
            "tg": "tg_TJ.utf-8",
            "th": "th_TH.utf-8",
            "ti": "ti_ER.utf-8",
            "tk": "tk_TM.utf-8",
            "tl": "tl_PH.utf-8",
            "tn": "tn_ZA.utf-8",
            "to": "to_TO.utf-8",
            "tr": "tr_TR.utf-8",
            "ts": "ts_ZA.utf-8",
            "tt": "tt_RU.utf-8",
            "ug": "ug_CN.utf-8",
            "uk": "uk_UA.utf-8",
            "ur": "ur_PK.utf-8",
            "uz": "uz_UZ.utf-8",
            "ve": "ve_ZA.utf-8",
            "vi": "vi_VN.utf-8",
            "wa": "wa_BE.utf-8",
            "wo": "wo_SN.utf-8",
            "xh": "xh_ZA.utf-8",
            "yi": "yi_US.utf-8",
            "yo": "yo_NG.utf-8",
            "zh": "zh_CN.utf-8",
            "zh_CN": "zh_CN.utf-8",
            "zh_TW": "zh_TW.utf-8",
            "zu": "zu_ZA.utf-8",
        }[lang]
    except KeyError:
        return lang


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

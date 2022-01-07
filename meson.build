# SPDX-FileCopyrightText: 2020, 2021 Romain Vigier <contact AT romainvigier.fr>
# SPDX-License-Identifier: GPL-3.0-or-later

project(
  'metadata-cleaner',
  version: '2.1.4',
  license: ['GPL-3.0-or-later', 'CC-BY-SA-4.0'],
  meson_version: '>= 0.59.0'
)

APP_ID = 'fr.romainvigier.MetadataCleaner'

gnome = import('gnome')
i18n = import('i18n')
python = import('python').find_installation('python3')

prefix = get_option('prefix')

bindir = prefix / get_option('bindir')
datadir = prefix / get_option('datadir')
localedir = prefix / get_option('localedir')
pythondir = prefix / python.get_install_dir()

appdatadir = datadir / 'metainfo'
applicationsdir = datadir / 'applications'
iconsdir = datadir / 'icons'
metadatacleanerdir = pythondir / 'metadatacleaner'
pkgdatadir = datadir / meson.project_name()
schemasdir = datadir / 'glib-2.0' / 'schemas'

devel = get_option('devel')

subdir('application')
subdir('help')
subdir('tests')

gnome.post_install(
  glib_compile_schemas: true,
  gtk_update_icon_cache: true,
  update_desktop_database: true
)

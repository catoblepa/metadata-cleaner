# SPDX-FileCopyrightText: Metadata Cleaner contributors
# SPDX-License-Identifier: GPL-3.0-or-later

project(
  'metadata-cleaner',
  version: '2.5.6',
  license: ['GPL-3.0-or-later', 'CC-BY-SA-4.0'],
  meson_version: '>= 0.59.0'
)

APP_ID = 'fr.romainvigier.MetadataCleaner'

gnome = import('gnome')
i18n = import('i18n')

prefix = get_option('prefix')

bindir = prefix / get_option('bindir')
datadir = prefix / get_option('datadir')
localedir = prefix / get_option('localedir')

appdatadir = datadir / 'metainfo'
applicationsdir = datadir / 'applications'
dbusdir = datadir / 'dbus-1' / 'services'
iconsdir = datadir / 'icons'
pkgdatadir = datadir / meson.project_name() / 'data'
pkgsrcdir = datadir / meson.project_name() / 'src'
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

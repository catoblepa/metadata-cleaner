# SPDX-FileCopyrightText: 2020, 2021 Romain Vigier <contact AT romainvigier.fr>
# SPDX-License-Identifier: GPL-3.0-or-later

project(
  'metadata-cleaner',
  version: '2.0.0',
  license: ['GPL-3.0-or-later', 'CC-BY-SA-4.0', 'CC0-1.0'],
  meson_version: '>= 0.51.0'
)

APP_ID = 'fr.romainvigier.MetadataCleaner'

gnome = import('gnome')
i18n = import('i18n')
python = import('python').find_installation('python3', modules: ['libmat2'])

# dependency('gtk4', version: '>=4.0')
# dependency('libadwaita-1')
# dependency('pygobject-3.0', version: '>=3.40')
# dependency('python3')

prefix = get_option('prefix')

bindir = prefix / get_option('bindir')
datadir = prefix / get_option('datadir')
libexecdir = prefix / get_option('libexecdir')
localedir = prefix / get_option('localedir')
pythondir = prefix / python.get_install_dir()

pkgdatadir = datadir / meson.project_name()

appdatadir = datadir / 'metainfo'
applicationsdir = datadir / 'applications'
metadatacleanerdir = pythondir / 'metadatacleaner'
iconsdir = datadir / 'icons'
schemasdir = datadir / 'glib-2.0' / 'schemas'

devel = get_option('devel')

bin_config = configuration_data()
bin_config.set('localedir', localedir)
bin_config.set('pkgdatadir', pkgdatadir)
bin_config.set('pythondir', pythondir)
bin_config.set('schemasdir', schemasdir)
bin_config.set('app_id', APP_ID)
bin_config.set('devel', devel)
bin_config.set('version', meson.project_version())

configure_file(
  input: 'metadata-cleaner.py.in',
  output: 'metadata-cleaner',
  configuration: bin_config,
  install_dir: bindir
)

subdir('data')
subdir('help')
subdir('metadatacleaner')
subdir('po')
subdir('tests')

meson.add_install_script('build-aux' / 'postinstall.py')

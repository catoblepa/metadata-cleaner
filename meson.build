# SPDX-FileCopyrightText: 2020 Romain Vigier <contact AT romainvigier.fr>
# SPDX-License-Identifier: GPL-3.0-or-later

project('metadata-remover',
  version: '1.0.6',
  meson_version: '>= 0.51.0'
)

APP_ID = 'fr.romainvigier.MetadataCleaner'

python = import('python').find_installation('python3', modules: 'libmat2')

prefix = get_option('prefix')

bindir = join_paths(prefix, get_option('bindir'))
datadir = join_paths(prefix, get_option('datadir'))
libexecdir = join_paths(prefix, get_option('libexecdir'))
localedir = join_paths(prefix, get_option('localedir'))
pythondir = join_paths(prefix, python.get_install_dir())

pkgdatadir = join_paths(datadir, meson.project_name())

appdatadir = join_paths(datadir, 'metainfo')
applicationsdir = join_paths(datadir, 'applications')
metadatacleanerdir = join_paths(pythondir, 'metadatacleaner')
iconsdir = join_paths(datadir, 'icons')
schemasdir = join_paths(datadir, 'glib-2.0', 'schemas')

dependency('gtk+-3.0', version: '>=3.24')
dependency('libhandy-1')
dependency('pygobject-3.0', version: '>= 3.30')
dependency('python3')

bin_config = configuration_data()
bin_config.set('localedir', localedir)
bin_config.set('pkgdatadir', pkgdatadir)
bin_config.set('pythondir', pythondir)
bin_config.set('schemasdir', schemasdir)
bin_config.set('app_id', APP_ID)
bin_config.set('version', meson.project_version())

configure_file(
  input: 'metadata-cleaner.py.in',
  output: 'metadata-cleaner',
  configuration: bin_config,
  install_dir: get_option('bindir')
)

sources = [
  'metadatacleaner/__init__.py',
  'metadatacleaner/aboutdialog.py',
  'metadatacleaner/aboutmetadataprivacydialog.py',
  'metadatacleaner/aboutremovingmetadatadialog.py',
  'metadatacleaner/addfilesbutton.py',
  'metadatacleaner/app.py',
  'metadatacleaner/cleanmetadatabutton.py',
  'metadatacleaner/emptyview.py',
  'metadatacleaner/file.py',
  'metadatacleaner/filebutton.py',
  'metadatacleaner/filechooserdialog.py',
  'metadatacleaner/filepopover.py',
  'metadatacleaner/filerow.py',
  'metadatacleaner/filesmanager.py',
  'metadatacleaner/filesview.py',
  'metadatacleaner/logger.py',
  'metadatacleaner/menubutton.py',
  'metadatacleaner/menupopover.py',
  'metadatacleaner/metadatadetails.py',
  'metadatacleaner/metadatawindow.py',
  'metadatacleaner/savefilesbutton.py',
  'metadatacleaner/savewarningdialog.py',
  'metadatacleaner/shortcutsdialog.py',
  'metadatacleaner/statusindicator.py',
  'metadatacleaner/window.py',
]
install_data(sources, install_dir: metadatacleanerdir)

subdir('data')
subdir('po')

meson.add_install_script('meson_postinstall.py')

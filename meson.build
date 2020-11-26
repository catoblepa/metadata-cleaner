project('metadata-remover',
  version: '1.0.0',
  meson_version: '>= 0.46.0'
)

PROJECT_RDNN_NAME = 'fr.romainvigier.MetadataCleaner'

python = import('python').find_installation('python3')

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


bin_config = configuration_data()
bin_config.set('localedir', localedir)
bin_config.set('pkgdatadir', pkgdatadir)
bin_config.set('pythondir', pythondir)
bin_config.set('schemasdir', schemasdir)
bin_config.set('app_id', PROJECT_RDNN_NAME)
bin_config.set('version', meson.project_version())

configure_file(
  input: 'metadata-cleaner.py.in',
  output: 'metadata-cleaner',
  configuration: bin_config,
  install_dir: get_option('bindir')
)

sources = [
  'metadatacleaner/__init__.py',
  'metadatacleaner/addfilesbutton.py',
  'metadatacleaner/app.py',
  'metadatacleaner/cleanmetadatabutton.py',
  'metadatacleaner/emptyview.py',
  'metadatacleaner/filebutton.py',
  'metadatacleaner/filepopover.py',
  'metadatacleaner/filerow.py',
  'metadatacleaner/filesmanager.py',
  'metadatacleaner/filesview.py',
  'metadatacleaner/menubutton.py',
  'metadatacleaner/menupopover.py',
  'metadatacleaner/metadataview.py',
  'metadatacleaner/window.py',
]
install_data(sources, install_dir: metadatacleanerdir)

subdir('data')
subdir('po')

meson.add_install_script('meson_postinstall.py')

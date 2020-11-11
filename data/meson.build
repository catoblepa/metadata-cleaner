gnome = import('gnome')
i18n = import('i18n')

gnome.compile_resources(
  PROJECT_RDNN_NAME,
  PROJECT_RDNN_NAME + '.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

gio_schemasdir = dependency('gio-2.0').get_pkgconfig_variable(
  'schemasdir',
  define_variable: ['datadir', datadir],
  default: schemasdir,
)

i18n.merge_file(
  type: 'desktop',
  input: PROJECT_RDNN_NAME + '.desktop.in',
  output: PROJECT_RDNN_NAME + '.desktop',
  po_dir: join_paths(meson.source_root(), 'po'),
  install: true,
  install_dir: applicationsdir
)


install_data(PROJECT_RDNN_NAME + '.gschema.xml', install_dir: schemasdir)
install_data('mime.types', install_dir: pkgdatadir)
install_subdir('icons/hicolor', install_dir: iconsdir)

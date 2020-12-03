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

# Validate MetaInfo file
metainfo_file = 'fr.romainvigier.MetadataCleaner.metainfo.xml'
ascli_exe = find_program('appstreamcli', required: false)
if ascli_exe.found()
  test(
    'validate metainfo file',
    ascli_exe,
    args: [
      'validate',
      '--no-net',
      '--pedantic',
      metainfo_file
    ]
  )
endif

i18n.merge_file(
  type: 'desktop',
  input: PROJECT_RDNN_NAME + '.desktop.in',
  output: PROJECT_RDNN_NAME + '.desktop',
  po_dir: join_paths(meson.source_root(), 'po'),
  install: true,
  install_dir: applicationsdir
)

i18n.merge_file(
  input: metainfo_file,
  output: 'fr.romainvigier.MetadataCleaner.metainfo.xml',
  type: 'xml',
  po_dir: join_paths (meson.source_root(), 'po'),
  install: true,
  install_dir: appdatadir
)


install_data(PROJECT_RDNN_NAME + '.gschema.xml', install_dir: schemasdir)
install_data('mime.types', install_dir: pkgdatadir)
install_subdir('icons/hicolor', install_dir: iconsdir)

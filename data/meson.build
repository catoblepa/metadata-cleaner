# SPDX-FileCopyrightText: 2020, 2021 Romain Vigier <contact AT romainvigier.fr>
# SPDX-License-Identifier: GPL-3.0-or-later

gnome.compile_resources(
  APP_ID,
  APP_ID + '.gresource.xml',
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
metainfo_file = APP_ID + '.metainfo.xml'
ascli_exe = find_program('appstreamcli', required: false)
if ascli_exe.found()
  test(
    'validate metainfo file',
    ascli_exe,
    args: [
      'validate',
      '--no-net',
      '--pedantic',
      meson.current_build_dir() / metainfo_file
    ]
  )
endif

i18n.merge_file(
  type: 'desktop',
  input: APP_ID + '.desktop.in',
  output: APP_ID + '.desktop',
  po_dir: meson.source_root() / 'po',
  install: true,
  install_dir: applicationsdir
)

i18n.merge_file(
  input: metainfo_file,
  output: APP_ID + '.metainfo.xml',
  type: 'xml',
  po_dir: meson.source_root() / 'po',
  install: true,
  install_dir: appdatadir
)


install_data(APP_ID + '.gschema.xml', install_dir: schemasdir)
install_subdir('icons/hicolor', install_dir: iconsdir)

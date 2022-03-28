# SPDX-FileCopyrightText: 2020-2022 Romain Vigier <contact AT romainvigier.fr>
# SPDX-License-Identifier: GPL-3.0-or-later

xdg_config = configuration_data()
xdg_config.set('bindir', bindir)

gnome.compile_resources(
  APP_ID,
  APP_ID + '.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
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
  input: configure_file(
    input: APP_ID + '.desktop.in',
    output: APP_ID + '.desktop.in',
    configuration: xdg_config,
  ),
  output: APP_ID + '.desktop',
  po_dir: appsrcdir / 'po',
  install: true,
  install_dir: applicationsdir
)

i18n.merge_file(
  input: metainfo_file,
  output: APP_ID + '.metainfo.xml',
  type: 'xml',
  po_dir: appsrcdir / 'po',
  install: true,
  install_dir: appdatadir
)

configure_file(
  input: APP_ID + '.service.in',
  output: APP_ID + '.service',
  configuration: xdg_config,
  install_dir: dbusdir
)


install_data(APP_ID + '.gschema.xml', install_dir: schemasdir)
install_subdir('icons/hicolor', install_dir: iconsdir)

# SPDX-FileCopyrightText: Metadata Cleaner contributors
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

desktop_file = i18n.merge_file(
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

# Validate Desktop file
desktop_file_validate_exe = find_program('desktop-file-validate', required: false)
if desktop_file_validate_exe.found()
  test('Validate desktop file',
    desktop_file_validate_exe,
    args: [desktop_file]
  )
endif

metainfo_file = i18n.merge_file(
  input: APP_ID + '.metainfo.xml',
  output: APP_ID + '.metainfo.xml',
  type: 'xml',
  po_dir: appsrcdir / 'po',
  install: true,
  install_dir: appdatadir
)

# Validate MetaInfo file
appstreamcli_exe = find_program('appstreamcli', required: false)
if (appstreamcli_exe.found())
  test('Validate metainfo file',
    appstreamcli_exe,
    args: ['validate', '--no-net', '--pedantic', metainfo_file],
    workdir: meson.current_build_dir()
  )
endif

configure_file(
  input: APP_ID + '.service.in',
  output: APP_ID + '.service',
  configuration: xdg_config,
  install_dir: dbusdir
)


install_data(APP_ID + '.gschema.xml', install_dir: schemasdir)

glib_compile_schemas_exe = find_program('glib-compile-schemas', required: false)
if glib_compile_schemas_exe.found()
  test('Validate schema file',
    glib_compile_schemas_exe,
    args: ['--strict', '--dry-run', meson.current_source_dir()]
  )
endif

install_data('icons' / APP_ID + '.svg', install_dir: iconsdir / 'hicolor' / 'scalable' / 'apps')
install_data('icons' / APP_ID + '-symbolic.svg', install_dir: iconsdir / 'hicolor' / 'symbolic' / 'apps')

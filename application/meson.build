# SPDX-FileCopyrightText: 2021 Romain Vigier <contact AT romainvigier.fr>
# SPDX-License-Identifier: GPL-3.0-or-later

appsrcdir = meson.project_source_root() / 'application'

bin_config = configuration_data()
bin_config.set('localedir', localedir)
bin_config.set('pkgdatadir', pkgdatadir)
bin_config.set('pythondir', pythondir)
bin_config.set('schemasdir', schemasdir)
bin_config.set('app_id', APP_ID)
bin_config.set('devel', devel)
bin_config.set('version', meson.project_version())

configure_file(
  input: 'main.py',
  output: meson.project_name(),
  configuration: bin_config,
  install_dir: bindir
)

subdir('data')
subdir('metadatacleaner')
subdir('po')

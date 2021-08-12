# SPDX-FileCopyrightText: 2021 Romain Vigier <contact AT romainvigier.fr>
# SPDX-License-Identifier: GPL-3.0-or-later

main = [
  '__init__.py',
  'app.py',
]
modules = [
  'modules/__init__.py',
  'modules/file.py',
  'modules/filestore.py',
  'modules/logger.py',
  'modules/metadata.py',
]
ui = [
  'ui/__init__.py',
  'ui/aboutdialog.py',
  'ui/addfilesbutton.py',
  'ui/badge.py',
  'ui/cleaningwarningdialog.py',
  'ui/cleanmetadatabutton.py',
  'ui/creditsrole.py',
  'ui/detailsview.py',
  'ui/emptyview.py',
  'ui/filechooserdialog.py',
  'ui/filerow.py',
  'ui/filesview.py',
  'ui/infodetails.py',
  'ui/menubutton.py',
  'ui/metadatadetails.py',
  'ui/metadatadetailsrow.py',
  'ui/outbutton.py',
  'ui/settingsbutton.py',
  'ui/statusindicator.py',
  'ui/window.py',
]

install_data(main, install_dir: metadatacleanerdir)
install_data(modules, install_dir: metadatacleanerdir / 'modules')
install_data(ui, install_dir: metadatacleanerdir / 'ui')

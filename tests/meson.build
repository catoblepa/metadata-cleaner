# SPDX-FileCopyrightText: 2021 Romain Vigier <contact AT romainvigier.fr>
# SPDX-License-Identifier: GPL-3.0-or-later

mypy_exe = find_program('mypy', required: false)
if mypy_exe.found()
  test(
    'Check typing (PEP 484)',
    mypy_exe,
    args: [
      '--ignore-missing-imports',
      meson.source_root() / 'metadatacleaner'
    ],
    suite: 'code',
  )
endif

pycodestyle_exe = find_program('pycodestyle', required: false)
if pycodestyle_exe.found()
  test(
    'Check code style (PEP 8)',
    pycodestyle_exe,
    args: [
      meson.source_root() / 'metadatacleaner'
    ],
    suite: 'code',
  )
endif

pydocstyle_exe = find_program('pydocstyle', required: false)
if pydocstyle_exe.found()
  test(
    'Check docstrings (PEP 257)',
    pydocstyle_exe,
    args: [
      meson.source_root() / 'metadatacleaner'
    ],
    suite: 'code',
  )
endif

reuse_exe = find_program('reuse', required: false)
if reuse_exe.found()
  test(
    'Comply with REUSE spec',
    reuse_exe,
    args: [
      '--root',
      meson.source_root(),
      'lint'
    ],
    suite: 'licenses',
  )
endif

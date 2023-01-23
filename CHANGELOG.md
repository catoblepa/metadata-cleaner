<!--
SPDX-FileCopyrightText: 2021 Romain Vigier <contact AT romainvigier.fr>
SPDX-License-Identifier: CC-BY-SA-4.0
-->

# Changelog


## [2.4.0] - 2023-01-23

### Added

- It is now possible to cancel adding and cleaning operations
- Adding files and checking metadata is now done at the same time to give accurate progress report

### Changed

- Updated Arabic translation (contributed by @Ali-98)
- Updated Chinese (simplified) translation (contributed by Ujhhgtg)
- Updated Croatian translation (contributed by @milotype)
- Updated Hungarian translation (contributed by Szia Tomi)


## [2.3.1] - 2023-01-09

### Changed

- Updated Galician translation (contributed by @gallegonovato)
- Updated German translation (contributed by @Atalanttore)
- Updated Italian translation (contributed by @albanobattistella)
- Updated Portuguese (Brazil) translation (contributed by Daniel Abrante)

### Fixed

- Screenshots in RTL languages were not in the correct direction


## [2.3.0] - 2023-01-07

Note to packagers: the application Python modules are now installed in the data directory.

### Changed

- Updated Chinese (simplified) translation (contributed by Ujhhgtg)
- Updated Dutch translation (contributed by @Vistaus)
- Updated French translation
- Updated German translation (contributed by @Atalanttore)
- Updated Spanish translation (contributed by Óscar Fernández Díaz)
- Updated Swedish translation (contributed by @eson)
- Updated Tamil translation (contributed by @kbdharun)
- Updated Turkish translation (contributed by @ersen)
- Updated Ukrainian translation (contributed by @ihor_ck)

### Fixed

- Screenshots in help were not translated


## [2.2.8] - 2022-12-07

### Added

- New Arabic translation (contributed by Ali Aljishi)

### Changed

- Updated Russian translation (contributed by @VoynovAR)


## [2.2.7] - 2022-11-17

Fix of version 2.2.6 due to CI test failure.

Notes from version 2.2.6:

### Added

- New Serbian translation (contributed by Andrija Djakovic)

### Changed

- Updated Finnish translation (contributed by @artnay)
- Updated Galician translation (contributed by @gallegonovato)
- Updated Lithuanian translation (contributed by @completed)


## [2.2.6] - 2022-11-17

### Added

- New Serbian translation (contributed by Andrija Djakovic)

### Changed

- Updated Finnish translation (contributed by @artnay)
- Updated Galician translation (contributed by @gallegonovato)
- Updated Lithuanian translation (contributed by @completed)


## [2.2.5] - 2022-10-06

### Added

- New Tamil translation (contributed by @kbdharun)

### Changed

- Updated Korean translation (contributed by @Junghee_Lee)
- Updated Occitan translation (contributed by @quenty_occitania)


## [2.2.4] - 2022-09-24

### Added
- New Azerbaijani translation (contributed by Ümid Quliyev)
- New Frisian translation (contributed by @vancha)
- New Greek translation (contributed by @Pyrofanis)

### Changed
- Updated Basque translation (contributed by @sergitroll9)
- Updated Chinese (Simplified) translation (contributed by Eric)
- Updated Croatian translation (contributed by @milotype)
- Updated Dutch translation (contributed by @Vistaus)
- Updated Finnish translation (contributed by @artnay)
- Updated French translation
- Updated Hungarian translation (contributed by Szia Tomi)
- Updated Indonesian translation (contributed by @t7260)
- Updated Italian translation (contributed by @albanobattistella)
- Updated Japanese translation (contributed by Kaede)
- Updated Occitan translation (contributed by @quenty_occitania)
- Updated Spanish translation (contributed by @oscfdezdz)
- Updated Swedish translation (contributed by @eson)
- Updated Turkish translation (contributed by @ersen and @libreajans)
- Updated Ukrainian translation (contributed by @ihor_ck)

## [2.2.2] - 2022-04-20


## [2.2.3] - 2022-06-02

### Added
- New Ukrainian translation (contributed by @ihor_ck)

### Changed
- Updated Basque translation (contributed by @sergitroll9)

## [2.2.2] - 2022-04-20


### Added
- New Bengali translation (contributed by Bingo and hELLOwORLD)

### Changed
- Updated Czech translation (contributed by pavelzahradnik)
- Updated Finnish translation (contributed by @artnay)
- Updated German translation (contributed by Cgrieger)
- Updated Indonesian translation (contributed by @cacing69)
- Updated Italian translation (contributed by @albanobattistella)
- Updated Norwegian Bokmål translation (contributed by @kingu)
- Updated Occitan translation (contributed by @quenty_occitania)
- Updated Russian translation (contributed by Sasha)

### Fixed
- Chinese translations were not loaded due to an incorrect language code


## [2.2.1] - 2022-03-28

### Changed
- Updated Croatian translation (contributed by @milotype)
- Updated Hungarian translation (contributed by Szia Tomi)
- Updated Swedish translation (contributed by @eson)

### Fixed
- DBus activation was not possible on some systems


## [2.2.0] - 2022-03-23

### Added
- Dropping of files to clean on the main window

### Changed
- Dependency upon GTK >= 4.6
- Dependency upon libadwaita >= 1.0.0
- User interface improvements
- Folder chooser recursive option is enabled by default
- Updated Chinese (simplified) translation (contributed by Eric)
- Updated Dutch translation (contributed by @Vistaus)
- Updated French translation
- Updated Polish translation (contributed by Anon Ymous)
- Updated Spanish translation (contributed by @oscfdezdz)
- Updated Turkish translation (contributed by @ersen)

### Fixed
- Titlebar buttons at the wrong position
- Settings help button didn't open the correct help section


## [2.1.5] - 2022-02-15

### Added
- New Chinese (simplified) translation (contributed by poi and Eric)
- New Portuguese translation (contributed by @JulianoSC)

### Changed
- Updated Basque translation (contributed by @sergitroll9)
- Updated French translation
- Updated Italian translation (contributed by @albanobattistella)
- Updated Polish translation (contributed by Zszywek)
- Updated Russian translation (contributed by Sasha)


## [2.1.4] - 2022-01-07

### Added
- New Galician translation (contributed by @frandieguez)
- Initial work on Polish translation (contributed by Zszywek)

### Changed
- Updated Finnish translation (contributed by Janne)
- Updated Indonesian translation (contributed by @0x6e656b6f)
- Updated Occitan translation (contributed by @quenty_occitania)
- Updated Portguese (Brazil) translation (contributed by Gabriel Gian)
- Updated Spanish translation (contributed by @oscfdezdz)


## [2.1.3] - 2021-12-03

### Changed
- Updated German translation (contributed by @eladyn)


## [2.1.2] - 2021-11-16

### Added
- New Czech translation (contributed by pavelzahradnik)


## [2.1.1] - 2021-11-11

### Added
- New Romanian translation (contributed by Victor Mihalache)

### Fixed
- Clicking the Help menu item froze the application
- A frame was not properly hidden in the details view of a cleaned file


## [2.1.0] - 2021-11-04

### Added
- New button to add folders
- Folder name is now displayed in the files view

### Changed
- Meson >= 0.59 is required
- Dependency upon libadwaita 1.0.0.alpha.4
- Info bar on the empty view is now a button
- Status indicator now tells which action it is doing
- About dialog is now scrollable
- Updated Basque translation (contributed by @sergitroll9)
- Updated Croatian translation (contributed by @milotype)
- Updated Dutch translation (contributed by @Vistaus)
- Updated Finnish translation (contributed by @artnay)
- Updated French translation
- Updated Hungarian translation (contributed by @urbalazs)
- Updated Italian translation (contributed by @albanobattistella)
- Updated Japanese translation (contributed by Kaede)
- Updated Lithuanian translation (contributed by @completed)
- Updated Occitan translation (contributed by @quenty_occitania)
- Updated Portuguese (Brazil) translation (contributed by Davi Patricio)
- Updated Spanish translation (contributed by @oscfdezdz)
- Updated Swedish translation (contributed by @eson)
- Updated Turkish translation (contributed by @ersen)


## [2.0.1] - 2021-09-28

### Added
- New Basque translation (contributed by @sergitroll9)

### Changed
- Dependency upon libadwaita 1.0.0.alpha.3
- Updated Croatian translation (contributed by @milotype)
- Updated Dutch translation (contributed by @Vistaus)
- Updated French translation
- Updated German translation (contributed by @milotype)
- Updated Hungarian translation (contributed by @urbalazs)
- Updated Lithuanian translation (contributed by @completed)
- Updated Spanish translation (contributed by @oscfdezdz)
- Updated Swedish translation (contributed by @eson)
- Updated Turkish translation (contributed by @ersen)

### Fixed
- Writing style (contributed by @BrainBlasted)
- Typos (contributed by @urbalazs)


## [2.0.0] - 2021-09-22

Metadata Cleaner v2.0.0 is a major release featuring a brand new user interface written in GTK4 and using libadwaita, a new help system and a whole set of new and updated translations.

### Added
- Dependency upon GTK >=4.4
- Dependency upon libadwaita commit `03f159488ec3b8e3ea4c3c2daa9c408b071d512d` (as the library is still in development, it is subject to API changes. When it is released, a new version of Metadata Cleaner will be tagged.)
- Help pages trough Yelp
- Adaptive user interface
- Details about a finished cleaning
- Menu item for clearing the window
- Persistent lightweight cleaning preference
- Window size saved on close
- New Hungarian translation (contributed by @urbalazs)
- New Japanese translation (contributed by Kaede)
- New Occitan translation (contributed by @quenty_occitania)
- Initial work on Danish translation (contributed by @kingu)
- Initial work on Norwegian Nynorsk translation (contributed by @kingu)
- Initial work on Russian translation (contributed by @BigmenPixel)

### Changed
- Cleaning and saving merged into a single action
- Social links added in the About dialog
- Updated Croatian translation (contributed by @milotype)
- Updated Dutch translation (contributed by @Vistaus)
- Updated Finnish translation (contributed by @artnay)
- Updated French translation
- Updated German translation (contributed by @milotype)
- Updated Indonesian translation (contributed by @t7260 and Reza Almanda)
- Updated Italian translation (contributed by @albanobattistella)
- Updated Lithuanian translation (contributed by @completed)
- Updated Norwegian Bokmål translation (contributed by @kingu)
- Updated Portuguese (Brazil) translation (contributed by @rafaelff and @xfgusta)
- Updated Spanish translation (contributed by @oscfdezdz)
- Updated Swedish translation (contributed by @eson and @kingu)
- Updated Turkish translation (contributed by @ersen)

### Removed
- Dependency upon GTK3 and libhandy


## [1.0.8] - 2021-08-10

### Added
- New Dutch translation (contributed by @Vistaus)
- New Italian translation (contributed by @albanobattistella)
- Initial work on Sinhala translation (contributed by HelaBasa)

### Changed
- Updated Indonesian translation (contributed by @t7260)


## [1.0.7] - 2021-07-05

### Added
- New Lithuanian translation (contributed by Gediminas Murauskas)
- Initial work on Finnish translation (contributed by @artnay)
- Initial work on Indonesian translation (contributed by @kingu)
- Initial work on Norwegian Bokmål translation (contributed by @t7260 and Reza Almanda)


## [1.0.6] - 2021-05-04

### Added

- New Croatian translation (contributed by @milotype)
- New Portuguese (Brazil) translation (contributed by @xfgusta)


## [1.0.5] - 2021-04-13

### Fixed
- Wrong accelerator in the shortcuts window


## [1.0.4] - 2021-04-02

### Added
- New Turkish translation (contributed by @ersen)


## [1.0.3] - 2021-02-17

### Changed
- Updated Spanish translation


## [1.0.2] - 2021-01-15

### Added
- New Spanish translation (contributed by @oscfdezdz)
- New Swedish translation (contributed by @eson)

### Fixed
- Files with uppercase extension can't be added


## [1.0.1] - 2020-12-28

### Added
- New German translation (contributed by @lux)


## [1.0.0] - 2020-12-10

First release! 🎉

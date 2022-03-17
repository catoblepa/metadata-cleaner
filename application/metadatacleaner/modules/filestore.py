# SPDX-FileCopyrightText: 2020-2022 Romain Vigier <contact AT romainvigier.fr>
# SPDX-License-Identifier: GPL-3.0-or-later

"""Files Manager object and states."""

import libmat2
import mimetypes

from concurrent.futures import ThreadPoolExecutor, as_completed
from enum import IntEnum, auto
from gi.repository import Gio, GLib, GObject
from threading import Thread
from typing import Dict, Iterable, List, Optional

from metadatacleaner.modules.file import File, FileState
from metadatacleaner.modules.logger import Logger as logger


def _get_supported_formats() -> Dict:
    formats = {}
    for parser in libmat2.parser_factory._get_parsers():
        for mimetype in parser.mimetypes:
            extensions = set()
            for extension in mimetypes.guess_all_extensions(mimetype):
                if extension not in libmat2.UNSUPPORTED_EXTENSIONS:
                    extensions.add(extension)
            if not extensions:
                continue
            formats[mimetype] = extensions
    return formats


SUPPORTED_FORMATS = _get_supported_formats()


class FileStoreState(IntEnum):
    """States the Files Manager can have."""

    IDLE = auto()
    WORKING = auto()


class FileStoreAction(IntEnum):
    """Actions the Files manager can do."""

    ADDING = auto()
    CHECKING = auto()
    CLEANING = auto()


class FileStore(Gio.ListStore):
    """File Store object."""

    __gtype_name__ = "FileStore"

    __gsignals__ = {
        "file-state-changed": (GObject.SIGNAL_RUN_LAST, None, (int,)),
        "state-changed": (GObject.SIGNAL_RUN_LAST, None, (int,)),
        "progress-changed": (GObject.SIGNAL_RUN_LAST, None, (int, int))
    }

    lightweight_mode: bool = GObject.Property(
        type=bool,
        nick="lightweight-mode",
        default=False)

    def __init__(self) -> None:
        """File Store initialization."""
        Gio.ListStore.__init__(self, item_type=File)
        self.state = FileStoreState.IDLE
        self.last_action: Optional[FileStoreAction] = None
        self.progress = (0, 0)

    def _on_file_state_changed(self, f: File, new_state: FileState) -> None:
        GLib.idle_add(
            self.emit,
            "file-state-changed",
            self.get_index_of_file(f))

    def _set_state(self, state: FileStoreState) -> None:
        if state == self.state:
            return
        self.state = state
        logger.debug(
            f"State of file store changed to {str(self.state)}.")
        GLib.idle_add(self.emit, "state-changed", state)

    def _set_progress(self, current: int, total: int) -> None:
        self.progress = (current, total)
        logger.debug(f"File store progress set to {self.progress}.")
        GLib.idle_add(self.emit, "progress-changed", current, total)

    def get_files(self) -> List[File]:
        """Get all the files from the File Store.

        Returns:
            List[File]: List of files.
        """
        return self

    def get_file_with_index(self, index: int) -> File:
        """Get a file at a specified index.

        Args:
            index (int): The desired index.

        Returns:
            Optional[File]: The file if found, else None.
        """
        f = self.get_item(index)
        if not f:
            raise RuntimeError("No file in the file store for this index.")
        return f

    def get_index_of_file(self, f: File) -> int:
        """Get the index of a given file.

        Args:
            f (File): The file to get the index for.

        Returns:
            int: The file index.
        """
        found, position = self.find(f)
        if not found:
            raise RuntimeError("File not found in file store.")
        return position

    def add_gfiles(
            self, gfiles: List[Gio.File], recursive: bool = True) -> None:
        """Add Gio Files to the Files Manager.

        Args:
            gfiles (List[Gio.File]): List of Gio Files to add.
            recursive (bool, optional): If subdirectories should also be looked
            into. Defaults to True.
        """
        all_gfiles: List[Gio.File] = []
        for gfile in gfiles:
            f_type = gfile.query_file_type(Gio.FileQueryInfoFlags.NONE, None)
            if f_type == Gio.FileType.DIRECTORY:
                all_gfiles.extend(self._get_gfiles_from_dir(gfile, recursive))
            elif f_type == Gio.FileType.REGULAR:
                all_gfiles.append(gfile)
            else:
                logger.info(
                    f"File {gfile.get_path()} is neither a directory nor a "
                    "regular file, skipping.")
        with ThreadPoolExecutor() as executor:
            files = list(filter(None, executor.map(
                self._file_from_gfile,
                all_gfiles)))
        if len(files) == 0:
            logger.info("No files to add.")
            return
        self.splice(len(self), 0, files)
        thread = Thread(
            target=self._check_metadata_of_files_async,
            args=(files,),
            daemon=False)
        thread.start()

    def _get_gfiles_from_dir(
            self, dir: Gio.File, recursive: bool) -> List[Gio.File]:
        gfiles: List[Gio.File] = []
        subdirs: List[Gio.File] = []
        children_enumerator = dir.enumerate_children(
            "",
            Gio.FileQueryInfoFlags.NONE,
            None)
        while True:
            info = children_enumerator.next_file(None)
            if info is None:
                break
            child = children_enumerator.get_child(info)
            if info.get_file_type() == Gio.FileType.DIRECTORY:
                if recursive:
                    subdirs.append(child)
            elif info.get_file_type() == Gio.FileType.REGULAR:
                gfiles.append(child)
        children_enumerator.close(None)
        with ThreadPoolExecutor() as executor:
            for subgfiles in executor.map(
                    self._get_gfiles_from_dir,
                    subdirs,
                    [recursive] * len(subdirs)):
                gfiles.extend(subgfiles)
        return gfiles

    def _file_from_gfile(self, gfile: Gio.File) -> Optional[File]:
        if not gfile.query_exists(None):
            logger.info(f"File {gfile.get_path()} does not exist, skipping.")
            return None
        if bool(list(filter(lambda x: x.path == gfile.get_path(), self))):
            logger.info(f"Skipping {gfile.get_path()}, already added.")
            return None
        f = File(gfile)
        f.connect("state-changed", self._on_file_state_changed)
        return f

    def _check_metadata_of_files_async(self, files: List[File]) -> None:
        self._set_progress(0, len(files))
        self._set_state(FileStoreState.WORKING)
        self.last_action = FileStoreAction.ADDING
        with ThreadPoolExecutor() as executor:
            futures = {
                executor.submit(f.setup_parser)
                for f in files
            }
            for i, future in enumerate(as_completed(futures)):
                self._set_progress(0, len(files))
        self.last_action = FileStoreAction.CHECKING
        with ThreadPoolExecutor() as executor:
            futures = {
                executor.submit(f.check_metadata)
                for f in files
            }
            for i, future in enumerate(as_completed(futures)):
                self._set_progress(i + 1, len(files))
        self._set_state(FileStoreState.IDLE)

    def remove_file(self, f: File) -> None:
        """Remove a file from the File Store.

        Args:
            f (File): The file to remove.
        """
        self.remove_file_with_index(self.get_index_of_file(f))

    def remove_file_with_index(self, index: int) -> None:
        """Remove the file with the given index from the File Store.

        Args:
            index (int): The index of the file to remove.
        """
        self.remove(index)

    def remove_files(self) -> None:
        """Remove all the files from the File Store."""
        self.remove_all()

    def clean_files(self) -> None:
        """Remove metadata from all the cleanable files."""
        thread = Thread(target=self._clean_files_async, daemon=False)
        thread.start()

    def _clean_files_async(self) -> None:
        cleanable_files = self.get_cleanable_files()
        number_of_cleanable_files = len(cleanable_files)
        self._set_progress(0, number_of_cleanable_files)
        self._set_state(FileStoreState.WORKING)
        self.last_action = FileStoreAction.CLEANING
        with ThreadPoolExecutor() as executor:
            futures = {
                executor.submit(f.clean, self.lightweight_mode)
                for f in cleanable_files
            }
            for i, future in enumerate(as_completed(futures)):
                self._set_progress(i + 1, number_of_cleanable_files)
        self._set_state(FileStoreState.IDLE)

    def get_cleanable_files(self) -> List[File]:
        """Get all the cleanable files.

        Returns:
            List[File]: List of cleanable files.
        """
        return self._get_files_with_states((
            FileState.HAS_METADATA,
            FileState.HAS_NO_METADATA))

    def get_cleaned_files(self) -> List[File]:
        """Get all the cleaned files.

        Returns:
            List[File]: List of cleaned files.
        """
        return self._get_files_with_states((FileState.CLEANED,))

    def get_errored_files(self) -> List[File]:
        """Get all the files with errors.

        Returns:
            List[File]: List of files with errors.
        """
        return self._get_files_with_states((
            FileState.ERROR_WHILE_INITIALIZING,
            FileState.ERROR_WHILE_CHECKING_METADATA,
            FileState.ERROR_WHILE_REMOVING_METADATA))

    def _get_files_with_states(
            self,
            states: Iterable[FileState]) -> List[File]:
        return list(filter(lambda f: f.state in states, self))

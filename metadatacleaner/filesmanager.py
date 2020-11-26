import libmat2
import logging
import mimetypes
import os

from collections import deque
from enum import Enum, auto
from gi.repository import Gio, GObject
from libmat2 import parser_factory
from libmat2.abstract import AbstractParser
from threading import Thread
from typing import Deque, Dict, Iterable, Optional, Set


def _get_supported_formats() -> Dict:
    formats = {}
    for parser in parser_factory._get_parsers():
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


class FileState(Enum):
    INITIALIZING = auto()
    ERROR_WHILE_INITIALIZING = auto()
    UNSUPPORTED = auto()
    SUPPORTED = auto()
    CHECKING_METADATA = auto()
    ERROR_WHILE_CHECKING_METADATA = auto()
    HAS_NO_METADATA = auto()
    HAS_METADATA = auto()
    REMOVING_METADATA = auto()
    ERROR_WHILE_REMOVING_METADATA = auto()
    CLEANED = auto()


class File(GObject.GObject):

    __gsignals__ = {
        "state-changed": (GObject.SIGNAL_RUN_FIRST, None, (str,))
    }

    state = FileState.INITIALIZING
    metadata: Optional[Dict] = None
    error: Optional[Exception] = None
    cleanable = True
    _checking = False
    _cleaning = False

    def __init__(self, gfile: Gio.File) -> None:
        super().__init__()
        self.path = gfile.get_path()
        self.filename = gfile.get_basename()

    def _set_state(self, state: FileState) -> None:
        if state != self.state:
            self.state = state
            self.emit("state-changed", state)

    def initialize_parser(self) -> None:
        logging.debug(f"Initializing parser for {self.filename}...")
        self._initialize_parser()

    def _initialize_parser(self) -> None:
        try:
            parser, mimetype = parser_factory.get_parser(self.path)
        except ValueError as e:
            self.error = e
            self._on_parser_initialization_error()
        else:
            self._parser = parser
            self._on_parser_initialization_finished()

    def _on_parser_initialization_error(self) -> None:
        logging.error(
            f"Error while initializing parser for {self.filename}: "
            f"{self.error}"
        )
        self._set_state(FileState.ERROR_WHILE_INITIALIZING)

    def _on_parser_initialization_finished(self) -> None:
        if self._parser:
            logging.debug(f"{self.filename} is supported.")
            self._set_state(FileState.SUPPORTED)
        else:
            logging.warning(f"{self.filename} is unsupported.")
            self._set_state(FileState.UNSUPPORTED)

    def check_metadata(self) -> None:
        if self.state != FileState.SUPPORTED:
            return
        logging.debug(f"Checking metadata for {self.filename}...")
        self._set_state(FileState.CHECKING_METADATA)
        thread = Thread(target=self._check_metadata)
        thread.daemon = True
        thread.start()

    def _check_metadata(self) -> None:
        try:
            metadata = self._parser.get_meta()
        except Exception as e:
            self.error = e
            self._on_check_metadata_error()
        else:
            self.metadata = metadata if bool(metadata) else None
            self._on_check_metadata_finished()

    def _on_check_metadata_error(self) -> None:
        logging.error(
            f"Error while checking metadata for {self.filename}: {self.error}"
        )
        self._set_state(FileState.ERROR_WHILE_CHECKING_METADATA)

    def _on_check_metadata_finished(self) -> None:
        if self.metadata:
            logging.debug(f"Found metadata for {self.filename}.")
            self._set_state(FileState.HAS_METADATA)
        else:
            logging.debug(f"Found no metadata for {self.filename}.")
            self._set_state(FileState.HAS_NO_METADATA)

    def remove_metadata(self) -> None:
        if self.state != FileState.HAS_METADATA:
            return
        logging.debug(f"Removing metadata for {self.filename}...")
        self._set_state(FileState.REMOVING_METADATA)
        thread = Thread(target=self._remove_metadata)
        thread.daemon = True
        thread.start()

    def _remove_metadata(self) -> None:
        try:
            self._parser.remove_all()
            # Because of flatpak sandbox we have to replace the original file
            os.replace(self._parser.output_filename, self.path)
        except (RuntimeError, OSError) as e:
            self.error = e
            self._on_remove_metadata_error()
        else:
            self._on_remove_metadata_finished()

    def _on_remove_metadata_error(self) -> None:
        logging.error(
            f"Error while removing metadata for {self.filename}: {self.error}"
        )
        self._set_state(FileState.ERROR_WHILE_REMOVING_METADATA)

    def _on_remove_metadata_finished(self) -> None:
        logging.debug(f"{self.filename} has been cleaned.")
        self._set_state(FileState.CLEANED)


class FilesManager(GObject.GObject):

    __gsignals__ = {
        "file-added": (GObject.SIGNAL_RUN_FIRST, None, (int,)),
        "file-state-changed": (GObject.SIGNAL_RUN_FIRST, None, (int,))
    }

    _files: Deque[File] = deque()

    def __init__(self) -> None:
        super().__init__()

    def get_files(self) -> Deque[File]:
        return self._files

    def get_file(self, index: int) -> File:
        return self._files[index]

    def add(self, f: File) -> None:
        if f.path not in [existing_file.path for existing_file in self._files]:
            self._files.append(f)
            f.connect("state-changed", self._on_file_state_changed)
            self.emit("file-added", len(self._files) - 1)

    def get_cleanable_files(self) -> Deque[File]:
        cleanable_files: Deque[File] = deque()
        for f in self._files:
            if f.state == FileState.HAS_METADATA:
                cleanable_files.append(f)
        return cleanable_files

    def _on_file_state_changed(self, file: File, new_state: FileState) -> None:
        self.emit("file-state-changed", self._files.index(file))

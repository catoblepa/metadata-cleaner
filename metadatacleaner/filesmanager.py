import libmat2
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
    UNSUPPORTED = auto()
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
        self._parser = self._get_parser()

    def _get_parser(self) -> Optional[AbstractParser]:
        parser, mimetype = parser_factory.get_parser(self.path)
        return parser

    def _set_state(self, state: FileState) -> None:
        if state != self.state:
            self.state = state
            self.emit("state-changed", state)

    def update_metadata(self) -> None:
        import time
        if not self._parser:
            self.cleanable = False
            self._set_state(FileState.UNSUPPORTED)
            return
        self._checking = True
        self._set_state(FileState.CHECKING_METADATA)
        thread = Thread(target=self._get_metadata)
        thread.daemon = True
        thread.start()

    def _get_metadata(self) -> None:
        if not self._parser:
            return None
        try:
            metadata = self._parser.get_meta()
        except (KeyError, ValueError) as e:
            self._on_get_metadata_error()
        else:
            self.metadata = metadata if bool(metadata) else None
            self._on_get_metadata_finished()

    def _on_get_metadata_finished(self) -> None:
        if self._cleaning:
            self._cleaning = False
            self.cleanable = False
            self._set_state(FileState.CLEANED)
        elif self.metadata:
            self._set_state(FileState.HAS_METADATA)
        else:
            self.cleanable = False
            self._set_state(FileState.HAS_NO_METADATA)
        self._checking = False

    def _on_get_metadata_error(self) -> None:
        self._set_state(FileState.ERROR_WHILE_CHECKING_METADATA)
        self._checking = False

    def remove_metadata(self) -> None:
        if self._parser and self.metadata:
            self._cleaning = True
            self._set_state(FileState.REMOVING_METADATA)
            thread = Thread(target=self._remove_metadata)
            thread.daemon = True
            thread.start()

    def _remove_metadata(self) -> None:
        if not self._parser:
            return
        try:
            self._parser.remove_all()
            # Because of flatpak sandbox we have to replace the original file
            os.replace(self._parser.output_filename, self.path)
        except (RuntimeError, OSError) as e:
            self.error = e
            self._on_remove_metadata_error()
        else:
            self._on_remove_metadata_finished()

    def _on_remove_metadata_finished(self) -> None:
        self.update_metadata()

    def _on_remove_metadata_error(self) -> None:
        self._set_state(FileState.ERROR_WHILE_REMOVING_METADATA)
        self._cleaning = False


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
            if f.cleanable:
                cleanable_files.append(f)
        return cleanable_files

    def _on_file_state_changed(self, file: File, new_state: FileState) -> None:
        self.emit("file-state-changed", self._files.index(file))

import libmat2
import logging
import mimetypes

from collections import deque
from concurrent.futures import ThreadPoolExecutor, as_completed
from enum import IntEnum, auto
from gi.repository import GObject
from threading import Thread
from typing import Deque, Dict, Set

from metadatacleaner.file import File, FileState


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


class FilesManagerState(IntEnum):
    IDLE = auto()
    WORKING = auto()


class FilesManager(GObject.GObject):

    __gsignals__ = {
        "file-added": (GObject.SIGNAL_RUN_FIRST, None, (int,)),
        "file-removed": (GObject.SIGNAL_RUN_FIRST, None, ()),
        "file-state-changed": (GObject.SIGNAL_RUN_FIRST, None, (int,)),
        "state-changed": (GObject.SIGNAL_RUN_FIRST, None, (int,)),
        "progress-changed": (GObject.SIGNAL_RUN_FIRST, None, (int, int))
    }

    state = FilesManagerState.IDLE
    progress = (0, 0)

    _files: Deque[File] = deque()

    def __init__(self) -> None:
        super().__init__()

    def _on_file_state_changed(self, file: File, new_state: FileState) -> None:
        self.emit("file-state-changed", self._files.index(file))

    def get_files(self) -> Deque[File]:
        return self._files

    def get_file(self, index: int) -> File:
        return self._files[index]

    def add_file(self, f: File) -> None:
        if f.path not in [existing_file.path for existing_file in self._files]:
            self._files.append(f)
            f.connect("state-changed", self._on_file_state_changed)
            self.emit("file-added", len(self._files) - 1)

    def remove_file(self, f: File) -> None:
        self._files.remove(f)
        f.remove()
        self.emit("file-removed")

    def clean_files(self, lightweight_mode=False) -> None:
        thread = Thread(
            target=self._clean_files_async,
            args=(lightweight_mode,),
            daemon=True
        )
        thread.start()

    def _clean_files_async(self, lightweight_mode: bool) -> None:
        cleanable_files = self.get_cleanable_files()
        number_of_cleanable_files = len(cleanable_files)
        self._set_progress(0, number_of_cleanable_files)
        self._set_state(FilesManagerState.WORKING)
        with ThreadPoolExecutor() as executor:
            futures = {
                executor.submit(f.remove_metadata, lightweight_mode)
                for f in cleanable_files
            }
            for i, future in enumerate(as_completed(futures)):
                self._set_progress(i + 1, number_of_cleanable_files)
        self._set_state(FilesManagerState.IDLE)

    def save_cleaned_files(self) -> None:
        thread = Thread(target=self._save_cleaned_files_async, daemon=True)
        thread.start()

    def _save_cleaned_files_async(self) -> None:
        cleaned_files = self.get_cleaned_files()
        number_of_cleaned_files = len(cleaned_files)
        self._set_progress(0, number_of_cleaned_files)
        self._set_state(FilesManagerState.WORKING)
        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(f.save)for f in cleaned_files}
            for i, future in enumerate(as_completed(futures)):
                self._set_progress(i + 1, number_of_cleaned_files)
        self._set_state(FilesManagerState.IDLE)

    def get_cleanable_files(self) -> Deque[File]:
        return self._get_files_with_state(FileState.HAS_METADATA)

    def get_cleaned_files(self) -> Deque[File]:
        return self._get_files_with_state(FileState.CLEANED)

    def _get_files_with_state(self, state: FileState) -> Deque[File]:
        wanted_files: Deque[File] = deque()
        for f in self._files:
            if f.state == state:
                wanted_files.append(f)
        return wanted_files

    def _set_state(self, state: FilesManagerState) -> None:
        if state != self.state:
            self.state = state
            logging.debug(
                f"State of files manager changed to {str(self.state)}."
            )
            self.emit("state-changed", state)

    def _set_progress(self, current: int, total: int) -> None:
        self.progress = (current, total)
        logging.debug(f"Files manager progress set to {self.progress}.")
        self.emit("progress-changed", current, total)

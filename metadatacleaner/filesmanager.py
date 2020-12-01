import libmat2
import logging
import mimetypes

from concurrent.futures import ThreadPoolExecutor, as_completed
from enum import IntEnum, auto
from gi.repository import Gio, GLib, GObject
from threading import Thread
from typing import Dict, Iterable, List, Set

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

    _files: List[File] = list()
    _paths: Set = set()

    def __init__(self) -> None:
        super().__init__()
        # self._files: List[File] = []
        # self._paths: Set = set()
        self.state = FilesManagerState.IDLE
        self.progress = (0, 0)
        self.lightweight_mode = False

    def _on_file_state_changed(self, f: File, new_state: FileState) -> None:
        GLib.idle_add(self.emit, "file-state-changed", self._files.index(f))

    def get_files(self) -> List[File]:
        return self._files

    def get_file(self, index: int) -> File:
        return self._files[index]

    def add_gfiles(self, gfiles: List[Gio.File]) -> None:
        thread = Thread(
            target=self._add_gfiles_async,
            args=(gfiles,),
            daemon=True
        )
        thread.start()

    def _add_gfiles_async(self, gfiles: List[Gio.File]) -> None:
        number_of_gfiles = len(gfiles)
        self._set_progress(0, number_of_gfiles)
        self._set_state(FilesManagerState.WORKING)
        with ThreadPoolExecutor() as executor:
            futures = {
                executor.submit(self.add_gfile, gfile)
                for gfile in gfiles
            }
            for i, future in enumerate(as_completed(futures)):
                self._set_progress(i + 1, number_of_gfiles)
        self._set_state(FilesManagerState.IDLE)

    def add_gfile(self, gfile: Gio.File) -> None:
        if gfile.get_path() in self._paths:
            return
        f = File(gfile)
        self._paths.add(f.path)
        self._files.append(f)
        GLib.idle_add(self.emit, "file-added", len(self._files) - 1)
        f.connect("state-changed", self._on_file_state_changed)
        f.initialize_parser()
        f.check_metadata()

    def remove_file(self, f: File) -> None:
        self._files.remove(f)
        self._paths.remove(f.path)
        f.remove()
        GLib.idle_add(self.emit, "file-removed")

    def clean_files(self) -> None:
        thread = Thread(
            target=self._clean_files_async,
            daemon=True
        )
        thread.start()

    def _clean_files_async(self) -> None:
        cleanable_files = self.get_cleanable_files()
        number_of_cleanable_files = len(cleanable_files)
        self._set_progress(0, number_of_cleanable_files)
        self._set_state(FilesManagerState.WORKING)
        with ThreadPoolExecutor() as executor:
            futures = {
                executor.submit(f.remove_metadata, self.lightweight_mode)
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

    def get_cleanable_files(self) -> List[File]:
        return self._get_files_with_states((
            FileState.HAS_METADATA,
            FileState.HAS_NO_METADATA
        ))

    def get_cleaned_files(self) -> List[File]:
        return self._get_files_with_states((FileState.CLEANED,))

    def _get_files_with_states(
        self,
        states: Iterable[FileState]
    ) -> List[File]:
        wanted_files: List[File] = []
        for f in self._files:
            if f.state in states:
                wanted_files.append(f)
        return wanted_files

    def _set_state(self, state: FilesManagerState) -> None:
        if state == self.state:
            return
        self.state = state
        logging.debug(
            f"State of files manager changed to {str(self.state)}."
        )
        GLib.idle_add(self.emit, "state-changed", state)

    def _set_progress(self, current: int, total: int) -> None:
        self.progress = (current, total)
        logging.debug(f"Files manager progress set to {self.progress}.")
        GLib.idle_add(self.emit, "progress-changed", current, total)

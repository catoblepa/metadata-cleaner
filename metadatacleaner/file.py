import logging
import os

from enum import IntEnum, auto
from gettext import gettext as _
from gi.repository import Gio, GObject
from libmat2 import parser_factory
from libmat2.abstract import AbstractParser
from threading import Thread
from typing import Dict, Optional, Set


class FileState(IntEnum):
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
    SAVING = auto()
    ERROR_WHILE_SAVING = auto()
    SAVED = auto()


class File(GObject.GObject):

    __gsignals__ = {
        "state-changed": (GObject.SIGNAL_RUN_FIRST, None, (int,)),
        "removed": (GObject.SIGNAL_RUN_FIRST, None, ())
    }

    state = FileState.INITIALIZING
    mimetype = "text/plain"
    metadata: Optional[Dict] = None
    error: Optional[Exception] = None

    def __init__(self, gfile: Gio.File) -> None:
        super().__init__()
        self.path = gfile.get_path()
        self.filename = gfile.get_basename()

    def _set_state(self, state: FileState) -> None:
        if state != self.state:
            self.state = state
            logging.debug(f"State of {self.filename} changed to {str(state)}.")
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
            self.mimetype = mimetype
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

    def remove_metadata(self, lightweight_mode=False) -> None:
        if self.state != FileState.HAS_METADATA:
            return
        logging.debug(f"Removing metadata for {self.filename}...")
        self._set_state(FileState.REMOVING_METADATA)
        try:
            self._parser.lightweight_cleaning = lightweight_mode
            self._parser.remove_all()
            if not os.path.exists(self._parser.output_filename):
                raise RuntimeError(_(
                    "Something bad happened during the removal, "
                    "cleaned file not found"
                ))
        except RuntimeError as e:
            self.error = e
            logging.error(
                "Error while removing metadata for "
                f"{self.filename}: {self.error}"
            )
            self._set_state(FileState.ERROR_WHILE_REMOVING_METADATA)
        else:
            logging.debug(f"{self.filename} has been cleaned.")
            self._set_state(FileState.CLEANED)

    def save(self) -> None:
        if self.state != FileState.CLEANED:
            return
        logging.debug(f"Saving {self.filename}...")
        self._set_state(FileState.SAVING)
        try:
            os.replace(self._parser.output_filename, self.path)
        except OSError as e:
            self.error = e
            logging.error(f"Error while saving {self.filename}: {self.error}")
            self._set_state(FileState.ERROR_WHILE_SAVING)
        else:
            logging.debug(f"{self.filename} has been saved.")
            self._set_state(FileState.SAVED)

    def remove(self) -> None:
        self.emit("removed")

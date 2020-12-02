"""File object and states."""

import logging
import os

from enum import IntEnum, auto
from gettext import gettext as _
from gi.repository import Gio, GLib, GObject
from libmat2 import parser_factory
from threading import Thread
from typing import Dict, Optional


class FileState(IntEnum):
    """States that a File can have."""

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
    """File object."""

    __gsignals__ = {
        "state-changed": (GObject.SIGNAL_RUN_FIRST, None, (int,)),
        "removed": (GObject.SIGNAL_RUN_FIRST, None, ())
    }

    def __init__(self, gfile: Gio.File) -> None:
        """File initialization.

        Args:
            gfile (Gio.File): The Gio File that the File will be built from.
        """
        super().__init__()
        self.path = gfile.get_path()
        self.filename = gfile.get_basename()
        self.state = FileState.INITIALIZING
        self.mimetype = "text/plain"
        self.metadata: Optional[Dict] = None
        self.error: Optional[Exception] = None

    def _set_state(self, state: FileState) -> None:
        if state != self.state:
            self.state = state
            logging.debug(f"State of {self.filename} changed to {str(state)}.")
            GLib.idle_add(self.emit, "state-changed", state)

    def initialize_parser(self) -> None:
        """Initialize the metadata parser."""
        logging.debug(f"Initializing parser for {self.filename}...")
        try:
            parser, mimetype = parser_factory.get_parser(self.path)
        except ValueError as e:
            self.error = e
            logging.error(
                f"Error while initializing parser for {self.filename}: "
                f"{self.error}"
            )
            self._set_state(FileState.ERROR_WHILE_INITIALIZING)
        else:
            self._parser = parser
            self.mimetype = mimetype
            if self._parser:
                logging.debug(f"{self.filename} is supported.")
                self._set_state(FileState.SUPPORTED)
            else:
                logging.warning(f"{self.filename} is unsupported.")
                self._set_state(FileState.UNSUPPORTED)

    def check_metadata(self) -> None:
        """Check the metadata present in the file."""
        if self.state != FileState.SUPPORTED:
            return
        logging.debug(f"Checking metadata for {self.filename}...")
        self._set_state(FileState.CHECKING_METADATA)
        try:
            metadata = self._parser.get_meta()
        except Exception as e:
            self.error = e
            logging.error(
                "Error while checking metadata for "
                f"{self.filename}: {self.error}"
            )
            self._set_state(FileState.ERROR_WHILE_CHECKING_METADATA)
        else:
            self.metadata = metadata if bool(metadata) else None
            if self.metadata:
                logging.debug(f"Found metadata for {self.filename}.")
                self._set_state(FileState.HAS_METADATA)
            else:
                logging.debug(f"Found no metadata for {self.filename}.")
                self._set_state(FileState.HAS_NO_METADATA)

    def remove_metadata(self, lightweight_mode=False) -> None:
        """Remove the metadata from the file.

        Args:
            lightweight_mode (bool, optional): Use mat2 lightweight mode to
                preserve data integrity. Defaults to False.
        """
        if self.state not in [
            FileState.HAS_METADATA,
            FileState.HAS_NO_METADATA
        ]:
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
        """Save the cleaned file."""
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
        """Remove the file from the application."""
        GLib.idle_add(self.emit, "removed")

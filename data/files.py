"""Atomic report writes: readers see either the old file or the complete new one."""

import json
import os
from pathlib import Path
from tempfile import NamedTemporaryFile
from threading import Lock
from time import sleep

# Reports are infrequent; one process-wide lock avoids competing Windows renames.
_WRITE_LOCK = Lock()


def write_text(path, text):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with _WRITE_LOCK:
        temporary = None
        try:
            with NamedTemporaryFile(
                mode="w", encoding="utf-8", dir=path.parent, delete=False
            ) as file:
                temporary = Path(file.name)
                file.write(text)
            for attempt in range(8):
                try:
                    os.replace(temporary, path)
                    break
                except OSError as error:
                    # Windows readers/scanners may briefly deny deletion/rename.
                    # Do not retry unrelated errors or hide permanent denials.
                    if getattr(error, "winerror", None) not in {5, 32, 33} or attempt == 7:
                        raise
                    sleep(0.01 * 2**attempt)
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)


def write_json(path, value):
    write_text(path, json.dumps(value, indent=2, allow_nan=False))

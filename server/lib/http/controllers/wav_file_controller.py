import os
from os import path
from typing import List
from typing import Optional
from typing import Tuple
import uuid
import wave

from lib.common import config
from lib.db.models.wav_file import WavFile


def get_samples() -> List[WavFile]:
    """
    Retrieves all of the WavFiles from the database.
    """
    # TODO: Split out into pagination, so that the query executes quickly even
    #       when we have many samples.
    return list(WavFile.select().execute())


def get_sample(id: str) -> Optional[Tuple[WavFile, bytes]]:
    """
    Retrieves a WavFile from the database. Uses the data contained therein to
    load a .wav file from the filesystem and return it as a string of bytes.
    """
    try:
        wav_file = WavFile.get_by_id(id)
    except WavFile.DoesNotExist:
        return None

    with open(wav_file.path, "rb") as f:
        data = f.read()

    return (wav_file, data)


def post_sample(name: str, data: bytes) -> WavFile:
    """
    Inserts a new WavFile into the database. Returns the corresponding WavFile
    that is constructed.
    """
    id = uuid.uuid4().hex
    path = _generate_path(id)

    with open(path, "wb") as f:
        f.write(data)

    wav_file = WavFile.create(id=id, path=path, name=name)

    return wav_file


def _generate_path(id: str) -> str:
    """
    Generates the path to a given .wav file. Uses the global configuration for
    the resource directory and the wav file subdirectory.

    Each individual file will be titled by its id in the database.
    """
    return path.join(config.RES_FILE_ROOT, config.WAV_FILE_ROOT, id + ".wav")

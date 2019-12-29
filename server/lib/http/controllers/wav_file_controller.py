from os import path
from typing import Optional
from typing import Tuple
import uuid
import wave

from lib.common import config
from lib.db.models.wav_file import WavFile


def post_wav_file(name: str, data: bytes) -> WavFile:
    """
    Inserts a new WavFile into the database. Returns the corresponding WavFile
    that is constructed.
    """
    id = uuid.uuid4().hex
    path = _generate_path(id)

    with open(path, "wb") as f:
        f.write(data)

    wav_file = WavFile(id=id, path=path, name=name)
    wav_file.save()

    return wav_file


def get_wav_file(id: str) -> Optional[Tuple[WavFile, bytes]]:
    """
    Retrieves a WavFile from the database. Uses the data contained therein to
    load a .wav file from the filesystem and return it as a string of bytes.
    """
    try:
        wav_file = WavFile.get_by_id(str)
    except WavFile.DoesNotExist:
        return None

    with open(wav_file.path, "rb") as f:
        data = f.read()

    return (wav_file, data)


def _generate_path(id: str) -> str:
    """
    Generates the path to a given .wav file. Uses the global configuration for
    the resource directory and the wav file subdirectory.

    Each individual file will be titled by its id in the database.
    """
    return path.join(config.RES_FILE_ROOT, config.WAV_FILE_ROOT, id, ".wav")

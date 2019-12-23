from enum import Enum
from peewee import CharField
from peewee import FloatField
from peewee import ForeignKeyField
from peewee import IntegerField

from lib.db import BaseModel
from lib.db.models.wav_file import WavFile
from lib.synth.notes import notes


class SynthButtonMode(Enum):
    Tone = "tone"
    Wav = "wav"


class SynthButtonSetting(BaseModel):
    index = IntegerField(primary_key=True)
    mode = CharField()

    linger_time = FloatField()

    # Tone-specific fields
    frequency = FloatField(null=True)
    overtones = IntegerField(null=True)

    # Wav-specific fields
    wav_id = ForeignKeyField(model=WavFile, null=True)

    @staticmethod
    def from_index(index: int) -> "SynthButtonSetting":
        """
        Produces a new, unpopulated SynthButtonSetting. Used for when the
        server is just started on a fresh system.

        Defaults to a tone generator button.

        Progresses from A3 at index 0 to A5 at index 16.
        """
        index_map = [
            "A3",
            "B3",
            "C4",
            "D4",
            "E4",
            "F4",
            "G4",
            "A4",
            "B4",
            "C5",
            "D5",
            "E5",
            "F5",
            "G5",
            "A5",
        ]

        return SynthButtonSetting(
            index=index,
            mode=SynthButtonMode.Tone.value,
            linger_time=0.25,
            frequency=notes[index_map[index]],
            overtones=4,
        )

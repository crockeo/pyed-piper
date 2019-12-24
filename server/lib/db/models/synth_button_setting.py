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

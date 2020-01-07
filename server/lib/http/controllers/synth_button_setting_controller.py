from playhouse.shortcuts import update_model_from_dict
from typing import Dict
from typing import List
from typing import Optional

from lib.common import config
from lib.common.adapters import synth_button_setting_to_base_driver
from lib.db.models.synth_button_setting import SynthButtonMode
from lib.db.models.synth_button_setting import SynthButtonSetting
from lib.db.models.wav_file import WavFile
from lib.synth import AudioManager
from lib.synth.driver import BaseDriver
from lib.synth.driver.lingering_driver import LingeringDriver
from lib.synth.driver.over_tone_driver import OverToneDriver
from lib.synth.driver.wave_driver import WaveDriver
from lib.synth.notes import notes


def get_synth_button_count() -> int:
    """
    Currently we only have 16 synth buttons.
    """
    return 16


def get_synth_button_settings() -> Optional[List[SynthButtonSetting]]:
    """
    Retrieves all SynthButtonSettings from the database. Note that this call
    corresponds to calling a sequence of get_synth_button_setting, so that we
    can construct each SynthButtonSetting if it does not yet exist.
    """
    buttons = []
    for i in range(get_synth_button_count()):
        buttons.append(get_synth_button_setting(i))
    return buttons


def get_synth_button_setting(index: int) -> Optional[SynthButtonSetting]:
    """
    Retrieves a SynthButtonSetting from the database. If no SynthButtonSetting
    exists, we construct one. This allows the HTTP API to serve a button index
    as though it always exists.
    """
    if index < 0 or index >= get_synth_button_count():
        return None

    try:
        setting = SynthButtonSetting.get_by_id(index)
    except SynthButtonSetting.DoesNotExist:
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
            "B5",
        ]

        setting = SynthButtonSetting.create(
            index=index,
            mode=SynthButtonMode.Tone.value,
            linger_time=0.25,
            frequency=notes[index_map[index]],
            overtones=4,
        )

    return setting


def put_synth_button_setting(
    index: int, new_fields: Dict, audio_manager: AudioManager,
) -> Optional[SynthButtonSetting]:
    """
    Updates a SynthButtonSetting. Checks that certain invariants hold on the
    updates being requested. Namely:

    - On mode change, ensure the following:
      - If mode -> tone: frequency and overtones must exist
      - If mode -> wav:  wav_id must exist, and there must exist a real wav at
        that ID
    """
    # TODO: Clean this whole thing up
    if (
        new_fields.get("mode") == SynthButtonMode.Tone.value
        and ("frequency" not in new_fields or "overtones" not in new_fields)
    ) or (
        new_fields.get("mode") == SynthButtonMode.Wav.value
        and ("wav_id" not in new_fields)
    ):
        return None

    if (
        new_fields.get("mode") == SynthButtonMode.Wav.value
        and "wav_id" in new_fields
        and len(WavFile.select().where(WavFile.id == new_fields["wav_id"])) == 0
    ):
        return None

    setting = get_synth_button_setting(index)
    if setting is None:
        return None

    update_model_from_dict(setting, new_fields)
    setting.save()

    audio_manager.set_driver(
        index, synth_button_setting_to_base_driver(config.SAMPLE_RATE, setting),
    )

    return setting

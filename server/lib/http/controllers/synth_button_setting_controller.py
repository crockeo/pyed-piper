from typing import Dict
from typing import Optional

from lib.db.models.synth_button_setting import SynthButtonMode
from lib.db.models.synth_button_setting import SynthButtonSetting
from lib.synth.notes import notes


def get_synth_button_count() -> int:
    """
    Currently we only have 16 synth buttons.
    """
    return 16


def get_synth_button_setting(index: int) -> Optional[SynthButtonSetting]:
    """
    Retrieves a SynthButtonSetting from the database. If no SynthButtonSetting
    exists, we construct one. This allows the HTTP API to serve a button index
    as though it always exists.
    """
    if index < 0 or index >= get_synth_button_count():
        return None

    # TODO: Something about SynthButtonSetting.get()?
    query = SynthButtonSetting.select().where(SynthButtonSetting.index == index)
    if len(query) == 0:
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

        setting = SynthButtonSetting.create(
            index=index,
            mode=SynthButtonMode.Tone,
            linger_time=0.25,
            frequency=notes[index_map[index]],
            overtones=4,
        )
    else:
        setting = query[0]

    return setting


def put_synth_button_setting(
    index: int, new_fields: Dict
) -> Optional[SynthButtonSetting]:
    """
    Updates a SynthButtonSetting.
    """
    if get_synth_button_setting(index) is None:
        return None

    # TODO: Check internal consistency before allowing update:
    #   - Tone mode = all tone fields defined, no wav fields defined
    #   - Wav mode = all wav fields defined, no tone fields defined
    SynthButtonSetting.update(**new_fields).where(
        SynthButtonSetting.index == index
    ).execute()

    return get_synth_button_setting(index)

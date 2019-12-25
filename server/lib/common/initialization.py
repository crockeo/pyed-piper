from typing import List

from lib.common.adapters import synth_button_setting_to_base_driver
from lib.db.models.synth_button_setting import SynthButtonSetting
from lib.http.controllers.synth_button_setting_controller import (
    get_synth_button_count,
    get_synth_button_setting,
)
from lib.synth.driver import BaseDriver


# TODO: Is it ok to depend on HTTP from this file? I was thinking that HTTP
#       should mostly be self-contained. I'm just going to do it for now, but
#       maybe come back and fix this at some point soon.


def load_drivers(sample_rate: float) -> List[BaseDriver]:
    """
    Loads all of the drivers for input keys [0, 15] inclusive. If any of the
    drivers don't exist when they are constructed, they are inserted into the
    database.
    """
    driver_count = get_synth_button_count()
    drivers = []
    for i in range(driver_count):
        drivers.append(
            synth_button_setting_to_base_driver(
                sample_rate, get_synth_button_setting(i),
            ),
        )
    return drivers

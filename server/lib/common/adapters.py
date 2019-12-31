from lib.db.models.synth_button_setting import SynthButtonMode
from lib.db.models.synth_button_setting import SynthButtonSetting
from lib.db.models.wav_file import WavFile
from lib.synth.driver import BaseDriver
from lib.synth.driver.over_tone_driver import OverToneDriver
from lib.synth.driver.lingering_driver import LingeringDriver
from lib.synth.driver.wave_driver import WaveDriver


def synth_button_setting_to_base_driver(
    sample_rate: float, synth_button_setting: SynthButtonSetting,
) -> BaseDriver:
    """
    Constructs the corresponding BaseDriver from a SynthButtonSetting. The
    mode in SynthButtonSetting determines the kind of BaseDriver. Each base
    driver is wrapped in a LingeringDriver, whose lingering time is determined
    by the SynthButtonSetting

        - Tone = OverToneDriver
        - Wav  = WaveDriver
    """
    if synth_button_setting.mode == SynthButtonMode.Tone.value:
        base_driver = _construct_over_tone_driver(sample_rate, synth_button_setting)
    elif synth_button_setting.mode == SynthButtonMode.Wav.value:
        base_driver = _construct_wave_driver(sample_rate, synth_button_setting)
    else:
        raise NotImplementedError(
            "synth_button_setting_to_base_driver not implemented for mode '{}'".format(
                synth_button_setting.mode
            )
        )

    return LingeringDriver(sample_rate, synth_button_setting.linger_time, base_driver)


def _construct_over_tone_driver(
    sample_rate: float, synth_button_setting: SynthButtonSetting,
) -> OverToneDriver:
    if synth_button_setting.mode != SynthButtonMode.Tone.value:
        raise ValueError(
            "_construct_over_tone_driver only defined on SynthButtonMode.Tone"
        )

    return OverToneDriver(
        sample_rate,
        synth_button_setting.frequency,
        1.0,  # TODO: Allow people to configure loudness driver-by-driver?
        synth_button_setting.overtones,
    )


def _construct_wave_driver(
    sample_rate: float, synth_button_setting: SynthButtonSetting,
) -> WaveDriver:
    if synth_button_setting.mode != SynthButtonMode.Wav.value:
        raise ValueError("_construct_wave_driver only defined on SynthButtonMode.Wav")

    return WaveDriver(sample_rate, synth_button_setting.wav_id.path)

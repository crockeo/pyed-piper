import keyboard

from lib.synth.input import BaseInput
from lib.synth.input import InputAction


class KeyboardInput:
    KEYBOARD_BUTTONS = [
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "q",
        "w",
        "e",
        "r",
        "t",
        "y",
        "u",
        "i",
    ]

    def __init__(self):
        self.button_states = {}

    def get_button_count(self) -> int:
        return 16

    def is_pressed(self, button: int) -> bool:
        key = self.KEYBOARD_BUTTONS[button]
        pressed = keyboard.is_pressed(key)
        self.button_states[key] = pressed
        return pressed

    def just_actioned(self, button: int) -> InputAction:
        key = self.KEYBOARD_BUTTONS[button]

        previously_pressed = self.button_states.get(key, False)
        currently_pressed = self.is_pressed(button)

        if currently_pressed and not previously_pressed:
            return InputAction.Pressed
        if not currently_pressed and previously_pressed:
            return InputAction.Released
        return InputAction.NoAction

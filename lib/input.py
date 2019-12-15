import keyboard
from typing import List


class KeyboardInput:
    def __init__(self):
        self.button_states = {}

    def is_pressed(self, button: str) -> bool:
        """
        Determines whether or not a button is currently pressed.
        """
        pressed = keyboard.is_pressed(button)
        self.button_states[button] = pressed
        return pressed

    def just_actioned(self, button: str) -> str:
        """
        Returns the action that was just performed on the keyboard for the
        given key, if any. Returns one of three things:

          - "pressed", if the key was just pressed
          - "released", if the key was just released
          - "none", otherwise
        """
        previously_pressed = self.button_states.get(button, False)
        currently_pressed = self.is_pressed(button)

        if currently_pressed and not previously_pressed:
            return "pressed"
        elif not currently_pressed and previously_pressed:
            return "released"
        else:
            return "none"

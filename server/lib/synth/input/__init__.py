from enum import Enum


class InputAction(Enum):
    """
    Enumeration of the actions that can occur in an input provider.
    """

    NoAction = "none"
    Pressed = "pressed"
    Released = "released"


class BaseInput:
    def get_button_count(self) -> int:
        raise NotImplementedError(
            "BaseDriver.get_button_count not implemented in {}".format(
                self.__class__.__name__
            )
        )

    def is_pressed(self, button: int) -> bool:
        """
        Determines whether or not a button is currently pressed.
        """
        raise NotImplementedError(
            "BaseDriver.is_pressed not implemented in {}".format(
                self.__class__.__name__
            )
        )

    def just_actioned(self, button: int) -> InputAction:
        """
        Returns the action that was just performed on the input device for the
        given button, if any. Returns an InputAction.
        """
        raise NotImplementedError(
            "BaseDriver.just_actioned not implemented in {}".format(
                self.__class__.__name__
            )
        )

import pytest
from typing import List

from lib import input


@pytest.fixture
def generate_mock_keyboard(mocker):
    """
    Generates a mock for the keyboard package, that allows one to define a list
    of return values for keyboard.is_pressed.

    Each time keyboard.is_pressed is called, it will return the value at the
    current index, and increment the index by 1.

    If called after all values have been exhausted, it will return the last
    returned value.
    """

    class MockKeyboard:
        def __init__(self, is_pressed_values: List[bool]):
            self.is_pressed_values = is_pressed_values
            self.index = 0

        def __call__(self, _: str):
            value = self.is_pressed_values[self.index]
            if self.index < len(self.is_pressed_values) - 1:
                self.index += 1
            return value

    def mock_keyboard(is_pressed_values: List[bool]):
        mk = MockKeyboard(is_pressed_values)
        return mocker.patch(
            "keyboard.is_pressed", side_effect=MockKeyboard(is_pressed_values),
        )

    return mock_keyboard


def test_keyboard_input_is_pressed(generate_mock_keyboard):
    """
    Tests that when a key is pressed, our input model reports that correctly.
    """
    keyboard_is_pressed = generate_mock_keyboard([True])

    keyboard_input = input.KeyboardInput()
    assert True == keyboard_input.is_pressed("")


def test_keyboard_input_is_not_pressed(generate_mock_keyboard):
    """
    Tests that when a key is not pressed, our input model reports that
    correctly.
    """
    generate_mock_keyboard([False])

    keyboard_input = input.KeyboardInput()
    assert False == keyboard_input.is_pressed("")


def test_keyboard_input_just_actioned_pressed(generate_mock_keyboard):
    """
    Tests that when a key has just been pressed, our just_actioned method
    reports that it has been pressed.
    """
    generate_mock_keyboard([False, True])

    keyboard_input = input.KeyboardInput()
    keyboard_input.is_pressed("")
    assert "pressed" == keyboard_input.just_actioned("")


def test_keyboard_input_just_actioned_released(generate_mock_keyboard):
    """
    Tests that when a key has just been released, our just_actioned method
    reports that it has been released.
    """
    generate_mock_keyboard([True, False])

    keyboard_input = input.KeyboardInput()
    keyboard_input.is_pressed("")
    assert "released" == keyboard_input.just_actioned("")


def test_keyboard_input_just_actioned_none(generate_mock_keyboard):
    """
    Tests that when no change occurs, i.e. a key is ether held or not held,
    our just_actioned method reports that no action has occurred.
    """
    generate_mock_keyboard([True, True, False, False])

    keyboard_input = input.KeyboardInput()

    keyboard_input.is_pressed("")
    assert "none" == keyboard_input.just_actioned("")

    keyboard_input.is_pressed("")
    assert "none" == keyboard_input.just_actioned("")

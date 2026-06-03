from pynput import keyboard
from ..instances import Direction

ARROWS = {keyboard.Key.up: Direction.NORTH,
          keyboard.Key.down: Direction.SOUTH,
          keyboard.Key.left: Direction.WEST,
          keyboard.Key.right: Direction.EAST}


class InputController:

    def __init__(self) -> None:
        self.listener = keyboard.Listener(
            on_press=self._on_press,
            suppress=True)
        self.formatted_inputs: dict = {
            'direction': None,
            'switch_fullscreen': False,
            'switch_pause': False}

    def start(self) -> None:
        self.listener.start()

    def stop(self) -> None:
        self.listener.stop()

    def clear_input(self) -> None:
        self.formatted_inputs['direction'] = None
        self.formatted_inputs['switch_fullscreen'] = False
        self.formatted_inputs['switch_pause'] = False

    def _on_press(self, key) -> None:

        if key in ARROWS:
            self.formatted_inputs['direction'] = ARROWS[key]

        elif (key == keyboard.Key.esc
              and not (self.formatted_inputs['switch_pause'])):
            self.formatted_inputs['switch_pause'] = True

        elif (key == keyboard.Key.f11
              and not (self.formatted_inputs['switch_fullscreen'])):
            self.formatted_inputs['switch_fullscreen'] = True

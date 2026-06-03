from pynput.keyboard import Listener, Key, KeyCode
from threading import Lock

from ..instances import Direction

ARROWS = {
    Key.up: Direction.NORTH,
    Key.down: Direction.SOUTH,
    Key.left: Direction.WEST,
    Key.right: Direction.EAST
}

WASD = {
    KeyCode.from_char('w'): Direction.NORTH,
    KeyCode.from_char('s'): Direction.SOUTH,
    KeyCode.from_char('a'): Direction.WEST,
    KeyCode.from_char('d'): Direction.EAST,
}


class InputHandler:
    def __init__(self) -> None:
        self._lock = Lock()

        def on_press(key: Key | KeyCode | None) -> None:
            with self._lock:
                if isinstance(key, Key):
                    if key in ARROWS:
                        self.formatted_inputs["direction"] = ARROWS[key]

                    elif key == Key.esc:
                        self.formatted_inputs["switch_pause"] = True

                    elif key == Key.f11:
                        self.formatted_inputs["switch_fullscreen"] = True

                elif isinstance(key, KeyCode) and key in WASD:
                    self.formatted_inputs["direction"] = WASD[key]

        self.listener = Listener(
            on_press=on_press,
            suppress=True
        )

        self.formatted_inputs: dict = {
            "direction": None,
            "switch_fullscreen": False,
            "switch_pause": False
        }

    def start(self) -> None:
        self.listener.start()

    def stop(self) -> None:
        self.listener.stop()

    def _clear_input(self) -> None:
        self.formatted_inputs["direction"] = None
        self.formatted_inputs["switch_fullscreen"] = False
        self.formatted_inputs["switch_pause"] = False

    def get_formatted_inputs(self) -> dict:
        with self._lock:
            to_return = self.formatted_inputs.copy()
            self._clear_input()
        return to_return

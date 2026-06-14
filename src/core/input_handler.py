from pynput.keyboard import Listener, Key, KeyCode
from threading import Lock

from ..state import EventsEnum


ARROWS = {
    Key.up: EventsEnum.UP,
    Key.down: EventsEnum.DOWN,
    Key.left: EventsEnum.LEFT,
    Key.right: EventsEnum.RIGHT
}

WASD = {
    KeyCode.from_char('w'): EventsEnum.UP,
    KeyCode.from_char('s'): EventsEnum.DOWN,
    KeyCode.from_char('a'): EventsEnum.LEFT,
    KeyCode.from_char('d'): EventsEnum.RIGHT
}


class InputHandler:
    def __init__(self) -> None:
        self._lock = Lock()

        def on_press(key: Key | KeyCode | None) -> None:
            with self._lock:
                if isinstance(key, Key):
                    if key in ARROWS:
                        self.formatted_inputs["direction"] = ARROWS[key]

                    elif key == Key.enter:
                        self.formatted_inputs["enter"] = True

                    elif key == Key.esc:
                        self.formatted_inputs["escape"] = True

                    elif key == Key.f11:
                        self.formatted_inputs["fullscreen"] = True

                    elif key == Key.space:
                        self.formatted_inputs["chars"] += " "

                    elif key == Key.backspace:
                        self.formatted_inputs["backspace"] = True

                elif isinstance(key, KeyCode) and key.char is not None:
                    if key in WASD:
                        self.formatted_inputs["direction"] = WASD[key]
                    if key.char.isprintable():
                        self.formatted_inputs["chars"] += key.char

        self.listener = Listener(
            on_press=on_press,
            suppress=False  # TEMP
        )

        self.formatted_inputs: dict = {
            "direction": None,
            "enter": False,
            "escape": False,
            "fullscreen": False,
            "backspace": False,
            "chars": ""
        }
        self.chars: str = ""

    def start(self) -> None:
        self.listener.start()

    def stop(self) -> None:
        self.listener.stop()

    def _clear_input(self) -> None:
        self.formatted_inputs["direction"] = None
        self.formatted_inputs["enter"] = False
        self.formatted_inputs["escape"] = False
        self.formatted_inputs["fullscreen"] = False
        self.formatted_inputs["backspace"] = False
        self.formatted_inputs["chars"] = ""

    def get_formatted_inputs(self) -> list[EventsEnum]:
        to_return = []
        with self._lock:
            if self.formatted_inputs["direction"]:
                to_return.append(self.formatted_inputs["direction"])
            if self.formatted_inputs["enter"]:
                to_return.append(EventsEnum.ENTER)
            if self.formatted_inputs["escape"]:
                to_return.append(EventsEnum.ESCAPE)
            if self.formatted_inputs["fullscreen"]:
                to_return.append(EventsEnum.FULLSCREEN)
            if self.formatted_inputs["backspace"]:
                to_return.append(EventsEnum.BACKSPACE)
            self.chars = self.formatted_inputs["chars"]
            self._clear_input()
        return to_return

import pyray

from ..state import GlobalState, EventsEnum

WORLD_WIDTH = 1280
WORLD_HEIGHT = 720


class WindowHandler:
    def __init__(self):
        self.dimensions = (pyray.get_screen_width(), pyray.get_screen_height())
        self.ratio = self.dimensions[0] / WORLD_WIDTH

    def update(self, globalstate: GlobalState):
        if EventsEnum.FULLSCREEN in globalstate.events:
            pyray.set_window_size(*self.dimensions)
            pyray.toggle_fullscreen()

    def to_screen(self, n: int) -> int:
        return int(n * self.ratio)

    def to_ratio(self, n: int) -> float:
        return n * self.ratio

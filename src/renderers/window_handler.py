import pyray

from ..state import GlobalState, EventsEnum

WORLD_WIDTH = 1280
WORLD_HEIGHT = 720


class WindowHandler:
    def __init__(self) -> None:
        self.windowed = (pyray.get_screen_width(), pyray.get_screen_height())
        self.dimensions = self.windowed
        self.ratio = self.dimensions[0] / WORLD_WIDTH
        self.borderless = False

    def update(self, globalstate: GlobalState) -> None:
        if EventsEnum.FULLSCREEN in globalstate.events:
            pyray.toggle_borderless_windowed()
            self.borderless = not self.borderless
            if self.borderless:
                mon = pyray.get_current_monitor()
                self.dimensions = (pyray.get_monitor_width(mon),
                                   pyray.get_monitor_height(mon))
            else:
                self.dimensions = self.windowed
            self.ratio = self.dimensions[0] / WORLD_WIDTH

    def to_screen(self, n: int) -> int:
        return int(n * self.ratio)

    def to_ratio(self, n: int) -> float:
        return n * self.ratio

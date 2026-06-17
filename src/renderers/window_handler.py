import pyray

from ..state import GlobalState, EventsEnum

WORLD_WIDTH = 1280
WORLD_HEIGHT = 720


class WindowHandler:
    """
    Tracks the window size and converts world units to screen pixels.

    Maintains the scale ratio between the fixed world dimensions and the
    actual window, and toggles borderless fullscreen on request.
    """

    def __init__(self) -> None:
        """
        Capture the initial window size and compute the scale ratio.
        """
        self.windowed = (pyray.get_screen_width(), pyray.get_screen_height())
        self.dimensions = self.windowed
        self.ratio = self.dimensions[0] / WORLD_WIDTH
        self.borderless = False

    def update(self, globalstate: GlobalState) -> None:
        """
        Toggle fullscreen and refresh the scale ratio when requested.

        Args:
            globalstate: The shared mutable game state (read for the
                fullscreen event).
        """
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
        """
        Scale a world-space length to integer screen pixels.

        Args:
            n: A length in world units.

        Returns:
            The length scaled to screen pixels, rounded to an int.
        """
        return int(n * self.ratio)

    def to_ratio(self, n: int) -> float:
        """
        Scale a world-space length to screen pixels without rounding.

        Args:
            n: A length in world units.

        Returns:
            The length scaled to screen pixels as a float.
        """
        return n * self.ratio

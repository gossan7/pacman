class Gum:
    """
    A regular pacgum that awards points when eaten.
    """

    def __init__(self, value: int) -> None:
        """
        Create a gum.

        Args:
            value: Points awarded when this gum is eaten.
        """
        self.value: int = value


class SuperGum(Gum):
    """
    A super-pacgum that, on top of points, frightens the ghosts.
    """

    def __init__(self, value: int) -> None:
        """
        Create a super-gum.

        Args:
            value: Points awarded when this super-gum is eaten.
        """
        super().__init__(value)

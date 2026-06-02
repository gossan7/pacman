class Gum:
    def __init__(self, value: int) -> None:
        self.value: int = value


class SuperGum(Gum):
    def __init__(self, value: int) -> None:
        super().__init__(value)

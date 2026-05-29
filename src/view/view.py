from typing import Dict
from abc import ABC, abstractmethod


class View(ABC):
    def __init__(self, config: Dict):
        pass

    @abstractmethod
    def update(self):
        pass

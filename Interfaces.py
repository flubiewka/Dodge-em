from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Game import Game


class IInputProvider(ABC):
    @abstractmethod
    def poll_events(self) -> str:
        pass

    @abstractmethod
    def get_actions(self) -> tuple[dict[str, bool], dict[str, bool]]:
        pass


class IRenderer(ABC):
    @abstractmethod
    def setup(self, game: "Game") -> None:
        pass

    @abstractmethod
    def render(self, game: "Game") -> None:
        pass

    @abstractmethod
    def tick(self) -> float:
        pass

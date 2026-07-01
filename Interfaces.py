from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Game import Game


class IInputProvider(ABC):
    @abstractmethod
    def poll_events(self) -> str:
        pass  # returns "quit"/"reset"/"continue"

    @abstractmethod
    def get_actions(self) -> tuple[dict[str, bool], dict[str, bool]]:
        pass  # per-player inputs


class IRenderer(ABC):
    @abstractmethod
    def setup(self, game: "Game") -> None:
        pass  # init resources

    @abstractmethod
    def render(self, game: "Game") -> None:
        pass  # draw frame

    @abstractmethod
    def tick(self) -> float:
        pass  # frame delta time

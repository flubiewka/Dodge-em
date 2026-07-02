from abc import ABC, abstractmethod


class IInputProvider(ABC):
    @abstractmethod
    def poll_events(self) -> str:
        pass  # quit/reset/continue

    @abstractmethod
    def get_actions(self) -> tuple[dict[str, bool], dict[str, bool]]:
        pass  # inputs


class IRenderer(ABC):
    @abstractmethod
    def setup(self, game) -> None:
        pass  # init resources

    @abstractmethod
    def render(self, game) -> None:
        pass  # draw frame

    @abstractmethod
    def tick(self) -> float:
        pass  # dt

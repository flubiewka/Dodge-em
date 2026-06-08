from typing import Any, Protocol


class Renderer(Protocol):
    """
    Контракт для любого рендерера.
    Реализуй этот интерфейс — и игра заработает без единого изменения.
    """

    def setup(self, game: Any) -> None:
        """Вызывается один раз перед стартом. Рендерер знакомится с игрой."""
        ...

    def poll_events(self) -> str:
        """Возвращает 'quit' | 'reset' | 'continue'."""
        ...

    def get_actions(self) -> dict:
        """Возвращает {'forward', 'brake', 'left', 'right', 'nitro'} → bool."""
        ...

    def render(self, game: Any) -> None:
        """Рисует текущее состояние игры."""
        ...

    def tick(self) -> float:
        """Ограничивает FPS, возвращает delta time в секундах."""
        ...

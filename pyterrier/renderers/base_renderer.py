from typing import Any


class BaseRenderer:

    def __init__(self) -> None:
        pass

    def render(self, template_name: str, context: Any) -> str:
        pass

from typing import Any


class BaseTemplateRenderer:

    def __init__(self) -> None:
        pass

    def render(self, template_name: str, context: Any) -> str:
        pass

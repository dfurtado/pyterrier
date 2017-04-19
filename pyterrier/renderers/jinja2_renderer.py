from jinja2 import Environment
from jinja2 import FileSystemLoader
from typing import List
from typing import Optional
from typing import Any

from .base_renderer import BaseRenderer


class Jinja2Renderer(BaseRenderer):
    """ The framework's default renderer """

    def __init__(self,
                 template_dir: str,
                 extensions: Optional[List[str]] = []) -> None:
        """
        Create a new template renderer. By default PyTerrier
        is using Jinja2
        """

        self._loader = FileSystemLoader(template_dir)
        self._env = Environment(loader=self._loader, extensions=extensions)

    def render(self, template_name: str, context: Any) -> str:
        """ Get and return the rendered template """

        template = self._env.get_template(template_name)
        return template.render(context)

import django
from django.template.loader import get_template
from django.conf import settings
from typing import Optional
from typing import Any

from .base_renderer import BaseRenderer


class DjangoRenderer(BaseRenderer):
    """Renderer for django templates"""

    def __init__(self,
                 template_dir: str,
                 extension: Optional[str] = 'django.template.backends.django.DjangoTemplates') -> None:
        """
        Create a new django template renderer.
        """

        settings.cofigure(TEMPLATES=[{
            'BACKEND': extension,
            'DIRS': [template_dir]
        }])

        django.setup()

    def render(self, template_name: str, context: Any) -> str:
        """ Get and return the rendered template """

        template = get_template(template_name)
        return template.render(context)

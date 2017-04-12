from typing import Any


class ViewResult:
    """
    Class represents a view result.
    It wraps the template and the data context and later
    uses it to compile a view using the default template
    engine.
    """

    def __init__(self, template: str, context: Any = {}) -> None:
        """
        Constructor

        :Parameters:
        - `template`: the template that will be used to render the view.
        - `context`: the object to be used as the view context.

        ..Note:: the framework's default template engine is Jinja2, this can
        be changed at the application start.
        """
        self._template = template
        self._context = context

    @property
    def template(self) -> str:
        return self._template

    @property
    def context(self) -> Any:
        return self._context

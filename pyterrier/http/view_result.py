
class ViewResult:
    """
    Class represents a view result.
    It wraps the template and the data context and later
    uses it to compile a view using the default template
    engine.
    """

    def __init__(self, template, context):
        self._template = template
        self._context = context


    @property
    def template(self):
        return self._template


    @property
    def context(self):
        return self._context

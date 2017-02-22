
class HtmlResult():
    """
    Class representing a action response.
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

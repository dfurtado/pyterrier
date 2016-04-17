from jinja2 import Environment, FileSystemLoader

class Jinja2TemplateRenderer:


    def __init__(self, template_dir):
        self._loader = FileSystemLoader(template_dir)
        self._env = Environment(loader = self._loader)


    def get_template(self, name):
        template = self._env.get_template(name)
        return template.render()

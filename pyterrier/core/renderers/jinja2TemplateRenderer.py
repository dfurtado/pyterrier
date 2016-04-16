from jinja2 import Environment, FileSystemLoader
import os

class Jinja2TemplateRenderer:


    def __init__(self, template_dir):
        print("PATH: {path}".format(path = os.path.join(os.path.dirname(__file__), 'templates')))
        self._loader = FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates'))
        self._env = Environment(loader = self._loader)


    def get_template(self, name):
        print("renderer : template name {name}".format(name = name))
        template = self._env.get_template(name)
        return template.render()

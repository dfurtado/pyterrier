from jinja2 import Environment, FileSystemLoader
import os

def main():

    
    loader = FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates'))
    env = Environment(loader = loader)
    
    template = env.get_template("index.html")
    
    print(template.render())



if __name__ == '__main__':
    main()

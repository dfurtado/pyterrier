# Pyterrier: The web framework for dog lovers! :dog: :dog: :dog:

Why do we need another framework you may ask? Well, why not? :goberserk:
The python community is blessed with really nice and well designed web frameworks like Django, Flask, Turbo Gears, Pyramid
and other. However, I've been in situations that Django was too overkill and Flask was too simplistic, I wanted something
simple and scalable and that's why I went on the adventure to develop the Pyterrier.

## From where the name come from?

I love dogs, all of them no matter what breed it is. This framework is a tribute to my dog Elsa which is a
miniature Schnauzer.

## Show me some code!!

``` python
from pyterrier.core import PyTerrier

app = PyTerrier(port=3000)

@app.get("/sayhello/to/{name:str}")
def sayhello(name):
    return app.get_template("index.html", { name = name })
```
This code is self-explanatory but anyways it will start a server running on the port 3000 and it will define a
function that will be executed when a GET request to /sayhello/to/{name:str} is made. The `{name:str}` is the
variable part this will be parsed and passed down to the sayhello function.

The sayhello function will return a html using the template index.html and passing a *context* object to that
template.

Let's have a look how the template looks like.

To avoid repeating html code everywhere we have a base HTML file.

``` html
<html>
    <head>
    </head>
    <body>
        <h1>This is the base HTML template</h1>
        {% block content %}
        {% endblock %}
    </body>
</html>
```
Then we have the index.html

``` html
{% extends "base.html" %}

{% block content %}
    Hello, {{name}}!
{% endblock %}

```
The default template engine that PyTerrier uses is Jinja2 and what that will do is when the index.html is requested
Jinja2 sees that the index.html extends base.html so it will read base and replace the *block content* by the
*block content* defined in the index.html bind the context and return it to the client.


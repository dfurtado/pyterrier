# PyTerrier :dog:

This project has started out of my curiosity to understand how web frameworks work under the hood, to study
closely the http module and also the feel that the Python community need to have frameworks written in Python 3, so
we can take advantage of all its neat features.

## From where the name come from?

I love dogs, all of them no matter what breed it is. This framework is a tribute to my dog Elsa who passed away in the Summer 2016.

## Highlight features

- Written in Python 3.6
- Favorite conventions over configuration
- Value simple code
- Flexible
- Provide a clean project structure

## Show me some code!!

PyTerrier favorite conventions over configurations, that mean the project have to follow a certain structure to
work, for instance, a minimum bare bone PyTerrier application would have the following structure:

```bash
app
├── app.py
├── controllers
├── static
└── templates
```

| Item| Description |
|:------|:-------------|
|app (folder)| It's the root of the application, obviously it can be any name you like|
|app.py| This is the application's entry point, there you can initialize the application and register routes|
|controllers (folder)| The `controllers`folder will be the place to file file containing your actions, a bit more of that later|
|static (folder)| The `static`folder is where you can place all the static assets of your application. CSS, JavaScript, Images, Fonts...|
|templates (folder)| This is the folder where Pyterrier will lookup for templates to rendered with the template engine of your choice|


A very simple PyTerrier application would look a bit like this:

``` python
from pyterrier import PyTerrier
from pyterrier.http import ViewResult

app = PyTerrier(port=3000)

@app.get("/sayhello")
def sayhello():
    return ViewResult("index.html", { "message": "Hellooooo!" })
```

This code will start a server running on the port 3000 and it will define a function that will be executed
when a GET request to `/sayhello` is made.

The sayhello function will return a `ViewResult` which will get a template and a context and render it using the
template engine of your choice. By default, PyTerrier uses Jinja2.

Let's have a look how the template looks like.

To avoid repeating HTML code we have a base file.

``` html
<html>
    <head>
    </head>
    <body>
        <h1>My first PyTerrier application</h1>
        {% block content %}
        {% endblock %}
    </body>
</html>
```

Then we have content html called `index.html`

``` html
{% extends "base.html" %}

{% block content %}
    Hello, {{message}}!
{% endblock %}

```

Now let's say we want to pass a parameter in the URL, you achieve that using a parameter placeholder:

``` python
from pyterrier import PyTerrier
from pyterrier.http import ViewResult

app = PyTerrier(port=3000)

@app.get("/sayhello/to/{name:str}")
def sayhello(name):
    return ViewResult("index.html", { "message": f"Hellooooo, {name}!" })
```
When a GET request is made to `/sayhello/to/daniel`, the HTML content containg the message
Hellooooo, daniel! will be returned.

At the moment only `str` and `int` parameter placeholders are supported.

To return a JSON result we can use the class HttpResult:

``` python
from pyterrier import PyTerrier
from pyterrier.http import HttpResult
from http import HTTPStatus

app = PyTerrier(port=3000)

@app.get("/api/user/{id:int}")
def sayhello(id):
    user = user_repository.get(id)

    if user == None:
        return HttpResult({}, HTTPStatus.NOT_FOUND)

    return HttpResult(user)
```

If `HTTPStatus` argument is not specified, `HttpResult` will return a `HTTPStatus.OK` by default.

Now, there are situations that it's not viable to keep all the api endpoints in a single file. By convention
PyTerrier looks for actions registered in files inside the `controllers` folder in the application root.
With that said, we can create a new folder called `controllers` and inside of that folder we can create a file
called `userController.py` with the following contents:

``` python
from pyterrier import PyTerrier
from pyterrier.http import HttpResult, get
from http import HTTPStatus

@get("/get/{id:int}")
def get(id):
    user = user_repository.get(id)

    if user == None:
        return HttpResult({}, HTTPStatus.NOT_FOUND)

    return HttpResult(user)
```

We also need to perform some changes in the application's main file, like so:

``` python
from pyterrier import PyTerrier


app = PyTerrier(port=3000)

def main():
    app.init_routes(prefix_routes=True)
    app.run()


if __name__ == "__main__":
    main()
```

The code is very similar with what we had before but now we are calling the method `init_routes`. This method will lookup
all the files in the `controllers` folder and register all the actions that it founds. Additionally, the argument `prefix_routes`
is set to `True` meaning that it will prefix the route with the controller prefix. For instance, the route that we just registered
in the `userController` file is `/get/{id:int}` with the `prefix_routes` set to `True` it will become `/user/get/{id:int}`.

## Copyright and License

Copyright (c) 2017 [Daniel Furtado](https://twitter.com/the8bitcoder). Code released under [the MIT license](LICENSE.md)

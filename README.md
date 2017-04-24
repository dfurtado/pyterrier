# PyTerrier :dog:

This project has started out of my curiosity to understand how web frameworks work under the hood, to study
closely the http module and also the feel that the Python community need to have frameworks written in Python 3, so
we can take advantage of all its neat features. PyTerrier is highly inspired by frameworks like Flask, Django and Microsoft's Web API.

## Highlight features

- Written in Python 3.6
- Favorite conventions over configuration
- Value simple code
- Flexible
- Provide a clean project structure

## Quick start

The quickest way to get started is to use the PyTerrier CLI

1. Clone the repository.
```shell
$ git clone https://github.com/dfurtado/pyterrier.git
```

2. Create a virtual environment and install the project dependencies:
```
$ cd pyterrier && pip install -r requirements.txt
```

3. Add the directory where you cloned PyTerrier to the PYTHONPATH variable.

**Unix/Linux/MacOSX**
```shell
$ export PYTHONPATH=$PYTHONPATH:<PyTerrier directory>
```

**Windows**
```shell
set PYTHONPATH=%PYTHONPATH%;<PyTerrier directory>
```

4. Now you can call the PyTerrier CLI or import PyTerrier outside the frameworks folder.
To create your first app, you can just do:
```shell
$ python -m pyterrier --newapp firstapp
$ cd firstapp && python app.py
```

By default, the application will run on the port 8000. Just browse to http://localhost:8000

To get a full description of the options available in the CLI you can use the `-h` option:

```text
usage: pyterrier [-h] [-v] [-c] [--newapp NAME] [--newcontroller NAME]

PyTerrier CLI

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -c, --currentdir      specify whether or not scaffold the application on the
                        current directory.
  --newapp NAME         creates a new PyTerrier application
  --newcontroller NAME  creates a new controller
```

## Show me some code!!

PyTerrier favorite conventions over configurations, that means the project have to follow a certain structure to
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
|:file_folder: app| It's the root of the application, obviously it can be any name you like|
|app.py| This is the application's entry point, there you can initialize the application and register routes|
|:file_folder: controllers| The `controllers`folder will be the place to file file containing your actions, a bit more of that later|
|:file_folder: static| The `static`folder is where you can place all the static assets of your application. CSS, JavaScript, Images, Fonts...|
|:file_folder: templates| This is the folder where Pyterrier will lookup for templates to rendered with the template engine of your choice|


A very simple PyTerrier application would look a bit like this:

``` python
from pyterrier import PyTerrier
from pyterrier.http import ViewResult

app = PyTerrier(port=3000)

@app.get('/sayhello')
def sayhello(self):
    return ViewResult('index.html', { 'message': 'Hellooooo!' })
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
One thing to notice here is that every function in `PyTerrier` have a first argument that is `self`. Self is a reference to the
function itself and expose a property called `request` which is (as the name says) information about the request that has been
performed. The `Request` object exposes the request path, the parameters and header values.

Now let's say we want to pass a parameter in the URL, you achieve that using a parameter placeholder:

``` python
from pyterrier import PyTerrier
from pyterrier.http import ViewResult


app = PyTerrier(port=3000)

@app.get("/sayhello/to/{name:str}")
def sayhello(self, name):
    return ViewResult("index.html", { "message": f"Hellooooo, {name}!" })
```
When a GET request is made to `/sayhello/to/daniel`, the HTML content containg the message
Hellooooo, daniel! will be returned.

At the moment only `str` and `int` parameter placeholders are supported.

To return a HTTP/200 response with the results, you can use the
`Ok` function.

``` python
from pyterrier import PyTerrier
from pyterrier.http import Ok, NotFound


app = PyTerrier(port=3000)

@app.get('/api/user/{id:int}')
def get(self, id):
    user = user_repository.get(id)

    if user == None:
        return NotFound()

    return Ok(user)
```

Now, there are situations that it's not viable to keep all the api endpoints in a single file. By convention
PyTerrier looks for actions registered in files inside the `controllers` folder in the application root.
With that said, we can create a new folder called `controllers` and inside of that folder we can create a file
called `userController.py` with the following contents:

``` python
from pyterrier import PyTerrier
from pyterrier.http import Ok, NotFound, get


@get("/get/{id:int}")
def get(self, id):
    user = user_repository.get(id)

    if user == None:
        return NotFound()

    return Ok(user)
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

## Posting data to the server

Performing a POST request is as simple as GET. It is only needed to import the `@post` decorator and
get the request data out of `self.request.params`:

```python
from pyterrier.http import Ok, post


@post("/add")
def add(self):

    id, name, email = self.request.params

    """ Update the user """

    return Ok()

```

## PUT request
```python
from pyterrier.http import Ok, put


@put("/update")
def update(self):

    id, name, email = self.request.params

    """ Update the user """

    return Ok()

```

## Delete request

```python
from pyterrier.http import Ok, delete


@delete("/user/{id:int}/delete")
def delete(self, id):
    deleted = user_repository.delete(id)
    return Ok()

```

## Copyright and License

Copyright (c) 2017 [Daniel Furtado](https://twitter.com/the8bitcoder). Code released under [BSD 3-clause license](LICENSE)

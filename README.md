# Pyterrier is a web framework in python!

Why do we need another framework you may ask? Well, there're many awesome frameworks out there like Django and Flask. 
Django has too much functionality if you want to create a simple application and Flask is too simplistic and it might get
complicated when trying to scale your application.

``` python
from pyterrier.core import PyTerrier

app = PyTerrier(port=3000)

@app.get("/sayhello/to/{name:str}")
def sayhello(name):
    return app.get_template("sayhello.html", { name = name })
```
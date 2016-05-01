from pyterrier.core import PyTerrier

app = PyTerrier(port=3000)

@app.get("/sayhello/to/{name:str}")
def action(name):
    return app.get_template(
            name="index2.html",
            context = { 'name': name })


if __name__ == "__main__":
    app.run()



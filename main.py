from pyterrier.core import PyTerrier

app = PyTerrier(port=3000)

@app.get("/say/{greetings:str}/to/{name:str}")
def action(greetings, name):

    return app.get_template(
            name="index.html",
            context = {"name": name, "greetings": greetings})


@app.page_not_found()
def handle_404():
    return app.get_template(name="404.html")


if __name__ == "__main__":
    app.run()



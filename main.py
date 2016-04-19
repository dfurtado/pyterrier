from pyterrier.core import PyTerrier

app = PyTerrier(port=3000)

@app.get("/say/{name:str}/{id:int}")
def action():
    return app.get_template(
            name="index.html",
            context = {"name": "Daniel"})


@app.get("/say/hello2/{name:str}")
def action2():
    return app.get_template(
            name="page2.html",
            context = {"name": "Daniel" })


@app.page_not_found()
def handle_404():
    return app.get_template(name="404.html")


if __name__ == "__main__":
    app.run()



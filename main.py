from pyterrier.core import PyTerrier

app = PyTerrier(port=3000)

@app.get("/say/hello")
def action():
    return app.get_template(
            name="index.html", 
            context = {"name":"Daniel Furtado"})

@app.page_not_found()
def handle_404():
    return app.get_template(name="404.html")


if __name__ == "__main__":
    app.run()



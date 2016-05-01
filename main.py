from pyterrier.core import PyTerrier

app = PyTerrier(port=3000)

@app.get("/")
def action():
    return app.get_template(name="index.html")


if __name__ == "__main__":
    app.run()



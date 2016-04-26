from pyterrier.core import PyTerrier

app = PyTerrier(port=3000)

@app.get("/api/{username:str}")
def action(username):
    return app.get_template(name="index2.html", context = {"username": username})


if __name__ == "__main__":
    app.run()



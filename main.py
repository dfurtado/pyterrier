from pyterrier.core import PyTerrier

app = PyTerrier(port=3000)

@app.get("/")
def action():
    return app.get_template(name="index2.html")


@app.post('/user/save')
def save_action(formdata):

    _context = {
            "firstname": formdata['firstname'],
            "lastname": formdata['lastname'],
            "email": formdata['email'],
    }

    return app.get_template(name="formresults.html", context = _context)


if __name__ == "__main__":
    app.run()



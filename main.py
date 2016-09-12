from pyterrier.core import PyTerrier

app = PyTerrier(port=3000)

@app.get("/")
def action():
    return app.view_result(name="index2.html")


@app.post('/user/save')
def save_action(formdata):

    _context = {
            "firstname": formdata['firstname'],
            "lastname": formdata['lastname'],
            "email": formdata['email'],
    }

    return app.view_result(name="formresults.html", context = _context)


if __name__ == "__main__":
    app.run()



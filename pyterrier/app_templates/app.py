from pyterrier import PyTerrier
from pyterrier.http import ViewResult

app = PyTerrier()


@app.get('/')
def index(self):
    return ViewResult('index.html', {'message': 'App works!'})

if __name__ == '__main__':
    app.init_routes(prefix_routes=True)
    app.run()

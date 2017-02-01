from pyterrier.core import PyTerrier
from mocks import UserRepository
app = PyTerrier(port=3000)

@app.get("/")
def index():
    repo = UserRepository()
    model = {"users": repo.users}
    return app.view_result(name="index.html", context=model)


if __name__ == "__main__":
    app.run()

        

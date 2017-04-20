from pyterrier.http import get, put, post, delete
from pyterrier.http import Ok, NotFound


@get('/get')
def get(self):
    pass


@post('/add')
def post(self):
    pass


@put('/update')
def put(self):
    pass


@delete('/delete')
def delete(self):
    pass

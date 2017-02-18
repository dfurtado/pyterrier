
def get(route):
    return lambda func: (route, 'GET', func)

def post(route):
    return lambda func: (route, 'POST', func)

def put(route):
    return lambda func: (route, 'PUT', func)

def delete(route):
    return lambda func: (route, 'DELETE', func)


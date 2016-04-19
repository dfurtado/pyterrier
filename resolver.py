import re

def main():

    routes = { 
        "/user/{userid:int}/{command:str}": ("GET", lambda : print("users route")),
        "/product/{productid:str}": ("GET", lambda : print("products route")),
    }

    rule1 = re.compile("\{\w+:int\}")
    rule2 = re.compile("\{\w+:str\}")

    match_rules = {
        "integer_params": (re.compile("\{\w+:int\}"), "(?P<typeid>[0-9]*)"),
        "str_param": (re.compile("\{\w+:str\}"), "(?P<strvalue>\w+)"),
    }

    d = [ rule1.sub("(?P<typeid>[0-9]*)", r) for r in get_routes()]

    print(d)
            
def get_routes():
    routes = { 
        "/user/{userid:int}/{command:str}": ("GET", lambda : print("users route")),
        "/product/{productid:str}": ("GET", lambda : print("products route")),
    }
    return routes

if __name__ == "__main__":
    main()

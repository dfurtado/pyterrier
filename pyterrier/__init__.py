from .http import http_result, view_result, Ok, NotFound, NoContent as http
from .pyterrier import PyTerrier

def init(*args, **kawrgs):
  raise NotImplementedError("You have installed pyterrier the web framework, not PyTerrier the information retrieval toolkit - " +
                            "To install the latter, use 'pip install python-terrier'. For more information see " +
                            "https://github.com/terrier-org/pyterrier/wiki/Installation-of-Wrong-Package")

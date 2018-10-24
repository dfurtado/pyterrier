import json
import re
from typing import Any
from typing import Dict


class DefaultJsonEncoder(json.JSONEncoder):
    """
    The framework's default JSON encoder.

    ..Note:: This can be changes at application start.
    """

    def __init__(self, **kwargs) -> None:
        """
        Constructor

        :Parameters:
        - `kwargs`: see json.JSONEncoder in the python's standard library.
        """
        super(DefaultJsonEncoder, self).__init__(**kwargs)

        self._builtin_types = (tuple, set, list, str, int, float, )

        self._regexp = re.compile(r'(\-|\_)')

        self._remove_special_chars = lambda key: self._regexp.sub(' ', key)
        self._to_lower = lambda key: key[0].lower() + key[1:] if key else key

    def to_camelcase(self, obj: Any) -> Dict:
        """
        Helper to convert a python object to JSON and change the properties
        to lowercase camel case format.

        :Parameters:
        - `obj`: the object to be converted to came case.
        """

        camel_case_keys = []

        for key in obj.__dict__.keys():
            clean_key = self._remove_special_chars(key)
            camelcase_key = ''.join(x for x in clean_key.title()
                                    if not x.isspace())
            camel_case_keys.append(self._to_lower(camelcase_key))

        return dict(zip(camel_case_keys, obj.__dict__.values()))

    def default(self, obj: Any):

        if isinstance(obj, self._builtin_types):
            return obj
        """
        elif isinstance(obj, Serializable):
            return self.to_camelcase(obj)
        else:
            return self.__dict__
        """

        return self.to_camelcase(obj)

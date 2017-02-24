import json, re


class DefaultJsonEncoder(json.JSONEncoder):

    def __init__(self, **kwargs):
        super(DefaultJsonEncoder, self).__init__(**kwargs)

        self._builtin_types = (
                tuple,
                set,
                list,
                str,
                int,
                float,)

        self._regexp = re.compile("(\-|\_)")

        self._remove_special_chars = lambda key: self._regexp.sub(" ", key)
        self._to_lower = lambda key:  key[0].lower() + key[1:] if key else key


    def to_camelcase(self, obj):

        camel_case_keys = []

        for key in obj.__dict__.keys():
            clean_key = self._remove_special_chars(key)
            camelcase_key = "".join(x for x in clean_key.title() if not x.isspace())
            camel_case_keys.append(self._to_lower(camelcase_key))

        return dict(zip(camel_case_keys, obj.__dict__.values()))


    def default(self, obj):

        if isinstance(obj, self._builtin_types):
            return obj
        elif isinstance(obj, Serializable):
            return self.to_camelcase(obj)
        else:
            return self.__dict__

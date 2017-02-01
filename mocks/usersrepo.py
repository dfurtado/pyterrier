import uuid

class User():

    def __init__(self, name, email):
        self._name = name
        self._email = email

    @property
    def name(self):
        return self._name

    @property
    def email(self):
        return self._email
        
    def __str__(self):
        return "{0} ({1})".format(self._name, self._email)
    

class UserRepository():

    def __init__(self):
        self._users = []
        for x in range(0, 100):
            name = str(uuid.uuid1())
            email = "{0}@{1}".format(str(uuid.uuid1()), "gmail.com")
            self._users.append(User(name, email))
                               
    @property
    def users(self):
        return self._users;

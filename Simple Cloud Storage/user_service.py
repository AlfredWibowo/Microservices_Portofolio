from nameko.rpc import rpc
from unicodedata import name
from dependencies import user


class UserService:
    name  = "user_service"

    database = user.Database()

    @rpc
    def register(self, username, password):
        return self.database.register(username, password)
    
    @rpc
    def login(self, username, password):
        return self.database.login(username, password)
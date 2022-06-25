from nameko.rpc import rpc
from dependencies import Database

class UserService:
    name = "user_service"

    database = Database()

    @rpc
    def register(self, username, password):
        return self.database.register(username, password)
    @rpc
    def login(self, username, password):
        return self.database.login(username, password)
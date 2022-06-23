from nameko.rpc import rpc
from dependencies.news import Database

class NewsService:
    name = "news_service"

    database = Database()

    @rpc
    def register(self, username, password):
        return self.database.register(username, password)

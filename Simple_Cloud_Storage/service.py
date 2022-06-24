from nameko.rpc import rpc
from dependencies import Database

class SimpleCloudStorageService:
    name = "storage_service"

    database = Database()

    @rpc
    def register(self, username, password):
        return self.database.register(username, password)
    @rpc
    def login(self, username, password):
        return self.database.login(username, password)

    @rpc
    def upload_file(self):
        return self.database.upload_file()
    
    @rpc
    def download_file(self):
        return self.database.download_file()
    
    @rpc
    def share_file(self):
        return self.database.share_file()

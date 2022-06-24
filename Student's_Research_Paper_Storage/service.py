from nameko.rpc import rpc
from dependencies import Database

class StudentResearchPaperStorageService:
    name = "storage_service"

    database = Database()

    @rpc
    def register(self, username, password):
        return self.database.register(username, password)
    @rpc
    def login(self, username, password):
        return self.database.login(username, password)

    @rpc
    def upload_paper(self):
        return self.database.upload_file()
    
    @rpc
    def download_paper(self):
        return self.database.download_file()
    
    @rpc
    def search(self):
        return self.database.share_file()

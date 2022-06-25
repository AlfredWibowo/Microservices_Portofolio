from django.dispatch import receiver
from nameko.rpc import rpc
from dependencies import Database

class StorageService:
    name = "storage_service"

    database = Database()
    
    @rpc
    def upload_file(self, uploader, file_name):
        return self.database.upload_file(uploader, file_name)
    
    @rpc
    def download_file(self, downloader, file_name):
        return self.database.download_file(downloader, file_name)
    
    @rpc
    def share_file(self, share_to, file_name):
        return self.database.share_file(share_to, file_name)

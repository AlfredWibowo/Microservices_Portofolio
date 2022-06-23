from nameko.rpc import rpc
from unicodedata import name
from dependencies import user

class StorageService:
    name = "storage_service"

    database = user.Database()

    




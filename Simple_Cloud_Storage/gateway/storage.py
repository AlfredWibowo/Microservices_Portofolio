import json
from nameko.web.handlers import http
from requests import session
import requests
from werkzeug.wrappers import Response
from nameko.rpc import RpcProxy

class StorageGatewayService:
    name = "storage_gateway"

    storage_rpc = RpcProxy('storage_service')

    @http('POST', '/storage/upload/')
    def upload_file(self, request):
        cookies = request.cookies
        
        responses = {
            'status': None,
            'message': None,
        }

        if cookies:
            username = cookies['USERNAME']
            file_name = ""

            result = self.storage_rpc.upload_file(username, file_name)
            
            if result != None:
                responses['status'] = "Success"
                responses['message'] = "File Uploaded"
                responses['data'] = json.dumps(result)
            else:
                responses['status'] = "Error"
                responses['message'] = "File Duplicate"
            
        else:
            responses['status'] = "Error"
            responses['message'] = "You Need to Login First"

        return Response(json.dumps(responses))
            
    @http('POST', '/storage/download/')
    def download_file(self, request):
        cookies = request.cookies
        
        responses = {
            'status': None,
            'message': None,
        }

        if cookies:
            username = cookies['USERNAME']
            file_name = ""
            
            data = format(request.get_data(as_text=True))
            element = requests.utils.unquote(data)
            node = element.split('=')
            file_name = node[1]

            result = self.storage_rpc.download_file(username, file_name)

            if result != None:
                #have access
                responses['status'] = "Success"
                responses['message'] = "File Downloaded"
                responses['data'] = result
                
            else:
                responses['status'] = "Error"
                responses['message'] = "Don't Have Access / File Does Not Exsist"
            
        else:
            responses['status'] = "Error"
            responses['message'] = "You Need to Login First"

        return Response(json.dumps(responses))

    @http('POST', '/storage/share/')
    def share_file(self, request):
        cookies = request.cookies
        
        responses = {
            'status': None,
            'message': None,
        }

        if cookies:
            username = cookies['USERNAME']
            file_name = ""
            
            data = format(request.get_data(as_text=True))
            element = requests.utils.unquote(data)
            node = element.split('=')
            file_name = node[1]

            result = self.storage_rpc.share_file(username, file_name)

            if result != None:
                #sharing
                responses['status'] = "Success"
                responses['message'] = "File Shared"
                responses['data'] = json.dumps(result)
            else:
                responses['status'] = "Error"
                responses['message'] = "File Already Shared"
            
        else:
            responses['status'] = "Error"
            responses['message'] = "You Need to Login First"

        return Response(json.dumps(responses))


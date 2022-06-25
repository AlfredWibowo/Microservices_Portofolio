import json
import os
from nameko.web.handlers import http
from requests import session
import requests
from werkzeug.wrappers import Response
from nameko.rpc import RpcProxy
from Session.redis import SessionProvider

class StorageGatewayService:
    name = "storage_gateway"

    session_provider = SessionProvider()
    storage_rpc = RpcProxy('storage_service')
    user_rpc = RpcProxy('user_service')

    @http('POST', '/user/register/')
    def register(self, request):
        data = format(request.get_data(as_text=True))
        elements = data.split("&")

        username = ""
        password = ""

        for element in elements:
            node = element.split("=")
            if (node[0] == "username"):
                username = node[1]
            elif (node[0] == "password"):
                password = node[1]
        
        result = self.user_rpc.register(username, password)

        responses = {
            'status': None,
            'message': None,
        }

        if result != None:
            responses['status'] = "Success"
            responses['message'] = "Register Successful"
            responses['data'] = result
        else:
            responses['status'] = "Error"
            responses['message'] = "Username Already Taken"

        return Response(json.dumps(responses))

    @http('POST', '/user/login/')
    def login(self, request):
        responses = {
            'status': None,
            'message': None,
            }

        cookies = request.cookies
        if cookies:
            responses['status'] = "Error"
            responses['message'] = "You Already Login"
            return Response(json.dumps(responses))
        else:
            data = format(request.get_data(as_text=True))
            elements = data.split("&")

            username = ""
            password = ""

            for element in elements:
                node = element.split('=')
                if (node[0] == "username"):
                    username = node[1]
                elif (node[0] == "password"):
                    password = node[1] 
            
            result = self.user_rpc.login(username, password)

            if result != None:
                responses['status'] = "Success"
                responses['message'] = "Login Successful"
                responses['data'] = result
                
                response = Response(json.dumps(responses))
                session_id = self.session_provider.set_session(responses)
                response.set_cookie('SESS_ID', session_id)
                
                return response
            else:
                responses['status'] = "Error"
                responses['message'] = "Wrong Username & Password"
                return Response(json.dumps(responses))

    @http('GET', '/user/logout/')
    def logout(self, request):
        cookies = request.cookies
        
        responses = {
            'status': None,
            'message': None,
        }

        if cookies:
            responses['status'] = "Success"
            responses['message'] = "Logout Successful"

            response = Response(json.dumps(responses))
            response.delete_cookie('SESS_ID')
            
            return response
        else:
            responses['status'] = "Error"
            responses['message'] = "You Need to Login First"

            return Response(json.dumps(responses))

    @http('GET', '/user/cookie_username/')
    def logout(self, request):
        cookies = request.cookies
        
        responses = {
            'username': None,
        }

        if cookies:
            responses['username'] = cookies['USERNAME']

        return Response(str(responses))

    @http('POST', '/storage/upload/')
    def upload_file(self, request):
        cookies = request.cookies
        
        responses = {
            'status': None,
            'message': None,
        }

        if cookies:
            #create folder storage if not exsist
            username = cookies['USERNAME']
            file_name = ""

            folder = "Storage/"
            if os.path.exists(folder) != True:
                os.makedirs(folder)
            
            #pick file in request (asumsi file 1 file / upload)
            request_file = request.files['file']
            
            #filename contains = username_filename
            file_name = f"{username}_{request_file.filename}"

            result = self.storage_rpc.upload_file(username, file_name)

            if result != None:
                #no duplicate in db then save to folder
                request_file.save(f"{folder}/{file_name}")

                responses['status'] = "Success"
                responses['message'] = "File Uploaded"
                responses['data'] = result
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
                file_path = f"Storage/{result}"


                # responses['status'] = "Success"
                # responses['message'] = "File Downloaded"
                # responses['data'] = result

                return Response(open(f"{file_path}", "rb").read())
                
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
            share_to = ""
            
            data = format(request.get_data(as_text=True))
            elements = data.split("&")

            for element in elements:
                node = element.split('=')
                if (node[0] == "share_to"):
                    username = node[1]
                elif (node[0] == "file_name"):
                    password = node[1] 

            result = self.storage_rpc.share_file(username, share_to, file_name)

            if result == None:
                responses['status'] = "Error"
                responses['message'] = "File Already Shared"
            elif result == 0:
                responses['status'] = "Error"
                responses['message'] = "User Does Not Exist"
            elif result == 1:
                responses['status'] = "Error"
                responses['message'] = "User Does Not Have Access"
            else:
                #sharing
                responses['status'] = "Success"
                responses['message'] = "File Shared"
                responses['data'] = json.dumps(result)
            
        else:
            responses['status'] = "Error"
            responses['message'] = "You Need to Login First"

        return Response(json.dumps(responses))


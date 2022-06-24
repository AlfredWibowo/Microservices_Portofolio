from nameko.web.handlers import http
from requests import session
from werkzeug.wrappers import Response
from nameko.rpc import RpcProxy
from Session.redis import SessionProvider

class StorageGatewayService:
    name = "storage_gateway"

    session_provider = SessionProvider()
    user_rpc = RpcProxy('storage_service')

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

        return Response(str(responses))

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
            return Response(str(responses))
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
                
                response = Response(str(responses))
                session_id = self.session_provider.set_session(responses)
                response.set_cookie('SESS_ID', session_id)
                
                return response
            else:
                responses['status'] = "Error"
                responses['message'] = "Wrong Username & Password"
                return Response(str(responses))

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

            response = Response(str(responses))
            response.delete_cookie('SESS_ID')
            
            return response
        else:
            responses['status'] = "Error"
            responses['message'] = "You Need to Login First"

            return Response(str(responses))

    @http('POST', '/user/upload/')
    def upload_file(self, request):
        cookies = request.cookies
        
        responses = {
            'status': None,
            'message': None,
        }

        if cookies:
            responses['status'] = "Success"
            responses['message'] = "Logout Successful"

            response = Response(str(responses))
            
            return response
        else:
            responses['status'] = "Error"
            responses['message'] = "You Need to Login First"

            return Response(str(responses))

    @http('POST', '/user/download/')
    def download_file(self, request):
        cookies = request.cookies
        
        responses = {
            'status': None,
            'message': None,
        }

        if cookies:
            responses['status'] = "Success"
            responses['message'] = "Logout Successful"

            response = Response(str(responses))
            
            return response
        else:
            responses['status'] = "Error"
            responses['message'] = "You Need to Login First"

            return Response(str(responses))

    @http('POST', '/user/share/')
    def share_file(self, request):
        cookies = request.cookies
        
        responses = {
            'status': None,
            'message': None,
        }

        if cookies:
            responses['status'] = "Success"
            responses['message'] = "Logout Successful"

            response = Response(str(responses))
            
            return response
        else:
            responses['status'] = "Error"
            responses['message'] = "You Need to Login First"

            return Response(str(responses))


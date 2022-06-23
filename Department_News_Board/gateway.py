import json
from nameko.web.handlers import http
from requests import session
from werkzeug.wrappers import Response

from nameko.rpc import RpcProxy

from dependencies.redis import SessionProvider

class GatewayService:
    name = "news_gateway"

    session_provider = SessionProvider()
    user_rpc = RpcProxy('news_service')

    @http('POST', '/user/register/')
    def register(self, request):
        data = request.get_data(as_text=True)
        array = data.split('&')
        username = ''
        password = ''
        for indices in array:
            element = indices.split('=')
            if (element[0] == 'username'):
                username = element[1]
            elif (element[0] == 'password'):
                password = element[1]

        result = self.user_rpc.register(username, password)
        
        responses = {
            'status': None
        }

        if result != None:
            responses['status'] = "Success"
            responses['message'] = "Register Successful"
            responses['data'] = result
        else:
            responses['status'] = "Error"
            responses['message'] = "Register Failed"

        return Response(str(result))
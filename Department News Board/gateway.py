from nameko.web.handlers import http
from requests import session
import requests
from werkzeug.wrappers import Response
from nameko.rpc import RpcProxy
from Session.redis import SessionProvider

class NewsGatewayService:
    name = "news_gateway"

    session_provider = SessionProvider()
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
            responses['message'] = "Register Failed"

        return Response(str(responses))

    @http('POST', '/user/login/')
    def login(self, request):
        cookies = request.cookies
        if cookies:
            return Response('You Already Login')
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

            responses = {
            'status': None,
            'message': None,
            }

            if result != None:
                responses['status'] = "Success"
                responses['message'] = "Login Successful"
                responses['data'] = result
            else:
                responses['status'] = "Error"
                responses['message'] = "User Not Found"

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

    @http('GET', '/news/')
    def get_all_news(self):
        result = self.user_rpc.get_all_news()

        responses = {
            'status': None,
        }

        if result != None:
            responses['status'] = "Success"
            responses['data'] = result
        else:
            responses['status'] = "Error"
            responses['message'] = "News Does Not Exist"

        return Response(str(responses))

    @http('GET', '/news/<int:news_id>/')
    def get_news_by_id(self, news_id):
        result = self.user_rpc.get_news_by_id(news_id)

        responses = {
            'status': None,
        }

        if result != None:
            responses['status'] = "Success"
            responses['data'] = result
        else:
            responses['status'] = "Success"
            responses['message'] = "News Not Found"
        
        return Response(str(responses))

    @http('POST', '/news/add/')
    def add_news(self, request):
        cookies = request.cookies

        responses = {
            'status': None,
            'message': None,
        }

        if cookies:
            data = format(request.get_data(as_text=True))
            element = requests.utils.unquote(data)
            node = element.split('=')
            desc = node[1]

            result = self.user_rpc.add_news(desc)

            if result != None:
                responses['status'] = "Success"
                responses['message'] = "News Added"
                responses['data'] = result
            else:
                responses['status'] = "Error"
                responses['message'] = "Add News Failed"
        else:
            responses['status'] = "Error"
            responses['message'] = "You Need to Login First"
        
        return Response(str(responses))

    @http('PUT', '/news/edit/<int:news_id>/')
    def edit_news(self, request, news_id):
        cookies = request.cookies

        responses = {
            'status': None,
            'message': None,
        }

        if cookies:
            result = self.user_rpc.edit_news(news_id)

            if result != None:
                responses['status'] = "Success"
                responses['message'] = "News Edited"
                responses['data'] = result
            else:
                responses['status'] = "Error"
                responses['message'] = "Edit News Failed"
        else:
            responses['status'] = "Error"
            responses['message'] = "You Need to Login First"
        
        return Response(str(responses))

    @http('DELETE', '/news/delete/<int:news_id>')
    def delete_news(self, request, news_id):
        cookies = request.cookies

        responses = {
            'status': None,
            'message': None,
        }

        if cookies:
            result = self.user_rpc.delete_news(news_id)

            if result != None:
                responses['status'] = "Success"
                responses['message'] = "News Deleted"
                responses['data'] = result
            else:
                responses['status'] = "Error"
                responses['message'] = "Delete News Failed"
        else:
            responses['status'] = "Error"
            responses['message'] = "You Need to Login First"
        
        return Response(str(responses))
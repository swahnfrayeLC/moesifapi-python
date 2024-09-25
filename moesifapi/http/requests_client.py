# -*- coding: utf-8 -*-

"""
    moesifapi.http.requests_client


"""

import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError
from ..configuration import Configuration
from .http_client import HttpClient
from .http_response import HttpResponse
from .http_method_enum import HttpMethodEnum


class CustomHTTPAdapter(HTTPAdapter):
    """Custom adapter to handle connection resets."""

    def send(self, request, **kwargs):
        try:
            # Try sending the request
            return super().send(request, **kwargs)
        except (ConnectionError) as e:
            # Handle connection reset
            self.close()  # Close the pool to reset connections
            # Retry the request once
            try:
                return super().send(request, **kwargs)
            except Exception as e:
                # If it fails again, raise the exception
                raise e

class RequestsClient(HttpClient):

    """An implementation of HttpClient that uses Requests as its HTTP Client
    
    """

    # connection pool here

    def __init__(self):
        self.session = requests.Session()
        self.adapter = HTTPAdapter(pool_connections=Configuration.pool_connections, pool_maxsize=Configuration.pool_maxsize)
        self.session.mount('http://', self.adapter)
        self.session.mount('https://', self.adapter)

    def execute_as_string(self, request):
        """Execute a given HttpRequest to get a string response back
       
        Args:
            request (HttpRequest): The given HttpRequest to execute.
            
        Returns:
            HttpResponse: The response of the HttpRequest.
            
        """	
        auth = None

        if request.username or request.password:
            auth=(request.username, request.password)

        # connection pool to make request
        response = self.session.request(HttpMethodEnum.to_string(request.http_method),
                                        request.query_url,
                                        headers=request.headers,
                                        params=request.query_parameters,
                                        data=request.parameters,
                                        files=request.files,
                                        auth=auth)

        return self.convert_response(response, False)
    
    def execute_as_binary(self, request):
        """Execute a given HttpRequest to get a binary response back
       
        Args:
            request (HttpRequest): The given HttpRequest to execute.
            
        Returns:
            HttpResponse: The response of the HttpRequest.
            
        """
        auth = None

        if request.username or request.password:
            auth=(request.username, request.password)
        
        response = requests.request(HttpMethodEnum.to_string(request.http_method), 
                                    request.query_url, 
                                    headers=request.headers,
                                    params=request.query_parameters, 
                                    data=request.parameters, 
                                    files=request.files,
                                    auth=auth)
                                   
        return self.convert_response(response, True)
    
    def convert_response(self, response, binary):
        """Converts the Response object of the HttpClient into an
        HttpResponse object.
       
        Args:
            response (dynamic): The original response object.
            
        Returns:
            HttpResponse: The converted HttpResponse object.
            
        """
        if binary == True:
            return HttpResponse(response.status_code, response.headers, response.content)
        else:
            return HttpResponse(response.status_code, response.headers, response.text)
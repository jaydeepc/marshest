import requests


class HTTPClientBase:

    def __init__(self):
        super(HTTPClientBase, self).__init__()

    def request(self, method, url, **kwargs):
        try:
            return requests.request(method, url, **kwargs)
        except Exception as e:
            raise e

    def put(self, url, **kwargs):
        """ HTTP PUT request """
        return self.request('PUT', url, **kwargs)

    def copy(self, url, **kwargs):
        """ HTTP COPY request """
        return self.request('COPY', url, **kwargs)

    def post(self, url, data=None, **kwargs):
        """ HTTP POST request """
        return self.request('POST', url, data=data, **kwargs)

    def get(self, url, **kwargs):
        """ HTTP GET request """
        return self.request('GET', url, **kwargs)

    def head(self, url, **kwargs):
        """ HTTP HEAD request """
        return self.request('HEAD', url, **kwargs)

    def delete(self, url, **kwargs):
        """ HTTP DELETE request """
        return self.request('DELETE', url, **kwargs)

    def options(self, url, **kwargs):
        """ HTTP OPTIONS request """
        return self.request('OPTIONS', url, **kwargs)

    def patch(self, url, **kwargs):
        """ HTTP PATCH request """
        return self.request('PATCH', url, **kwargs)


class HTTPClient(HTTPClientBase):

    def __init__(self):
        super(HTTPClient, self).__init__()
        self.default_headers = {}

    def request(
            self, method, url, headers=None, params=None, data=None,
            kwargs=None):

        kwargs = kwargs if (
            kwargs is not None) else {}

        #defaults
        params = params if params is not None else {}
        verify = False

        headers = dict(self.default_headers, **(headers or {}))

        if 'url' in list(kwargs.keys()):
            url = kwargs.get('url', None) or url
            del kwargs['url']

        if 'method' in list(kwargs.keys()):
            method = kwargs.get('method', None) or method
            del kwargs['method']

        for key in list(kwargs.keys()):
            if kwargs[key] is None:
                del kwargs[key]

        kwargs = dict(
            {'headers': headers, 'params': params, 'verify': verify,
             'data': data}, **kwargs)

        # Run request
        return super(HTTPClient, self).request(
            method, url, **kwargs)


class MarshHTTPClient(HTTPClient):

    def __init__(self, format_for_serializing=None, format_for_deserializing=None):
        self.format_for_serializing = format_for_serializing
        self.format_for_deserializing = format_for_deserializing or self.format_for_serializing

    def request(
            self, method, url, headers=None, params=None, data=None,
            response_entity_type=None, request_entity=None,
            kwargs=None):

        kwargs = kwargs if (kwargs is not None) else {}

        if request_entity is not None:
            kwargs = dict(
                {'data': request_entity.serialize(self.format_for_serializing)},
                **kwargs)

        # Run request
        response = super(MarshHTTPClient, self).request(
            method, url, headers=headers, params=params, data=data,
            kwargs=kwargs)

        response.request.__dict__['entity'] = None
        response.__dict__['entity'] = None

        if response.request is not None:
            response.request.__dict__['entity'] = request_entity

        if response_entity_type is not None:
            response.__dict__['entity'] = response_entity_type.deserialize(
                response.content,
                self.format_for_deserializing)

        return response
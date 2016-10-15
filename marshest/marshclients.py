import requests


class RequestClientBase:

    def __init__(self):
        super(RequestClientBase, self).__init__()

    def request(self, method, url, **kwargs):
        try:
            return requests.request(method, url, **kwargs)
        except Exception as e:
            raise e

    def head(self, url, **kwargs):
        return self.request('HEAD', url, **kwargs)

    def put(self, url, **kwargs):
        return self.request('PUT', url, **kwargs)

    def copy(self, url, **kwargs):
        return self.request('COPY', url, **kwargs)

    def patch(self, url, **kwargs):
        return self.request('PATCH', url, **kwargs)

    def post(self, url, data=None, **kwargs):
        return self.request('POST', url, data=data, **kwargs)

    def get(self, url, **kwargs):
        return self.request('GET', url, **kwargs)

    def delete(self, url, **kwargs):
        return self.request('DELETE', url, **kwargs)

    def options(self, url, **kwargs):
        return self.request('OPTIONS', url, **kwargs)


class RequestClient(RequestClientBase):

    def __init__(self):
        super(RequestClient, self).__init__()
        self.default_headers = {}

    def request(
            self, method, url, headers=None, params=None, data=None,
            kwargs=None):

        kwargs = kwargs if (
            kwargs is not None) else {}

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
            {'headers': headers, 'params': params, 'data': data}, **kwargs)

        # Run request
        return super(RequestClient, self).request(
            method, url, **kwargs)


class MarshClient(RequestClient):

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
        response = super(MarshClient, self).request(
            method, url, headers=headers, params=params, data=data,
            kwargs=kwargs)

        response.request.__dict__['object'] = None
        response.__dict__['object'] = None

        if response.request is not None:
            response.request.__dict__['object'] = request_entity

        if response_entity_type is not None:
            response.__dict__['object'] = response_entity_type.deserialize(
                response.content,
                self.format_for_deserializing)

        return response
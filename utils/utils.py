import os
from urllib import parse

def standardize_path(path):
    return os.path.normpath(path).strip("/")

def compare(route, request):
    route_url = parse.urlsplit(route.path)
    route_query_params = dict(parse.parse_qsl(route_url.query))
    request_query_params = dict(parse.parse_qsl(request.url.query))
    without_namespace = "/".join(request.url.path.split("/")[2:])
    return standardize_path(route_url.path) == standardize_path(without_namespace) and route_query_params == request_query_params

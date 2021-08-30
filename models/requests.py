from typing import Dict
from pydantic import BaseModel
from enum import Enum

class StatusCode(Enum):
    OK = 200
    CREATED = 201
    ACCEPTED = 202
    MOVED_PERMANENTLY = 301
    FOUND = 302
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    PAYMENT_REQUIRED = 402
    FORBIDDEN = 404
    METHOD_NOT_ALLOWED = 405
    NOT_ACCEPTABLE = 406

class Verb(Enum):
    GET = "GET"
    PUT = "PUT"
    POST = "POST"
    PATCH = "PATCH"
    DELETE = "DELETE"

class RouteRequest(BaseModel):
    class Config:
        use_enum_values = True

    uuid: str
    path: str
    verb: Verb
    status_code: StatusCode
    namespace_uuid: str
    headers: Dict = {}
    body: Dict = {}

class NamespaceRequest(BaseModel):
    class Config:
        use_enum_values = True

    uuid: str
    route: RouteRequest

from typing import Dict
from pydantic import BaseModel
from enum import Enum

class StatusCode(Enum):
    OK = 200
    FOUND = 302
    UNAUTHORIZED = 401

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

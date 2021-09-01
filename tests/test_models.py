import json
import uuid
from models.base import PynamoCrud
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute
from models.base import Namespace, Route
from utils.utils import compare
from models.requests import StatusCode, Verb, RouteRequest, NamespaceRequest
from urllib import parse

class TestModel(Model, PynamoCrud):
    class Meta:
        table_name = 'dynamodb-route'
        region = 'us-west-1'

    uuid = UnicodeAttribute(null=False)
    email = UnicodeAttribute(null=False)

def test_pynamo():
    test = TestModel(uuid='1234-5678', email='chris@example.com')
    assert test.uuid == '1234-5678'
    assert test.email == 'chris@example.com'

def test_pynamo_crud():
    test = TestModel()
    test.set_attributes({'uuid': '1234-5678', 'email': 'chris@example.com'})
    assert test.uuid == '1234-5678'
    assert test.email == 'chris@example.com'

def test_route_model():
    route = Route()
    request = RouteRequest(
        uuid=str(uuid.uuid4()),
        namespace_uuid=str(uuid.uuid4()),
        path="/users",
        verb=Verb.GET.value,
        status_code=StatusCode.OK.value,
        header={},
        body={}
    )
    route.set_attributes(request.dict())
    assert route.path == "users"
    assert route.verb == Verb.GET.value

def test_route_standarization():
    route = Route()
    expectations = [
        ("users", "users"),
        ("/users", "users"),
        ("/users/hello", "users/hello"),
        ("/users///hello", "users/hello"),
    ]
    for (_input, expected) in expectations:
        request = RouteRequest(
            uuid=str(uuid.uuid4()),
            namespace_uuid=str(uuid.uuid4()),
            path=_input,
            verb=Verb.GET.value,
            status_code=StatusCode.OK.value,
            header={},
            body={}
        )

        route.set_attributes(request.dict())
        assert route.path == expected

def test_namespace_model():
    namespace = Namespace()
    route_request = RouteRequest(
        uuid=str(uuid.uuid4()),
        namespace_uuid=str(uuid.uuid4()),
        path="users",
        verb=Verb.GET.value,
        status_code=StatusCode.OK.value,
        header={},
        body={}
    )
    request = NamespaceRequest(
        uuid="12345",
        route=route_request,
    )
    namespace.set_attributes(request.dict())
    assert namespace.uuid == "12345"



class MockRequest():
    def __init__(self, url):
        self._url = url

    @property
    def url(self):
        return self._url

def test_compare():
    expectations = [
        ("users?hello=world&yes=no", "/users?yes=no&hello=world"),
    ]
    for (_input, expected) in expectations:
        route = Route(path=_input)
        request = MockRequest(parse.urlsplit(expected))
        assert compare(route, request)

def test_curl_command():
    namespace_uuid = '1234'
    route = Route(verb=Verb.POST.value, namespace_uuid=namespace_uuid, path="users?hello=world&yes=no")
    assert route.curl_command == "curl -X POST https://www.mockachino.com/1234/users?hello=world&yes=no"

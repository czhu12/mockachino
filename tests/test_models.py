import json
from models.base import PynamoCrud
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute
from models.base import Namespace, Route
from models.requests import StatusCode, Verb, RouteRequest, NamespaceRequest

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
        path="users",
        verb=Verb.GET.value,
        status_code=StatusCode.OK.value,
        header={},
        body={}
    )
    route.set_attributes(request.dict())
    assert route.path == "users"
    assert route.verb == Verb.GET.value

def test_namespace_model():
    namespace = Namespace()
    route_request = RouteRequest(
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

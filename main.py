import os
import uvicorn
from typing import Dict
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from models.base import Namespace, Route, Credentials, NotFoundException
from models.requests import StatusCode, Verb, RouteRequest, NamespaceRequest
import requests
import json

import random
import uuid
from dotenv import load_dotenv

USEFUL_SPACES = [
    #blogs, social network, films, products
]


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
@app.get("/favicon.ico")
async def favicon(): return FileResponse('./static/favicon.ico')

templates = Jinja2Templates(directory="templates")

@app.post("/api/namespaces")
async def create_namespace(namespace_request: NamespaceRequest):
    namespace = Namespace(uuid=namespace_request.uuid)
    namespace.save()

    route = Route()
    route.set_attributes(namespace_request.route.dict())
    route.save()

    return JSONResponse(content={'redirect': '/spaces/{}'.format(namespace.uuid)})

@app.put("/api/namespaces/{namespace_uuid}/routes/{route_uuid}")
async def update_namespace(namespace_uuid: str, route_uuid: str, route_request: RouteRequest):
    try:
        route = [r for r in Route.query(namespace_uuid, Route.uuid == route_uuid)][0]
        route.set_attributes(route_request.dict())
        route.save()
        return JSONResponse(content={'redirect': '/spaces/{}'.format(namespace_uuid)})
    except (NotFoundException, IndexError):
        return JSONResponse(content={"message": "Route {} not found in {}".format(route_uuid, namespace_uuid)}, status_code=404)


@app.delete("/api/namespaces/{namespace_uuid}/routes/{route_uuid}")
async def delete_namespace(namespace_uuid: str, route_uuid: str):
    try:
        route = [r for r in Route.query(namespace_uuid, Route.uuid == route_uuid)][0]
        route.delete()
        return JSONResponse(content={'redirect': '/spaces/{}'.format(namespace_uuid)})
    except (NotFoundException, IndexError):
        return JSONResponse(content={"message": "Route {} not found in {}".format(route_uuid, namespace_uuid)}, status_code=404)

@app.get("/spaces/{namespace_uuid}")
async def show_namespace(request: Request, namespace_uuid: str):
    try:
        namespace = Namespace.first(namespace_uuid)
        routes = namespace.get_routes()
        new_route = Route(
            uuid=str(uuid.uuid4()),
            path="users",
            namespace_uuid=namespace_uuid,
            headers=json.dumps({"Content-Type": "application/json"}),
            status_code=StatusCode.OK.value,
            verb=Verb.GET.value,
            body=json.dumps({"users": [{"first_name": "Barack", "last_name": "Obama", "date_of_birth": "1961-08-04"}]}),
        )
        return templates.TemplateResponse("namespaces/show.html", {
            "StatusCode": StatusCode,
            "Verb": Verb,
            "request": request,
            "uuid": namespace_uuid,
            "routes": routes,
            "new_route": new_route,
        })
    except (NotFoundException, IndexError):
        return templates.TemplateResponse("namespaces/404.html", {
            "request": request,
        })


@app.get("/")
async def index(request: Request):
    namespace_uuid = str(uuid.uuid4())[:16]
    route = Route(
        uuid=str(uuid.uuid4()),
        path="users",
        namespace_uuid=namespace_uuid,
        headers=json.dumps({"Content-Type": "application/json"}),
        status_code=StatusCode.OK.value,
        verb=Verb.GET.value,
        body=json.dumps({"users": [{"first_name": "Barack", "last_name": "Obama", "date_of_birth": "1961-08-04"}]}),
    )
    return templates.TemplateResponse("index.html", {
        "Verb": Verb,
        "StatusCode": StatusCode,
        "request": request,
        "route": route,
        "uuid": namespace_uuid,
        "useful_spaces": USEFUL_SPACES
    })

@app.get("/{namespace_uuid}/{path:path}")
@app.post("/{namespace_uuid}/{path:path}")
@app.put("/{namespace_uuid}/{path:path}")
@app.patch("/{namespace_uuid}/{path:path}")
@app.delete("/{namespace_uuid}/{path:path}")
async def api(request: Request, namespace_uuid: str, path: str):
    verb = Verb(request.method)
    try:
        namespace = Namespace.first(namespace_uuid)
        route = [r for r in namespace.get_routes() if r.path == path and r.verb == verb.value][0]
        headers = json.loads(route.headers)
        return JSONResponse(content=json.loads(route.body), headers=headers, status_code=route.status_code)
    except (NotFoundException, IndexError):
        return JSONResponse(content={"message": "/{} not found in {}".format(path, namespace_uuid)}, status_code=404)


if __name__ == "__main__":
    load_dotenv()
    Credentials.aws_access_key_id = os.environ.get('AWS_ACCESS_KEY')
    Credentials.aws_secret_access_key = os.environ.get('AWS_SECRET_KEY')
    print(Credentials.aws_secret_access_key)
    print(Credentials.aws_access_key_id)
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT', "8000")))

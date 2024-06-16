import mimetypes
import pathlib

from fastapi import (
    Request,
    FastAPI,
    WebSocket,
    WebSocketDisconnect
)
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import PlainTextResponse

from server.ntpro_server import NTProServer

api = FastAPI()
server = NTProServer()
templates = Jinja2Templates(directory="templates")

api.mount("/static", StaticFiles(directory="static"), name="static")


@api.get('/')
async def get(request: Request):
    return templates.TemplateResponse("test.html", {"request": request})


@api.get('/static/{path}')
async def get(path: pathlib.Path):
    static_file = (pathlib.Path('static') / path).read_text()
    mime_type, encoding = mimetypes.guess_type(path)
    return PlainTextResponse(static_file, media_type=mime_type)


@api.websocket('/ws/')
async def websocket_endpoint(websocket: WebSocket):
    await server.connect(websocket)

    try:
        await server.serve(websocket)
    except WebSocketDisconnect:
        server.disconnect(websocket)

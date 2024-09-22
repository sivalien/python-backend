import re
import urllib.parse

from tasks.task1.handlers import get_factorial, get_fibonacci, get_mean
from tasks.task1.response import Response


async def app(scope, receive, send):
    path = scope['path']
    method = scope['method']

    if method == 'GET' and path == '/factorial':
        response = await get_factorial(urllib.parse.parse_qs(scope['query_string'].decode('utf-8'), send))
    elif method == 'GET' and path == '/fibonacci':
        response = Response( 422, b"Missing required parameter n")
    elif method == 'GET' and re.fullmatch('/fibonacci/([^/]+)', path) is not None:
        response = await get_fibonacci(scope['path'].split('/')[2])
    elif method == 'GET' and path == '/mean':
        body = await get_body(receive)
        response = await get_mean(body.decode('utf-8'))
    else:
        response = Response(404, b"Not found")

    await send_response(send, response)

async def get_body(receive):
    body = b''
    more_body = True
    while more_body:
        message = await receive()
        body += message.get("body", b"")
        more_body = message.get("more_body", False)
    return body

async def send_response(send, response):
    await send({
        'type': 'http.response.start',
        'status': response.status,
        'headers': response.header
    })

    await send({
        'type': 'http.response.body',
        'body': response.body,
    })

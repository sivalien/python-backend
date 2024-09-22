import json
import math
import re
from json import JSONDecodeError

from tasks.task1.response import Response, JSON_HEADER


async def get_factorial(params) -> Response:
    if 'n' not in params:
        return Response(422, b"Missing required parameter n")

    elif not re.fullmatch("-?\d+", params['n'][0]):
        return Response(422, b"Parameter n must be a digit")

    else:
        n = int(params['n'][0])
        if n < 0:
            return Response(400, b"Parameter n must be positive")

        result = math.factorial(n)
        return Response(200, json.dumps({"result": result}).encode("utf-8"), JSON_HEADER)

async def get_fibonacci(param):
    if not re.fullmatch('-?\d+', param):
        return Response(422, b"Parameter n must be a number")

    n = int(param)
    if n < 0:
        return Response(400, b"Parameter n must be positive")

    prev, curr = 0, 1
    for _ in range(n):
        prev, curr = curr, prev + curr

    return Response(200, json.dumps({"result": prev}).encode("utf-8"), JSON_HEADER)

async def get_mean(body):
    try:
        json_body = json.loads(body)
    except JSONDecodeError:
        return Response(422, b"Invalid request body")

    if not isinstance(json_body, list):
        return Response(422, b"Body must contain an array")

    if len(json_body) == 0:
        return Response( 400, b"Body must contain non empty array")

    try:
        data = list(map(float, json_body))
    except ValueError:
        return Response(422, b"Array in request body must contain only floats")

    result = sum(data) / len(data)
    return Response(200, json.dumps({"result": result}).encode("utf-8"), JSON_HEADER)
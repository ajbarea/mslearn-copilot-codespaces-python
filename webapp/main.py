import os
import base64
from typing import Union
from os.path import dirname, abspath, join
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

current_dir = dirname(abspath(__file__))
static_path = join(current_dir, "static")

app = FastAPI()
app.mount("/ui", StaticFiles(directory=static_path), name="ui")


class Body(BaseModel):
    length: Union[int, None] = 20


@app.get('/')
def root():
    """
    Returns the index.html file as a response.
    """
    html_path = join(static_path, "index.html")
    return FileResponse(html_path)


@app.post('/generate')
def generate(body: Body):
    """
    Generate a pseudo-random token ID of twenty characters by default.

    Args:
        body (Body): The request body containing the length of the token.

    Returns:
        dict: A dictionary containing the generated token.

    Example POST request body:
    {
        "length": 20
    }
    """
    string = base64.b64encode(os.urandom(64))[:body.length].decode('utf-8')
    return {'token': string}


class Token(BaseModel):
    token: str


@app.post('/checksum')
def checksum(token: Token):
    """
    Generate a checksum of the token.

    Args:
        token (Token): The request body containing the token.

    Returns:
        dict: A dictionary containing the checksum of the token.

    Example POST request body:
    {
        "token": "<your_token_here>"
    }
    """
    checksum = 0
    for char in token.token:
        checksum += ord(char)
    return {'checksum': checksum}

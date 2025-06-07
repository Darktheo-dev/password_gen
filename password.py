# Author: Kevin Varghese
# Date: April 2, 2025
# Description: A web-based password generator using FastAPI.

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import random
import string
import uvicorn

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def generate_password(length, include_upper, include_digits, include_symbols):
    characters = string.ascii_lowercase  # Always include lowercase

    if include_upper:
        characters += string.ascii_uppercase
    if include_digits:
        characters += string.digits
    if include_symbols:
        characters += string.punctuation

    if not characters:
        return "Please select at least one character type!"

    password = ''.join(random.choice(characters) for _ in range(length))
    return password

@app.get("/", response_class=HTMLResponse)
async def form_get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "password": None})

@app.post("/", response_class=HTMLResponse)
async def form_post(
    request: Request,
    length: int = Form(...),
    include_upper: bool = Form(False),
    include_digits: bool = Form(False),
    include_symbols: bool = Form(False)
):
    password = generate_password(length, include_upper, include_digits, include_symbols)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "password": password
    })

if __name__ == "__main__":
    uvicorn.run("password:app", reload=True)
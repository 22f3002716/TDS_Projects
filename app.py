# To check the evaluation url server is working fine. Created a simple echo server.

from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/")
async def echo(request: Request):
    body = await request.body()
    headers = dict(request.headers)
    return {
        "method": request.method,
        "headers": headers,
        "body": body.decode("utf-8")  # If expecting text input
    }
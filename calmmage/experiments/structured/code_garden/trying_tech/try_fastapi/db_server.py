import json

from fastapi import FastAPI
from fastapi import Request, Response
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

data = {}

origins = [
    "http://localhost",
    "http://localhost:8000"
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/data/{key}")
def read_item(key: str, response: Response):
    if key in data:
        response.body = json.dumps({"key": key, "value": data[key]}).encode()
        # response.content = json.dumps({"key": key, "value": data[key]})
        response.status_code = 200
        return response
    else:
        response.body = json.dumps({"key": key, "value": None}).encode()
        # response.content = json.dumps({"key": key, "value": None})
        response.status_code = 200
        return response


@app.put("/data/{key}")
async def update_item(key: str, request: Request, response: Response):
    body = await request.body()
    value = json.loads(body.decode())["value"]
    data[key] = value
    response_data = {"message": f"Key '{key}' updated successfully", "key": key, "value": value}
    response.body = json.dumps(response_data).encode()
    response.status_code = 200
    return response


@app.put("/data2/{key}")
async def update_item_new(key: str, request: Request):
    value = json.loads((await request.body()).decode())["value"]
    data[key] = value
    return {"message": f"Key '{key}' updated successfully"}


@app.get("/data2/{key}")
def read_item(key: str):
    if key in data:
        return {"value": data[key]}
    else:
        return {"value": None}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)

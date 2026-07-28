from mcp.server.fastmcp import FastMCP
from fastapi import FastAPI, Request

mcp = FastMCP("Test Server", json_response=True)


@mcp.tool()
def add(a: int, b: int):
    return a + b


@mcp.tool()
def sub(a: int, b: int):
    return a - b


@mcp.tool()
def divide(a: int, b: int):
    return a // b


@mcp.tool()
def mul(a: int, b: int):
    return a * b

mcp_app = mcp.streamable_http_app()
app = FastAPI()

@app.middleware("http")
async def log_request(request: Request, call_next):
    print("HOST:", request.headers.get("host"))
    return await call_next(request)

app.mount("/mcp", mcp_app)

@app.get("/")
def root():
    return {"status": "ok"}


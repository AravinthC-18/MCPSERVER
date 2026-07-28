from mcp.server.fastmcp import FastMCP

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

app = mcp.streamable_http_app()

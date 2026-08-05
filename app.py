# In your MCP server (CMRServer.py)
from mcp.server import Server
from mcp.types import Tool, TextContent

server = Server("test_server")


@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="add",
            description="Add two numbers together",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"}
                },
                "required": ["a", "b"]
            }
        ),
        Tool(
            name="ocr",
            description="Extract text from PDF using OCR",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "Path to PDF file"}
                },
                "required": ["file_path"]
            }
        ),
        Tool(
            name="get_ocr_status",
            description="Check OCR status and get results using job ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "job_id": {"type": "string", "description": "Job ID from ocr tool"}
                },
                "required": ["job_id"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "add":
        result = arguments["a"] + arguments["b"]
        return [TextContent(type="text", text=f"Result: {result}")]

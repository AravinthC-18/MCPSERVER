import requests
import json
import logging
import sys
from mcp.server.transport_security import TransportSecuritySettings
logging.basicConfig(stream=sys.stderr, level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    "test_server",
    json_response=True,
    host="0.0.0.0",
    transport_security=TransportSecuritySettings(
        enable_dns_rebinding_protection=True,
        allowed_hosts=["mcpserver-fzg9.onrender.com", "mcpserver-fzg9.onrender.com:*"],
        allowed_origins=["https://mcpserver-fzg9.onrender.com"],
    ),
)
@mcp.tool()
def paddle_ocr(filename: str) -> str:
    file_path=r"C:\Users\kathir.karthikeyan\Desktop\MCP_DEMO\sample.pdf"
    url="http://172.19.101.194:5000/ocr"
    ocr_response = requests.post(
        url=url,
        json={"file_path": file_path},  
        timeout=config.600
    )
    if ocr_response.status_code != 200:
        raise Exception(f"OCR Service returned HTTP {ocr_response.status_code}: {ocr_response.text}")
    return ocr_response.json().get("text", "")
 



transport_security = TransportSecuritySettings(enable_dns_rebinding_protection=False)
app = mcp.streamable_http_app()

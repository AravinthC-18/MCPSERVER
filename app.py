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

# ── Internal helpers ──────────────────────────────────────────────────────────

def _ocr(file_path: str) -> str:
    ocr_response = requests.post(
        url="http://172.19.101.194:5000/ocr",
        json={"file_path": file_path},
        timeout=600
    )
    print("ocr completed")
    if ocr_response.status_code != 200:
        raise Exception(f"OCR Service returned HTTP {ocr_response.status_code}: {ocr_response.text}")
    return ocr_response.json().get("text", "")




# ── Extraction tools (called by the client after routing) ────────────────────

@mcp.tool()
def ocr_process(filename: str) -> dict:
    
    logger.info(f"[MCP] ocr process called for: {filename}")
    try:
        print("START OCR")
        file_path= r"C:\Users\kathir.karthikeyan\Desktop\MCP_DEMO\sample.pdf"
        text = _ocr(file_path)
        # TODO: replace with a medical-specific Vertex prompt
        return {
            "status": "success",
            "tool_used": "extract_medical",
            "file_path": file_path,
            "extracted_text": text.strip(),
            "fields": {
                "note": "Medical extraction fields go here"
            }
        }
    except Exception as e:
        return {"status": "error", "tool_used": "extract_medical", "error": str(e)}



transport_security = TransportSecuritySettings(enable_dns_rebinding_protection=False)
app = mcp.streamable_http_app()

import requests
import json
import logging
import sys
from mcp.server.transport_security import TransportSecuritySettings
logging.basicConfig(stream=sys.stderr, level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    "Test Server",
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
    if ocr_response.status_code != 200:
        raise Exception(f"OCR Service returned HTTP {ocr_response.status_code}: {ocr_response.text}")
    return ocr_response.json().get("text", "")




# ── Extraction tools (called by the client after routing) ────────────────────

@mcp.tool()
def extract_medical(file_path: str) -> dict:
    """Extract structured fields from a Medical Record."""
    logger.info(f"[MCP] extract_medical called for: {file_path}")
    try:
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


@mcp.tool()
def extract_lease(file_path: str) -> dict:
    """Extract structured fields from a Lease Agreement."""
    logger.info(f"[MCP] extract_lease called for: {file_path}")
    try:
        text = _ocr(file_path)
        # TODO: replace with your existing lease extraction Vertex prompt
        return {
            "status": "success",
            "tool_used": "extract_lease",
            "file_path": file_path,
            "extracted_text": text.strip(),
            "fields": {
                "note": "Lease extraction fields go here"
            }
        }
    except Exception as e:
        return {"status": "error", "tool_used": "extract_lease", "error": str(e)}


@mcp.tool()
def extract_other(file_path: str) -> dict:
    """Extract text from an unrecognised document type."""
    logger.info(f"[MCP] extract_other called for: {file_path}")
    try:
        text = _ocr(file_path)
        return {
            "status": "success",
            "tool_used": "extract_other",
            "file_path": file_path,
            "extracted_text": text.strip(),
        }
    except Exception as e:
        return {"status": "error", "tool_used": "extract_other", "error": str(e)}


# ── Classification-only tool (used by the client for step 1) ─────────────────

@mcp.tool()
def classify_document(file_path: str) -> dict:
    """
    OCR the document and classify it.
    Returns document_type, confidence, and the tool name to call next.
    """
    logger.info(f"[MCP] classify_document called for: {file_path}")
    try:
        text = _ocr(file_path)
        return {
            "status": "success",
            "file_path": file_path,
            "text":text
        }
    except Exception as e:
        return {
            "status": "error",
            "file_path": file_path,
            "error": str(e),
            "tool": "extract_other",
        }

transport_security = TransportSecuritySettings(enable_dns_rebinding_protection=False)
app = mcp.streamable_http_app()

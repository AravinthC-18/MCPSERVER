from mcp.server.fastmcp import FastMCP
from flask import Flask, request, redirect
from mcp.server.transport_security import TransportSecuritySettings

flask_app = Flask(__name__)
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
def add(a: int, b: int):
    print("Calling add")
    return add_func(a,b)
    
@flask_app.route('/add', methods=['GET', 'POST'])
def add_func():
    print("add func")
     if request.method == 'POST':
        data = request.json()
        a = data["a"]
        b = data["b"]
        return add(a,b)
     else:
         return 0

@mcp.tool()
def sub(a: int, b: int):
    print("Calling sub")
    return a - b


@mcp.tool()
def divide(a: int, b: int):
    print("Calling div")
    return a // b


@mcp.tool()
def mul(a: int, b: int):
    print("Calling mul")
    return a * b


transport_security = TransportSecuritySettings(enable_dns_rebinding_protection=False)
app = mcp.streamable_http_app()

if __name__ == '__main__':
    flask_app.run()

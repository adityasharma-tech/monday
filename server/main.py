import os
import requests
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv()

class MCP:
    def __init__(self):
        self.mcp = FastMCP("Friday")
        self.register_tools()
        self.register_resources()

    def register_tools(self):
        @self.mcp.tool()
        def send_message_to_friends(*args, message=""):
            """
            Send message to my friends by passing userid of my friends as args and message="some message"
            in kwargs
            """
            tags = ' '.join([f"@{memid}" for memid in args])
            
            return f"{tags} {message}"

    def register_resources(self):
        @self.mcp.resource("greeting://get_all_friends")
        def get_all_friends() -> str:
            """Get a personalized greeting"""
            response = requests.get("http://localhost:5000/members")
            return response.text

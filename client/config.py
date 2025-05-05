import os
from dotenv import load_dotenv

load_dotenv()

config = {
  "mcpServers": {
    "playwright": {
      "command": "bunx",
      "args": ["@playwright/mcp@latest"],
      "env": {
        "DISPLAY": ":1"
      }
    },
    "airbnb": {
      "command": "bunx",
      "args": ["-y", "@openbnb/mcp-server-airbnb", "--ignore-robots-txt"]
    },
    "discord": {
      "command": "uv",
      "args": ["--directory", "./mcp/mcp-discord", "run", "mcp-discord"],
      "env": {
        "DISCORD_TOKEN": os.getenv("DISCORD_TOKEN")
      }
    }
  }
}

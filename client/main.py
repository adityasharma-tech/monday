import os
import art
import json
import logging
import asyncio
import argparse
from config import config as mcp_config

from google import genai
from dotenv import load_dotenv
from mcp_use import MCPAgent, MCPClient
from datetime import datetime
from rich.style import Style as RichStyle
from rich.console import Console
from rich.markdown import Markdown
from prompt_toolkit import prompt, print_formatted_text
from langchain_google_genai import ChatGoogleGenerativeAI
from prompt_toolkit.styles import Style
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.shortcuts.prompt import PromptSession


class Friday:
    def __init__(self):
        art.tprint("FRIDAY")
        self.console = Console()
        self.session = PromptSession()
        self.load_config()

        client = MCPClient.from_dict(config=mcp_config)
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            api_key=os.getenv("GOOGLE_API_KEY")
        )

        self.agent = MCPAgent(llm=llm, client=client, max_steps=30)

    def load_config(self):
        self.prompt_style = Style.from_dict({
            'guide': 'fg:#ff8037',
            'tilde': 'fg:#e5e7e9',
        })
        self.print_style = Style.from_dict({
            'guide': 'fg:#18e3c8',
            'tilde': 'fg:#e5e7e9',
        })
        self.prompt_text = HTML('<guide>guide</guide>  <tilde>~</tilde> ')

    async def start_prompting(self):
        while True:
            request = await self.get_prompt()
            if request.replace(" ", "") == "":
                self.print_result("Please provide a message")
                continue
            if request == "exit":
                break
            result = await self.get_response(request)
            self.print_result(result)

    async def get_prompt(self):
        return await self.session.prompt_async(self.prompt_text, style=self.prompt_style)

    async def get_response(self, message: str) -> str:
        try:
            response = await self.agent.run(message)
            return response
        except Exception as e:
            print("Error: \n")
            print(e)
            return "Something went wrong!, Retrying connection..."

    def print_result(self, message: str):
        text = HTML(f'<guide>friday</guide> <tilde>~</tilde> ')
        print_formatted_text(text, style=self.print_style, end='')
        self.console.print(Markdown(message), style=RichStyle(dim=True))

if __name__ == "__main__":
    load_dotenv()
    agent = Friday()
    asyncio.run(agent.start_prompting())
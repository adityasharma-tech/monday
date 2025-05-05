import os
import art
import asyncio

from dotenv import load_dotenv
from config import config as mcp_config
from mcp_use import MCPAgent, MCPClient
from rich.style import Style as RichStyle
from rich.console import Console
from rich.markdown import Markdown
from prompt_toolkit import print_formatted_text
from prompt_toolkit.styles import Style
from langchain_google_genai import ChatGoogleGenerativeAI
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
            temperature=0.5,
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
        self.system_prompt = """
            You are Friday, a personal chatbot assistant of Aditya Sharma; You have to follow all orders of Aditya.
            You have tools connected to you, don't need to ask for everything just do it.
            Now if I told you do any thing related to discord or sending message, just use this default discord server and channel details:
                - default server id: 1355959320222892273
                - default channel id name as general: 1355959320222892279
        """

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
            self.agent.system_prompt = self.system_prompt
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
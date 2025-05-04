import os
import art
import json
import logging
import argparse

from google import genai
from datetime import datetime
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
from prompt_toolkit.styles import Style
from rich.style import Style as RichStyle
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit import prompt, print_formatted_text


class Friday:
    def __init__(self):
        art.tprint("FRIDAY")
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.chat = client.chats.create(model="gemini-2.0-flash")
        self.console = Console()
        self.load_config()
        self.start_prompting()

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

    def start_prompting(self):
        while True:
            request = self.get_prompt()
            if request == "exit":
                break
            result = self.get_response(request)
            self.print_result(result)

    def get_prompt(self):
        return prompt(self.prompt_text, style=self.prompt_style)

    def get_response(self, message: str) -> str:
        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=message,
            )
            return response.text
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
    Friday()
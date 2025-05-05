import os
import threading
from flask import Flask, jsonify
from dotenv import load_dotenv
import discord
from discord.ext import commands
from google import genai

load_dotenv()

intents = discord.Intents().default()
intents.message_content = True
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
app = Flask(__name__)
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
chat = client.chats.create(model="gemini-2.0-flash")

status = True

def get_members():
    guild = bot.get_guild(1355959320222892273)
    if not guild:
        raise Exception("Guild not found!")
    memes = [{ "username": member.name, "id": member.id, "name": member.global_name } for member in guild.members if not member.bot]
    return memes


@app.route('/members', methods=['GET'])
def members():
    members_list = get_members()
    return jsonify({"members": members_list})

def get_response(message: str) -> str:
    try:
        response = chat.send_message(message)
        return response.text
    except Exception as e:
        print("Error: \n")
        print(e)
        return "Something went wrong!, Retrying connection..."


async def handle_message(message: discord.Message):
    user = message.author
    content = message.content

    global status

    if "start" in content and str(user) == "adityasharmalive" and status is False:
        await message.channel.send("<@325866452089307146> I am on")
        status = True

    if "stop" in content and str(user) == "adityasharmalive":
        await message.channel.send("<@325866452089307146> bye")
        status = False

    if "@1368647373110382702" in content:
        if status is False:
            await message.channel.send("Please ask <@1186231758191071313> sr to start me.")
            return
        response = get_response(f"user: {user}, message: {content}, system: 'you are a good friend of all users and a chatbot, reply as human message in a chatbox in short messages. But all friends can abuse a little you can also do that if they ask to do to you.'")
        await message.channel.send(response)

@bot.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return

    await handle_message(message)  # Call your function

    # Optional: if using commands, don't forget this
    await bot.process_commands(message)


@bot.command()
async def server_id(ctx):
    await ctx.send(f"The server ID is: {ctx.guild.id}")





def start_flask():
    app.run(port=7860)

@bot.event
async def on_ready():
    print(f"Bot logged in as {bot.user}")
    flask_thread = threading.Thread(target=start_flask)
    flask_thread.start()


bot.run(os.getenv("DISCORD_BOT_TOKEN"))
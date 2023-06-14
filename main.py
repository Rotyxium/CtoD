# This is an example that uses the websockets api to know when a prompt execution is done
# Once the prompt execution is done it downloads the images using the /history endpoint

# import asyncio
import websocket
import random
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from PIL import Image
import io
import tempfile
import comfyAPI


client = commands.Bot(command_prefix= '!', intents=discord.Intents.all())
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


@client.event
async def on_ready():
    print("The bot is now ready for use!")


@client.command()
async def hello(ctx):
    await ctx.send("hello!")


@client.command()
async def new(ctx):
    seed = random.randint(0, 0xffffffffff)
    comfyAPI.prompt["3"]["inputs"]["seed"] = seed
    ws = websocket.WebSocket()
    ws.connect("ws://{}/ws?clientId={}".format(comfyAPI.server_address, comfyAPI.client_id))
    print("Current seed:", seed)
    images = comfyAPI.get_images(ws, comfyAPI.prompt)
    for node_id in images:
        for image_data in images[node_id]:
            image = Image.open(io.BytesIO(image_data))
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
                image.save(temp_file.name)
                await ctx.send(f"Generated new image!\nCurrent seed: {seed}", file=discord.File(temp_file.name))

client.run(TOKEN)
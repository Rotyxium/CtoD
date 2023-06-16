import asyncio
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
# import openai


prompt = comfyAPI.prompt
prompt["3"]["inputs"]["sampler_name"] = "dpmpp_2m"
prompt["3"]["inputs"]["scheduler"] = "karras"
prompt["3"]["inputs"]["steps"] = 30
prompt["3"]["inputs"]["cfg"] = 7
prompt["4"]["inputs"]["ckpt_name"] = "abyssorangemix2_Hard.safetensors"


client = commands.Bot(command_prefix='!', intents=discord.Intents.all(), heartbeat_interval=90)
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
folder_path = 'your-folder-to stable-diffusion-webui/models or Comfyui/models' # to check for available models
active_command = None


async def read_files_in_subfolder(ctx, folder_path, subfolder_name):
    subfolder_path = os.path.join(folder_path, subfolder_name)
    if not os.path.isdir(subfolder_path):
        await ctx.send(f"Subfolder '{subfolder_name}' does not exist.")
        return

    extensions = ['.ckpt', '.pth', '.safetensors']

    for root, dirs, files in os.walk(subfolder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            _, file_extension = os.path.splitext(file_name)
            if file_extension in extensions:
                await ctx.send(file_name)


@client.event
async def on_ready():
    print("The bot is now ready for use!")


@client.command()
async def hello(ctx):
    await ctx.send("hello!")


@client.command()
async def model(ctx):
    global active_command
    if active_command is not None:
        await ctx.send("Please finish the previous command before issuing a new one.")
        return

    active_command = "model"

    current_name = prompt["4"]["inputs"]["ckpt_name"]
    await ctx.send(f"The current Model is: {current_name}.\n\nDo you want to change it? (yes/no)")

    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    try:
        message = await client.wait_for('message', check=check, timeout=30)
        response = message.content.lower()
        subfolder_name = "Stable-diffusion"
        if response == "yes":
            await ctx.send("Currently available Models:")
            await read_files_in_subfolder(ctx, folder_path, subfolder_name)
            await ctx.send("Enter the new Model name:")
            try:
                message = await client.wait_for('message', check=check, timeout=30)
                new_name = message.content
                prompt["4"]["inputs"]["ckpt_name"] = new_name
                await ctx.send(f"Model has been updated to: {new_name}")
            except asyncio.TimeoutError:
                await ctx.send("Timeout! Please try again.")
        elif response == "no":
            await ctx.send("No changes made.")
        else:
            await ctx.send("Invalid response. No changes made.")
    except asyncio.TimeoutError:
        await ctx.send("Timeout! Please try again.")
        
    active_command = None

@client.command()
async def positive(ctx):
    global active_command
    if active_command is not None:
        await ctx.send("Please finish the previous command before issuing a new one.")
        return

    active_command = "positive_prompt"

    current_prompt = prompt["6"]["inputs"]["text"]
    await ctx.send(f"The current positive prompt is: ")
    await ctx.send(current_prompt)
    await ctx.send(f"Do you want to change it? (yes/no)")
    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    try:
        message = await client.wait_for('message', check=check, timeout=30)
        response = message.content.lower()
        if response == "yes":
            await ctx.send("Enter the new prompt:")
            try:
                message = await client.wait_for('message', check=check, timeout=30)
                new_prompt = message.content
                prompt["6"]["inputs"]["text"] = new_prompt
                await ctx.send(f"Prompt has been updated to: {new_prompt}")
            except asyncio.TimeoutError:
                await ctx.send("Timeout! Please try again.")
        elif response == "no":
            await ctx.send("No changes made.")
        else:
            await ctx.send("Invalid response. No changes made.")
    except asyncio.TimeoutError:
        await ctx.send("Timeout! Please try again.")

    active_command = None


@client.command()
async def negative(ctx):
    global active_command
    if active_command is not None:
        await ctx.send("Please finish the previous command before issuing a new one.")
        return

    active_command = "negative_prompt"

    current_prompt = prompt["7"]["inputs"]["text"]
    await ctx.send(f"The current negative prompt is: ")
    await ctx.send(current_prompt)
    await ctx.send(f"Do you want to change it? (yes/no)")
    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    try:
        message = await client.wait_for('message', check=check, timeout=30)
        response = message.content.lower()
        if response == "yes":
            await ctx.send("Enter the new negative prompt:")
            try:
                message = await client.wait_for('message', check=check, timeout=30)
                new_prompt = message.content
                prompt["7"]["inputs"]["text"] = new_prompt
                await ctx.send(f"Negative prompt has been updated to: {new_prompt}")
            except asyncio.TimeoutError:
                await ctx.send("Timeout! Please try again.")
        elif response == "no":
            await ctx.send("No changes made.")
        else:
            await ctx.send("Invalid response. No changes made.")
    except asyncio.TimeoutError:
        await ctx.send("Timeout! Please try again.")
    
    active_command = None


@client.command()
async def sampler(ctx):
    global active_command
    if active_command is not None:
        await ctx.send("Please finish the previous command before issuing a new one.")
        return

    active_command = "sampler"

    current_name = prompt["3"]["inputs"]["sampler_name"]
    await ctx.send(f"The current sampler name is: {current_name}.\n\nDo you want to change it? (yes/no)")

    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    try:
        message = await client.wait_for('message', check=check, timeout=30)
        response = message.content.lower()
        if response == "yes":
            samplers = "euler, euler_ancestral, heun, dpm_2, dpm_2_ancestral, lms,\ndpm_fast, dpm_adaptive, dpmpp_2s_ancestral, dpmpp_sde,\ndpmpp_2m, dpmpp_2m_sde, ddim uni_pc, uni_pc_bh2"
            await ctx.send(f"Currently available sampler:\n {samplers}\nEnter the new sampler name:")
            try:
                message = await client.wait_for('message', check=check, timeout=30)
                new_name = message.content
                prompt["3"]["inputs"]["sampler_name"] = new_name
                await ctx.send(f"Sampler name has been updated to: {new_name}")
            except asyncio.TimeoutError:
                await ctx.send("Timeout! Please try again.")
        elif response == "no":
            await ctx.send("No changes made.")
        else:
            await ctx.send("Invalid response. No changes made.")
    except asyncio.TimeoutError:
        await ctx.send("Timeout! Please try again.")

    active_command = None


@client.command()
async def scheduler(ctx):
    global active_command
    if active_command is not None:
        await ctx.send("Please finish the previous command before issuing a new one.")
        return

    active_command = "scheduler"

    current_scheduler = prompt["3"]["inputs"]["scheduler"]
    await ctx.send(f"The current scheduler is: {current_scheduler}. Do you want to change it? (yes/no)")

    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    try:
        message = await client.wait_for('message', check=check, timeout=30)
        response = message.content.lower()
        if response == "yes":
            schedulers = "normal, karras, exponential, simple, ddim_uniform"
            await ctx.send(f"Available scheduler:\n{schedulers}\nEnter the new scheduler:")
            try:
                message = await client.wait_for('message', check=check, timeout=30)
                new_scheduler = message.content
                prompt["3"]["inputs"]["scheduler"] = new_scheduler
                await ctx.send(f"Scheduler has been updated to: {new_scheduler}")
            except asyncio.TimeoutError:
                await ctx.send("Timeout! Please try again.")
        elif response == "no":
            await ctx.send("No changes made.")
        else:
            await ctx.send("Invalid response. No changes made.")
    except asyncio.TimeoutError:
        await ctx.send("Timeout! Please try again.")

    active_command = None


@client.command()
async def cfg(ctx):
    global active_command
    if active_command is not None:
        await ctx.send("Please finish the previous command before issuing a new one.")
        return

    active_command = "cfg"

    current_cfg = prompt["3"]["inputs"]["cfg"]
    await ctx.send(f"The current cfg value is: {current_cfg}.\nDo you want to change it? (yes/no)")

    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    try:
        message = await client.wait_for('message', check=check, timeout=30)
        response = message.content.lower()
        if response == "yes":
            await ctx.send("Enter the new cfg value:")
            try:
                message = await client.wait_for('message', check=check, timeout=30)
                new_cfg = message.content
                prompt["3"]["inputs"]["cfg"] = new_cfg
                await ctx.send(f"cfg value has been updated to: {new_cfg}")
            except asyncio.TimeoutError:
                await ctx.send("Timeout! Please try again.")
        elif response == "no":
            await ctx.send("No changes made.")
        else:
            await ctx.send("Invalid response. No changes made.")
    except asyncio.TimeoutError:
        await ctx.send("Timeout! Please try again.")

    active_command = None


@client.command()
async def steps(ctx):
    global active_command
    if active_command is not None:
        await ctx.send("Please finish the previous command before issuing a new one.")
        return

    active_command = "steps"

    current_steps = prompt["3"]["inputs"]["steps"]
    await ctx.send(f"The current steps value is: {current_steps}.\n\nDo you want to change it? (yes/no)")

    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    try:
        message = await client.wait_for('message', check=check, timeout=30)
        response = message.content.lower()
        if response == "yes":
            await ctx.send("Enter the new steps value:")
            try:
                message = await client.wait_for('message', check=check, timeout=30)
                new_steps = message.content
                prompt["3"]["inputs"]["steps"] = new_steps
                await ctx.send(f"steps value has been updated to: {new_steps}")
            except asyncio.TimeoutError:
                await ctx.send("Timeout! Please try again.")
        elif response == "no":
            await ctx.send("No changes made.")
        else:
            await ctx.send("Invalid response. No changes made.")
    except asyncio.TimeoutError:
        await ctx.send("Timeout! Please try again.")

    active_command = None


@client.command()
async def new(ctx):
    global active_command
    if active_command is not None:
        await ctx.send("Please finish the previous command before issuing a new one.")
        return

    active_command = "new"
    seed = random.randint(0, 0xffffffffff)
    prompt["3"]["inputs"]["seed"] = seed
    sampler_name = prompt["3"]["inputs"]["sampler_name"]
    scheduler_name = prompt["3"]["inputs"]["scheduler"]
    steps_int = prompt["3"]["inputs"]["steps"]
    cfg_int = prompt["3"]["inputs"]["cfg"]
    model_name = prompt["4"]["inputs"]["ckpt_name"]
    positive_prompt = prompt["6"]["inputs"]["text"]
    negative_prompt = prompt["7"]["inputs"]["text"]
    ws = websocket.WebSocket()
    ws.connect("ws://{}/ws?clientId={}".format(comfyAPI.server_address, comfyAPI.client_id))
    print("Current seed:", seed)
    images = comfyAPI.get_images(ws, prompt)
    for node_id in images:
        for image_data in images[node_id]:
            image = Image.open(io.BytesIO(image_data))
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
                image.save(temp_file.name)
                await ctx.send(f"Image generated from ComfyUI!\nmodel name: {model_name}\nseed: {seed}\npositive prompt : {positive_prompt}\nnegative prompt: {negative_prompt}\nsteps: {steps_int}\ncfg: {cfg_int}\nsampler: {sampler_name}\nscheduler: {scheduler_name}", file=discord.File(temp_file.name))

            os.remove(temp_file.name)

    active_command = None
    
# @client.command()
# async def readfiles(ctx, subfolder_name):
#     await read_files_in_subfolder(ctx, folder_path, subfolder_name)

# im using gpt4all here

# @client.event
# async def on_message(message):
#     # Ignore messages from the bot itself to prevent loops
#     if message.author == client.user:
#         return

#     # Check if a command is already in progress
#     global active_command
#     if active_command is not None:
#         return

#     await client.process_commands(message)  # Process commands first

#     content = message.content.lower()

#     # Check if a command trigger is present
#     if any(trigger in content for trigger in ['generate a picture', 'generate image','generate an image','generate new image']):
#         await message.reply("Generating new image from ComfyUI, please wait...")
#         ctx = await client.get_context(message)
#         await ctx.invoke(client.get_command('new'))

#     elif any(trigger in content for trigger in ['sampler', 'change sampler', 'set sampler']):
#         ctx = await client.get_context(message)
#         await ctx.invoke(client.get_command('sampler'))

#     elif any(trigger in content for trigger in ['model', 'change model', 'set model']):
#         ctx = await client.get_context(message)
#         await ctx.invoke(client.get_command('model'))

#     elif any(trigger in content for trigger in ['positive', 'positive prompt', 'set positive']):
#         ctx = await client.get_context(message)
#         await ctx.invoke(client.get_command('positive'))

#     elif any(trigger in content for trigger in ['negative', 'negative prompt', 'set negative']):
#         ctx = await client.get_context(message)
#         await ctx.invoke(client.get_command('negative'))

#     elif any(trigger in content for trigger in ['scheduler', 'change scheduler', 'set scheduler']):
#         ctx = await client.get_context(message)
#         await ctx.invoke(client.get_command('scheduler'))

#     elif any(trigger in content for trigger in ['cfg', 'change cfg', 'set cfg']):
#         ctx = await client.get_context(message)
#         await ctx.invoke(client.get_command('cfg'))

#     elif any(trigger in content for trigger in ['steps', 'change steps', 'set steps']):
#         ctx = await client.get_context(message)
#         await ctx.invoke(client.get_command('steps'))

#     else:
#         # Send the user's message to OpenAI API for processing
#         openai.api_base = "http://localhost:4891/v1"
#         # openai.api_base = "https://api.openai.com/v1"
#         openai.api_key = "not needed for a local LLM"
#         # prompt = "Write me a text prompt for a text-to-image of a girl with a school uniform which would be perfect for 16:9 using Stable-diffusion prompt formula"
#         # model = "gpt-3.5-turbo"
#         # model = "mpt-7b-chat"
#         model = "ggml-gpt4all-j-v1.3-groovy.bin"
#         response = openai.Completion.create(
#             model=model,
#             prompt=message.content,
#             temperature=0.7,
#             max_tokens=50,
#             n=1,
#             stop=None
#         )

#         # Get the generated response from OpenAI
#         generated_text = response['choices'][0]['text']
#         # Send the generated response back to the Discord channel
#         await message.channel.send(generated_text)


client.run(TOKEN)

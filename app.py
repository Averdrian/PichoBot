import discord
from discord.ext import commands
import random
import logging
from dotenv import load_dotenv
import os
import logging
import requests
from cerebras.cloud.sdk import Cerebras
import yt_dlp

load_dotenv()

token = os.getenv("DISCORD_TOKEN")

handler = logging.FileHandler(filename='discord.log', encoding='utf-8',  mode='w')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='p!', intents=intents)


@bot.event
async def on_ready():
    print("Weno dia")


def just_text(message: discord.Message):
    return (
        message.content.strip() != "" and
        not message.attachments and
        not message.embeds and
        not message.stickers
    )


@bot.command()
async def hello(ctx : discord.Message):
    await ctx.send(f"Hello {ctx.author.mention}!")

@bot.command()
async def bulo(ctx : discord.Message):
    canal = list(filter(lambda x : x.name == "bulos-de-picho", ctx.guild.text_channels))
    if not canal:
        await ctx.channel.send("Este canal no tiene bulos de picho :(")
        return
    canal = canal[0]
    messages = [message async for message in canal.history(limit=1000) if just_text(message) and message.author.name != 'cristian.aparicio']
    message_random = random.choice(messages)

    await ctx.channel.send(message_random.content)

@bot.command()
async def creabulo(ctx: discord.Message, *args):
    logging.info(ctx)
    await ctx.channel.send(" ".join(args))

@bot.command()
async def polibulo(ctx, *args):

    error_response = b'I\xe2\x80\x99m sorry, but I can\xe2\x80\x99t help with that.'

    prompt = 'dame_un_bulo_que_protagonice_picho_' + "_".join(args) + "_y_que_sea_algo_corto_de_pocas_frases"
    message = requests.get(f"https://text.pollinations.ai/{prompt}")

    if message.status_code != 200 or message.content == error_response:
        logging.error(message.content)
        await ctx.channel.send(f"Picho no tiene bulos para ti")
        return

    await ctx.channel.send(message.content.decode('utf-8'))
    # message = [message.content[i:i+1000] for i in range(0, len(message.content), 1000)]
    # message = list(map(lambda m: m.decode('utf-8'), message))

    # for i in message:
    #     await ctx.channel.send(i)

    # logging.info(message)
    # print(message)
    # message = message.content.decode('utf-8')


YDL_OPTIONS = {
    'format': 'bestaudio/best',
    'noplaylist': True,
}

# FFMPEG_OPTIONS = {
#     'options': '-vn'
# }

FFMPEG_OPTIONS = {
    'options': '-vn',
    'executable': r'C:\ffmpeg\bin\ffmpeg.exe'
}

@bot.command()
async def play(ctx, url: str):
    # Verifica que el usuario esté en un canal de voz
    if not ctx.author.voice:
        await ctx.send("❌ Debes estar en un canal de voz.")
        return

    channel = ctx.author.voice.channel

    # Conecta al canal de voz
    if not ctx.voice_client:
        await channel.connect()
    else:
        await ctx.voice_client.move_to(channel)

    # Descarga info del audio
    with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False)
        audio_url = info['url']
        title = info.get('title', 'Audio')

    source = await discord.FFmpegOpusAudio.from_probe(
        audio_url,
        **FFMPEG_OPTIONS
    )

    ctx.voice_client.play(source)

    await ctx.send(f"🎶 Reproduciendo: **{title}**")

@bot.command()
async def stop(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("⏹️ Música detenida.")
    else:
        await ctx.send("❌ No estoy en un canal de voz.")

bot.run(token, log_handler=handler, log_level=logging.INFO)
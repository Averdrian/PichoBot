import discord
from discord.ext import commands
import random
import logging
from dotenv import load_dotenv
import os
import logging

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


bot.run(token, log_handler=handler, log_level=logging.INFO)
import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import asyncio


load_dotenv()

token = os.getenv("DISCORD_TOKEN")

handler = logging.FileHandler(filename='discord.log', encoding='utf-8',  mode='w')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='p!', intents=intents)


async def main():
    async with bot:
        await load_extensions()
        await bot.start(token)


async def load_extensions():
    await bot.load_extension('commands.commands')

if __name__ == "__main__":
    asyncio.run(main())
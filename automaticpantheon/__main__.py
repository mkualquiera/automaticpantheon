from curses import panel
import logging
import os
from typing import cast
import discord
import dotenv
import ZODB
import ZODB.FileStorage
from ZODB.Connection import RootConvenience
import re

from .bootstrap import ensure_bootstrapped
from .utils import setup_logging


setup_logging()

STORAGE = ZODB.FileStorage.FileStorage("data.fs")
DB = ZODB.DB(STORAGE)
CONNECTION = DB.open()
DB_ROOT = cast(RootConvenience, CONNECTION.root)

dotenv.load_dotenv()

INTENTS = discord.Intents.default()
INTENTS.message_content = True
INTENTS.members = True

CLIENT = discord.Client(intents=INTENTS)

_LOG = logging.getLogger(__name__)


@CLIENT.event
async def on_ready() -> None:
    """Event handler for when the client is ready."""

    _LOG.info(f"Logged in as {CLIENT.user}")

    await ensure_bootstrapped(CLIENT, DB_ROOT)

@CLIENT.event
async def on_message(message) -> None:
    # don't respond to ourselves
    if message.author == CLIENT.user:
        return
    guild_id = message.guild.id
    pantheon_manager =  DB_ROOT.pantheon_manager
    pantheon = pantheon_manager[guild_id]
    if message.content == '🙇‍♂️':
        response_str = "Whom do you bow to? No god at all. You must choose a god to worship.\n"
        for god in pantheon.get_gods():
            response_str += f"\n{god.name} is {god.type} and responds to the sigal {god.symbol}"
            for rival in god.get_rivals():
                response_str += f"    \n{god.name} is a rival of {rival.name}"
            response_str += "\n"
        await message.channel.send(response_str)

if __name__ == "__main__":
    BOT_TOKEN = os.getenv("AUTOMATICPANTHEON_TOKEN")

    if BOT_TOKEN is None:
        raise ValueError("Bot token not found")

    CLIENT.run(BOT_TOKEN)

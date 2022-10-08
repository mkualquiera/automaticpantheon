import logging
import os
from typing import cast

import discord
import dotenv
import ZODB
import ZODB.FileStorage
from ZODB.Connection import RootConvenience

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


if __name__ == "__main__":
    BOT_TOKEN = os.getenv("AUTOMATICPANTHEON_TOKEN")

    if BOT_TOKEN is None:
        raise ValueError("Bot token not found")

    CLIENT.run(BOT_TOKEN)

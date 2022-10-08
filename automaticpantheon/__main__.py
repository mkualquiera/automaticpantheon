from typing import cast
import discord
import dotenv
import os
import logging
import ZODB, ZODB.FileStorage
from ZODB.Connection import RootConvenience
from .utils import setup_logging
from .channels import CoreChannelRoles, CoreChannelRoleManager
import transaction

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


async def ensure_guild() -> None:
    """Ensure that the main guild exists."""

    num_guilds = len(CLIENT.guilds)
    if num_guilds == 0:
        _LOG.warning("No guilds found. Creating one...")

        guild = await CLIENT.create_guild(name="Automatic Pantheon")

        _LOG.info("Created guild %s", guild)


async def ensure_invite(guild: discord.Guild) -> None:
    """Ensure that the main guild has an invite.

    Parameters
    ----------
    guild: discord.Guild
        The guild to ensure an invite for."""

    invites = await guild.invites()

    for invite in invites:
        if invite.channel == guild.system_channel:
            _LOG.info("Found invite %s", invite.url)
            return

    _LOG.warning("No invite found. Creating one...")
    # Cast is safe because we just checked that the system channel is not None
    system_channel = cast(discord.TextChannel, guild.system_channel)
    invite = await system_channel.create_invite()

    _LOG.info("Created invite %s", invite.url)


async def ensure_core_channel(
    guild: discord.Guild, role: CoreChannelRoles, role_manager: CoreChannelRoleManager
) -> None:
    """Ensure that a core channel exists.

    Parameters
    ----------
    guild: discord.Guild
        The guild to ensure the core channel exists in.
    role: CoreChannelRoles
        The role of the core channel.
    role_manager: CoreChannelRoleManager
        The role manager for the guild.
    """

    must_create = False

    try:
        channel_id = role_manager.get_core_channel(role)
    except KeyError:

        # Edge case: system channel
        if role == CoreChannelRoles.SYSTEM:

            # Check if the guild has a system channel
            if guild.system_channel is None:
                _LOG.warning("No system channel found. Creating one...")
                must_create = True
            else:
                _LOG.info("Found system channel %s", guild.system_channel)
                role_manager.set_core_channel(role, guild.system_channel.id)
                transaction.commit()

        else:
            must_create = True
    else:
        _LOG.info("Found channel in db %s", guild.get_channel(channel_id))
        _LOG.info("Checking if it still exists...")
        channel = guild.get_channel(channel_id)

        must_create = channel is None

    if must_create:
        _LOG.warning("No %s channel found. Creating one...", role.name)
        channel = await guild.create_text_channel(role.name)
        _LOG.info("Created channel %s", channel)
        role_manager.set_core_channel(role, channel.id)
        transaction.commit()


async def ensure_core_channels(guild: discord.Guild) -> None:
    """Ensure that all core channels exist.

    Parameters
    ----------
    guild: discord.Guild
        The guild to ensure the core channels exist in.
    """

    try:
        role_managers = DB_ROOT.channel_role_managers
    except AttributeError:
        DB_ROOT.channel_role_managers = {}
        role_managers = DB_ROOT.channel_role_managers

    try:
        role_manager = role_managers[guild.id]
    except KeyError:
        role_managers[guild.id] = CoreChannelRoleManager()
        role_manager = role_managers[guild.id]

    for role in CoreChannelRoles:
        await ensure_core_channel(guild, role, role_manager)


@CLIENT.event
async def on_ready() -> None:
    """Event handler for when the client is ready."""

    _LOG.info(f"Logged in as {CLIENT.user}")

    await ensure_guild()

    for guild in CLIENT.guilds:
        await ensure_core_channels(guild)
        await ensure_invite(guild)


if __name__ == "__main__":
    BOT_TOKEN = os.getenv("AUTOMATICPANTHEON_TOKEN")

    if BOT_TOKEN is None:
        raise ValueError("Bot token not found")

    CLIENT.run(BOT_TOKEN)

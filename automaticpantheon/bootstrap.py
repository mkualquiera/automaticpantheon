import logging
from gettext import translation
from typing import cast

import discord
import transaction
from ZODB.Connection import RootConvenience

from .channels import CoreChannelRoleManager, CoreChannelRoles

_LOG = logging.getLogger(__name__)


async def ensure_bootstrapped(client: discord.Client, db_root: RootConvenience) -> None:
    """Ensure that the guild

    Parameters
    ----------
    client: discord.Client
        The client to bootstrap.
    db_root: RootConvenience
        The root of the database.
    """

    await ensure_guild(client)
    for guild in client.guilds:
        await ensure_core_channels(guild, db_root)
        await ensure_invite(guild)


async def ensure_guild(client: discord.Client) -> None:
    """Ensure that the main guild exists."""

    num_guilds = len(client.guilds)
    if num_guilds == 0:
        _LOG.warning("No guilds found. Creating one...")

        guild = await client.create_guild(name="Automatic Pantheon")

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


async def ensure_core_channels(guild: discord.Guild, db_root: RootConvenience) -> None:
    """Ensure that all core channels exist.

    Parameters
    ----------
    guild: discord.Guild
        The guild to ensure the core channels exist in.
    db_root: RootConvenience
        The root of the database.
    """

    try:
        role_managers = db_root.channel_role_managers
    except AttributeError:
        db_root.channel_role_managers = {}
        role_managers = db_root.channel_role_managers

    try:
        role_manager = role_managers[guild.id]
    except KeyError:
        role_managers[guild.id] = CoreChannelRoleManager()
        role_manager = role_managers[guild.id]

    for role in CoreChannelRoles:
        await ensure_core_channel(guild, role, role_manager)

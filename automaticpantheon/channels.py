from enum import Enum

from discord import Guild
from persistent import Persistent


class CoreChannelRoles(Enum):
    """Enum for core channel roles.

    Attributes
    ----------
    SYSTEM
        The system channel. When a new user joins the guild, they will be
        greeted in this channel.
    LAWS
        The laws channel. This channel is used to display the current laws
        of the guild.
    PROPOSALS
        The proposals channel. This channel is used to display the current
        proposals minigames for passing laws.
    """

    SYSTEM = 0
    LAWS = 1
    PROPOSALS = 2


class CoreChannelRoleManager(Persistent):
    """A class for managing core channel roles. It knows which channels are
    core channels and which roles they have.

    Attributes
    ----------
    core_channels
        A dictionary mapping core channel roles to channel IDs.
    """

    def __init__(self):
        self.core_channels: dict[CoreChannelRoles, int] = {}

    def get_core_channel(self, role: CoreChannelRoles) -> int:
        """Get the channel ID of a core channel.

        Parameters
        ----------
        role: CoreChannelRoles
            The role of the core channel.

        Returns
        -------
        int
            The channel ID of the core channel.
        """
        return self.core_channels[role]

    def get_channel_role(self, channel_id: int) -> CoreChannelRoles:
        """Get the role of a core channel.

        Parameters
        ----------
        channel_id: int
            The ID of the channel.

        Returns
        -------
        CoreChannelRoles
            The role of the core channel.
        """
        for role, channel in self.core_channels.items():
            if channel == channel_id:
                return role
        raise KeyError(f"Channel {channel_id} is not a core channel")

    def set_core_channel(self, role: CoreChannelRoles, channel_id: int) -> None:
        """Set the channel ID of a core channel.

        <!> Make sure to call `transaction.commit()` after calling this method.
        to save the changes to the database.

        Parameters
        ----------
        role: CoreChannelRoles
            The role of the core channel.
        channel_id: int
            The ID of the channel.
        """
        self.core_channels[role] = channel_id
        self._p_changed = True

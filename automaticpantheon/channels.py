from enum import Enum
from persistent import Persistent
from discord import Guild


class CoreChannelRoles(Enum):
    SYSTEM = 0
    LAWS = 1
    PROPOSALS = 2


class CoreChannelRoleManager(Persistent):
    def __init__(self, guild: Guild):
        self.guildA_id = guild.id
        self.core_channels: dict[CoreChannelRoles, int] = {}

    def get_core_channel(self, role: CoreChannelRoles) -> int:
        return self.core_channels[role]

    def get_channel_role(self, channel_id: int) -> CoreChannelRoles:
        for role, channel in self.core_channels.items():
            if channel == channel_id:
                return role
        raise KeyError(f"Channel {channel_id} is not a core channel")

    def set_core_channel(self, role: CoreChannelRoles, channel_id: int) -> None:
        self.core_channels[role] = channel_id
        self._p_changed = True

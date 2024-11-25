import disnake.ui

import database
from Guild import Guild


class DelegateRoleDropDown(disnake.ui.RoleSelect):

    def __init__(self, guild: Guild):
        self.guild = guild
        super().__init__(placeholder="Select a Role that'll be used to verify attendees", min_values=1, max_values=1)

    async def callback(self, inter: disnake.MessageInteraction):
        guild_id = inter.guild_id
        guild = Guild(guild_id)
        guild.delegate_role = self.values[0].id
        database.add_update_guild(guild)
        await inter.response.send_message(f"Your chosen role is: {self.values[0].name}")

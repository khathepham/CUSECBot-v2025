import disnake.ui

import database
from Guild import Guild


class BaseView(disnake.ui.View):
    def __init__(self, component):
        super().__init__()
        self.add_item(component)


class DelegateRoleDropDown(disnake.ui.RoleSelect):

    def __init__(self, guild: Guild):
        self.guild = guild
        super().__init__(placeholder="Select a Role that'll be used to verify attendees", min_values=1, max_values=1)

    async def callback(self, inter: disnake.MessageInteraction):
        guild_id = inter.guild_id
        guild = Guild(guild_id)
        guild.delegate_role = self.values[0].id
        database.add_update_guild(guild)

        vip_role_select = VIPRoleDropDown(guild)
        await inter.response.send_message(f"Your verified attendee role is: {self.values[0].name}.\n Please select a role that will be used to identify VIP members.",
                                          view=BaseView(vip_role_select), ephemeral=True)


class VIPRoleDropDown(disnake.ui.RoleSelect):

    def __init__(self, guild: Guild):
        self.guild = guild
        super().__init__(placeholder="Select a Role that'll be used to identify VIP Members", min_values=1,
                         max_values=1)

    async def callback(self, inter: disnake.MessageInteraction):
        guild_id = inter.guild_id
        guild = Guild(guild_id)
        guild.vip_role = self.values[0].id
        database.add_update_guild(guild)
        await inter.response.send_message(f"Your chosen role is: {self.values[0].name}", ephemeral=True)

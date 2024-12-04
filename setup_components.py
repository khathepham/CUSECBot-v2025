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
        guild = database.get_guild_by_id(guild_id)
        guild.delegate_role = self.values[0].id
        database.add_update_guild(guild)

        vip_role_select = VIPRoleDropDown(guild)
        await inter.response.send_message(
            f"Your verified attendee role is: **{self.values[0].name}**.\n Please select a role that will be used to identify VIP members.",
            view=BaseView(vip_role_select), ephemeral=True)


class VIPRoleDropDown(disnake.ui.RoleSelect):

    def __init__(self, guild: Guild):
        self.guild = guild
        super().__init__(placeholder="Select a Role that'll be used to identify VIP Members", min_values=1,
                         max_values=1)

    async def callback(self, inter: disnake.MessageInteraction):
        guild_id = inter.guild_id
        guild = database.get_guild_by_id(guild_id)
        guild.vip_role = self.values[0].id
        database.add_update_guild(guild)

        sponsor_role_select = SponsorRoleDropDown(guild)
        await inter.response.send_message(
            f"Your VIP attendee role is: **{self.values[0].name}**.\n Please select a role that will be used for Sponsors.",
            view=BaseView(sponsor_role_select), ephemeral=True
        )


class SponsorRoleDropDown(disnake.ui.RoleSelect):
    def __init__(self, guild: Guild):
        self.guild = guild
        super().__init__(placeholder="Select a role that'll be used to verify Sponsors", min_values=1, max_values=1)

    async def callback(self, inter: disnake.MessageInteraction):
        guild_id = inter.guild_id
        guild = database.get_guild_by_id(guild_id)
        guild.sponsor_role = self.values[0].id
        database.add_update_guild(guild)

        speaker_role_select = SpeakerRoleDropDown(guild)
        await inter.response.send_message(
            f"Your Sponsor role is: **{self.values[0].name}**.\n Please select a role that will be used for Speakers.",
            view=BaseView(speaker_role_select), ephemeral=True
        )


class SpeakerRoleDropDown(disnake.ui.RoleSelect):
    def __init__(self, guild: Guild):
        self.guild = guild
        super().__init__(placeholder="Select a Role that'll be used to verify Speakers", min_values=1, max_values=1)

    async def callback(self, inter: disnake.MessageInteraction):
        guild_id = inter.guild_id
        guild = database.get_guild_by_id(guild_id)
        guild.speaker_role = self.values[0].id
        database.add_update_guild(guild)

        next_prompt = VerificationPromptChannelDropDown(guild)
        await inter.response.send_message(
            f"Your Speaker role is: {self.values[0].name}.\nPlease choose a channel for the verification prompt.",
            view=BaseView(next_prompt), ephemeral=True
        )


class VerificationPromptChannelDropDown(disnake.ui.ChannelSelect):
    def __init__(self, guild: Guild):
        self.guild = guild
        super().__init__(placeholder="Select a channel where a verification prompt for attendees will be sent",
                         min_values=1, max_values=1)

    async def callback(self, inter: disnake.MessageInteraction):
        guild_id = inter.guild_id
        guild = database.get_guild_by_id(guild_id)
        guild.verification_channel = self.values[0].id
        database.add_update_guild(guild)

        next_view = VerificationModChannelDropDown(guild)
        await inter.response.send_message(
            f"Your Verification Prompt Channel is: {self.values[0].name}.\nPlease choose a channel where mods/organizers see prompts and verify people manually",
            view=BaseView(next_view), ephemeral=True
        )


class VerificationModChannelDropDown(disnake.ui.ChannelSelect):
    def __init__(self, guild: Guild):
        self.guild = guild
        super().__init__(placeholder="Select a channel where a verification prompt for organizers to confirm will be sent",
                         min_values=1, max_values=1)

    async def callback(self, inter: disnake.MessageInteraction):
        guild_id = inter.guild_id
        guild = database.get_guild_by_id(guild_id)
        guild.verification_requests_channel = self.values[0].id
        database.add_update_guild(guild)

        next_view = ModeratorRoleDropDown(guild)
        await inter.response.send_message(
            f"Your Moderation Verification Channel is: {self.values[0].name}. Please select your moderation role.",
            view=BaseView(next_view), ephemeral=True
        )


class ModeratorRoleDropDown(disnake.ui.RoleSelect):
    def __init__(self, guild: Guild):
        self.guild = guild
        super().__init__(placeholder="Select a Role that represents possible moderators", min_values=1, max_values=1)

    async def callback(self, inter: disnake.MessageInteraction):
        guild_id = inter.guild_id
        guild = database.get_guild_by_id(guild_id)
        guild.moderation_role = self.values[0].id
        database.add_update_guild(guild)

        await inter.response.send_message(
            f"Your Moderation Role role is: {self.values[0].name}.\nCompleted Setup", ephemeral=True
        )

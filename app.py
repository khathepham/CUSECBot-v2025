from infisical_sdk import InfisicalSDKClient
import disnake
from disnake import app_commands
from disnake.ext import commands
import os
from dotenv import load_dotenv

import verification_modal
from verification_modal import AttendeeVerificaionModal, OSSVerificationModal
from setup_components import DelegateRoleDropDown
import database

print("[INFO] Loading env variables")
load_dotenv()

print("[INFO] Connecting to Infisical")
i_client = InfisicalSDKClient(host="https://app.infisical.com")
i_client.auth.universal_auth.login(client_id=os.environ.get("I_CLIENT_ID"),
                                   client_secret=os.environ.get("I_CLIENT_SECRET"))
i_response = i_client.secrets.get_secret_by_name(secret_name="BOT_TOKEN",
                                                 project_id="fcdb0041-ad1d-4fa6-854d-0745640829d0",
                                                 environment_slug="prod", secret_path="/")
print("[INFO] Received bot_token")
bot_token = i_response.secret.secret_value

intents = disnake.Intents.all()
intents.message_content = True

command_sync_flags = commands.CommandSyncFlags.default()
command_sync_flags.sync_commands_debug = True

bot = commands.Bot(command_prefix="^", intents=intents, command_sync_flags=command_sync_flags)


@bot.slash_command(description="Pongs your Ping")
async def ping(inter: disnake.ApplicationCommandInteraction):
    await inter.response.send_message('pong', ephemeral=True)


@bot.slash_command(description="Verify to gain access to the rest of the server!")
async def verify(inter: disnake.ApplicationCommandInteraction):
    pass


@verify.sub_command(description="For those who bought or received a ticket, verify now!")
async def attendee(inter: disnake.ApplicationCommandInteraction):
    modal = AttendeeVerificaionModal()
    await inter.response.send_modal(modal=modal)


@verify.sub_command(description="For Sponsors, Speakers, Keynotes, and Panelists to verify!")
async def sponsor(inter: disnake.ApplicationCommandInteraction):
    modal = OSSVerificationModal(verification_modal.ConferenceRole.SPONSOR)
    await inter.response.send_modal(modal=modal)


@verify.sub_command(description="For Speakers, Keynotes, and Panelists to verify!")
async def speaker_keynote_panelist(inter: disnake.ApplicationCommandInteraction):
    modal = OSSVerificationModal(verification_modal.ConferenceRole.SPEAKER)
    await inter.response.send_modal(modal=modal)


@bot.slash_command(description="For Admins to set up the verification bot")
async def verification_setup(inter: disnake.ApplicationCommandInteraction):
    guild = database.get_guild_by_id(inter.guild_id)
    delegate_role_select = DelegateRoleDropDown(guild)
    await inter.response.send_message("What role do you want your verified delegates to have?", view=BaseView(delegate_role_select), ephemeral=True)


@bot.event
async def on_ready():
    print(f"{bot.user} has logged onto Discord!")


class BaseView(disnake.ui.View):
    def __init__(self, component):
        super().__init__()
        self.add_item(component)


if __name__ == '__main__':
    bot.run(bot_token)

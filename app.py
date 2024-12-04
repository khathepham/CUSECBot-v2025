from infisical_sdk import InfisicalSDKClient
import disnake
from disnake import app_commands
from disnake.ext import commands
import os
from dotenv import load_dotenv

import verification_modal
from verification_modal import AttendeeVerificationModal, OSSVerificationModal
from setup_components import DelegateRoleDropDown, BaseView
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
    await inter.response.send_message('pong')


@bot.slash_command(description="Verify to gain access to the rest of the server!")
async def verify(inter: disnake.ApplicationCommandInteraction):
    if database.get_guild_by_id(inter.guild_id) is None:
        inter.response.send_message("Verification has not been set up yet. Please contact the admins to set up "
                                    "verification for this server.")
    pass


@verify.sub_command(description="For those who bought or received a ticket, verify now!")
async def attendee(inter: disnake.ApplicationCommandInteraction):
    await verify_attendee(inter)


@verify.sub_command(description="For Sponsors, Speakers, Keynotes, and Panelists to verify!")
async def sponsor(inter: disnake.ApplicationCommandInteraction):
    await verify_sponsor(inter)


@verify.sub_command(description="For Speakers, Keynotes, and Panelists to verify!")
async def speaker_keynote_panelist(inter: disnake.ApplicationCommandInteraction):
    modal = OSSVerificationModal(verification_modal.ConferenceRole.SPEAKER)
    await inter.response.send_modal(modal=modal)


@bot.slash_command(description="For Admins to set up the verification bot")
@commands.default_member_permissions(manage_guild=True, moderate_members=True)
async def verification_setup(inter: disnake.ApplicationCommandInteraction):
    guild = database.get_guild_by_id(inter.guild_id)
    delegate_role_select = DelegateRoleDropDown(guild)
    await inter.response.send_message("What role do you want your verified delegates to have?",
                                      view=BaseView(delegate_role_select), ephemeral=True)


@bot.slash_command(description="To create a permanent verification prompt.")
@commands.default_member_permissions(moderate_members=True)
async def create_verification_prompt(inter: disnake.ApplicationCommandInteraction):
    await inter.channel.send(
        "How would you like to verify?",
        components=[
            disnake.ui.Button(label="Verify Delegate/Attendee Ticket", style=disnake.ButtonStyle.primary,
                              custom_id="attendee"),
            disnake.ui.Button(label="Verify as a Sponsor", style=disnake.ButtonStyle.secondary,
                              custom_id="sponsor"),
            disnake.ui.Button(label="Verify as a Speaker", style=disnake.ButtonStyle.secondary,
                              custom_id="speaker"),
        ]
    )


@bot.listen("on_button_click")
async def verify_listener(inter: disnake.MessageInteraction):
    if inter.component.custom_id not in ["sponsor", "speaker", "attendee"]:
        return

    if inter.component.custom_id == "sponsor":
        await verify_sponsor(inter)
    elif inter.component.custom_id == "speaker":
        await verify_speaker(inter)
    elif inter.component.custom_id == "attendee":
        await verify_attendee(inter)


@bot.listen("on_button_click")
async def re_verify_attendee_listener(inter: disnake.MessageInteraction):
    await verify_attendee(inter)


async def verify_sponsor(inter: disnake.Interaction):
    modal = OSSVerificationModal(verification_modal.ConferenceRole.SPONSOR)
    await inter.response.send_modal(modal=modal)


async def verify_speaker(inter: disnake.Interaction):
    modal = OSSVerificationModal(verification_modal.ConferenceRole.SPEAKER)
    await inter.response.send_modal(modal=modal)


async def verify_attendee(inter: disnake.Interaction):
    modal = AttendeeVerificationModal()
    await inter.response.send_modal(modal=modal)
    pass


@bot.event
async def on_ready():
    print(f"{bot.user} has logged onto Discord!")


if __name__ == '__main__':
    bot.run(bot_token)

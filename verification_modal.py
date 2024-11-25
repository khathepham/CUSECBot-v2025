# At the top of the file.
import uuid

import disnake
from disnake.ext import commands
from disnake import TextInputStyle
import ticket_tailor
from enum import Enum


# Subclassing the modal.
class AttendeeVerificaionModal(disnake.ui.Modal):
    def __init__(self):
        # The details of the modal, and its components
        components = [
            disnake.ui.TextInput(
                label="Ticket Code found on your Ticket",
                placeholder="a7Bt3A",
                custom_id=f"ticket_code",
                style=TextInputStyle.short,
                max_length=8,
                required=True
            ),
            disnake.ui.TextInput(
                label="Email that was used to recieve your ticket",
                placeholder="youremail@email.com",
                custom_id="email",
                style=TextInputStyle.short,
                required=True
            ),
        ]
        super().__init__(title="Verify User", components=components)

    # The callback received when the user input is completed.
    async def callback(self, inter: disnake.ModalInteraction):
        ticket_code = inter.text_values.get("ticket_code")
        email = inter.text_values.get("email")

        ticket = ticket_tailor.get_ticket_by_ticket_code(ticket_code)
        if ticket is None:
            embed = disnake.Embed(title="Unable to Verify",
                                  description="The ticket code you entered doesn't match an existing one.")
            embed.add_field(name="You entered this ticket code", value=ticket_code)
            embed.add_field(name="", value="Try again?")
            embed.add_field(name="You entered this email", value=email)
            components = [
                disnake.ui.Button(label="Yeah, let's try that again", style=disnake.ButtonStyle.success,
                                  custom_id="reverify"),
            ]
            await inter.response.send_message(embed=embed, components=components, ephemeral=True)
        elif email not in ticket.emails:
            embed = disnake.Embed(title="Unable to Verify",
                                  description="We found your ticket, but your email doesn't quite match.")
            embed.add_field(name="You entered this ticket code", value=ticket_code)
            embed.add_field(name="You entered this email", value=email)
            embed.add_field(name="", value="Try again?")
            components = [
                disnake.ui.Button(label="Yeah, let's try that again", style=disnake.ButtonStyle.success,
                                  custom_id="reverify"),
            ]
            await inter.response.send_message(embed=embed, components=components, ephemeral=True)
        if ticket is not None and email in ticket.emails:
            # Add Role
            # Notify Verify Channel
            # Change nickname
            embed = disnake.Embed(title=f"Hi {ticket.first_name}, You're Verified!",
                                  description="You should be able to see the verified-only channels (which is most of the server)")
            await inter.response.send_message(embed=embed, ephemeral=True)


class ConferenceRole(Enum):
    SPEAKER = "Speaker"
    SPONSOR = "Sponsor"
    PANELIST = "Panelist"


class OSSVerificationModal(disnake.ui.Modal):
    def __init__(self, conference_role: ConferenceRole):
        # The details of the modal, and its components
        components = [
            disnake.ui.TextInput(
                label="First Name",
                placeholder="George",
                custom_id=f"OSS_first_name",
                style=TextInputStyle.short,
                max_length=20,
                required=True
            ),
            disnake.ui.TextInput(
                label="Last Name",
                placeholder="Town",
                custom_id=f"OSS_last_name",
                style=TextInputStyle.short,
                max_length=20,
                required=True
            )
        ]
        super().__init__(title="Verify User", components=components)

    # The callback received when the user input is completed.
    async def callback(self, inter: disnake.ModalInteraction):
        f_name = inter.text_values.get("first_name")
        embed = disnake.Embed(title=f"Hi {f_name}",
                              description="Your verification request has been sent to the Organizing team. We'll grant you access shortly.")
        await inter.response.send_message(embed=embed, ephemeral=True)

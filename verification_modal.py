# At the top of the file.
import uuid

import disnake
from disnake.ext import commands
from disnake import TextInputStyle

import database
import ticket_tailor
from enum import Enum

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(filename="verification.log", level=logging.INFO)


# Subclassing the modal.
class AttendeeVerificationModal(disnake.ui.Modal):
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
                label="Email that was used to receive your ticket",
                placeholder="youremail@email.com",
                custom_id="email",
                style=TextInputStyle.short,
                required=True
            ),
        ]
        super().__init__(title="Verify User", components=components)

    # The callback received when the user input is completed.
    async def callback(self, inter: disnake.ModalInteraction):
        ticket_code = inter.text_values.get("ticket_code").strip()
        email = inter.text_values.get("email").strip().lower()
        guild = database.get_guild_by_id(inter.guild_id)
        verify_channel = inter.guild.get_channel(guild.logs_channel)

        ticket = ticket_tailor.get_ticket_by_ticket_code(ticket_code)
        if ticket is None:
            embed = disnake.Embed(title="Unable to Verify",
                                  description="The ticket code you entered doesn't match an existing one. Want to try again?")
            embed.add_field(name="You entered this ticket code", value=ticket_code)
            embed.add_field(name="You entered this email", value=email)

            components = [
                disnake.ui.Button(label="Yeah, let's try that again", style=disnake.ButtonStyle.success,
                                  custom_id="reverify"),
            ]
            await inter.response.send_message(embed=embed, components=components, ephemeral=True)
            logger.info(
                f"{inter.user.global_name} was unable to verify using {ticket_code} {email} due to an invalid ticket code.")
            await verify_channel.send(embed=disnake.Embed(
                title="Failed Verification",
                description=f"{inter.user.mention} was unable to verify using {ticket_code}, {email}. Invalid or void ticket code."
            ))
        elif email not in ticket.emails:
            embed = disnake.Embed(title="Unable to Verify",
                                  description="We found your ticket, but your email doesn't quite match. Try again?")
            embed.add_field(name="You entered this ticket code", value=ticket_code)
            embed.add_field(name="You entered this email", value=email)
            components = [
                disnake.ui.Button(label="Yeah, let's try that again", style=disnake.ButtonStyle.success,
                                  custom_id="reverify"),
            ]
            await inter.response.send_message(embed=embed, components=components, ephemeral=True)
            logger.info(
                f"{inter.user.global_name} was unable to verify using {ticket_code} {email} due to an invalid email. Ticket was found.")
            await verify_channel.send(embed=disnake.Embed(
                title="Failed Verification",
                description=f"{inter.user.mention} was unable to verify using {ticket_code}, {email}. Ticket was found, but email does not match."
            ))

        if ticket is not None and email in ticket.emails:
            # Add Role
            await inter.user.add_roles(inter.guild.get_role(guild.delegate_role))

            if "VIP" in ticket.ticket_type:
                await inter.user.add_roles(inter.guild.get_role(guild.vip_role))

            # Notify Verify Channel
            embed = disnake.Embed(
                title="Attendee Verified",
                description=f"**{ticket.first_name} {ticket.last_name}** ({inter.user.mention}) has been verified with ticket code {ticket.ticket_code} and email {email}"
            )

            await verify_channel.send(embed=embed)

            embed = disnake.Embed(title=f"Hi {ticket.first_name}, You're Verified!",
                                  description="You should be able to see the verified-only channels (which is most of the server)")
            await inter.response.send_message(embed=embed, ephemeral=True)
            logger.info(
                f"{inter.user.global_name} was able to verify using {ticket_code} {email} as {ticket.first_name} {ticket.last_name}")


class ConferenceRole(Enum):
    SPEAKER = "Speaker"
    SPONSOR = "Sponsor"
    PANELIST = "Panelist"


class OSSVerificationModal(disnake.ui.Modal):
    def __init__(self, conference_role: ConferenceRole):
        # The details of the modal, and its components
        self.conference_role = conference_role
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
                placeholder="Lucas",
                custom_id=f"OSS_last_name",
                style=TextInputStyle.short,
                max_length=20,
                required=True
            )
        ]

        if conference_role == ConferenceRole.SPONSOR:
            components.append(
                disnake.ui.TextInput(
                    label="Company/Agency Name",
                    placeholder="Star Tours",
                    custom_id="OSS_company_name"
                )
            )
        super().__init__(title="Verify User", components=components)

    # The callback received when the user input is completed.
    async def callback(self, inter: disnake.ModalInteraction):
        f_name = inter.text_values.get("OSS_first_name", "")
        l_name = inter.text_values.get("OSS_last_name", "")
        company = inter.text_values.get("OSS_company_name", None)
        user = inter.user
        embed = disnake.Embed(title=f"Hi {f_name},",
                              description="Your verification request has been sent to the Organizing team. We'll grant you access shortly.")
        await inter.response.send_message(embed=embed, ephemeral=True)

        guild = database.get_guild_by_id(inter.guild_id)
        verification_log_channel = inter.guild.get_channel(guild.verification_requests_channel)
        mod_role = inter.guild.get_role(guild.moderation_role)

        embed = disnake.Embed(
            title=f"Verification Request - {self.conference_role.value}",
            description=f"**{f_name.strip()} {l_name.strip()}** {f'from **{company.strip()}**' if company is not None else ''} needs to be manually verified. "
                        f"Please double check and verify them.\n"
                        f"{user.mention}"
        )

        # await verification_log_channel.send(content=f"{mod_role.mention}", embed=embed)
        await verification_log_channel.send(embed=embed)

import discord # noqa
from main import GUILD_ID
from discord import app_commands
from discord.ext import commands
from datetime import timedelta


class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} is online!")

    @app_commands.command(
            name="ban", description="Ban a user from the discord.")
    @app_commands.guilds(GUILD_ID)
    @app_commands.choices(
        delete_messages=[
            app_commands.Choice(
                name="❌ Don't Delete Any", value=0),
            app_commands.Choice(
                name="🕛 Previous 24 Hours", value=1),
            app_commands.Choice(
                name="🕐 Previous 48 Hours", value=2),
            app_commands.Choice(
                name="🕒 Previous 3 Days", value=3),
            app_commands.Choice(
                name="🕝 Previous 5 Days", value=5),
            app_commands.Choice(
                name="⭐ Previous 7 Days - Recommended", value=7)
        ]
    )
    @app_commands.describe(
        user="User to Ban.",
        reason="Reason for the Ban.",
        delete_messages="How much user history to Delete."
    )
    async def user_ban(self, interaction: discord.Interaction, user: discord.User, delete_messages:int, reason: str = "No reason provided."):  # noqa
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "❌ You don't have permission to ban members.", ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)

        try:
            await interaction.guild.ban(user, reason=reason, delete_message_days=delete_messages)  # noqa
            await interaction.followup.send(
                f"✅ Successfully banned {user.name}. Deleted messages from the last **{delete_messages} day(s)**.", ephemeral=True) # noqa
        except discord.Forbidden:
            await interaction.followup.send(
                "❌ You do not have permission to ban this user",
                ephemeral=True)
        except discord.HTTPException as e:
            await interaction.followup.send(
                f"⚠️ An error occurred while banning: {e}", ephemeral=True)

    @app_commands.command(
            name="unban", description="Unban a user from the discord.")
    @app_commands.guilds(GUILD_ID)
    @app_commands.describe(user_id="User ID to unban.")
    async def user_unban(self, interaction: discord.Interaction, user_id: str):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "❌ You don't have permission to unban members.",
                ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)

        try:
            user_id = int(user_id)
            user = await self.client.fetch_user(user_id)

            bans = [entry async for entry in interaction.guild.bans()]
            banned_entry = discord.utils.find(
                lambda entry: entry.user.id == user.id, bans)

            if banned_entry is None:
                await interaction.followup.send(
                    "❌ This user is not currently banned.", ephemeral=True)
                return

            await interaction.guild.unban(banned_entry.user)
            await interaction.followup.send(
                f"✅ Successfully unbanned {banned_entry.user}.",
                ephemeral=True)

        except ValueError:
            await interaction.followup.send(
                "❌ Invalid ID format. Please enter a numeric user ID.",
                ephemeral=True)

        except discord.NotFound:
            await interaction.followup.send(
                "❓ User not found. make sure the ID is correct.",
                ephemeral=True)

        except discord.Forbidden:
            await interaction.followup.send(
                "❗ Bot unable to unban UserID. Check permissions & role hierarchy", # noqa
                ephemeral=True)

        except discord.HTTPException as e:
            await interaction.followup.send(
                f"⚠️ An error occurred while unbanning: {e}", ephemeral=True)

        except Exception as e:
            print(f"Unexpected error in /unban: {e}")
            await interaction.followup.send(
                "⚠️ An unexpected error occurred while processing the unban request.", # noqa
                ephemeral=True
            )

    @app_commands.command(
            name="timeout",
            description="Timeout select user from the discord.")
    @app_commands.guilds(GUILD_ID)
    @app_commands.describe(
        user="User to Timeout",
        reason="Reason for the Timeout.",
        duration="Timeout duration."
    )
    async def user_timeout(self, interaction: discord.Interaction, user: discord.Member, duration: int, reason: str = "No reason provided."): # noqa
        if not interaction.user.guild_permissions.moderate_members:
            await interaction.response.send_message(
                "❌ You don't have permission to timeout members.",
                ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)

        if duration < 1 or duration > 10000:
            await interaction.followup.send(
                "⚠️ Duration must be between 1 and 10080 minutes (7 days).",
                ephemeral=True)
            return

        try:
            timeout_until = discord.utils.utcnow() + timedelta(
                minutes=duration)
            await user.timeout(timeout_until, reason=reason)

            await interaction.followup.send(
                f"✅ {user.mention} has been timed out for "
                f"**{duration} minutes**. \nReason: {reason}", ephemeral=True)
        except discord.Forbidden:
            await interaction.followup.send(
                "❌ You do not have permission to timeout this user",
                ephemeral=True)
        except discord.HTTPException as e:
            await interaction.followup.send(
                f"⚠️ An error occurred while timing out: {e}",
                ephemeral=True)


async def setup(client):
    await client.add_cog(Moderation(client))

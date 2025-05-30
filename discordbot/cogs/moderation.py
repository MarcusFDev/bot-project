import discord # noqa
from main import GUILD_ID
from discord import app_commands
from discord.ext import commands
from datetime import timedelta
from typing import Optional


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
    async def user_ban(self,
                       interaction: discord.Interaction,
                       user: discord.User,
                       delete_messages: int,
                       reason: str = "No reason provided."):

        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "❌ You don't have permission to use this command.",
                ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)

        try:
            await interaction.guild.ban(
                user, reason=reason, delete_message_days=delete_messages)
            await interaction.followup.send(
                f"✅ Successfully banned {user.name}. Deleted messages from the"
                f" last **{delete_messages} day(s)**.", ephemeral=True)
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
    async def user_unban(self,
                         interaction: discord.Interaction,
                         user_id: str):

        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "❌ You don't have permission to use this command.",
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
                "❗ Bot unable to unban UserID. Check permissions & role"
                " hierarchy",
                ephemeral=True)

        except discord.HTTPException as e:
            await interaction.followup.send(
                f"⚠️ An error occurred while unbanning: {e}", ephemeral=True)

        except Exception as e:
            print(f"Unexpected error in /unban: {e}")
            await interaction.followup.send(
                "⚠️ An unexpected error occurred while processing the unban"
                " request.",
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
    async def user_timeout(self,
                           interaction: discord.Interaction,
                           user: discord.Member,
                           duration: int,
                           reason: str = "No reason provided."):

        if not interaction.user.guild_permissions.moderate_members:
            await interaction.response.send_message(
                "❌ You don't have permission to use this command.",
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

    @app_commands.command(
            name="kick", description="Kicks select user from the discord.")
    @app_commands.guilds(GUILD_ID)
    @app_commands.describe(
        user="User to kick.",
        reason="Reason for the kick."
    )
    async def user_kick(self,
                        interaction: discord.Interaction,
                        user: discord.Member,
                        reason: str = "No reason provided."):

        if not interaction.user.guild_permissions.kick_members:
            await interaction.response.send_message(
                "❌ You don't have permission to use this command.",
                ephemeral=True)
            return

        try:
            await user.kick(reason=reason)
            await interaction.response.send_message(
                f"✅ Successfully kicked {user.name} \nReason: {reason}",
                ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message(
                "❌ You do not have permission to kick this user",
                ephemeral=True)
        except discord.HTTPException as e:
            await interaction.response.send_message(
                f"⚠️ An error occurred while kicking user: {e}",
                ephemeral=True)

    @app_commands.command(
            name="clear", description="Clear select messages from channel.")
    @app_commands.guilds(GUILD_ID)
    @app_commands.describe(
        user="Optional: Specify User messages to delete.",
        amount="Amount to delete."
    )
    async def clear(self,
                    interaction: discord.Interaction,
                    amount: int,
                    user: Optional[discord.Member] = None):

        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "❌ You don't have permission to use this command.",
                ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)

        def check(message: discord.Message):
            return user is None or message.author == user

        try:
            deleted = await interaction.channel.purge(
                limit=amount, check=check)
            target = f"from {user.mention}" if user else "from the channel"
            await interaction.followup.send(
                f"✅ Successfully deleted {len(deleted)} messages {target}.",
                ephemeral=True)
        except discord.Forbidden:
            await interaction.followup.send(
                "❌ You don't have permission to clear this channels messages.",
                ephemeral=True)
        except discord.HTTPException as e:
            await interaction.followup.send(
                f"⚠️ An error occurred while clearing messages: {e}",
                ephemeral=True)

    @app_commands.command(name="nickname", description="Change user nickname.")
    @app_commands.guilds(GUILD_ID)
    @app_commands.describe(
        user="User nickname to change.",
        nickname="Enter Nickname here."
    )
    async def user_nickname(self, interaction: discord.Interaction,
                            user: discord.Member,
                            nickname: str = None):

        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "❌ You don't have permission to use this command.",
                ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)

        try:
            await user.edit(nick=nickname)
            if nickname:
                msg = f"✅ Nickname for {user.mention}"
                f" changed to **{nickname}**."
            else:
                msg = f"✅ Nickname for {user.mention} has been reset."
            await interaction.followup.send(msg, ephemeral=True)

        except discord.Forbidden:
            await interaction.followup.send(
                "❌ You don't have permission to change that user's nickname.",
                ephemeral=True)
        except discord.HTTPException as e:
            await interaction.followup.send(
                f"⚠️ An error occorred while changing nickname: {e}",
                ephemeral=True)

    @app_commands.command(
            name="warn", description="Warn a user with a message.")
    @app_commands.guilds(GUILD_ID)
    @app_commands.describe(
        user="User to warn.",
        message="Enter warning message."
    )
    async def user_warn(self,
                        interaction: discord.Interaction,
                        user: discord.Member,
                        message: str):

        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "❌ You don't have permission to use this command.",
                ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)

        try:
            await interaction.channel.send(
                f"⚠️ {user.mention}, you have been warned by"
                f" {interaction.user.mention}: \n> {message}"
            )
            try:
                await user.send(
                    "You have received a warning in"
                    f" **{interaction.guild.name}**:\n> {message}"
                )
            except discord.Forbidden:
                await interaction.followup.send(
                    f"⚠️ Warned {user.mention}, but could not DM them.",
                    ephemeral=True
                )
            else:
                await interaction.followup.send(
                    f"✅ Successfully warned {user.mention} and sent them a DM."
                )

        except discord.Forbidden:
            await interaction.followup.send(
                "❌ You don't have permisison to warn that user.",
                ephemeral=True)
        except discord.HTTPException as e:
            await interaction.followup.send(
                f"⚠️ An error occurred while warning user: {e}",
                ephemeral=True)

    @app_commands.command(name="add_role", description="Add a role to a user.")
    @app_commands.guilds(GUILD_ID)
    @app_commands.describe(
        user="User to assign role to.",
        role="Role name to assign. ❗Reminder: Bot can not assign roles hire"
        " than itself."
    )
    async def user_addrole(self,
                           interaction: discord.Interaction,
                           user: discord.Member,
                           role: discord.Role):

        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "❌ You don't have permission to use this command.",
                ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)

        bot = interaction.guild.me
        if role >= bot.top_role:
            await interaction.followup.send(
                "❌ Role cannot be applied. Check bot role hierachy.")
            return

        if role in user.roles:
            await interaction.followup.send(
                f"❗{user.mention} already has the role {role.mention}.",
                ephemeral=True
            )
            return

        try:
            await user.add_roles(role)
            await interaction.followup.send(
                f"✅ Successfully added {role.mention} to {user.mention}.",
                ephemeral=True)
        except discord.Forbidden:
            await interaction.followup.send(
                "❌ You do not have permission to assign that role.",
                ephemeral=True)
        except discord.HTTPException as e:
            await interaction.followup.send(
                f"⚠️ An error occurred while assigning role: {e}",
                ephemeral=True)

    @app_commands.command(
            name="remove_role", description="Removes role from a user.")
    @app_commands.guilds(GUILD_ID)
    @app_commands.describe(
        user="User to remove role from.",
        role="Role name to remove. ❗Reminder: Bot can not remove roles hire"
        " than itself."
    )
    async def user_removerole(self,
                              interaction: discord.Interaction,
                              user: discord.Member,
                              role: discord.Role):

        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "❌ You don't have permission to use this command.",
                ephemeral=True
            )
            return

        await interaction.response.defer(ephemeral=True)

        bot = interaction.guild.me
        if role >= bot.top_role:
            await interaction.followup.send(
                "❌ Role cannot be removed. Check bot role hierachy.",
                ephemeral=True
            )
            return

        if role not in user.roles:
            await interaction.followup.send(
                f"❗ {user.mention} does not have the role {role.mention}.",
                ephemeral=True
            )
            return

        try:
            await user.remove_roles(role)
            await interaction.followup.send(
                f"✅ Successfully removed {role.mention} from {user.mention}.",
                ephemeral=True)
        except discord.Forbidden:
            await interaction.followup.send(
                "❌ You do not have permisison to remove that role.",
                ephemeral=True)
        except discord.HTTPException as e:
            await interaction.followup.send(
                f"⚠️ An error occurred while removing role: {e}",
                ephemeral=True
            )

    @app_commands.command(
            name="remove_allroles", description="Removes all roles from user.")
    @app_commands.guilds(GUILD_ID)
    @app_commands.describe(
        user="User to remove all roles from.",
        reason="Reason for role removal."
    )
    async def user_remove_allroles(self,
                                   interaction: discord.Interaction,
                                   user: discord.Member,
                                   reason: str = "No Reason was given."):

        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "❌ You don't have permission to use this command.",
                ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)

        bot = interaction.guild.me
        remove_roles = [
            role for role in user.roles
            if role != interaction.guild.default_role and role < bot.top_role
        ]

        if not remove_roles:
            await interaction.followup.send(
                f"❗ {user.mention} has no removable roles.",
                ephemeral=True)
            return

        try:
            await user.remove_roles(*remove_roles, reason=reason)
            await interaction.followup.send(
                f"✅ Successfully removed all roles from {user.mention}. \n"
                f"> **Reason:** {reason}"
            )
        except discord.Forbidden:
            await interaction.followup.send(
                "❌ You do not have permission to remove one or more roles.",
                ephemeral=True)
        except discord.HTTPException as e:
            await interaction.followup.send(
                f"⚠️ An error occurred while removing all roles: {e}",
                ephemeral=True)


async def setup(client):
    await client.add_cog(Moderation(client))

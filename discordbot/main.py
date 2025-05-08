"""
Main file for intial bot functionality.
Contains Bot StartUp, Guild Syncing, User Slash Commands.
"""
import os
import asyncio
import discord
from discord.ext import commands, tasks
from discord import app_commands  # noqa
from dotenv import load_dotenv
from itertools import cycle


# Loads .env file variables.
load_dotenv()

# Discord Bot setup for intent permissions.
# Allows Bot to utilize permissions given to it by Developer Portal.
intents = discord.Intents.default()
intents.message_content = True

# Contains Development Server ID.
GUILD_ID = discord.Object(id=382873288520499201)


class Client(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def setup_hook(self):
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                await self.load_extension(f"cogs.{filename[:-3]}")

        # Loads persistent views.
        self.add_view(ButtonArray())
        self.add_view(EmbedButton())

    async def on_ready(self):
        """
        When Bot successfully connects to discord this method is called.
        Attempts to sync all slash commands to development server.
        """
        print(f'Logged on as {self.user}!')

        try:
            guild = discord.Object(id=382873288520499201)
            synced = await self.tree.sync(guild=guild)
            print(f'Synced {len(synced)} commands to guild {guild.id}')

        except Exception as e:
            print(f'Error syncing commands: {e}')

        change_bot_status.start()

    async def on_reaction_add(self, reaction, user):
        """
        Handles message reactions.
        Responds with a message to every reaction.
        """
        await reaction.message.channel.send('You reacted!')


client = Client(command_prefix="!", intents=intents)

bot_status = cycle(
    [
        discord.Activity(
            type=discord.ActivityType.watching, name="over the server 👀"),
        discord.Activity(
            type=discord.ActivityType.listening, name="lofi beats 🎧"),
        discord.Activity(
            type=discord.ActivityType.playing, name="with Python 🐍"),
        discord.Activity(
            type=discord.ActivityType.competing, name="in bug fixing 💥"),
        discord.Activity(
            type=discord.ActivityType.watching, name="over your messages 👀"),
        discord.Activity(
            type=discord.ActivityType.listening, name="your commands 🔊"),
        discord.Activity(
            type=discord.ActivityType.competing, name="in uptime battles ⏱️"),
        discord.Activity(
            type=discord.ActivityType.playing, name="with Discord API ⚙️"),
        discord.Activity(
            type=discord.ActivityType.watching, name="the server logs 📜"),
        discord.Activity(
            type=discord.ActivityType.listening, name="bug reports 🐞"),
        discord.Activity(
            type=discord.ActivityType.watching, name="you 👁️"),
    ])


@tasks.loop(seconds=60)
async def change_bot_status():
    await client.change_presence(activity=next(bot_status))


# Slash command: /example_embed
@client.tree.command(name="example_embed",
                     description="Creates a embedded message.",
                     guild=GUILD_ID)
async def embed_example(interaction: discord.Interaction):
    # Grabs file from repository for Discord to use.
    bot_icon = discord.File("assets/icons/bot-icon1.png",
                            filename="bot-image1.png")
    embed = discord.Embed(title="This is the Title",
                          url="https://github.com/MarcusFDev/bot-project",
                          description="I am the description",
                          color=discord.Color.green())
    # Uses 'attachment://' to pull image file.
    embed.set_thumbnail(url="attachment://bot-image1.png")
    embed.add_field(name="Field 1 Title", value="Field One Contents",
                    inline=False)
    embed.add_field(name="Field 2 Title", value="Field Two Contents",
                    inline=True)
    embed.add_field(name="Field 3 Title", value="Field Three Contents",
                    inline=True)
    embed.set_footer(text="This is the footer")
    embed.set_author(name=interaction.user.name,
                     url="https://github.com/MarcusFDev/bot-project",
                     icon_url="attachment://bot-image1.png")
    await interaction.response.send_message(embed=embed, file=bot_icon)


# Slash command: /example_embed_large
@client.tree.command(name="example_embed_large",
                     description="Creates a maximum sized embedded message.",
                     guild=GUILD_ID)
async def embed_example_large(interaction: discord.Interaction):
    # Grabs file from repository for Discord to use.
    bot_icon = discord.File("assets/icons/bot-icon1.png",
                            filename="bot-icon1.png")
    camera_icon = discord.File("assets/icons/camera-icon1.png",
                               filename="camera-icon1.png")
    embed = discord.Embed(
        title="📗 **Title:** Maximum 256 characters.",
        url="https://github.com/MarcusFDev/bot-project",
        description=" **Description:** Maximum 4096 characters.\n"
                    "*The total characters a embedded message can have"
                    " is 6000.*",
        color=discord.Color.dark_orange())
    # Uses 'attachment://' to pull image file.
    embed.set_thumbnail(url="attachment://bot-icon1.png")
    embed.add_field(name="\u200b", value="\u200b", inline=False)
    embed.add_field(
        name="📖 **Field Title:** Maximum 256 characters.",
        value="✏️ **Field Content:** 1024 characters.\n\n"
              "*Total count of Fields allowed is 25!*",
        inline=False)

    embed.add_field(name="\u200b", value="\u200b", inline=False)
    embed.add_field(name="\u200b", value="\u200b", inline=False)

    embed.add_field(
        name="**❓ Quick Tip:**",
        value="- Using `\\u200b` makes invisible text allowing Field"
              " name & value to appear empty.\n"
              "- One Image (not including thumbnail) can be added to a"
              " embedded message using `.set_image(url=)`.",
        inline=False)
    embed.add_field(name="\u200b", value="\u200b", inline=False)

    embed.set_image(url="attachment://camera-icon1.png")

    embed.set_footer(text="Footer: Maximum 2048 characters.")
    embed.set_author(name="Author: Maximum 256 characters.",
                     url="https://github.com/MarcusFDev/bot-project",
                     icon_url="attachment://bot-icon1.png")
    await interaction.response.send_message(
        embed=embed, files=[bot_icon, camera_icon])


class ButtonArray(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(discord.ui.Button(
            label="Link Button",
            style=discord.ButtonStyle.link,
            emoji="🔗",
            url="https://github.com/MarcusFDev/bot-project"
        ))

    @discord.ui.button(label="Success Button",
                       style=discord.ButtonStyle.success,
                       emoji="⭐",
                       custom_id="persistent_success")
    async def button1_callback(self, button, interaction):
        await button.response.send_message(
            "You have clicked the ⭐ **Success button**!", ephemeral=True)

    @discord.ui.button(label="Danger Button",
                       style=discord.ButtonStyle.danger,
                       emoji="🔥",
                       custom_id="persistent_danger")
    async def button2_callback(self, button, interaction):
        await button.response.send_message(
            "You have clicked the 🔥 **Danger button**!", ephemeral=True)

    @discord.ui.button(label="Primary Button",
                       style=discord.ButtonStyle.primary,
                       emoji="🛡️",
                       custom_id="persistent_primary")
    async def button3_callback(self, button, interaction):
        await button.response.send_message(
            "You have clicked the 🛡️ **Primary button**!", ephemeral=True)

    @discord.ui.button(label="Secondary Button",
                       style=discord.ButtonStyle.secondary,
                       emoji="🔎",
                       custom_id="persistent_secondary")
    async def button4_callback(self, button, interaction):
        await button.response.send_message(
            "You have clicked the 🔎 **Secondary button**!", ephemeral=True)


# Slash command: /button_array
@client.tree.command(name="button_array",
                     description="Creates a selection of buttons.",
                     guild=GUILD_ID)
async def button_array(interaction: discord.Interaction):
    await interaction.response.send_message(view=ButtonArray())


class EmbedButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="See Example!",
                       style=discord.ButtonStyle.success,
                       emoji="🖼️",
                       custom_id="persistent_embedbutton")
    async def button1_callback(self, button, interaction):
        file = discord.File("assets/images/example-embed-btn.png",
                            filename="example-embed-btn.png")
        embed = discord.Embed(title="Here's your example!")
        embed.set_image(url="attachment://example-embed-btn.png")
        await button.response.send_message(embed=embed, file=file,
                                           ephemeral=True)


# Slash command: /example_embed_button
@client.tree.command(name="example_embed_button",
                     description="Creates a button on a embedded message.",
                     guild=GUILD_ID)
async def embedbtn_example(interaction: discord.Interaction):
    # Grabs file from repository for Discord to use.
    bot_icon = discord.File("assets/icons/bot-icon1.png",
                            filename="bot-icon1.png")
    embedbtn = discord.Embed(title="Embed with Button",
                             url="https://github.com/MarcusFDev/bot-project",
                             description="This is a button attached to a "
                                         "embedded message.",
                             color=discord.Color.pink())
    # Uses 'attachment://' to pull image file.
    embedbtn.set_thumbnail(url="attachment://bot-icon1.png")
    embedbtn.add_field(name="", value="**=============================**",
                       inline=False)
    embedbtn.add_field(name="How it works simplified:",
                       value="- Create a embed with `discord.Embed`.\n"
                             "- Create a class with `discord.ui.View`.\n"
                             "- Using `@discord.ui.button` customize"
                             " the button.\n"
                             "- Then pass both together in a interaction",
                       inline=False)
    embedbtn.add_field(name="", value="**=============================**",
                       inline=False)
    embedbtn.set_footer(text="Created with the Discord.py library.")
    embedbtn.set_author(name=interaction.user.name,
                        url="https://github.com/MarcusFDev/bot-project",
                        icon_url="attachment://bot-icon1.png")
    await interaction.response.send_message(
        view=EmbedButton(), embed=embedbtn, file=bot_icon)


# Retrieve & validate Private Token ID for Discord.
async def main():
    bot_token = os.getenv("BOT_TOKEN")
    if not bot_token:
        raise ValueError("⚠️ BOT_TOKEN is not set in the enviroment")
    async with client:
        await client.start(bot_token)

if __name__ == "__main__":
    asyncio.run(main())

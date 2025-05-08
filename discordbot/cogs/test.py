import discord # noqa
from discord import app_commands
from discord.ext import commands

# Contains Development Server ID.
GUILD_ID = discord.Object(id=382873288520499201)


class Test(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} is online!")

    @commands.Cog.listener()
    async def on_message(self, message):
        """
        Handles incoming messages.
        Ignores messages from the bot account itself.
        """
        if message.author == self.client.user:
            return

        if message.content.lower().startswith(("hello", "hey", "hi", "howdy")):
            await message.channel.send(f'Hi there {message.author}!')

    # Slash command: /hello
    @app_commands.command(name="hello", description="Say hello!")
    @app_commands.guilds(GUILD_ID)
    async def say_hello(self, interaction: discord.Interaction):
        await interaction.response.send_message("Hi there!")

    # Slash command: /printer
    @app_commands.command(name="printer",
                          description="I will print whatever you give me!")
    @app_commands.guilds(GUILD_ID)
    async def printer(self, interaction: discord.Interaction, printer: str):
        await interaction.response.send_message(printer)


async def setup(client):
    await client.add_cog(Test(client))

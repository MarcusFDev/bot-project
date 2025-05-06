"""
Main file for intial bot functionality.
Contains Bot StartUp, Guild Syncing, User Slash Commands.
"""
import os
import discord
from discord.ext import commands
from discord import app_commands # noqa
from dotenv import load_dotenv

# Loads .env file variables.
load_dotenv()


class Client(commands.Bot):
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

    async def on_message(self, message):
        """
        Handles incoming messages.
        Ignores messages from the bot account itself.
        """
        if message.author == self.user:
            return

        if message.content.startswith('hello'):
            await message.channel.send(f'Hi there {message.author}!')

    async def on_reaction_add(self, reaction, user):
        """
        Handles message reactions.
        Responds with a message to every reaction.
        """
        await reaction.message.channel.send('You reacted!')


# Discord Bot setup for intent permissions.
# Allows Bot to utilize permissions given to it by Developer Portal.
intents = discord.Intents.default()
intents.message_content = True
client = Client(command_prefix="!", intents=intents)

# Contains Development Server ID.
GUILD_ID = discord.Object(id=382873288520499201)


# Slash command: /hello
@client.tree.command(name="hello", description="Say hello!", guild=GUILD_ID)
async def say_hello(interaction: discord.Interaction):
    await interaction.response.send_message("Hi there!")


# Slash command: /printer
@client.tree.command(name="printer",
                     description="I will print whatever you give me!",
                     guild=GUILD_ID)
async def printer(interaction: discord.Interaction, printer: str):
    await interaction.response.send_message(printer)


# Slash command: /example_embed
@client.tree.command(name="example_embed",
                     description="Creates a embedded message.",
                     guild=GUILD_ID)
async def embed_example(interaction: discord.Interaction):
    # Grabs file from repository for Discord to use.
    bot_image = discord.File("assets/images/bot-image.png",
                             filename="bot-image.png")
    embed = discord.Embed(title="This is the Title",
                          url="https://github.com/MarcusFDev/bot-project",
                          description="I am the description",
                          color=discord.Color.green())
    # Uses 'attachment://' to pull image file.
    embed.set_thumbnail(url="attachment://bot-image.png")
    embed.add_field(name="Field 1 Title", value="Field One Contents",
                    inline=False)
    embed.add_field(name="Field 2 Title", value="Field Two Contents",
                    inline=True)
    embed.add_field(name="Field 3 Title", value="Field Three Contents",
                    inline=True)
    embed.set_footer(text="This is the footer")
    embed.set_author(name=interaction.user.name,
                     url="https://github.com/MarcusFDev/bot-project",
                     icon_url="attachment://bot-image.png")
    await interaction.response.send_message(embed=embed, file=bot_image)

# Retrieve & validate Private Token ID for Discord.
bot_token = os.getenv("BOT_TOKEN")
if not bot_token:
    raise ValueError("⚠️ BOT_TOKEN is not set in the enviroment")
else:
    client.run(bot_token)

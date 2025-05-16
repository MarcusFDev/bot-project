import discord # noqa
from main import GUILD_ID # noqa
from discord import app_commands # noqa
from discord.ext import commands


class Translate(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} is online!")


async def setup(client):
    await client.add_cog(Translate(client))

import os
import discord
from dotenv import load_dotenv

load_dotenv()


class Client(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        # Prevents bot responding to itself.
        if message.author == self.user:
            return

        if message.content.startswith('hello'):
            await message.channel.send(f'Hi there {message.author}!')

    async def on_reaction_add(self, reaction, user):
        await reaction.message.channel.send('You reacted!')


intents = discord.Intents.default()
intents.message_content = True


client = Client(intents=intents)

token = os.getenv("DISCORD_TOKEN")

if not token:
    raise ValueError("⚠️ DISCORD_TOKEN is not set in the enviroment")
else:
    client.run(token)

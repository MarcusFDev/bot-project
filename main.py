import os
import discord
from dotenv import load_dotenv

load_dotenv()


class Client(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')


intents = discord.Intents.default()
intents.message_content = True


client = Client(intents=intents)

token = os.getenv("DISCORD_TOKEN")

if not token:
    raise ValueError("⚠️ DISCORD_TOKEN is not set in the enviroment")
else:
    client.run(token)

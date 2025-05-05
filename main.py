import discord

class Client(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

intents = discord.Intents.default()
intents.message_content = True


client = Client(intents=intents)
client.run('MTM2ODg2Nzg3MTkyODYxNDk2Mg.GYh1Ks.mYGrcB7mWpC0Q87W4i-0tgIIzGvH5q7JZpVNk4')
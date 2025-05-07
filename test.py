# Used as Example Code for embeds with attached buttons.
"""
# Create Button View Class
class TestView(discord.ui.View):
    @discord.ui.button(label="", style=discord.ButtonStyle.blurple, emoji="")
    async def button_callback(self, button, interaction):
        await button.response.send_message("")

# Create slash command & embedded message.
@client.tree.command(name="", description="", guild=GUILD_ID)
async def example(interaction: discord.Interaction):
    embed = discord.Embed(title="", description="")
    embed.add_field(name="", value="")
    embed.set_footer(text="")
    await interaction.response.send_message(view=TestView(), embed=embed)

"""

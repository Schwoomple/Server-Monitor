import discord
from discord.ext import commands

with open("token.txt", "r", encoding="utf-8") as f:
    TOKEN = f.read().strip()
    
intents = discord.Intents.default()

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.tree.command(name="ping", description="Check if the bot is alive")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")
    
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    
    try:
        await bot.tree.sync()
        print("Slash commands synced.")
    except Exception as e:
        print(f"Slash command sync failed: {e}")
        
if __name__ == "__main__":
    if not TOKEN:
        raise SystemExit("Missing token in token.txt")
    bot.run(TOKEN)
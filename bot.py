import discord
from discord import app_commands
from discord.ext import commands

with open("token.txt", "r", encoding="utf-8") as f:
    TOKEN = f.read().strip()
    
with open("guild_id.txt", "r", encoding="utf-8") as f2:
    GUILD_ID = f2.read().strip()
    guild = discord.Object(id=GUILD_ID)
    
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

# Test ping command
@tree.command(name="ping", description="Check if the bot is alive")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")

# Add server command
@tree.command(name="addserver", description="Add a server to monitor")
@app_commands.describe(
    server_name="Name of the server",
    server_ip="IP address of the server",
    players="Current players (e.g., 0/16)"
)
async def addserver(interaction: discord.Interaction, server_name: str, server_ip: str, players: str):
    embed = discord.Embed(
        title=f"{server_name}",
        description=f"IP: {server_ip}",
        color=0x666df2
    )
    embed.add_field(name="Status", value="🟢 Online", inline=True)
    embed.add_field(name="Players", value=players, inline=True)

    # Step 1: acknowledge the command quietly
    await interaction.response.send_message(content="Thinking", ephemeral=True)

    # Step 2: delete that hidden ack so nothing lingers
    try:
        await interaction.delete_original_response()
    except:
        pass  # ignore if it fails (e.g. no perms)

    # Step 3: send only the embed visibly
    await interaction.channel.send(embed=embed)

# On ready
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    print(f"Guild ID: {GUILD_ID}")
    await tree.sync(guild=guild)
    print("Slash commands synced to test server.")

if __name__ == "__main__":
    if not TOKEN:
        raise SystemExit("Missing token in token.txt")
    bot.run(TOKEN)

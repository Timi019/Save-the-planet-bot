import discord,os,random
from discord.ext import commands
from discord import app_commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler

intents = discord.Intents.default()
# enable reading messages
intents.message_content = True
token = os.environ["TOKEN"]
bot = commands.Bot(command_prefix='/',intents=intents)
facts = [
    "Segreguj śmieci",
    "Oszczędzaj wodę",
    "Wybieraj odnawialne źródła energii"
]

@bot.event
async def on_ready():
    # Set up the hourly task 
    scheduler = AsyncIOScheduler() 
    scheduler.add_job(send_hourly_message, 'interval')
    scheduler.start() 
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
        print('bot is ready')
    except Exception as e:
        print(e)

@bot.tree.command(name='czesc')
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Cześć, {interaction.user.mention}!")

@bot.tree.command(name='gadaj')
@app_commands.describe(tekstdogadania = "Co mam powiedzieć?")
async def say(interaction: discord.Interaction, tekstdogadania: str):
    await interaction.response.send_message(f"{interaction.user.name} powiedział: {tekstdogadania}")

async def send_hourly_message(interaction: discord.Interaction):
    advice = random.choice(facts)
    await interaction.response.send_message(f"Oto godzinna wskazówka: {advice}")

@bot.tree.command(name='pa')
async def bye(interaction: discord.Interaction):
    await interaction.response.send_message(f"Żegnaj, {interaction.user.mention}!")

bot.run(token)
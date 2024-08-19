import discord,os,random
from discord.ext import commands
from discord import app_commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler

intents = discord.Intents.default()
# enable reading messages
intents.message_content = True
token = os.environ["TOKEN"]
bot = commands.Bot(command_prefix='/',intents=intents)
channel_id = 1275019583446843433
facts = [
    "Segreguj śmieci",
    "Oszczędzaj wodę",
    "Wybieraj odnawialne źródła energii"
]

async def send_hourly_message():
    advice = random.choice(facts)
    c = bot.get_channel(channel_id)
    await c.send(f"Oto godzinna wskazówka: {advice}")

@bot.event
async def on_ready():
    try:    
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
        print('bot is ready')
        #initializing scheduler
        scheduler = AsyncIOScheduler()

        #sends "s!t" to the channel when time hits 10/20/30/40/50/60 seconds, like 12:04:20 PM
        scheduler.add_job(send_hourly_message, 'interval', minutes=1) 

        #starting the scheduler
        scheduler.start()
    except Exception as e:
        print(e)

@bot.tree.command(name='czesc')
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Cześć, {interaction.user.mention}!")

@bot.tree.command(name='gadaj')
@app_commands.describe(tekstdogadania = "Co mam powiedzieć?")
async def say(interaction: discord.Interaction, tekstdogadania: str):
    await interaction.response.send_message(f"{interaction.user.name} powiedział: {tekstdogadania}")

@bot.tree.command(name='pa')
async def bye(interaction: discord.Interaction):
    await interaction.response.send_message(f"Żegnaj, {interaction.user.mention}!")

bot.run(token)
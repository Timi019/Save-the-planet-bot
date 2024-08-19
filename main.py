import discord,os,random
from discord.ext import commands
from discord import app_commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from model.model import detect_trash

intents = discord.Intents.default()
# enable reading messages
intents.message_content = True
token = os.environ["TOKEN"]
bot = commands.Bot(command_prefix='/',intents=intents)
earthot = bot.get_emoji(1275024848405532735)
channel_id = 1275019583446843433
facts = [
    "Ograniczaj, wykorzystuj ponownie i poddawaj recyklingowi. Ograniczaj to, co wyrzucasz. Postępuj zgodnie z zasadą trzech „R”, aby oszczędzać zasoby naturalne i miejsce na wysypiskach.",
    "Zostań wolontariuszem. Zgłoś się jako wolontariusz w akcjach sprzątania w swojej okolicy. Możesz również zaangażować się w ochronę pobliskich zbiorników wodnych.",
    "Edukuj. Kiedy rozwiniesz swoją wiedzę o ratowaniu planety, możesz pomóc innym zrozumieć znaczenie i wartość naszych zasobów naturalnych.",
    "Oszczędzaj wodę. Im mniej wody zużywasz, tym mniej spływu i ścieków ostatecznie trafia do oceanu.",
    "Kupuj rozważnie. Kupuj mniej plastiku i noś wielorazową torbę na zakupy.",
    "Używaj żarówek o długiej żywotności. Energooszczędne żarówki redukują emisję gazów cieplarnianych. Pamiętaj o wyłączeniu światłą, gdy wychodzisz z pokoju!",
    "Posadź drzewo. Drzewa dostarczają pożywienia i tlenu. Pomagają oszczędzać energię, oczyszczać powietrze i walczyć ze zmianą klimatu.",
    "Nie wlewaj chemikaliów do wody. Staraj się wybierać nietoksyczne chemikalia.",
    "Rower jest bardziej eko od pojazdów spalinowych. Jeździj nim więcej, aby walczyć ze zmianami klimatu.",
    "Jeśli to możliwe, używaj elektrycznych środków transportu lub komunikacji miejskiej."
]

async def send_hourly_message():
    advice = random.choice(facts)
    c = bot.get_channel(channel_id)
    await c.send(f"Oto godzinna wskazówka: {advice} Dbaj o planetę aby nie była <:earthot:1275024848405532735>")

@bot.event
async def on_ready():
    try:    
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
        print('bot is ready')
        #initializing scheduler
        scheduler = AsyncIOScheduler()

        #sends advice to the channel 
        scheduler.add_job(send_hourly_message, 'interval', hours=1) 

        #starting the scheduler
        scheduler.start()
    except Exception as e:
        print(e)

@bot.tree.command(name='witaj')
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Cześć, {interaction.user.mention}!")

@bot.tree.command(name='gadaj')
@app_commands.describe(tekstdogadania = "Co mam powiedzieć?")
async def say(interaction: discord.Interaction, tekstdogadania: str):
    await interaction.response.send_message(f"{interaction.user.mention} powiedział: {tekstdogadania}")

@bot.tree.command(name='pomocy')
async def help(interaction: discord.Interaction):
    advice = random.choice(facts)
    await interaction.response.send_message(f"Oto twoja wskazówka: {advice} Dbaj o planetę aby nie była <:earthot:1275024848405532735>!")

@bot.tree.command(name='gdzie_wrzucic')
async def check(interaction: discord.Interaction, attachment: discord.Attachment):
    name = attachment.filename
    await attachment.save(name)
    result = detect_trash(name, "model/keras_model.h5", "model/labels.txt")
    con_score = result[1] * 100
    result = result[0].strip()
    if int(con_score) >= 50:
        if result == "czerwonego":
            await interaction.response.send_message(f"Jestem na {con_score}% pewny, że możesz wrzucić to do czerwonego lub żółtego pojemnika.")
        else:
            await interaction.response.send_message(f"Jestem na {con_score}% pewny, że powinieneś wrzucić to do {result} pojemnika.")
    else:
        await interaction.response.send_message("Nie jestem pewny gdzie to wyrzucić :(")
    os.remove(name)

@bot.tree.command(name='pa')
async def bye(interaction: discord.Interaction):
    await interaction.response.send_message(f"Żegnaj, {interaction.user.mention}!")

bot.run(token)
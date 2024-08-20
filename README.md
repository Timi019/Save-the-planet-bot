# Save-the-planet-bot
## Discord bot to help you save the planet

This bot will help you with saving the environment by sending some advice to you

- code from my other repo: [Discord-bot](https://github.com/Timi019/Discord-bot)
- advice from https://oceanservice.noaa.gov/ocean/earthday.html

---

## Setup guide

1. Firstly I recommend having python 3.11
2. Open a terminal and type: `pip install -r requirements.txt`
3. Go to the **.envv** file and change its name to **.env**
4. Go to [Discord Developer Portal](https://discord.com/developers/applications) and create an app
5. Grab the token and paste it into **.env** file
6. Enable all *Privileged Gateway Intents*
7. Go to OAuth2 tab scroll down and select **bot** then scroll down more and select **Administrator**
8. Grab the link from the bottom and paste it into new window
9. Select the server you want the bot to be in
10. Copy the channel id you want your advice to be in
11. Run the file with: `python3 main.py`
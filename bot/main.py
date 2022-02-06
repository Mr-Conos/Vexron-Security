import disnake
import os
from dotenv import load_dotenv
from addon import Vexron

intents = disnake.Intents(members = True, guilds = True, messages = True)
load_dotenv()
bot_data = {
    "intents": intents,
    "token": os.getenv("THE_TOKEN")
}
bot = Vexron(**bot_data)


bot.starter()
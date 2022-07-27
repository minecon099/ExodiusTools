from os import environ
from dotenv import load_dotenv

load_dotenv()
TOKEN = environ.get("TOKEN")

from nextcord.ext.commands import Bot

bot = Bot(command_prefix="ex!")

#Disable extensions with commentaries.
bot.load_extension("images")
bot.load_extension("fun")
bot.load_extension("presence")
#bot.load_extension("music")
#bot.load_extension("roleplay")  A wild new extension has appeared! - Can you guess what we are using?

bot.run(TOKEN)

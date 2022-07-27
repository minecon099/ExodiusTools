from nextcord import Activity, ActivityType
from nextcord.ext.commands import Bot, Cog

print("Module presence.py loaded.")

class presence(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @Cog.listener()
    async def on_ready(self) -> None:
        await self.bot.change_presence(activity=Activity(name="with the dev's time :D", type=ActivityType.playing))

def setup(bot: Bot) -> None:
    bot.add_cog(presence(bot))
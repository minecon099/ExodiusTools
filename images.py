from nekosbest import Client

from nextcord import Interaction, slash_command, embeds
from nextcord.ext.commands import Bot, Cog

Neko = Client()

print("Module images.py loaded.")

class images(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @slash_command(
        name="neko",
        description="Get a random Neko Image (SFW ofc).",
        default_member_permissions=None,
    )
    async def neko(self, inter: Interaction) -> None:

        #Get the respective values:
        neko_image = await Neko.get_image(category="neko")

        #Build the Embed
        NekoEmbed = embeds.Embed(color=0xe303fc, title=f"Imwage Sowuce", url=neko_image.url)
        NekoEmbed.set_image(url=neko_image.url)
        NekoEmbed.set_footer(text="Powered by Nekos.best API Wrapper")

        await inter.send(embed=NekoEmbed)

    @slash_command(
        name = "waifu",
        description = "Get a random Waifu Image (SFW ofc).",
        default_member_permissions = None,
    )
    async def waifu(self, inter: Interaction) -> None:
        #Get the respective values:
        waifu_image = await Neko.get_image(category="waifu")
    
        #Build the Embed
        WaifuEmbed = embeds.Embed(color=0xe303fc, title=f"Image Source", url=waifu_image.url)
        WaifuEmbed.set_image(url=waifu_image.url)
        WaifuEmbed.set_footer(text="Powered by Nekos.best API Wrapper")
    
        await inter.send(embed=WaifuEmbed)
    
    @slash_command(
        name = "kitsune",
        description = "Get a random Kitsune Image (SFW ofc).",
        default_member_permissions = None,
    )
    async def kitsune(self, inter: Interaction) -> None:
        #Get the respective values:
        kitsune_image = await Neko.get_image(category="kitsune")
    
        #Build the Embed
        KitsuneEmbed = embeds.Embed(color=0xe303fc, title=f"Image source", url=kitsune_image.url)
        KitsuneEmbed.set_image(url=kitsune_image.url)
        KitsuneEmbed.set_footer(text="Powered by Nekos.best API Wrapper")
    
        await inter.send(embed=KitsuneEmbed)

def setup(bot: Bot) -> None:
    bot.add_cog(images(bot))

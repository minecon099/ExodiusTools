import random
import randfacts
import aiohttp

from nextcord import Interaction, slash_command, embeds, SlashOption, VoiceChannel #Ignore VoiceChannel if you want, it will be used in the future though.
from nextcord.ext.commands import Bot, Cog
from nextcord.ext import activities #Trust me, you'll need this in a future update.
from dadjokes import Dadjoke

print("Module fun.py loaded.")

class fun(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
    
    @slash_command(
        name="ping",
        description="Simple Ping-Pong command, also returns response time in ms.",
        default_member_permissions=None,
    )
    async def Ping(self, inter: Interaction) -> None:
        await inter.send(f"Pong! - Response time: {self.bot.latency * 1000:.2f}ms 🏓")
    
    @slash_command(
        name="dadjoke",
        description="Only the best dadjokes. Get one, then laugh.",
        default_member_permissions=None,
    )
    async def dadjoke(self, inter: Interaction):
        message = Dadjoke()
        await inter.send(message.joke)

    @slash_command(
        name="8ball",
        description="Magic 8-Ball, ask a question and get a random answer.",
        default_member_permissions=None,
    )
    async def eightball(self, inter: Interaction, question: str) -> None:
        answers = ['It is certain.',
        'It is decidedly so.',
        'Without a doubt.',
        'Yes - definitely.',
        'You may rely on it.',
        'As I see it, yes.',
        'Most likely.',
        'Outlook good.',
        'Yes.', 'Signs point to yes.',
        'Reply hazy, try again.',
        'Ask again later.',
        'Better not tell you now.',
        'Cannot predict now.',
        'Concentrate and ask again.',
        'Don\'t count on it.',
        'My reply is no.',
        'My sources say no.',
        'Outlook not so good.',
        'Very doubtful.']

        embed8Ball = embeds.Embed(title="Exodius Bot's Magic 8 Ball:", color=0xe303fc)
        embed8Ball.add_field(name="Your question:",value=question,inline=False)
        embed8Ball.add_field(name="Answer:",value=f"🎱 {random.choice(answers)}",inline=False)
        await inter.send(embed=embed8Ball)
    
    @slash_command(
        name="choose",
        description="I'll choose a random between number 1 and the number of your choice.",
        default_member_permissions=None,
    )
    async def choose(self, inter: Interaction, max_number: int = SlashOption(description="The highest number to choose (Cannot be greater than 10000).")) -> None:
        if max_number <= 0:
            await inter.send("You can't choose a negative number.")
        elif max_number <= 1:
            await inter.send("You can't choose a number less than 1.")
        elif max_number >= 10001:
            await inter.send("You can't choose a number greater than 10000.")
        else:
            await inter.send(f"🎲 I choose {random.randint(1, max_number)}")

    @slash_command(
        name="randomfact",
        description="Get a random fact from anything at all. Really, anything.",
        default_member_permissions=None,
    )
    async def randomfact(self, inter: Interaction) -> None:
        await inter.send(randfacts.get_fact())
    
    @slash_command(
        name="rock",
        description="Get a random image of a rock. Either drawn, real photos, I dunno.",
        default_member_permissions=None,
    )
    async def rock(self, inter: Interaction) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://rockapi.apiworks.tech/rock/random") as resp:
                data = await resp.json()

                rock_name = data["name"]
                rock_desc = data["desc"]
                rock_image = data["image"]

                embed = embeds.Embed(title=rock_name, description=rock_desc, color=0xe303fc)
                embed.set_image(url=rock_image)

                await inter.send(embed=embed)
    
    @slash_command(
        name="randomcolor",
        description="Get a random color in RGB and HEX code.",
        default_member_permissions=None,
    )
    async def randomColor(self, inter: Interaction) -> None:

        #Get random RGB values
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)

        #Convert to HEX
        hex_color = f"{r:02x}{g:02x}{b:02x}" #string
        

        #Display RGB and HEX values in an Embed and make the embed's color with the color generated
        ColorEmbed = embeds.Embed(color=int(hex_color, 16))
        ColorEmbed.add_field(name="HEX", value=f"#{hex_color}", inline=False)
        ColorEmbed.add_field(name="RGB", value=f"{r}, {g}, {b}", inline=False)

        await inter.send(embed=ColorEmbed)

def setup(bot: Bot) -> None:
    bot.add_cog(fun(bot))

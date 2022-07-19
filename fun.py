import random
import randfacts
import aiohttp

from nextcord import Interaction, slash_command, embeds
from nextcord.ext.commands import Bot, Cog
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
    async def eightball(self, inter: Interaction) -> None:
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

        await inter.send(f"🎱 {random.choice(answers)}")
    
    @slash_command(
        name="choose",
        description="I'll choose a random between number 1 and the number of your choice.",
        default_member_permissions=None,
    )
    async def choose(self, inter: Interaction, max_number: int) -> None:
        if max_number is None:
            await inter.send("You didn't choose a number.")
        elif max_number <= 0:
            await inter.send("You can't choose a negative number.")
        elif max_number <= 1:
            await inter.send("You can't choose a number less than 1.")
        elif max_number >= 10000:
            await inter.send("You can't choose a number greater than 10000.")
        else:
            await inter.send(f"🎲 I choose {random.randint(1, max_number)}")

    @slash_command(
        name="randomfact",
        description="Get a random fact from anything at all. Really, anything.",
        default_member_permissions=None,
    )
    async def randfact(self, inter: Interaction) -> None:
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
                rock_desc = data["description"]
                rock_image = data["image"]

                embed = embeds.Embed(title=rock_name, description=rock_desc, color=0xe303fc)
                embed.set_image(url=rock_image)

                await inter.send(embed=embed)
                

def setup(bot: Bot) -> None:
    bot.add_cog(fun(bot))
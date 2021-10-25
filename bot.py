#Import modules, in this case we will need Discord, Discord commands handler, Dadjokes (For joke command), Random for 8ball 
#command, Requests for APIs usage and JSON for APIs responses reading

#You may also add more modules if you want to add even more things to your bot

#Remember to do pip install (module) before running this or you won't be able to start your bot!

import discord
import random
import requests
import json
from dadjokes import Dadjoke
from discord.ext import commands

#The bot's prefix, you may change it at your own will
client = commands.Bot(command_prefix = 'ex!')

#Using the ZenQuotes API to request a quote from the API
def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return(quote)

#Print that the bot has logged in successfully if there are no errors during the bot's startup
@client.event
async def on_ready():
    print('I have logged on Discord with Sucess!')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.competing, name="against DayMines",   ))

#The classic one, ping pong command
@client.command(aliases=['p'])
async def ping(ctx):
    await ctx.send('Pong!')

#8ball command using the random module and Glowstik's 8ball answers (modified for no self-promo)
@client.command(aliases=['8ball', '8b'])
async def _8ball(ctx, *, question):
    responses = [
        'Hell no.',
        'Prolly not.',
        'Idk bro.',
        'Prob.',
        'Hell yeah my dude.',
        'It is certain.',
        'It is decidedly so.',
        'Without a Doubt.',
        'Yes - Definitaly.',
        'You may rely on it.',
        'As i see it, Yes.',
        'Most Likely.',
        'Outlook Good.',
        'Yes!',
        'No!',
        'Signs a point to Yes!',
        'Reply Hazy, Try again.',
        'idk',
        'Better not tell you know.',
        'Cannot predict now.',
        'Concentrate and ask again.',
        "Don't Count on it.",
        'My reply is No.',
        'My sources say No.',
        'Outlook not so good.',
        'Very Doubtful']
    await ctx.send(f':8ball: Question: {question}\n:8ball: Answer: {random.choice(responses)}')

#Kick a member
@client.command()
async def kick(ctx, member:discord.Member, *, reason=None):
    if (not ctx.author.guild_permissions.kick_members):
        await ctx.send('You require the permission: ``Kick Members``')
    
    else:
        await member.kick(reason=reason)
        await ctx.send(f'{member.mention} has been kicked!')

#Ban a user (or yeet it for more simpler terms)
@client.command(aliases=['yeet'])
async def ban(ctx, member:discord.Member, *, reason=None):
    if (not ctx.author.guild_permissions.ban_members):
        await ctx.send('You require the permission: ``Ban Members``')

    else:
        await member.ban(reason=reason)
        await ctx.send(f'{member.mention} has been yeeted!')

#Unban a user (or forgive him)
@client.command(aliases=['forgive'])
async def unban(ctx, *, member):
    if (not ctx.author.guild_permissions.ban_members):
        await ctx.send('You require the permission: ``Ban Members``')
    
    else:
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if(user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'Unbanned {user.mention}')
                return

#Purge the called channel for a max of 100 messages (You may change it to whatever you need)
@client.command(aliases=['purge'])
async def clear(ctx, amount=11):
    if (not ctx.author.guild_permissions.manage_messages):
        await ctx.send('You require the permission: ``Manage Messages``')
    amount = amount+1
    if amount > 101:
        embed_purge=discord.Embed(title="I cannot delete more than 100 messages!", color=0xe303fc)
        await ctx.send(embed=embed_purge)
    else:
        await ctx.channel.purge(limit=amount)
        embed_purge_sucess=discord.Embed(title="Sucessfully deleted {amount} messages!")
        await ctx.send(embed=embed_purge_sucess)

#Using ZenQuotes.io API
@client.command(aliases=['phrase'])
async def inspire(ctx):
    quote = get_quote() #Use function get_quote()
    embed_quote=discord.Embed(title="Inspirational Quote for you!", description=quote, colour=0xe303fc)
    await ctx.send(embed=embed_quote)

#Uses DadJokes API Wrapper module
@client.command(aliases=['joke'])
async def dadjoke(ctx):
    dadjoke = Dadjoke() #Gather a random Joke from import Dadjoke
    embed_joke=discord.Embed(title="Random Joke:", description=dadjoke.joke, color=0xe303fc)
    await ctx.send(embed=embed_joke)

#My community server, you aren't forced to join but I usually give support to new users of the bot
@client.command(aliases=['community'])
async def server(ctx):
    community_embed=discord.Embed(title="Join our community Server!", description="You can join our community server by clicking the title in this embed! - We have a Minecraft Server and a friendly community!", color=0xe303fc, url="https://dsc.gg/drkmines")
    await ctx.send(embed=community_embed)

#Just mere self-promo about the release, but it would be rad if you kept this lines alone
@client.command(aliases=['invitebot'])
async def invite(ctx):
    embed_invite=discord.Embed(title="Invite the bot", description="Currently Exodius Tools is restricted to this Guild only, in a future however it will be available for all Discord Guilds to be invited", color=0xe303fc)
    embed_invite.set_author(text="minecon099", icon_url="https://avatars.githubusercontent.com/u/74718722?v=4")
    embed_invite.add_field(name="Why? - I like this bot and I need it!", value="Despite your valuable interest, this bot won't be availble to everyone to use until we release ourselves in Top.gg and we finish our desired features", inline=False)
    embed_invite.add_field(name="Do you have any release time?", value="There is no ETA on when will we be 100% complete, but you will know it when you find Exodius Bot on Top.gg page ;)", inline=False)
    embed_invite.add_field(name="Can I be a testing Guild?", value="We will soon release a testing Guilds program for partenered people with the Bot's owner and we will soon release the bot on a limited quantity of guilds, right now we will see about it :P", inline=False)
    embed_invite.set_footer(text="Expected ETA: Early 2022")
    await ctx.send(embed=embed_invite)

#Replace BOTTOKEN with your own token, you can gather it on discord.com/developers/applications
client.run('BOTTOKEN')

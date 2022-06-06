#Warning! - This code is the last update of the Prefix Based Version of Exodius Tools as of June 6th 2022. Code may contain errors or unintended behavior, by using this
#           code, you assume everything that will happen after using it. - In sumarry, this version is deprecated and it's usage is under your own responsability.

#Import modules, in this case we will need Discord, Discord commands handler, Dadjokes (For joke command), Random for 8ball 
#command, Requests for APIs usage and JSON for APIs responses reading

#You may also add more modules if you want to add even more things to your bot

#Remember to do pip install (module) before running this or you won't be able to start your bot!

import random
import requests
import json
import time
import asyncio
import datetime
import os
import nextcord
import randfacts
import urllib
import nacl

#This is to keep your token safe
from dotenv import load_dotenv

from dadjokes import Dadjoke
from PIL import Image
from io import BytesIO
from nextcord.ext import commands
from nekosbest import Client

os.chdir('D:\ExodiusTools')

#Load your 'TOKEN' from an .env file
load_dotenv()

nekoclient = Client()
client = commands.Bot(command_prefix = 'ex!')
client.remove_command('help')

def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return(quote)

def convert(time):
    pos = ["s","m","h","d"]

    time_dict = {"s" : 1, "m" : 60, "h" : 3600, "d" : 3600*24}

    unit = time[-1]

    if unit not in pos:
        return -1
    try:
        val = int(time[:-1])
    except:
        return -2
    

    return val * time_dict[unit]

@client.event
async def on_ready():
    print('I have logged on nextcord with Sucess!')
    await client.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.playing, name=f"With {len(client.guilds)} Guilds!"))

@client.command(aliases=['p'])
async def ping(ctx):
    await ctx.send('Pong!')

@client.command(aliases=['8ball', '8b'])
async def eightball(ctx, *, question = None):
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

    if question == None:
        await ctx.send(":8ball: I don't see any question to answer")
    
    else:
        await ctx.send(f':8ball: Question: {question}\n:8ball: Answer: {random.choice(responses)}')

@client.command()
async def kick(ctx, member : nextcord.Member, *, reason=None):
    if (not ctx.author.guild_permissions.kick_members):
        await ctx.send('You require the permission: ``Kick Members``',delete_after=5)
    
    else:
        await member.kick(reason=reason)
        await ctx.semd(f'{member.mention} has been kicked!')

@client.command(aliases=['yeet'])
async def ban(ctx, member : nextcord.Member, *, reason=None):
    if (not ctx.author.guild_permissions.ban_members):
        await ctx.send('You require the permission: ``Ban Members``')

    else:
        await member.ban(reason=reason)
        await ctx.send(f'{member.mention} has been yeeted/banned!')

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

@client.command(aliases=['purge'])
async def clear(ctx, amount=11):
    if (not ctx.author.guild_permissions.manage_messages):
        await ctx.send('You require the permission: ``Manage Messages``')
    amount = amount+1
    if amount > 101:
        embed_purge=nextcord.Embed(title="I cannot delete more than 100 messages!", color=0xe303fc)
        await ctx.send(embed=embed_purge)
    else:
        await ctx.channel.purge(limit=amount)

@client.command(aliases=['phrase'])
async def inspire(ctx):
    quote = get_quote()
    embed_quote=nextcord.Embed(title="Inspirational Quote for you!", description=quote, colour=0xe303fc)
    await ctx.send(embed=embed_quote)

@client.command(aliases=['joke'])
async def dadjoke(ctx):
    dadjoke = Dadjoke()
    embed_joke=nextcord.Embed(title="Random Joke:", description=dadjoke.joke, color=0xe303fc)
    await ctx.send(embed=embed_joke)

#Uncomment this if you'd like to keep the community server command.
#@client.command(aliases=['community'])
#async def server(ctx):
#    community_embed=nextcord.Embed(title="Join our community Server!", description="You can join our community server by clicking the title in this embed! - We have a Minecraft Server and a friendly community!", color=0xe303fc, url="https://dsc.gg/drkmines")
#    await ctx.send(embed=community_embed)

#This is the whole giveaway section
@client.command(aliases=['raffle'])

@commands.has_role("Giveaways")

async def giveaway(ctx):
    await ctx.send("Let's begin with the Giveaway! - Answer this three question within 15 seconds!")

    questions = ["Where should we host the giveaway?", 
                "How much time will the giveaway last? - (s|m|h|d)",
                "What is the prize for this giveaway?"]

    answers = []

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    for i in questions:
        await ctx.send(i)

        try:
            msg = await client.wait_for('message', timeout=15.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send("You haven't answered in time, giveaway cancelled :/")
            return
        else:
            answers.append(msg.content)
    
    try:
        c_id = int(answers[0][2:-1])
    except:
        await ctx.send(f"You haven't mentioned a channel properly - Do it like this: {ctx.channel.mention} next time!")
        return

    channel = client.get_channel(c_id)

    time = convert(answers[1])
    if time == -1:
        await ctx.send(f"You haven't answered the time with a proper unit! - Use ((s)econds|((m)inutes)|((h)ours)|((d)ays)")
        return
    elif time == -2:
        await ctx.send(f"The time must be a Number (Integer) - Please enter a Number next time!")
        return
    prize = answers[2]

    await ctx.send(f"The Giveaway will be hosted on {channel.mention} and will last {answers} seconds ")

    embed_giveaway = nextcord.Embed(title="Giveaway!", description=f"{prize}", color=0xe303fc)
    embed_giveaway.add_field(name="Hosted by:", value=ctx.author.mention)
    embed_giveaway.set_footer(text=f"Ends {answers[1]} from now!")

    giveaway_msg = await channel.send(embed=embed_giveaway)
    await giveaway_msg.add_reaction("🎉")

    await asyncio.sleep(time)

    new_giveaway_msg = await channel.fetch_message(giveaway_msg.id)

    users = await new_giveaway_msg.reactions[0].users().flatten()
    users.pop(users.index(client.user))

    winner = random.choice(users)

    await channel.send(f"Congratulations {winner.mention} has won **{prize}**")
#This is the end of the Giveaway command :P

#Now we do a reroll command which is less complicated:
@client.command(aliases=["replay"])
@commands.has_role("Giveaways")
async def reroll(ctx, channel : nextcord.TextChannel, id_ : int):
    try:
        new_msg = await channel.fetch_message(id_)
    except:
        await ctx.send("You have entered an invalid id :(")
        return

    users = await new_msg.reactions[0].users().flatten()
    users.pop(users.index(client.user))

    winner = random.choice(users)

    await channel.send(f"The new winner of the Giveaway is {winner.mention}")  

@client.command(aliases=['flipacoin','coin'])
async def coinflip(ctx):
    coinflip = ['Head','Tails']
    choice = random.choice(coinflip)

    coinflipEmbed = nextcord.Embed(title=f"The coin says: {choice} :coin:", color=0xe303fc)
    await ctx.send(embed=coinflipEmbed)

@client.command()
async def dice(ctx):
    dice_values = ['1','2','3','4','5','6']
    dice_choice = random.choice(dice_values)

    diceEmbed = nextcord.Embed(title=f"The dice has rolled a: {dice_choice} :game_die:", color=0xe303fc)
    await ctx.send(embed=diceEmbed)

@client.command(aliases=['silence'])
async def mute(ctx, member : nextcord.Member, *, reason=None):
    if (not ctx.author.guild_permissions.manage_messages):
        await ctx.send("You require the permission: ``Manage Messages``")
        return
    guild = ctx.guild
    muterole = nextcord.utils.get(guild.roles, name="Muted")

    if not muterole:
        await ctx.send("Muted role was not found, creating one for you...")
        muteRole = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(muteRole, speak=False, send_messages=False, read_message_history=False, read_messages=True)
        await member.add_roles(muteRole, reason=reason)
        mutedEmbed = nextcord.Embed(title=f"Successfully muted {member}", color=0xe303fc)
        await ctx.send(embed=mutedEmbed)
        await member.send(f"You have been muted from **{guild.name}** for the reason: **{reason}**")
    
@client.command(aliases=['unsilence'])
async def unmute(ctx, member : nextcord.Member):
    if (not ctx.author.guild_permissions.manage_messages):
        await ctx.send("You require the permission ``Manage Messages``")
        return
    guild  = ctx.guild
    mutedRole = nextcord.utils.get(guild.roles, name="Muted")

    if not mutedRole:
        await ctx.send("Muted role wasn't found :(")
        return
    
    await member.remove_roles(mutedRole)
    unmuteEmbed = nextcord.Embed(title=f"{member} has been unmuted", color=0xe303fc)
    await ctx.send(embed=unmuteEmbed)
    await member.send(f"You have been unmuted from **{guild.name}**")

#You'll need a specific image and PIL to use this. The image has been added to the repository as well.
@client.command(aliases=['ifearnoman'])
async def fear(ctx, member : nextcord.Member = None):
    if member == None:
        member = ctx.author
    
    ifearnoman = Image.open('ifearnoman.jpg')

    asset = member.avatar_url_as(size = 128)
    data = BytesIO(await asset.read())
    profile_picture = Image.open(data)

    profile_picture = profile_picture.resize((300, 300))

    ifearnoman.paste(profile_picture, (414, 377))

    ifearnoman.save('generated_ifearnoman.jpg')

    await ctx.send(file = nextcord.File('generated_ifearnoman.jpg'))

    os.remove('generated_ifearnoman.jpg')

@client.command(aliases=['getthebanana'])
async def banana(ctx, member : nextcord.Member = None):
    if member == None:
        await ctx.send("Try this command again, but mentioning a user on it")
        return
    else:
        bananaEmbed = nextcord.Embed(description=f"{ctx.author} told {member} to get the banana!", color=0xe303fc)
        bananaEmbed.set_image(url="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/a2e157a4-66f9-4d47-ac14-3376f5330cfb/deruqto-b5bfed3a-7bfc-4d19-bcda-a1861f8202b9.gif?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiJcL2ZcL2EyZTE1N2E0LTY2ZjktNGQ0Ny1hYzE0LTMzNzZmNTMzMGNmYlwvZGVydXF0by1iNWJmZWQzYS03YmZjLTRkMTktYmNkYS1hMTg2MWY4MjAyYjkuZ2lmIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.PVvXOAKctRS1EpSdsYPXlSi9jKcXK6kM22TCQhTFEz0")
        await ctx.send(embed=bananaEmbed)

@client.command(pass_context=True)
async def help(ctx, *, choice = 1):
    if choice == 1:
        helpEmbed = nextcord.Embed(title="All the Current commands!", color=0xe303fc)
        helpEmbed.add_field(name="These are all the available commands for Exodius Tools as December 13 2021", value="**General Commands:**\n`ex!help` Displays this message\n`ex!ping` Simple, no need to explain\n\n**Moderation Commands:**\n`ex!kick` Kick a member from this guild, requires permission `Kick Members`\n`ex!ban` Bans a user, requires permission `Ban Members`\n`ex!unban` Unbans a member, requires permission `Ban Members`\n`ex!clear (number)` Clears messages, defaulted to 11 messages if a number is not given\n`ex!mute` Mute a user, cannot mute users on a higher hierarchy\n\n**Fun Commands:**\n`ex!eightball` Not sure on something? - Ask the 8 Ball!\n`ex!inspire` Grabs a random quote from ZenQuotes.io API\n`ex!dadjoke` Only the best Dad Jokes :)\n`ex!coinflip` Flip a coin, no mystery\n`ex!dice` Roll a 6 faces dice\n`ex!neko` Display a random neko image (SFW)\n`ex!meme` Get a random meme from all Reddit\n\n**Giveaway Commands:**\n`ex!giveaway` Requires a role named Giveaways\n`ex!reroll (channel id) (message id)` Reroll a giveaway, requires Giveaways role and Channel and Message ID")
        helpEmbed.set_footer(text="Page (1/2)")
        await ctx.send(embed=helpEmbed)
    else:
        await ctx.send("I have no idea what page are you trying to look, attempt with a valid number instead!")

@client.command(aliases=['randomneko'])
async def neko(ctx):
    nekoIMG = await nekoclient.get_image(category="neko")
    nekoEmbed = nextcord.Embed(title=f"Made by {nekoIMG.artist_name}", color=0xe303fc)
    nekoEmbed.set_thumbnail(url=nekoIMG.url)
    nekoEmbed.set_footer(text=f"Image Source: {nekoIMG.source_url}")
    await ctx.send(embed=nekoEmbed)

@client.command(aliases=['randomfact'])
async def randfact(ctx):
    fact = randfacts.get_fact()
    randomFact = nextcord.Embed(title="Random fact:", description=fact, color=0xe303fc)
    await ctx.send(embed=randomFact)

@client.command(aliases=['speak'])
async def say(ctx, *, text = None):
    if text == None:
        await ctx.send("What do you want me to say, nothing?")
        return
    else:
        await ctx.send(text)

@client.command()
async def meme(ctx):
    memeApi = urllib.request.urlopen("https://meme-api.herokuapp.com/gimme")

    memeData = json.load(memeApi)

    memeUrl = memeData['url']
    memeName = memeData['title']
    memeAuthor = memeData['author']
    memeSub = memeData['subreddit']
    memeLink = memeData['postLink']

    memeEmbed = nextcord.Embed(title=memeName, colour=0xe303fc)
    memeEmbed.set_image(url=memeUrl)
    memeEmbed.set_footer(text=f"Meme by: {memeAuthor} | Subreddit: {memeSub} | Post: {memeLink}")
    await ctx.send(embed=memeEmbed)

#Music Section Test:
@client.command(aliases=['connect'])
async def join(ctx):
    voicetrue = ctx.author.voice
    if voicetrue is None:
        notJoinEmbed = nextcord.Embed(title="You are not connected to a Voice Channel", colour=0xe303fc)
        notJoinEmbed.set_footer(text="Connect to a voice channel so I can join!")
        return await ctx.send(embed=notJoinEmbed)

    await ctx.author.voice.channel.connect()
    connectEmbed = nextcord.Embed(title="Joined you your current Voice Channel", colour=0xe303fc)
    connectEmbed.set_footer(text="Try out playing some music!")
    await ctx.send(embed=connectEmbed)

@client.command(aliases=['leave'])
async def disconnect(ctx):
    voicetrue = ctx.author.voice
    mevoicetrue = ctx.guild.me.voice
    if voicetrue is None:
        notVC = nextcord.Embed(title="You are not in a Voice Channel", color=0xe303fc)
        notVC.set_footer(text="Tried connecting in the VC I'm on?")
        return await ctx.send(embed=notVC)
    if mevoicetrue is None:
        notPlaying = nextcord.Embed(title="I am not playing music here", color=0xe303fc)
        notPlaying.set_footer(text="Tried connecting me to a VC?")
        return await ctx.send(embed=notPlaying)
    await ctx.voice_client.disconnect()

    disconnectEmbed = nextcord.Embed(title="Disconnected from your Voice Channel", color=0xe303fc)
    disconnectEmbed.set_footer(text="See you next music session!")
    await ctx.send(embed=disconnectEmbed)

#Instructions:
#1. Create a file that ends in ".env" (AKA Enviroment Variable file)
#2. Edit it with notepad and add "TOKEN=[Token goes here]" with your bot token.
#3. Reload the bot.
client.run(os.getenv('TOKEN'))

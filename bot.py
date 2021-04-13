#Bot made by minecon09
#Version released at April 13, 2020

#Note that the Bot Token is replaced as TOKEN so you can test with your OWN TOKEN
#Channel id is replaced as ChannelID so you can replace it with your OWN CHANNEL ID

#Import Discord Package
import discord

#Client (Actual Bot)
client = discord.Client()

@client.event
async def on_ready():
    #Actions

    general_channel = client.get_channel(ChannelID)
    await general_channel.send("Change this in bot.py")

@client.event
async def on_message(message):
    
    if message.content == "version":
        general_channel = client.get_channel(ChannelID)
        await general_channel.send("Bot Version is 1.0 ALPHA")

#Run the bot
client.run("TOKEN")

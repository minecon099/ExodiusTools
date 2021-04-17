#Bot made by minecon09
#Version released at April 13, 2020

#Note that the Bot Token is replaced as Token goes here! so you can test with your OWN TOKEN
#Channel id is replaced as ChannelID so you can replace it with your OWN CHANNEL ID

#Import Packages
import discord
from discord.ext import commands

#The bot itself
client = commands.Bot(command_prefix="tt!")

#Print a succesful execution if no exeptions were raised:
print("The bot has been successfully settled in discord!")

#Actions:
#Prefix usage example:
@client.command(name="version")
async def version(context):
        
     general_channel = client.get_channel("Main ID channel here too")
        
     embed1 = discord.Embed(title="Versión Actual:", description="DJ Tetra está en la versión ALPHA 1.1", color=0x00ff00)
     embed1.add_field(name="Versión por código:", value="1.0.0", inline=False)
     embed1.add_field(name="Fecha de lanzamiento", value="17 de Abril del 2021", inline=False)
     embed1.set_footer(text="Visita mi Página de desarrollo con tt!github")
     embed1.set_author(name="Pogamepayer#3492")

     await context.message.channel.send(embed=embed1)
    
#Upon bot connects
@client.event
async def on_ready():

    general_channel = client.get_channel("Main channel ID Goes here as well")

    await general_channel.send("Me he conectado con éxito al servidor :green_circle:")

#Upon bot disconnects
@client.event
async def on_disconnect():
     general_channel = client.get_channel("Main channel ID Goes here too!")

     await general_channel.send("Me estoy desconectando, Buenas Noches :red_circle:")

#Upon specific message ("Version")
@client.event
async def on_message(message):
    
    if message.content == "version":
        general_channel = client.get_channel("Main channel ID Goes here!")
        
        embed1 = discord.Embed(title="Versión Actual:", description="DJ Tetra está en la versión ALPHA 1.1", color=0x00ff00)
        embed1.add_field(name="Versión por código:", value="1.0.0", inline=False)
        embed1.add_field(name="Fecha de lanzamiento", value="17 de Abril del 2021", inline=False)
        embed1.set_footer(text="Visita mi Página de desarrollo con tt!github")
        embed1.set_author(name="Pogamepayer#3492")

        await general_channel.send(embed=embed1)
    
    #Enables compartibility between commands and messages 
    await client.process_commands(message)

#Run the bot:
client.run("Token goes here!")

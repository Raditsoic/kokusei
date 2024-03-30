import discord
import discord.ext.commands as cex
import os
from dotenv import load_dotenv
import asyncio
import requests

def get_prefix(bot: cex.Bot, message: discord.Message):
    guild_id = str(message.guild.id)
    api_url = f"http://localhost:3000/guild/{guild_id}"
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()

        data = response.json()
        guild_prefix = data.get("prefix", "!")
        return guild_prefix
    except requests.RequestException as e:
        print(f"Error: Requesting Guild Prefix 404")
        return "!"
 
       
load_dotenv()
TOKEN = os.getenv("TOKEN")
intents = discord.Intents.all()
intents.message_content = True
client = cex.Bot(command_prefix=get_prefix, intents=intents)

client.remove_command("help")

@client.event
async def on_ready():
    await client.tree.sync()
    print("Booting up Kokusei...")

async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await client.load_extension(f"cogs.{filename[:-3]}")
            
async def main():
    async with client:
        await load()
        await client.start(TOKEN)
    
if __name__ == '__main__':
    asyncio.run(main())
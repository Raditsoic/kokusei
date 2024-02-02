import discord
import discord.ext.commands as cex
import os
from dotenv import load_dotenv
import asyncio
from database import Database

db = Database()
def get_server_prefix(client, message):
    return db.get_prefix(message.guild.id)

load_dotenv()
TOKEN = os.getenv("TOKEN")
intents = discord.Intents.all()
intents.message_content = True
client = cex.Bot(command_prefix=get_server_prefix, intents=intents)

client.remove_command("help")

async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await client.load_extension(f"cogs.{filename[:-3]}")
            
async def main():
    await load()
    await client.start(TOKEN)
    
if __name__ == '__main__':
    asyncio.run(main())
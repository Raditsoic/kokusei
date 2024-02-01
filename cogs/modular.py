import discord
from discord.ext import commands
from database import Database
import json

class Modular(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.db = Database()
        
    @commands.Cog.listener()
    async def on_ready(self):
        user = str(self.client.user)
        username = user[:-5]
        print("Commands Available")
        await print(f'{username} is now online')
        
        
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        default_prefix = '!'
        await self.db.set_prefix(guild.id, default_prefix)
            
    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        await self.db.remove_prefix(guild.id)

async def setup(client):
    await client.add_cog(Modular(client))
            
import discord
from discord.ext import commands
import requests

class Modular(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("Success: Modular Cog is active...")
        
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        default_prefix = '!'
        api_url = 'http://localhost:3000/guild'
        
        data = {
            "id": f"{guild.id}",
            "name": f"{guild.name}",
            "prefix": default_prefix
        }
        
        try:
            response = await requests.post(api_url, json=data)
            response.raise_for_status()
            print("Successfully POST guild data")
        except requests.RequestException as e:
            print("Error: Failed to POST guild data, {e}")
            
    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        api_url = f"http://localhost:3000/guild/{guild.id}"
        
        try:
            response = await requests.delete(api_url)
            response.raise_for_status()
            print("Successfully DELETE guild data")
        except requests.RequestException as e:
            print("Error: Failed to DELETE guild data, {e}")
        
    @commands.Cog.listener()
    async def on_member_join(self, ctx, member: discord.Member):
        await ctx.send(f"Konnichiwa {member.mention}!! Welcome to {ctx.guild.name}")

async def setup(client):
    await client.add_cog(Modular(client))
            
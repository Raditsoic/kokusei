from discord.ext import commands
import discord
from dotenv import load_dotenv
import os
import requests as r
import json

class Responses(commands.Cog):
    def __init__(self, client):
        self.client = client
        load_dotenv()
        
    @commands.Cog.listener()
    async def on_ready(self):
        await print("Success: Response Cog is active...")
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return
        
        print(f"Message from {message.author}: {message.content}")
        
        content = message.content.lower()
        bad_words = ['fuck', 'shit', 'bitch']
        
        for word in bad_words:
            if word in content:
                await message.channel.send("Don't use bad words plss!!!")
                break

        # Important: allows command processing to still work
        await self.client.process_commands(message)     
        
async def setup(client):
    await client.add_cog(Responses(client))
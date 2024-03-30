from discord.ext import commands
from dotenv import load_dotenv
import discord
import os
import requests

async def get_server_prefix(bot, message):
    api_url = f'http://localhost:3000/guild/{str(message.guild.id)}'

    try:
        response = await requests.get(api_url)
        response.raise_for_status()

        data = response.json()
        guild_prefix = data.get("prefix", "!")
        return guild_prefix
    except requests.RequestException as e:
        print(f"Error: error in getting prefix, {e}")

class Command(commands.Cog):
    def __init__(self, client):
        self.client = client
        load_dotenv()
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("Success: Commands Cog is active...")
        
    @commands.command()
    async def shutdown(self, ctx):
        owner_id = int(os.getenv("OWNER_ID"))
        if ctx.author.id == owner_id:
            print(f"Shutting down...")
            await self.client.close()
            
    @commands.command()
    async def prefix(self, ctx):
        await ctx.send(self.client.command_prefix)
            
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setprefix(self, ctx, *, new_prefix):
        api_url = f'http://localhost:3000/guild/{ctx.guild.id}'

        new_data = {
            "id": str(ctx.guild.id),
            "name": str(ctx.guild.name),
            "prefix": new_prefix
        }
        
        try:
            response = requests.put(api_url, json=new_data)
            response.raise_for_status()
        except requests.RequestException as e:
            return await ctx.send(f"Error: in setting prefix, {e}")
        await ctx.send(f"Prefix has successfully been set to: {new_prefix}")
        self.client.change_prefix(get_server_prefix)
        
            
    @commands.command(aliases=['whois', 'who'])
    async def userinfo(self, ctx, member:  discord.Member=None):
        if member is None:
            member = ctx.author
            
        embed = discord.Embed(title="User Information", description=f"Here is the user information of {member.global_name}", color =  discord.Color.dark_blue(), timestamp=ctx.message.created_at)
        embed.add_field(name="Username", value=member.name, inline=True)
        embed.add_field(name="Nickname", value=member.global_name, inline=True)
        embed.add_field(name="Joined At", value=member.joined_at.strftime("%d %B %Y"))
        embed.add_field(name="Created At", value=member.created_at.strftime("%d %B %Y"), inline=True)
        embed.set_thumbnail(url=member.avatar)
        embed.set_footer(text=f"Powered by {ctx.bot.user.name}")
        await ctx.send(embed=embed)
        
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, msgcount:int=2):
        await ctx.channel.purge(limit=msgcount)
        await ctx.send(f"{msgcount if msgcount != 2 else msgcount - 1} message(s) has been deleted.")
        
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, reason):
        await ctx.guild.kick(member)
        await ctx.send(f"{member.name} has been kicked for {reason}.")
        
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, reason):
        await ctx.guild.ban(member)
        await ctx.send(f"{member.name} has been banned for {reason}.")
        
    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingFlagArgument):
            await ctx.send(f"Usage: !kick <member>")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(f"You don't have the permission to kick member(s).")
            
    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingFlagArgument):
            await ctx.send(f"Usage: !ban <member>")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(f"You don't have the permission to ban member(s).")
            
    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingFlagArgument):
            await ctx.send(f"Usage: !clear <messageCount>")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(f"You don't have the permission to clear messages")
            
    @setprefix.error
    async def setprefix_error(self, ctx, error):
        if isinstance(error, commands.MissingFlagArgument):
            await ctx.send(f"Usage: !setprefix <newprefix>")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(f"You don't have the permission to set new prefix")
        
async def setup(client):
    await client.add_cog(Command(client))
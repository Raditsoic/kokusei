from discord.ext import commands
from dotenv import load_dotenv
from database import Database
import discord
import os

class Command(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.db = Database()
        self.bot_name = os.getenv('BOT_NAME')
        load_dotenv()
        
    @commands.command()
    async def ping(self, ctx):
        bot_latency = round(self.client.latency * 1000)
        await ctx.send(f"Konnichiwa!! {bot_latency} ms.")
        
    @commands.command()
    async def shutdown(self, ctx):
        owner_id = int(os.getenv("OWNER_ID"))
        if ctx.author.id == owner_id:
            print(f"Shutting down...")
            await self.client.close()
            
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setprefix(self, ctx, *, new_prefix):
        self.db.set_prefix(ctx.guild.id, new_prefix)
        await ctx.send(f"Prefix has successfully been set to: {new_prefix}")
            
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
        embed.set_footer(text=f"Powered by {self.bot_name}")
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
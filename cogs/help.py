import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(title="Help", description="All commands:", color=discord.Color.random(), timestamp=ctx.message.created_at)
        embed.set_author(name=ctx.bot.user.name, icon_url=ctx.bot.user.avatar)
        embed.add_field(name="prefix", value=f"The currect prefix is {self.client.command_prefix(self.client, ctx.message)}")
        embed.add_field(name="ping", value=f"Pings {ctx.bot.user.name}", inline=False)
        embed.add_field(name="setprefix", value=f"Sets a new command prefix to this server. **!setprefix <newprefix>**", inline=False)
        embed.add_field(name="userinfo", value="Get member details by ID or mention. **!who/!whois/!userinfo <member>**", inline=False)
        embed.add_field(name="clear", value="Clear previous messages. **!clear <messages_count>**", inline=False)
        embed.add_field(name="kick", value="Kick a member from this server. **!kick <member> <reason>**", inline=False)
        embed.add_field(name="ban", value="Ban a member from this server. **!ban <member> <reason>**", inline=False)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar)
        await ctx.send(embed=embed)
        
async def setup(client):
    await client.add_cog(Help(client))
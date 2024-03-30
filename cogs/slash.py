import discord
from discord.ext import commands
from discord import app_commands

class Slash(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.tree.sync()
        print("Success: Slash Cog is active...")
           
    @app_commands.command(name="ping", description="Shows bot current latency in ms.")
    async def ping(self, interaction:discord.Interaction):
        bot_latency = round(interaction.client.latency * 1000)
        await interaction.response.send_message(f"Pong! Bot latency is `{bot_latency}`ms")
        
    @app_commands.command(name="coinflip", description="Flip a Coin.")
    async def coinflip(self, interaction:discord.Interaction):
        import random
        coin = ["Head","Tail"]
        await interaction.response.send_message(f"Your coin is {random.choice(coin)}!!")
        
    @app_commands.command(name="roulette", description="Spin a Roulette.")
    async def roulette(self, interation:discord.Interaction, low:int=0, high:int=100):
        import random
        await interation.response.send_message(f"You got {random.randint(low, high)}!!")
        
    @app_commands.command(name="whois", description="Display user information.")
    async def whois(self, interaction:discord.Interaction, user:discord.Member):
        roles = [role.name for role in user.roles]
        embed = discord.Embed(title=user.display_name, color= discord.Color.dark_blue(), timestamp=interaction.created_at)
        embed.add_field(name="Username", value=user.name, inline=True)
        embed.add_field(name="Joined At", value=user.joined_at.strftime("%d %B %Y"))
        embed.add_field(name="Created At", value=user.created_at.strftime("%d %B %Y"), inline=True)
        embed.add_field(name="Roles", value=", ".join(roles) if roles else "No roles", inline=True)
        embed.set_thumbnail(url=user.avatar)
        embed.set_footer(text=f"Powered by {self.bot.user.name}")
        await interaction.response.send_message(embed=embed)
        
    @app_commands.command(name="help", description="Display Kokusei commands.")
    async def help(self, interaction:discord.Interaction, optional:str=None):
        embed = discord.Embed(title="Kokusei", color=discord.Color.random(), timestamp=interaction.created_at)
        embed.add_field(name="**/ping**", value=f"Pings Kokusei.", inline=True)
        embed.add_field(name="**/whois**", value="Display user information.", inline=True)
        embed.add_field(name="**/coin**", value="Flip a coin.", inline=True)
        embed.add_field(name="**/roulette**", value="Spin a roulette.", inline=True)
        embed.set_footer(text=f"Powered by {self.bot.user.name}")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        
    @app_commands.command(name="quote", description="Get an Anime Quote.")
    async def quote(self, interaction:discord.Interaction):
        #Get Random Quote from animechan
        import requests, json
        req = requests.get("https://animechan.xyz/api/random")
        content = req.content.decode("utf-8")
        data = json.loads(content)
        character = data['character']
        anime = data['anime']
        quote = data['quote']
        
        #Get Character image from Jikan
        data = requests.get(f'https://api.jikan.moe/v4/characters?q="{character}"')
        character_data = data.json()
        character_data = character_data['data']
        
        embed = discord.Embed(title=anime, timestamp=interaction.created_at, color=discord.Color.random())
        if character_data != []:
            character_data = character_data[0]
            image_url = character_data['images']['jpg']['image_url']
            embed.set_thumbnail(url=image_url)
        embed.add_field(name="", value=f"{quote} - **{character}**")
        embed.set_footer(text="Powered by Animechan & Jikan")
        await interaction.response.send_message(embed=embed)
        
    @app_commands.command(name="clear", description="Clear message(s).")
    async def clear(self, interaction:discord.Interaction, count:int=2):
        await interaction.channel.purge(limit=count)
        await interaction.response.send_message(f"{count if count != 2 else count - 1} message(s) has been deleted.")
        
    @app_commands.command(name="chara", description="Get anime character biodata.")
    async def chara(self, interaction:discord.Interaction, character:str):
        import requests
        data = requests.get(f'https://api.jikan.moe/v4/characters?q="{character}"')
        character_data = data.json()
        character_data = character_data['data']
        
        if character_data != []:  
            character_data = character_data[0]
            image_url = character_data['images']['jpg']['image_url']
            name = character_data['name']
            kanji_name = character_data['name_kanji']
            about_section = character_data['about'].split('\n')
            about = {}
            for line in about_section:
                if ':' in line:
                    key, value = line.split(':', 1)
                    about[key.strip()] = value.strip()
  
            embed = discord.Embed(title=name, timestamp=interaction.created_at, color=discord.Color.random())
            embed.add_field(name="Kanji", value=kanji_name)
            for info, val in about.items():
                if val == "":
                    continue
                embed.add_field(name=info, value=val)
            embed.set_thumbnail(url=image_url)
            embed.set_footer(text='Powered by Jikan')
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(f"There is no character with the name of **{character}**.")
        
        
async def setup(client):
    await client.add_cog(Slash(client))
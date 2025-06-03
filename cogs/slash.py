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
        print("test")
        print(user)
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
    @app_commands.describe(
        anime="Anime name (optional)",
        character="Character name (optional)",
        random="Set to false if you want to filter by anime or character"
    )
    async def quote(self, interaction:discord.Interaction, anime:str=None, character:str=None, random:bool=True):
        import requests

        base_url = "https://api.animechan.io/v1/quotes"

        if random:
            url = f"{base_url}/random"
            params = {}
        elif anime and character:
            url = f"{base_url}/quotes"
            params = {"anime": anime, "character": character}
        elif anime:
            url = f"{base_url}/quotes"
            params = {"anime": anime}
        elif character:
            url = f"{base_url}/quotes"
            params = {"character": character}
        else:
            url = f"{base_url}/random"
            params = {}

        response = requests.get(url, params=params)
        
        if response.status_code != 200:
            await interaction.response.send_message("Failed to fetch quotes.")
            return
        
        data = response.json()
        print(f"Response Data: {data}")  # Debugging line to check the response data
        
        if not data:
            await interaction.response.send_message("No quotes found.")
            return
        
        data = data.get('data', {})  # Handle both single quote and list of quotes
        
        quote = data.get('content')
        character = data['character']['name']
        anime = data['anime']['name']

        print(f"Quote: {quote}, Character: {character}, Anime: {anime}")  # Debugging line to check the quote details
        
        embed = discord.Embed(
            title="Anime Quote",
            timestamp=interaction.created_at,
            color=discord.Color.light_grey()
        )
        embed.add_field(
            name="Quote",
            value=f"\"{quote}\"\n— **{character}**, *{anime}*",
            inline=False
        )
        embed.set_footer(text="Powered by Animechan")
        
        try:
            await interaction.response.send_message(embed=embed)
        except discord.HTTPException:
            await interaction.response.send_message("The character's information is too long to display.")
        
    @app_commands.command(name="clear", description="Clear message(s).")
    async def clear(self, interaction:discord.Interaction, count:int=2):
        await interaction.channel.purge(limit=count)
        await interaction.response.send_message(f"{count if count != 2 else count - 1} message(s) has been deleted.")
        
    @app_commands.command(name="chara", description="Get anime character biodata.")
    async def chara(self, interaction:discord.Interaction, character:str):
        import requests
        data = requests.get(f'https://api.jikan.moe/v4/characters?q="{character}"')

        if data.status_code != 200:
            await interaction.response.send_message("Failed to fetch character info.")
            return
        
        character_data = data.json().get('data', [])
        if not character_data:
            await interaction.response.send_message(f"There is no character with the name of **{character}**.")
            return
        
        character_data = character_data[0]
        image_url = character_data['images']['jpg']['image_url']
        name = character_data['name']
        kanji_name = character_data.get('name_kanji', "Unknown")
        about = character_data.get('about', 'No description available.')
        about = about[:128] + '...' if len(about) > 128 else about

        embed = discord.Embed(title=name, timestamp=interaction.created_at, color=discord.Color.random())
        embed.add_field(name="Kanji", value=kanji_name)
        embed.add_field(name="About", value=about[:1024])
        embed.set_thumbnail(url=image_url)
        embed.set_footer(text='Powered by Jikan')
        
        try:
            await interaction.response.send_message(embed=embed)
        except discord.HTTPException:
            await interaction.response.send_message("The character's information is too long to display.")    

    @app_commands.command(name="ask", description="Ask a question to Kokusei.")
    async def ask(self, interaction: discord.Interaction, question:str):
        import random
        answers = [
            "Yes, definitely.",
            "No, not at all.",
            "Maybe, who knows?",
            "Absolutely!",
            "I wouldn't count on it.",
            "It's possible.",
            "Ask again later.",
            "I'm not sure, try again.",
            "The answer is unclear, try again."
        ]
        response = random.choice(answers)
        await interaction.response.send_message(f"**Question:** {question}\n**Answer:** {response}")
        
        
async def setup(client):
    await client.add_cog(Slash(client))
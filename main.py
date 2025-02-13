import discord
from discord.ext import commands
import random
from pato_utils import constants, memes

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'{bot.user.name} está online!')

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

@bot.command()
async def fernando(ctx):
    await ctx.send('Viva ao Rei Fernando!')

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("Tens de estar num canal de voz para me chamar!")

@bot.command()
async def leave(ctx):
    voice_client = ctx.guild.voice_client
    if voice_client:
        await voice_client.disconnect()
    else:
        await ctx.send("Eu não estou ligado a nenhum canal de voz.")

@bot.command()
async def meme(ctx):
    await ctx.send(random.choice(memes.memes_list))

bot.run(constants.DISCORD_KEY)
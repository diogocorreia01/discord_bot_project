import discord
from discord.ext import commands
import random
from pato_utils import constants
import requests
from gtts import gTTS
import os
import yt_dlp

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'{bot.user.name} está online!')

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

@bot.command()
async def fernando(ctx):
    await ctx.send(constants.FERNANDO)

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
    response = requests.get(constants.MEME_API)
    memes = response.json()['data']['memes']
    meme = random.choice(memes)
    await ctx.send(f"Meme: {meme['name']}\nURL: {meme['url']}")

@bot.command()
async def speak(ctx, *, texto: str):
    # Verificar se o utilizador está num canal de voz
    if ctx.author.voice:
        # Obtem o canal de voz do utilizador
        channel = ctx.author.voice.channel
        voice_client = ctx.guild.voice_client

        # Se o bot já tiver conectado, usa a conexão existente
        if not voice_client:
            voice_client = await channel.connect()
        elif voice_client.channel != channel:
            await voice_client.move_to(channel)

        # Gera o áudio com o Google TTS
        tts = gTTS(text=texto, lang='pt-pt')
        tts.save("text.mp3")

        # Reproduz o áudio no canal de voz
        ffmpeg_path = constants.FFMPEG_PATH
        voice_client.play(discord.FFmpegPCMAudio("text.mp3", executable=ffmpeg_path))

        # Aguarda a reprodução terminar
        while voice_client.is_playing():
            await discord.utils.sleep_until(discord.utils.utcnow())

        # Remove o ficheiro de áudio após reprodução
        os.remove("text.mp3")

    else:
        await ctx.send("Tens de estar num canal de voz para eu falar!")

@bot.command()
async def play(ctx, url: str):
    # Verifica se o bot está no canal de voz
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        voice_client = ctx.guild.voice_client

        if not voice_client:
            voice_client = await channel.connect()
        elif voice_client.channel != channel:
            await voice_client.move_to(channel)

        # Configura as opções do yt-dlp
        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'quiet': True,
            'extractaudio': True,
            'audioformat': 'mp3',
            'outtmpl': 'song.%(ext)s',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            song_url = info['url']

        # Reproduz o áudio do YouTube no canal de voz
        ffmpeg_path = constants.FFMPEG_PATH
        voice_client.play(discord.FFmpegPCMAudio(song_url, executable=ffmpeg_path))

        await ctx.send(f'A tocar: {info["title"]}')
    else:
        await ctx.send("Tens de estar num canal de voz para tocar a música!")

bot.run(constants.DISCORD_KEY)
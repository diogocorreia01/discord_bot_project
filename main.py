import discord
from discord.ext import commands
import random
from pato_utils import constants
import requests
from gtts import gTTS
import os
from pato_utils.voice import VoiceManager
from pato_utils.trivia import TriviaGame

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

voice_manager = VoiceManager(bot)
trivia_game = TriviaGame(bot)

@bot.event
async def on_ready():
    print(f'{bot.user.name} está online!')

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

@bot.command()
async def join(ctx):
    """Comando para o bot entrar num canal de voz"""
    await voice_manager.join_voice_channel(ctx)

@bot.command()
async def leave(ctx):
    """Comando para o bot sair de um canal de voz"""
    await voice_manager.leave_voice_channel(ctx)

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
async def start_trivia(ctx, difficulty: str):
    """Starts a trivia game with the chosen difficulty."""
    await trivia_game.start_game(ctx, difficulty.lower())

@bot.command()
async def answer(ctx, *, player_answer: str):
    """Processes a player's answer to the current trivia question."""
    await trivia_game.process_answer(ctx, player_answer)

@bot.command()
async def stop_trivia(ctx):
    """Stops the current trivia game manually."""
    await trivia_game.stop_game(ctx)

bot.run(constants.DISCORD_KEY)
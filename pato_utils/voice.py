import os
import gtts
from discord.ext import commands
import discord

class VoiceManager:
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def join_voice_channel(self, ctx):
        """Faz o bot entrar no canal de voz onde o autor está."""
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            voice_client = ctx.guild.voice_client

            # Se o bot já estiver no canal, move-o
            if not voice_client:
                await channel.connect()
            elif voice_client.channel != channel:
                await voice_client.move_to(channel)
            await ctx.send(f"🔊 Connected to channel: {channel.name}")
        else:
            await ctx.send("❌ You need to be in a voice channel to summon me!")

    async def leave_voice_channel(self, ctx):
        """Faz o bot sair do canal de voz."""
        voice_client = ctx.guild.voice_client
        if voice_client:
            await voice_client.disconnect()
            await ctx.send("👋 Disconnected from the voice channel!")
        else:
            await ctx.send("❌ I am not in any voice channel.")

    async def speak(self, ctx, text: str, lang: str = "en"):
        """Converts text to speech and plays it in the voice channel."""
        if ctx.voice_client is None:
            await self.join_voice_channel(ctx)

        tts = gtts.gTTS(text, lang=lang)
        filename = "speech.mp3"
        tts.save(filename)

        voice_client = ctx.voice_client
        if voice_client.is_playing():
            await ctx.send("⏳ Please wait, I am already speaking!")
            return

        voice_client.play(discord.FFmpegPCMAudio(filename), after=lambda e: os.remove(filename))
        await ctx.send(f"🗣️ Speaking in `{lang}`: {text}")
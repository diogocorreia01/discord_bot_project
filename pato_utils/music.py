import discord
from discord.ext import commands
import yt_dlp as youtube_dl

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_clients = {}

    async def join_voice(self, ctx):
        """Makes the bot join the user's voice channel."""
        if ctx.author.voice is None:
            await ctx.send("❌ You must be in a voice channel to use this command.")
            return

        channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            self.voice_clients[ctx.guild.id] = await channel.connect()
        else:
            await ctx.voice_client.move_to(channel)

    async def leave_voice(self, ctx):
        """Makes the bot leave the current voice channel."""
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            self.voice_clients.pop(ctx.guild.id, None)
        else:
            await ctx.send("❌ I am not connected to a voice channel.")

    async def play_music(self, ctx, url):
        """Plays music from a YouTube URL."""
        await self.join_voice(ctx)

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'socket_timeout': 60,
            'quiet': True,
            'noplaylist': True,
            'nocheckcertificate': True,
        }

        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                url2 = info['url']
        except Exception as e:
            await ctx.send(f"❌ An error occurred: {str(e)}")
            return

        voice_client = ctx.voice_client
        if voice_client.is_playing():
            await ctx.send("❌ I am already playing music!")
            return

        voice_client.play(discord.FFmpegPCMAudio(url2), after=lambda e: print(f"Finished playing: {e}"))
        await ctx.send(f"🎵 Now playing: **{info['title']}**")

    async def stop_music(self, ctx):
        """Stops music playback."""
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send("⏹️ Music stopped.")
        else:
            await ctx.send("❌ No music is currently playing.")

    async def pause_music(self, ctx):
        """Pauses the current music."""
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send("⏸️ Music paused.")
        else:
            await ctx.send("❌ No music is currently playing.")

    async def resume_music(self, ctx):
        """Resumes paused music."""
        if ctx.voice_client and ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send("▶️ Music resumed.")
        else:
            await ctx.send("❌ No music is currently paused.")
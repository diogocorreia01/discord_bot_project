from discord.ext import commands

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
            await ctx.send(f"🔊 Conectado ao canal: {channel.name}")
        else:
            await ctx.send("❌ Você precisa estar num canal de voz para me chamar!")

    async def leave_voice_channel(self, ctx):
        """Faz o bot sair do canal de voz."""
        voice_client = ctx.guild.voice_client
        if voice_client:
            await voice_client.disconnect()
            await ctx.send("👋 Desconectado do canal de voz!")
        else:
            await ctx.send("❌ Não estou em nenhum canal de voz.")

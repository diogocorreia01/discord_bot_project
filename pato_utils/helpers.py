import discord
from discord.ext import commands

class HelpCommand:
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def show_help(self, ctx):
        """Displays an interactive help menu with all bot commands."""
        embed = discord.Embed(
            title="📖 Pato Help Menu",
            description="Here are all the commands you can use:",
            color=discord.Color.blue()
        )

        embed.add_field(
            name="🎵 Music Commands",
            value=(
                "`!play <url>` - Play music from a YouTube URL.\n"
                "`!pause` - Pause the current music.\n"
                "`!resume` - Resume the paused music.\n"
                "`!stop` - Stop the music.\n"
            ),
            inline=False
        )

        embed.add_field(
            name="🔊 Voice Commands",
            value=(
                "`!join` - Make the bot join your voice channel.\n"
                "`!leave` - Disconnect the bot from the voice channel.\n"
                "`!speak <lang> <text>` - Make the bot say something in a specific language."
            ),
            inline=False
        )

        embed.add_field(
            name="🧠 Trivia Commands",
            value=(
                "`!start_trivia <easy/hard>` - Start a trivia game.\n"
                "`!answer <your answer>` - Submit an answer to the trivia question.\n"
                "`!stop_trivia` - Stop the trivia game."
            ),
            inline=False
        )

        embed.add_field(
            name="😂 Meme Commands",
            value="`!meme` - Get a random meme from Reddit.",
            inline=False
        )

        embed.add_field(
            name="🤖 AI Commands",
            value="`!ask <question>` - Ask something to the AI model.",
            inline=False
        )

        # 🌦️ Utility Commands
        embed.add_field(
            name="🌦️ Utilities",
            value="`!weather <city>` - Get weather info\n"
                  "`!pato_status` - Show server status",
            inline=False
        )

        # 🎮 League of Legends Commands
        embed.add_field(
            name="🎮 League of Legends",
            value="`!champion_rotation` - Free champion rotation\n"
                  "`!summoner_info <game_name> <tag>` - Summoner details\n"
                  "`!match_history <game_name> <tag>` - Last 10 matches\n"
                  "`!champion_info <champion>` - Champion details",
            inline=False
        )

        embed.add_field(
            name="ℹ️ General",
            value=(
                "`!ping` - Check if the bot is online.\n"
                "`!commands` - Show this help menu."
            ),
            inline=False
        )

        embed.set_footer(text="Use the commands with '!' before them. Example: !play https://youtube.com/song")

        await ctx.send(embed=embed)

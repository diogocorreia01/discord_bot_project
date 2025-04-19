import discord
from discord.ext import commands
from pato_utils import constants
from pato_utils.voice import VoiceManager
from pato_utils.trivia import TriviaGame
from pato_utils.music import Music
from pato_utils.memes import MemeFetcher
from pato_utils.helpers import HelpCommand
from pato_utils.ai import AIModel
from pato_utils.utils import Utils
from pato_utils.league_of_legends import RiotAPI

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

voice_manager = VoiceManager(bot)
trivia_game = TriviaGame(bot)
music_player = Music(bot)
meme_fetcher = MemeFetcher()
help_command = HelpCommand(bot)
ai_model = AIModel(model_name="gemma:2b")
utils_manager = Utils(bot, constants.NEWS_API_KEY, constants.WEATHER_API_KEY, constants.CHANNEL_ID)
riot_api = RiotAPI(api_key=constants.RIOT_API_KEY)

@bot.event
async def on_ready():
    print(f'{bot.user.name} está online!')

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

@bot.command(name="commands")
async def show_commands(ctx):
    """Displays the bot's help menu."""
    await help_command.show_help(ctx)

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
    """Calls the meme fetcher to retrieve and send a meme."""
    await meme_fetcher.get_meme(ctx)

@bot.command()
async def speak(ctx, lang, *, text):
    """Bot speaks the given text in the specified language."""
    await voice_manager.speak(ctx, text, lang)

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

@bot.command()
async def play(ctx, url):
    """Plays music from a YouTube URL."""
    await music_player.play_music(ctx, url)

@bot.command()
async def stop(ctx):
    """Stops the currently playing music."""
    await music_player.stop_music(ctx)

@bot.command()
async def pause(ctx):
    """Pauses the currently playing music."""
    await music_player.pause_music(ctx)

@bot.command()
async def resume(ctx):
    """Resumes paused music."""
    await music_player.resume_music(ctx)

@bot.command()
async def ask(ctx, *, question):
    """Command to ask something to the AI model. (beta)"""
    try:
        # Generate the model's response (using the AIModel class method)
        response = ai_model.generate_response(question)

        # Check if the response is not empty before sending
        if response:
            await ctx.send(response)
        else:
            await ctx.send("Sorry, I couldn't generate a response. Please try again later.")

    except Exception as e:
        # If an error occurs, send an error message
        await ctx.send(f"An error occurred while trying to generate the response: {str(e)}")

@bot.command()
async def weather(ctx, *, city: str):
    """Fetches the weather for a given city"""
    weather_info = utils_manager.fetch_weather(city)
    await ctx.send(weather_info)


@bot.command()
async def champion_rotation(ctx):
    """Get League of Legends free champion rotation in a well-formatted embed"""
    formatted_champions = riot_api.get_champion_rotation(constants.CHAMPION_ID_MAP)

    embed = discord.Embed(
        title="✨ Free Champion Rotation ✨",
        description="🔥 **These champions are free to play this week!** 🔥",
        color=discord.Color.gold()
    )
    embed.add_field(name="🛡️ Available Champions", value=formatted_champions, inline=False)

    embed.set_footer(text="Try them out before they rotate! 🎮")

    await ctx.send(embed=embed)

@bot.command()
async def summoner_info(ctx, game_name: str, tag_line: str):
    """Fetch and display League of Legends summoner and ranked information"""

    # Fetch complete summoner details (basic + ranked info)
    summoner_data = riot_api.get_complete_summoner_info(game_name, tag_line)

    if "error" in summoner_data:
        await ctx.send(f"❌ Error: {summoner_data['error']}")
        return

    # Extract summoner details
    summoner_info = summoner_data.get("summoner_info", {})
    ranked_info = summoner_data.get("ranked_info", [])

    summoner_name = summoner_info.get("name", game_name + "#" + tag_line)
    summoner_level = summoner_info.get("summonerLevel", "N/A")
    profile_icon_id = summoner_info.get("profileIconId", 0)

    # Construct profile icon URL
    profile_icon_url = f"https://ddragon.leagueoflegends.com/cdn/13.24.1/img/profileicon/{profile_icon_id}.png"

    # Get ranked details (Solo/Duo queue, if available)
    solo_rank = "Unranked"
    ranked_lp = "-"
    wins = 0
    losses = 0

    for queue in ranked_info:
        if queue["queueType"] == "RANKED_SOLO_5x5":
            solo_rank = f"{queue['tier']} {queue['rank']} ({queue['leaguePoints']} LP)"
            wins = queue["wins"]
            losses = queue["losses"]
            break  # Stop after finding solo/duo queue

    # Calculate win rate
    total_games = wins + losses
    win_rate = f"{(wins / total_games) * 100:.2f}%" if total_games > 0 else "N/A"

    # Create embed message
    embed = discord.Embed(
        title=f"🔎 Summoner Profile: {summoner_name}",
        description=f"🌟 **Level:** {summoner_level}",
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url=profile_icon_url)  # Profile icon

    embed.add_field(name="🎖️ **Ranked (Solo/Duo)**", value=f"🏆 {solo_rank}", inline=False)
    embed.add_field(name="📊 **Wins / Losses**", value=f"✅ {wins} Wins / ❌ {losses} Losses", inline=True)
    embed.add_field(name="📈 **Win Rate**", value=f"🔥 {win_rate}", inline=True)

    embed.set_footer(text="Data retrieved from Riot API")

    await ctx.send(embed=embed)


@bot.command()
async def match_history(ctx, game_name: str, tag_line: str):
    """Displays the last 10 matches of a summoner"""

    # Retrieve summoner information
    data = riot_api.get_complete_summoner_info(game_name, tag_line)

    if "error" in data:
        await ctx.send(f"❌ Error: {data['error']}")
        return

    summoner_info = data.get("summoner_info")
    puuid = summoner_info.get("puuid")

    # Get the last 10 matches using PUUID
    recent_matches = riot_api.get_recent_matches(puuid)

    if "error" in recent_matches:
        await ctx.send(f"❌ Error fetching match history: {recent_matches['error']}")
        return

    # Prepare match details
    match_details = []
    total_kills = 0
    total_deaths = 0
    total_assists = 0
    total_wins = 0
    total_losses = 0

    for match_id in recent_matches:
        match_data = riot_api.get_match_details(match_id)
        if "error" in match_data:
            continue
        match_details.append(match_data)

    # Prepare the embed to display match history
    embed = discord.Embed(
        title=f"📊 Match History: {game_name}#{tag_line}",
        description=f"**Last 10 matches of {game_name}**",
        color=discord.Color.blue()
    )

    # Add match details to the embed
    for match in match_details:
        # Find the correct participant in the match
        participant = next(p for p in match["info"]["participants"] if p["puuid"] == puuid)
        champion_id = participant["championId"]
        champion_name = constants.CHAMPION_ID_MAP.get(champion_id, "Unknown Champion")
        win_status = "✅ Victory" if participant["win"] else "❌ Defeat"
        kda = f"🔫 {participant['kills']} / 💀 {participant['deaths']} / 🛡️ {participant['assists']}"
        match_duration = match["info"]["gameDuration"] // 60  # Convert duration to minutes

        # Count victories and defeats
        if participant["win"]:
            total_wins += 1
        else:
            total_losses += 1

        # Sum KDA to calculate the average later
        total_kills += participant['kills']
        total_deaths += participant['deaths']
        total_assists += participant['assists']

        # Set the embed color based on the match result
        match_color = discord.Color.green() if participant["win"] else discord.Color.red()

        # Add match information to the embed
        embed.add_field(
            name=f"🧑‍🎤 {champion_name} - {win_status}",
            value=f"{kda}\n⏳ Duration: {match_duration} min",
            inline=False
        )

    # Calculate average KDA
    total_matches = len(match_details)
    average_kills = total_kills / total_matches if total_matches > 0 else 0
    average_deaths = total_deaths / total_matches if total_matches > 0 else 0
    average_assists = total_assists / total_matches if total_matches > 0 else 0
    average_kda = f"{average_kills:.1f} / {average_deaths:.1f} / {average_assists:.1f}"

    # Add total wins, losses, and average KDA to the embed
    embed.add_field(
        name="📊 General Stats",
        value=f"**Wins**: {total_wins} 🏆 | **Losses**: {total_losses} 💔\n"
              f"**Average KDA**: {average_kda} 🎯",
        inline=False
    )

    # Send the embed with the match history
    await ctx.send(embed=embed)


# Discord command to show champion information
@bot.command()
async def champion_info(ctx, champion_name: str):
    """Displays detailed champion information, including lore, abilities, and skins"""
    # Fetch the champion data
    data = riot_api.get_champion_info(champion_name)

    if "error" in data:
        await ctx.send(f"Error: {data['error']}")
        return

    lore = data.get("lore")
    image = data.get("image")
    tags = ", ".join(data.get("tags", []))
    partype = data.get("partype")
    stats = data.get("stats")
    abilities = data.get("abilities")
    skins = data.get("skins")

    # Creating the embed message
    embed = discord.Embed(
        title=f"{champion_name.capitalize()} - Champion Information 🌟",
        description=f"\n🔮 **Lore:**\n{lore}",
        color=discord.Color.blue()
    )

    # Adding image to embed
    embed.set_thumbnail(url=image)

    # Adding tags and partype to embed
    embed.add_field(name="🛡️ Tags", value=tags if tags else "No tags available", inline=True)
    embed.add_field(name="🔋 Partype", value=partype, inline=True)

    # Adding stats to embed
    embed.add_field(name="📊 Stats", value=stats if stats else "No stats available", inline=False)

    # Adding abilities to embed
    embed.add_field(name="⚡ Abilities", value="\n".join(abilities) if abilities else "No abilities listed",
                    inline=False)

    # Adding skins to embed
    embed.add_field(name="👕 Skins", value="\n".join(skins) if skins else "No skins listed", inline=False)

    # Send the embed to Discord
    await ctx.send(embed=embed)

@bot.command()
async def generate_image(ctx, *, prompt):
    """Gera uma imagem baseada num prompt com IA"""
    await ctx.send("🎨 A gerar imagem...")

    image_path = ai_model.generate_image(prompt)
    if image_path:
        await ctx.send(file=discord.File(image_path))
    else:
        await ctx.send("❌ Falhou ao gerar imagem. Tenta com outro prompt.")


@bot.command()
async def pato_status(ctx):
    """Fetches the system status using Utils"""
    await utils_manager.get_status(ctx)

bot.run(constants.DISCORD_KEY)

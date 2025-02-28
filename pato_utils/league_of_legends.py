import requests
import logging

class RiotAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://euw1.api.riotgames.com"
        self.ddragon_url = "https://ddragon.leagueoflegends.com/cdn"

    def get_summoner_by_id(self, summoner_id):
        """Obtém as informações do invocador utilizando o seu ID"""
        url = f"{self.base_url}/lol/summoner/v4/summoners/{summoner_id}"
        headers = {"X-Riot-Token": self.api_key}

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Failed to fetch summoner info by ID: {response.status_code}"}

    def get_summoner_info(self, summoner_name):
        """Obtém informações do invocador pelo nome de usuário"""
        url = f"{self.base_url}/lol/summoner/v4/summoners/by-name/{summoner_name}"
        headers = {"X-Riot-Token": self.api_key}

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Failed to fetch summoner info: {response.status_code}"}

    def get_champion_rotation(self, champion_id_map):
        """Obtém informações do invocador pelo nome de usuário"""
        url = f"{self.base_url}/lol/platform/v3/champion-rotations"
        headers = {"X-Riot-Token": self.api_key}

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            free_champion_ids = data["freeChampionIds"]
            free_champion_names = [champion_id_map.get(champ_id, f"Unknown ID {champ_id}") for champ_id in
                                   free_champion_ids]

            return "\n".join(f"🔹 **{name}**" for name in free_champion_names)
        else:
            return {"error": f"❌ Failed to fetch champion rotation info: {response.status_code}"}

    def get_account_info_by_riot_id(self, game_name, tag_line):
        """Retrieve account information using Riot ID (gameName + tagLine)"""
        if not game_name or not tag_line:
            return {"error": "Both `game_name` and `tag_line` must be provided."}

        url = f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}/?api_key={self.api_key}"
        #headers = {"X-Riot-Token": self.api_key}

        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 403:
            return {"error": "Forbidden: Access denied. Check your API key or permissions."}
        else:
            return {"error": f"Failed to fetch account info by Riot ID: {response.status_code}"}

    def get_summoner_info_by_puuid(self, puuid):
        """Retrieves summoner (LoL) information using PUUID"""
        url = f"{self.base_url}/lol/summoner/v4/summoners/by-puuid/{puuid}"
        headers = {"X-Riot-Token": self.api_key}

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Failed to fetch summoner info: {response.status_code}"}

    def get_ranked_info_by_puuid(self, puuid):
        """Retrieve ranked information using PUUID"""
        url = f"{self.base_url}/lol/league/v4/entries/by-puuid/{puuid}"
        headers = {"X-Riot-Token": self.api_key}

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()  # Returns a list of ranked queues (solo/duo, flex, etc.)
        else:
            return {"error": f"Failed to fetch ranked info: {response.status_code}"}

    def get_recent_matches(self, puuid):
        """Retrieve the last 10 matches of a player using their PUUID"""
        url = f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?count=10"
        headers = {"X-Riot-Token": self.api_key}

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()  # Returns a list of match IDs
        else:
            return {"error": f"Failed to fetch recent matches: {response.status_code}"}

    def get_match_details(self, match_id):
        """Retrieve detailed match information by match ID"""
        url = f"https://europe.api.riotgames.com/lol/match/v5/matches/{match_id}"
        headers = {"X-Riot-Token": self.api_key}

        response = requests.get(url , headers=headers)

        if response.status_code == 200:
            return response.json()  # Returns detailed match data
        else:
            return {"error": f"Failed to fetch match details: {response.status_code}"}

    def get_complete_summoner_info(self, game_name, tag_line):
        """
        Retrieves full player information using Riot ID (gameName + tagLine).
        Steps:
        1. Get PUUID using Riot ID.
        2. Use PUUID to fetch summoner details.
        3. Use PUUID to fetch ranked details.
        """
        if not game_name or not tag_line:
            return {"error": "Both `game_name` and `tag_line` must be provided."}

        account_info = self.get_account_info_by_riot_id(game_name, tag_line)
        if "error" in account_info:
            return account_info

        puuid = account_info.get("puuid")
        if not puuid:
            return {"error": "PUUID not found in Riot API response"}

        summoner_info = self.get_summoner_info_by_puuid(puuid)
        ranked_info = self.get_ranked_info_by_puuid(puuid)

        return {
            "summoner_info": summoner_info,
            "ranked_info": ranked_info
        }

    def get_champion_data(self, version="12.23.1"):
        """Fetch champion data (abilities, lore, skins, etc.) from Data Dragon"""
        url = f"{self.ddragon_url}/{version}/data/en_US/champion.json"
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()  # Return JSON data
        else:
            return {"error": f"Failed to fetch champion data: {response.status_code}"}

    def get_champion_info(self, champion_name, version="12.23.1"):
        """Get full champion information: lore, image, tags, partype, stats, abilities, and skins"""
        champion_data = self.get_champion_data(version)
        if "error" in champion_data:
            return champion_data

        champion = champion_data.get("data", {}).get(champion_name.capitalize())
        if not champion:
            return {"error": f"Champion {champion_name} not found."}

        # Extracting champion details
        lore = champion.get("blurb", "Lore not available.")
        image = f"http://ddragon.leagueoflegends.com/cdn/{version}/img/champion/{champion['id']}.png"  # Champion image
        tags = champion.get("tags", [])
        partype = champion.get("partype", "No partype available.")
        stats = champion.get("stats", {})

        # Formatting stats into a string
        stats_str = "\n".join([f"**{key}**: {value}" for key, value in stats.items()])

        # Extracting abilities and skins
        abilities = champion.get("spells", [])
        skins = champion.get("skins", [])

        abilities_list = [ability["name"] for ability in abilities]
        skins_list = [skin["name"] for skin in skins]

        return {
            "lore": lore,
            "image": image,
            "tags": tags,
            "partype": partype,
            "stats": stats_str,
            "abilities": abilities_list,
            "skins": skins_list
        }
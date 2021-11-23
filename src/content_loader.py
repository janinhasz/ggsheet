import requests

class Loader:

    @staticmethod 
    def fetch(endpoint="/"):
        data = requests.get(f"https://valorant-api.com/v1{endpoint}")
        return data.json()

    @staticmethod 
    def load_all_content(client):
        content_data = {
            "agents": [],
            "maps": [],
            "modes": [],   
            "comp_tiers": [],
            "season": {},
            "queue_aliases": { #i'm so sad these have to be hardcoded but oh well :(
                "newmap": "Novo Mapa",
                "competitive": "Competitivo",
                "unrated": "Sem Class.",
                "spikerush": "D. da Spike",
                "deathmatch": "Mata-Mata",
                "ggteam": "Escalação",
                "onefa": "Replicação",
                "custom": "Jogo Personalizado",
                "snowball": "Batalha Nevada",
                "": "Jogo Personalizado",
            },
            "team_aliases": {
                "TeamOne": "Defensor",
                "TeamTwo": "Atacante",
                "TeamSpectate": "Observante",
                "TeamOneCoaches": "Coach defensor",
                "TeamTwoCoaches": "Coach atacante",
                "Red": ""
            },
            "team_image_aliases": {
                "TeamOne": "team_defender",
                "TeamTwo": "team_attacker",
                "Red": "team_defender",
                "Blue": "team_attacker",
            },
            "modes_with_icons": ["ggteam","onefa","snowball","spikerush","unrated","deathmatch"]
        }
        all_content = client.fetch_content()
        agents = Loader.fetch("/agents")["data"]
        maps = Loader.fetch("/maps")["data"]
        modes = Loader.fetch("/gamemodes?language=pt-BR")["data"]
        comp_tiers = Loader.fetch("/competitivetiers?language=pt-BR")["data"][-1]["tiers"]
        

        for season in all_content["Seasons"]:
            if season["IsActive"] and season["Type"] == "act":
                content_data["season"] = {
                    "competitive_uuid": season["ID"],
                    "season_uuid": season["ID"],
                    "display_name": season["Name"]
                }
        
        for agent in agents:
            content_data["agents"].append({
                "uuid": agent["uuid"],
                "display_name": agent["displayName"].replace("/",""),
                "internal_name": agent["developerName"]
            })

        for game_map in maps:
            content_data["maps"].append({
                "uuid": game_map["uuid"],
                "display_name": game_map["displayName"],
                "path": game_map["mapUrl"],
                "internal_name": game_map["mapUrl"].split("/")[-1]
            })

        for mode in modes:
            content_data["modes"].append({
                "uuid": mode["uuid"],
                "display_name": mode["displayName"],
            })

        for tier in comp_tiers:
            content_data["comp_tiers"].append({
                "display_name": tier["tierName"],
                "id": tier["tier"],
            })

        return content_data

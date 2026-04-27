import os
from espn_api.football import League, Team 
from supabase import create_client, Client
from dotenv import load_dotenv
import pprint

load_dotenv()

ESPN_S2="AEAIBpeKez2Fe5c0gC7eZfHrQ4vMdw2rx22Ke4SfA1vTA38LRqGhw8b4XCtMbDJmpYn01ZHmNKntP76Wnmt2sZoV5uUXYWgQIaXxIiJVH7v%2BXm0%2FLU0Qn3mc1G%2FBd4nvxFLnArwapm0piyPVyNPgEBkuA1bzqngn6lmewp3zdd9SuVwCjpiv6ADlaCQiuDjus0ndWzHk3EtNTL5rGDz61eMvlM7ljFDasQ86Uer8Dy6XwKtT0s1cdmdwR3R6thicM8g%3D"
SWID="{68D93F50-01F5-4D09-993F-5001F53D095F}"

league_2025 = League(league_id=11802874, year=2025, espn_s2=os.environ.get("ESPN_S2"), swid=os.environ.get("SWID"))
league_2024 = League(league_id=11802874, year=2024, espn_s2=ESPN_S2, swid=SWID)


player_bug = league_2025.player_info(name="Lamar Jackson", playerId=3916387)
player_works = league_2025.player_info(playerId=3916387)

print(player_bug) # None
print(player_works) # Player(Lamar Jackson)
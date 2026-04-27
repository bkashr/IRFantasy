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

db: Client = create_client(
    os.environ.get("SUPABASE_URL"),
    os.environ.get("SUPABASE_PUBLISHABLE_KEY")
)

# League
response = (
    db.table("League")
    .insert({
        "espn_league_id": 11802874,
        "is_espn_league": True
    })
    .execute()
)
print("Inserted league")
db_league_id = response.data[0]["id"]
team_ids = {}

# Teams
for team in league_2025.teams:
    res = (
        db.table("Team")\
        .insert({
            "team_name": team.team_name,
            "league_id": db_league_id,
            "year": 2025,
            "espn_team_id": team.team_id,
            "owners": [owner["firstName"] + " " + owner["lastName"] for owner in team.owners]
        })\
        .execute()
    )
    team_ids[team.team_id] = res.data[0]["id"]
    print(f"Inserted team: {team.team_name}")

# Draft
for pick in league_2025.draft:
    player = league_2025.player_info(playerId=pick.playerId)
    
    if player is None:
        res = (
            db.table("Player")\
            .insert({
                "espn_player_id": pick.playerId,
                "name": pick.playerName,
            })\
            .execute()
        )
    else:
        res = (
            db.table("Player")\
            .insert({
                "espn_player_id": pick.playerId,
                "name": pick.playerName,
                "position": player.position,
                "nfl_team": player.proTeam
            })\
            .execute()
        )
    
    db_player_id = res.data[0]["id"]
    res = (
        db.table("Draft")\
        .insert({
            "year": 2025,
            "team_id": team_ids[pick.team.team_id],
            "round": pick.round_num,
            "pick": pick.round_pick,
            "player_id": db_player_id,
            "league_id": db_league_id
        })\
        .execute()
    )
    print(f"Inserted draft pick: {pick.playerName}")
        



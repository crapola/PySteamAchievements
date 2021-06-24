# std
import os
# local
from interface import Application
from steam_app import run_steam_app
import steam.owned_games
import steam.steam_games

def owned_games(path,account_id):
	owned_appids=steam.owned_games.owned_games(path,account_id)
	all_games=steam.steam_games.steam_games()
	return {x:all_games.get(x,f"{x}_GAME_NAME") for x in owned_appids}

def user_info():
	info=run_steam_app()
	apps=owned_games(info["steam_path"],info["account_id"])
	return {"name":info["steam_name"],"id":info["steam_id"],"apps":apps}

def get_achievements(appid):
	return run_steam_app(str(appid))

def unlock_achievement(appid,name)->bool:
	return run_steam_app(str(appid),name)

def main():
	os.chdir(os.path.dirname(os.path.realpath(__file__)))
	Application.run(user_info(),get_achievements,unlock_achievement)

if __name__=="__main__":
	main()
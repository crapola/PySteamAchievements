# std
import json
import requests

def steam_games():
	"""
	Get the list of all Steam games using Web API and cache result.
	Returns a dictionary where keys are AppIDS and values are names.
	"""
	game_json_path="games.json"
	def download_game_list():
		response=requests.get("https://api.steampowered.com/ISteamApps/GetAppList/v2/?key=STEAMKEY",timeout=10)
		print(response.headers)
		print(response.history)
		if response.status_code==200:
			every_game=response.json()
			print("Response size:",len(response.content))
			print("Numer of apps:",len(every_game["applist"]["apps"]))
			with open(game_json_path,"w") as outfile:
				json.dump(every_game,outfile)
			print(f"Downloaded game list to {game_json_path}.")
			return every_game
		else:
			return None
	def load_games_list():
		#return None
		try:
			with open(game_json_path,"r") as infile:
				every_game=json.load(infile)
				print(f"Loaded {game_json_path}.")
				return every_game
		except FileNotFoundError:
			return None
	games=(load_games_list() or download_game_list())["applist"]["apps"]
	result={int(x["appid"]):x["name"] for x in games}
	return result

if __name__=="__main__":
	sg=steam_games()
	print(len(sg))
	ids=(5,220,440,100,474030,1295970,1179900)
	ids_with_names=tuple(sorted([ (x,sg.get(x,f"{x}_GAME_NAME")) for x in ids]))
	print(ids_with_names)

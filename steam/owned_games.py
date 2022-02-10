# libs
# https://github.com/ValvePython/vdf
import vdf


def owned_games(steam_path:str,account_id)->tuple:
	"""
	Return owned games as list of AppID's.
	> steam_path:  Path to Steam.
	> account_id: These are the four lower bytes of the Steam ID.
	"""
	stuff=vdf.load(open(f"{steam_path}/userdata/{account_id}/config/localconfig.vdf","r",encoding="utf-8"))
	apps=stuff["UserLocalConfigStore"]["Software"]["Valve"]["Steam"]["apps"]
	ids=sorted([int(x) for x in apps])
	ids.remove(0)
	return tuple(ids)

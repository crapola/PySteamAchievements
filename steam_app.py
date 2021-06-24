# std
import argparse
from ctypes import byref,c_bool,c_char_p
import os
import json
import subprocess
# local
import steam.steam
import steam.client

def run_steam_app(*args):
	proc=subprocess.run(['python','steam_app.py',*args],capture_output=True)
	result=proc.stdout
	print("stdout:",result)
	if len(proc.stderr)>0:
		print("stderr:",proc.stderr)
		return {}
	d=json.loads(result)
	return d

def deref(iptr):
	return iptr.contents.contents

def user_info(isteamclient,isteamuser,user,pipe,path):
	id=steam.common.CSteamID()
	foo=deref(isteamuser).GetSteamID(isteamuser,byref(id))
	account_id=id.value&0xFFFFFFFF
	ifriends=deref(isteamclient).GetISteamFriends(isteamclient,user,pipe,steam.friends.STEAMFRIENDS_INTERFACE_VERSION)
	name=deref(ifriends).GetPersonaName(ifriends)
	name=name.decode("utf8")
	return {"steam_id":id.value,"account_id":account_id,"steam_name":name,"steam_path":path}

def unlock_achievement(name:str,isteamstats):
	achievement_name=name.encode("ascii")
	return deref(isteamstats).SetAchievement(isteamstats,achievement_name)

def main():
	description="""
If no argument is passed, dump user information.
If only [appid] is passed, dump achievement list for that AppID.
If both [appid] and [achname] are passed, it will try to unlock that achievement.
"""
	parser=argparse.ArgumentParser(description=description,formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument("appid",type=int,help="The App ID",nargs="?")
	parser.add_argument("achname",type=str,help="Achievement internal name to unlock",nargs="?")
	args=parser.parse_args()
	appid=args.appid
	if appid is None:
		appid=0

	os.environ["SteamAppId"]=str(appid)
	# Load DLL.
	s=steam.steam.Steam()

	isteamclient=s.create_interface(steam.client.STEAMCLIENT_INTERFACE_VERSION,ptype=steam.client.SteamClient)
	pipe=deref(isteamclient).CreateSteamPipe(isteamclient)
	if not pipe:
		raise RuntimeError("Failed to open pipe! Is Steam running?")
	user=deref(isteamclient).ConnectToGlobalUser(isteamclient,pipe)
	isteamuser=deref(isteamclient).GetISteamUser(isteamclient,user,pipe,c_char_p(steam.user.STEAMUSER_INTERFACE_VERSION))
	if not isteamuser:
		raise RuntimeError("Failed to create ISteamUser. Expired license?")
	isteamuserstats=deref(isteamclient).GetISteamUserStats(isteamclient,user,pipe,c_char_p(steam.userstats.STEAMUSERSTATS_INTERFACE_VERSION))
	if not isteamuserstats:
		raise RuntimeError("GetISteamUserStats() failed.")
	ok=deref(isteamuserstats).RequestCurrentStats(isteamuserstats)

	if not appid:
		result=user_info(isteamclient,isteamuser,user,pipe,s.path)
	elif args.achname:
		result=(unlock_achievement(args.achname,isteamuserstats))
	else:
		# Dump achievement stats.
		a=deref(isteamuserstats).GetNumAchievements(isteamuserstats)
		result={}
		for i in range(a):
			name=deref(isteamuserstats).GetAchievementName(isteamuserstats,i)
			unlocked=c_bool(False)
			deref(isteamuserstats).GetAchievement(isteamuserstats,name,byref(unlocked))
			result[name.decode('ansi')]=unlocked.value

	# Dump result to stdout.
	print(json.dumps(result))
	# Cleanup.
	deref(isteamclient).ReleaseUser(isteamclient,pipe,user)
	deref(isteamclient).BReleaseSteamPipe(isteamclient,pipe)

if __name__=="__main__":
	main()

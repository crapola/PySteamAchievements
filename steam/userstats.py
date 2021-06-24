# std
from ctypes import Structure, POINTER, c_uint32
from ctypes import (c_bool,c_char,c_wchar,c_byte,c_ubyte,c_short,c_ushort,c_int,
c_uint,c_long,c_ulong,c_longlong,c_ulonglong,c_size_t,c_ssize_t,c_float,
c_double,c_longdouble,c_char_p,c_wchar_p,c_void_p)
# local
from .common import *

STEAMUSERSTATS_INTERFACE_VERSION=b"STEAMUSERSTATS_INTERFACE_VERSION012"

class SteamUserStats(Structure):
	_fields_=[
	# Asynchronously request the user's current stats and achievements from the server.
	# You must always call this first to get the initial status of stats and achievements.
	# Only after the resulting callback comes back can you start calling the
	# rest of the stats and achievement functions for the current user.
	("RequestCurrentStats",THISFUNCTYPE(c_bool)),
	# Data accessors.
	("GetStatInt32",THISFUNCTYPE(c_bool,c_char_p,POINTER(c_int32))),
	("GetStatFloat",THISFUNCTYPE(c_bool,c_char_p,POINTER(c_float))),
	# Set/update data.
	("SetStatInt32",THISFUNCTYPE(c_bool,c_char_p,c_int32)),
	("SetStatFloat",THISFUNCTYPE(c_bool,c_char_p,c_float)),
	("UpdateAvgRateStat",THISFUNCTYPE(c_bool,c_char_p,c_float,c_double)),
	# Achievement flag accessors.
	("GetAchievement",THISFUNCTYPE(c_bool,c_char_p,POINTER(c_bool))),
	("SetAchievement",THISFUNCTYPE(c_bool,c_char_p)),
	("ClearAchievement",THISFUNCTYPE(c_bool,c_char_p)),
	# Get the achievement status, and the time it was unlocked if unlocked.
	# If the return value is true, but the unlock time is zero, that means it was unlocked before Steam
	# began tracking achievement unlock times (December 2009). Time is seconds since January 1, 1970.
	("GetAchievementAndUnlockTime",THISFUNCTYPE(c_bool,c_char_p,POINTER(c_bool),POINTER(c_uint32))),
	# Store the current data on the server, will get a callback when set,
	# and one callback for every new achievement.
	("StoreStats",THISFUNCTYPE(c_bool)),
	("GetAchievementIcon",THISFUNCTYPE(c_int,c_char_p)),
	("GetAchievementDisplayAttribute",THISFUNCTYPE(c_char_p,c_char_p,c_char_p)),
	("IndicateAchievementProgress",THISFUNCTYPE(c_bool,c_char_p,c_uint32,c_uint32)),
	("GetNumAchievements",THISFUNCTYPE(c_uint32)),
	("GetAchievementName",THISFUNCTYPE(c_char_p,c_uint32)),
	#("",THISFUNCTYPE()),
	]

ISteamUserStats=POINTER(POINTER(SteamUserStats))
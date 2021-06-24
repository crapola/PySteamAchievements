# std
from ctypes import Structure,CFUNCTYPE,POINTER
from ctypes import (c_bool,c_char,c_wchar,c_byte,c_ubyte,c_short,c_ushort,c_int,
c_uint,c_long,c_ulong,c_longlong,c_ulonglong,c_size_t,c_ssize_t,c_float,
c_double,c_longdouble,c_char_p,c_wchar_p,c_void_p)
# local
from .common import *
from .friends import *
from .userstats import *
from .user import *

STEAMCLIENT_INTERFACE_VERSION="SteamClient020"

class SteamClient(Structure):
	_fields_=[
	# Creates a communication pipe to the Steam client.
	("CreateSteamPipe",THISFUNCTYPE(HSteamPipe)),
	# Releases a previously created communications pipe.
	("BReleaseSteamPipe",THISFUNCTYPE(c_bool,HSteamPipe)),
	# Connects to an existing global user, failing if none exists.
	# Used by the game to coordinate with the steamUI.
	("ConnectToGlobalUser",THISFUNCTYPE(HSteamUser, HSteamPipe)),
	# Used by game servers, create a steam user that won't be shared with anyone else.
	("CreateLocalUser",THISFUNCTYPE(HSteamUser,POINTER(HSteamPipe),EAccountType)),
	# Removes an allocated user.
	("ReleaseUser",THISFUNCTYPE(None,HSteamPipe,HSteamUser)),
	# Retrieves the ISteamUser interface associated with the handle.
	("GetISteamUser",THISFUNCTYPE(ISteamUser,HSteamUser,HSteamPipe,c_char_p)),
	# Retrieves the ISteamGameServer interface associated with the handle.
	("GetISteamGameServer",CFUNCTYPE(c_int,c_int,c_int,c_char_p)),

	("SetLocalIPBinding",CFUNCTYPE(None,c_int,c_int)),
	# Returns the ISteamFriends interface.
	("GetISteamFriends",THISFUNCTYPE(ISteamFriends,HSteamUser,HSteamPipe,c_char_p)),

	("GetISteamUtils",CFUNCTYPE(c_int,c_int,c_char_p)),

	("GetISteamMatchmaking",CFUNCTYPE(c_int,c_int,c_int,c_char_p)),

	("GetISteamMatchmakingServers",CFUNCTYPE(c_int,c_int,c_int,c_char_p)),

	("GetISteamGenericInterface",CFUNCTYPE(None,c_int,c_int,c_char_p)),
	# Returns the ISteamUserStats interface.
	("GetISteamUserStats",THISFUNCTYPE(ISteamUserStats,HSteamUser,HSteamPipe,c_char_p)),

	("GetISteamGameServerStats",CFUNCTYPE(c_int,c_int,c_int,c_char_p)),

	("GetISteamApps",CFUNCTYPE(c_void_p,c_int,c_int,c_char_p)),

	# ("GetISteamNetworking",CFUNCTYPE(c_int)),
	# ("GetISteamRemoteStorage",CFUNCTYPE(c_int)),
	# ("GetISteamScreenshots",CFUNCTYPE(c_int)),
	# ("GetISteamGameSearch",CFUNCTYPE(c_int)),
	# ("RunFrame",CFUNCTYPE(None)),
	# ("GetIPCCallCount",CFUNCTYPE(c_int)),
	# ("SetWarningMessageHook",CFUNCTYPE(c_int)),
	# ("BShutdownIfAllPipesClosed",CFUNCTYPE(c_bool)),
	# ("GetISteamHTTP",CFUNCTYPE(c_int)),
	# ("DEPRECATED_GetISteamUnifiedMessages",CFUNCTYPE(None)),
	# ("GetISteamController",CFUNCTYPE(c_int)),
	# ("GetISteamUGC",CFUNCTYPE(c_int)),
	# ("GetISteamAppList",CFUNCTYPE(c_int)),
	# ("GetISteamMusic",CFUNCTYPE(c_int)),
	# ("GetISteamMusicRemote",CFUNCTYPE(c_int)),
	# ("GetISteamHTMLSurface",CFUNCTYPE(c_int)),
	# ("DEPRECATED_Set_SteamAPI_CPostAPIResultInProcess",CFUNCTYPE(None)),
	# ("DEPRECATED_Remove_SteamAPI_CPostAPIResultInProcess",CFUNCTYPE(None)),
	# ("Set_SteamAPI_CCheckCallbackRegisteredInProcess",CFUNCTYPE(None)),
	# ("GetISteamInventory",CFUNCTYPE(c_int)),
	# ("GetISteamVideo",CFUNCTYPE(c_int)),
	# ("GetISteamParentalSettings",CFUNCTYPE(c_int)),
	# ("GetISteamInput",CFUNCTYPE(c_int)),
	# ("GetISteamParties",CFUNCTYPE(c_int))
	]
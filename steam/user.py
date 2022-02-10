# std
from ctypes import POINTER, Structure, c_bool

# local
from steam.common import *

STEAMUSER_INTERFACE_VERSION=b"SteamUser021"

class SteamUser(Structure):
	_fields_=[
	# Returns the HSteamUser this interface represents.
	("GetHSteamUser",THISFUNCTYPE(HSteamUser)),
	# Returns true if the Steam client current has a live connection to the Steam servers.
	# If false, it means there is no active connection due to either a networking issue on the local machine, or the Steam server is down/busy.
	# The Steam client will automatically be trying to recreate the connection as often as possible.
	("BLoggedOn",THISFUNCTYPE(c_bool)),
	# Returns the CSteamID of the account currently logged into the Steam client.
	# a CSteamID is a unique identifier for an account, and used to differentiate users in all parts of the Steamworks API.
	#("GetSteamID",THISFUNCTYPE(CSteamID)),
	# Official signature is wrong. It takes a ref param. What does it return?
	("GetSteamID",THISFUNCTYPE(None,POINTER(CSteamID))),
	]

ISteamUser=POINTER(POINTER(SteamUser))

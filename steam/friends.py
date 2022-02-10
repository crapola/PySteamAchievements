# std
from ctypes import POINTER, Structure, c_char_p

# local
from steam.common import *

STEAMFRIENDS_INTERFACE_VERSION=b"SteamFriends017"

class SteamFriends(Structure):
	_fields_=[
	# Returns the local player's name - guaranteed to not be NULL.
	# This is the same name as on the user's community profile page.
	# This is stored in UTF-8 format.
	# Like all the other interface functions that return a char *, it's important
	# that this pointer is not saved off; it will eventually be free'd or re-allocated.
	("GetPersonaName",THISFUNCTYPE(c_char_p))
	]

ISteamFriends=POINTER(POINTER(SteamFriends))

# std
from ctypes import Structure, POINTER
from ctypes import (c_bool,c_char,c_wchar,c_byte,c_ubyte,c_short,c_ushort,c_int,
c_uint,c_long,c_ulong,c_longlong,c_ulonglong,c_size_t,c_ssize_t,c_float,
c_double,c_longdouble,c_char_p,c_wchar_p,c_void_p)
# local
from .common import *

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
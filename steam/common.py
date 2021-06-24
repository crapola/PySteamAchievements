from ctypes import c_int,c_int32, c_int64,c_void_p,CFUNCTYPE

class EAccountType(c_int):
	k_EAccountTypeInvalid=0
	k_EAccountTypeIndividual=1		# single user account
	k_EAccountTypeMultiseat=2			# multiseat (e.g. cybercafe) account
	k_EAccountTypeGameServer=3		# game server account
	k_EAccountTypeAnonGameServer=4# anonymous game server account
	k_EAccountTypePending=5				# pending
	k_EAccountTypeContentServer=6	# content server
	k_EAccountTypeClan=7
	k_EAccountTypeChat=8
	k_EAccountTypeConsoleUser=9		# Fake SteamID for local PSN account on PS3 or Live account on 360, etc.
	k_EAccountTypeAnonUser=10
	k_EAccountTypeMax=11

class HSteamPipe(c_int32):
	pass

class HSteamUser(c_int32):
	pass

class CSteamID(c_int64):
	pass

def THISFUNCTYPE(restype,*argtypes,**kw):
	"""
	CFUNCTYPE with a 'this' parameter (c_void_p) inserted.
	"""
	argtypes=(c_void_p,)+argtypes
	return CFUNCTYPE(restype,*argtypes,**kw)
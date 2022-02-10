# std
import ctypes
import winreg


def steam_path_from_registry()->str:
	k=winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,"SOFTWARE\Wow6432Node\Valve\Steam")
	return winreg.QueryValueEx(k,"InstallPath")[0]

class Steam:
	""" Access to steamclient64.dll """

	def __init__(self):
		self.handle:ctypes.WinDLL=None
		self.path=steam_path_from_registry()
		self.load()

	def create_interface(self,version:str,ptype):
		"""
		Create interface.
		> version: name/version of interface.
		> ptype: type of returned object.
		< Interface or None on failure.
		"""
		i=ctypes.c_int(0)
		version=bytes(version,"utf-8")
		self.handle.CreateInterface.restype=ctypes.POINTER(ctypes.POINTER(ptype))
		addr=self.handle.CreateInterface(version,ctypes.byref(i))
		return addr

	def load(self):
		if self.handle!=None:
			return
		self.handle=ctypes.WinDLL(self.path+"/steamclient64.dll")


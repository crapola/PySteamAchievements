# std
from tkinter import ttk
import tkinter as tk
import tkinter.messagebox

def grid_configure(widget):
	widget.columnconfigure(0,weight=1)
	widget.rowconfigure(0,weight=1)

def make_treeview_sortable(treeview:ttk.Treeview):
	""" Based on https://stackoverflow.com/a/1967793 """
	def sort_column(tv,col,reverse):
		l=[(tv.set(k,col),k) for k in tv.get_children('')]
		l.sort(reverse=reverse)
		# Rearrange items in sorted positions.
		for index,(val,k) in enumerate(l):
				tv.move(k,'', index)
		# Reverse sort next time.
		tv.heading(col,command=lambda:sort_column(tv,col,not reverse))
	for c in treeview["columns"]:
		treeview.heading(c,command=sort_column(treeview,c,False))

class Application(tk.Frame):
	def __init__(self,master,info:dict,get_achievements_callback,unlock_achievement_callback):
		tk.Frame.__init__(self,master)
		master.minsize(512,256)
		# Set weights to make content resizable.
		grid_configure(master)
		grid_configure(self)
		self.grid(sticky=tk.NSEW)
		ttk.Sizegrip(self).grid(row=1,sticky=tk.SE)
		# Split pane with movable divider.
		self.paned_window=tk.PanedWindow(self,orient=tk.HORIZONTAL)
		self.paned_window.grid(row=0,column=0,sticky=tk.NSEW)
		# Labeled frame for Games.
		self.lf_games=tk.LabelFrame(self.paned_window,text="Games",width=256)
		self.lf_games.grid_propagate(0)
		grid_configure(self.lf_games)
		# Game list.
		self.games=ttk.Treeview(self.lf_games,columns=("id","title"),show=("headings"),selectmode="browse")
		self.games.heading("id",text="App ID")
		self.games.heading("title",text="Title")
		self.games.column(0,width=64,stretch=0)
		self.games.grid(sticky=tk.NSEW)
		self.games.bind("<<TreeviewSelect>>",self.on_game_selected)
		grid_configure(self.games)
		make_treeview_sortable(self.games)
		# Game list's scrollbar.
		self.games_scollbar=tk.Scrollbar(self.lf_games)
		self.games_scollbar.config(command=self.games.yview)
		self.games.config(yscrollcommand=self.games_scollbar.set)
		self.games_scollbar.grid(row=0,column=1,sticky=tk.NS)
		# Labeled frame for Achievements.
		self.lf_achievements=tk.LabelFrame(self.paned_window,text="Achievements")
		grid_configure(self.lf_achievements)
		# Achievement list.
		self.achievements=ttk.Treeview(self.lf_achievements,columns=("id","unlocked"),show=("headings"),selectmode="browse")
		self.achievements.heading("id",text="Internal Name")
		self.achievements.heading("unlocked",text="Unlocked")
		self.achievements.column("unlocked",width=64,stretch=0)
		self.achievements.grid(sticky=tk.NSEW)
		self.achievements.bind("<<TreeviewSelect>>",self.on_achievement_selected)
		grid_configure(self.achievements)
		make_treeview_sortable(self.achievements)
		# Achievement list's scrollbar.
		self.achievements_scollbar=tk.Scrollbar(self.lf_achievements)
		self.achievements_scollbar.config(command=self.achievements.yview)
		self.achievements.config(yscrollcommand=self.achievements_scollbar.set)
		self.achievements_scollbar.grid(row=0,column=1,sticky=tk.NS)
		# Unlock button.
		self.unlock=tk.Button(self,text="Unlock",command=self.on_click_unlock,state="disabled")
		self.unlock.grid(row=1,column=0,sticky=tk.S)
		# Add frames to the paned window.
		self.paned_window.add(self.lf_games,stretch="always")
		self.paned_window.add(self.lf_achievements,stretch="always")
		# Info about user and owned games.
		self.info=info
		# Function that returns achievements dictionary for a given App ID.
		self.get_achievements_callback=get_achievements_callback
		# Function that unlocks achievement for given AppID and name.
		self.unlock_achievement_callback=unlock_achievement_callback
		# Cached database of achievements.
		# It gets populated as the user selects games.
		self.database:dict[int,dict[str,bool]]={}
		# Refesh game list.
		self.games_update()

	def get_achievement_list(self,appid):
		if appid in self.database:
			return self.database[appid]
		else:
			result=self.get_achievements_callback(appid)
			if len(result)>0:
				self.database[appid]=result
			return result

	def games_update(self):
		game_dict=self.info["apps"]
		for k,v in sorted(game_dict.items(),key=lambda x:x[1]):
			self.games.insert("",tk.END,None,values=(k,v))

	def on_achievement_selected(self,what):
		unlocked=self.achievements.item(self.achievements.focus())["values"][1]
		if unlocked=="False":
			self.unlock["state"]=tk.ACTIVE
		else:
			self.unlock["state"]=tk.DISABLED

	def on_game_selected(self,what):
		w=what.widget
		game=w.item(w.focus())["values"]
		cheevos=self.get_achievement_list(game[0])
		self.unlock["state"]=tk.DISABLED
		self.achievements.delete(*self.achievements.get_children())
		for k,v in cheevos.items():
			self.achievements.insert("",0,None,values=(k,v))

	def on_click_unlock(self):
		try:
			appid=self.games.item(self.games.focus())["values"][0]
			appname=self.games.item(self.games.focus())["values"][1]
			cheevo=self.achievements.item(self.achievements.focus())["values"][0]
		except tk.TclError:
			return
		result=tk.messagebox.askokcancel("Confirm",f"{appname}\nUnlock {cheevo}?")
		if result:
			ok=self.unlock_achievement_callback(appid,cheevo)
			if ok:
				self.achievements.item(self.achievements.focus(),values=(cheevo,True))
				self.unlock["state"]=tk.DISABLED
				self.database[appid][cheevo]=True

	@staticmethod
	def run(user_info,achievements_callback,unlock_achievement_callback):
		"""
		> user_info: dict
			'id': Steam ID.
			'name': Steam name.
			'apps': Dictionary Dict[appid,name].
		> achievements_callback: Callable[[int]]
			What to call to retrieve achievement stats for a given AppID.
			It must return a dictionary Dict[name,bool].
		> unlock_achievement_callback: Callable[[int,str]]
			What to call to unlock the given achievement.
		"""
		root=tk.Tk()
		app=Application(root,user_info,achievements_callback,unlock_achievement_callback)
		app.master.title(f"Steam Thing - {user_info['name']} ({user_info['id']})")
		root.mainloop()

if __name__=="__main__":
	# Interface test.
	def test_achievements_callback(id):
		return {"Tutorial_completed":True,"Won_the_game":False,"Something":False}
	def test_unlock(a,n):
		print("Get",a,n)
		return True
	games={220:"Half Life 2",8000000:"Half Life 3",440:"Team Fortress 2",12345:"Test"}
	user_info={"name":"InterfaceTester","id":1234567890,"apps":games}
	Application.run(user_info,test_achievements_callback,test_unlock)
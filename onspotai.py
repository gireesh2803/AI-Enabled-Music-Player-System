import dearpygui.dearpygui as dpg
import ntpath
import json
import mpv
import threading
import time
import atexit
from youtubesearchpython import VideosSearch
from bardapi import Bard
from secret import BARD_TOKEN, BEST_SONG, RECOMMEND_SONG
from helper import *


dpg.create_context()
dpg.create_viewport(title="OnSpotAI")

global state
global player
global bard
state=None
player = mpv.MPV(video=False, ytdl=True, log_handler=print)
bard = Bard(token=BARD_TOKEN)

def update_slider():
	global state
	while is_playing(player):
		dpg.configure_item(item="pos",default_value=player.time_pos)
		time.sleep(0.7)
	if state==None:
		dpg.configure_item("cstate",default_value=f"State: None")
		dpg.configure_item("csong",default_value="Now Playing : ")
		dpg.configure_item("play",label="Play")
		dpg.configure_item(item="pos",max_value=100)
		dpg.configure_item(item="pos",default_value=0)
	exit(0)

def play(sender, app_data, user_data):
	global state
	global player
	if user_data:
		song = user_data[0]
		link = user_data[1]
		duration = user_data[2]
		update_database(song)
		duration_sec = convert_duration(duration)
		dpg.configure_item(item="pos",max_value=duration_sec)
		player.pause = False
		player.play(link)
		player.wait_until_playing()
		thread=threading.Thread(target=update_slider,daemon=False).start()
		if is_playing(player):
			dpg.configure_item("play",label="Pause")	
			state="playing"
			dpg.configure_item("cstate",default_value=f"State: Playing")
			dpg.configure_item("csong",default_value=f"Now Playing : {ntpath.basename(song)}")

def play_pause():
	global state
	if state == "playing":
		state="paused"
		player.pause = True
		dpg.configure_item("play",label="Play")
		dpg.configure_item("cstate",default_value=f"State: Paused")
	elif state == "paused":
		state="playing"
		player.pause = False
		dpg.configure_item("play",label="Pause")
		dpg.configure_item("cstate",default_value=f"State: Playing")
	thread = threading.Thread(target=update_slider,daemon=False).start()

def stop():
	global state
	player.stop()
	state=None
	thread = threading.Thread(target=update_slider,daemon=False).start()

def best_songs(sender, app_data, user_data):
	prompt = BEST_SONG
	response = music_ai(prompt, bard)
	song_list = parse_response(response)
	for song in song_list:
		search(app_data=song, sender=sender, user_data=user_data)

def recommend_songs(sender, app_data, user_data):
	songs = load_database()
	prompt = RECOMMEND_SONG % str(songs)
	print("RHA: recommend_songs: prompt:", prompt)
	response = music_ai(prompt, bard)
	song_list = parse_response(response)
	print("RHA: recommend_songs: song_list:", song_list)
	for song in song_list:
		search(app_data=song, sender=sender, user_data=user_data)

def search(sender, app_data, user_data):
	print("DEBUG: search(): sender:", sender, "app_data:", app_data, "user_data:", user_data)
	videosSearch = VideosSearch(app_data, limit = 1)
	res = videosSearch.result()
	song_info = []
	song_info.append(res["result"][0]["title"])
	song_info.append(res["result"][0]["link"])
	song_info.append(res["result"][0]["duration"])
	song = song_info[0]
	link = song_info[1]
	dpg.add_button(label=song, callback=play,width=-1, height=25, user_data=song_info, parent="list")
	dpg.add_spacer(height=2,parent="list")
	
def removeall():
	dpg.delete_item("list", children_only=True)

with dpg.theme(tag="base"):
	with dpg.theme_component():
		dpg.add_theme_color(dpg.mvThemeCol_Button, (130, 142, 250))
		dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (137, 142, 255, 95))
		dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (137, 142, 255))
		dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 3)
		dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 4)
		dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 4, 4)
		dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 4, 4)
		dpg.add_theme_style(dpg.mvStyleVar_WindowTitleAlign, 0.50, 0.50)
		dpg.add_theme_style(dpg.mvStyleVar_WindowBorderSize,0)
		dpg.add_theme_style(dpg.mvStyleVar_WindowPadding,10,14)
		dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (25, 25, 25))
		dpg.add_theme_color(dpg.mvThemeCol_Border, (0,0,0,0))
		dpg.add_theme_color(dpg.mvThemeCol_ScrollbarBg, (0,0,0,0))
		dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (130, 142, 250))
		dpg.add_theme_color(dpg.mvThemeCol_CheckMark, (221, 166, 185))
		dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (172, 174, 197))

with dpg.theme(tag="slider_thin"):
	with dpg.theme_component():
		dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (130, 142, 250,99))
		dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (130, 142, 250,99))
		dpg.add_theme_color(dpg.mvThemeCol_SliderGrabActive, (255, 255, 255))
		dpg.add_theme_color(dpg.mvThemeCol_SliderGrab, (255, 255, 255))
		dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (130, 142, 250,99))
		dpg.add_theme_style(dpg.mvStyleVar_GrabRounding, 3)
		dpg.add_theme_style(dpg.mvStyleVar_GrabMinSize, 30)

with dpg.theme(tag="slider"):
	with dpg.theme_component():
		dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (130, 142, 250,99))
		dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (130, 142, 250,99))
		dpg.add_theme_color(dpg.mvThemeCol_SliderGrabActive, (255, 255, 255))
		dpg.add_theme_color(dpg.mvThemeCol_SliderGrab, (255, 255, 255))
		dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (130, 142, 250,99))
		dpg.add_theme_style(dpg.mvStyleVar_GrabRounding, 3)
		dpg.add_theme_style(dpg.mvStyleVar_GrabMinSize, 30)

with dpg.theme(tag="songs"):
	with dpg.theme_component():
		dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 2)
		dpg.add_theme_color(dpg.mvThemeCol_Button, (89, 89, 144,40))
		dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (0,0,0,0))

with dpg.font_registry():
	monobold = dpg.add_font("fonts/MonoLisa-Bold.ttf", 12)
	head = dpg.add_font("fonts/MonoLisa-Bold.ttf", 15)

with dpg.window(tag="main",label="window title"):
	with dpg.child_window(autosize_x=True,height=45,no_scrollbar=True):
		dpg.add_text(f"Now Playing : ",tag="csong")
	dpg.add_spacer(height=2)

	with dpg.group(horizontal=True):
		with dpg.child_window(width=225,tag="sidebar"):
			dpg.add_text("OnSpotAI",color=(137, 142, 255))
			dpg.add_text("AI Assisted Music Player")
			dpg.add_spacer(height=2)
			dpg.add_separator()
			dpg.add_spacer(height=5)
			dpg.add_button(label="Best Songs",width=-1,height=28,callback=best_songs)
			dpg.add_button(label="Recommend Songs",width=-1,height=28,callback=recommend_songs)
			dpg.add_button(label="Remove All Songs",width=-1,height=28,callback=removeall)
			dpg.add_spacer(height=5)
			dpg.add_separator()
			dpg.add_spacer(height=5)
			dpg.add_text(f"State: {state}",tag="cstate")
			dpg.add_spacer(height=5)
			dpg.add_separator()

		with dpg.child_window(autosize_x=True,border=False):
			with dpg.child_window(autosize_x=True,height=50,no_scrollbar=True):
				with dpg.group(horizontal=True):
					dpg.add_button(label="Play",width=65,height=30,tag="play",callback=play_pause)
					dpg.add_button(label="Stop",callback=stop,width=65,height=30)
					dpg.add_slider_float(tag="pos",width=-1,pos=(295,19),format="")

			with dpg.child_window(autosize_x=True,delay_search=True):
				with dpg.group(horizontal=True,tag="query"):
					dpg.add_input_text(hint="Search for a song",width=-1,callback=search)
				dpg.add_spacer(height=5)
				with dpg.child_window(autosize_x=True,delay_search=True,tag="list"):
					songs = load_database()
					for song in songs:
						search(app_data=song, sender=None, user_data=None)

	dpg.bind_item_theme("pos","slider")
	dpg.bind_item_theme("list","songs")

dpg.bind_theme("base")
dpg.bind_font(monobold)

def safe_exit():
	player.stop()

atexit.register(safe_exit)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("main",True)
dpg.maximize_viewport()
dpg.start_dearpygui()
dpg.destroy_context()

import json

def convert_duration(duration):
	duration = duration.split(":")
	duration = [int(i) for i in duration]
	if len(duration) == 3:
		return duration[0] * 3600 + duration[1] * 60 + duration[2]
	elif len(duration) == 2:
		return duration[0] * 60 + duration[1]
	elif len(duration) == 1:
		return duration[0]

def is_playing(player):
	return not player.core_idle

def music_ai(prompt, ai):
	res = ai.get_answer(prompt)
	return res['content']

def parse_response(response):
	start = response.find('[')
	end = response.find(']')+1
	music_list = eval(response[start:end])
	return music_list

def load_database():
	songs = json.load(open("data/songs.json", "r+"))["songs"]
	return songs

def update_database(song: str):
	data = json.load(open("data/songs.json", "r+"))
	if song not in data["songs"]:
		data["songs"] += [song]
	json.dump(data, open("data/songs.json", "r+"), indent=4)
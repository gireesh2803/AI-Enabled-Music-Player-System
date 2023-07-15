## OnSpotAI

An AI assisted music player that is capable of recommending songs based on previous history of the user as well as provide the best songs from the music history.

OnSpotAI has been created for its user-friendliness as well as for its various features.

### Features
- As every other music player does, this music player is also capable of playing, pausing and stopping a song.
- The "Best Songs" feature is one of our flagship feature which provides user with the latest and top hit songs in the industry.
- The "Reccomend Songs" feature is the other flagship feature which provides the user with the best recommended songs provided by google own generative AI called Bard. It is based on the previous song history that the user has listened to.
- The app provides anonymity for all listeners increasing their privacy without providing any login mechanism and using a generic API token for all applications.
- The user can reset his recommendation history just by removing the file called songs.json
- Users can freely share the songs.json file in order to get the recommendation of some other user

### Dependencies
- dearpygui
- mpv
- youtube-search-python
- bardapi
- yt-dlp

### Installation

Run the below command to install the player,
```
pip3 install -r requirements.txt
python3 onspotai
```

### Contributors
- Adhithya
- Gireesh
- Aswin K


import os 
import random
import threading

try:
    from playsound import playsound
    PLAYSOUND_OK = True
except ImportError:
    PLAYSOUND_OK = False
    print ("Music: playsound isnt installed.")
    
MUSIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "photontracks")

# tracks last played track, avoids repeats
last_track_idx = -1

# scans music folder
def get_tracks():
    tracks = []
    for f in os.listdir(MUSIC_DIR):
        if f.endswith(".mp3"):
            tracks.append(os.path.join(MUSIC_DIR, f))
    return tracks
    
def play(path):
    if not PLAYSOUND_OK:
        return
    music_thread = threading.Thread(target = playsound, args = (path,), daemon = True)
    music_thread.start()
    
# picks random track, avoids repeat, plays it
def play_music():
    global last_track_idx
    tracks = get_tracks()
    
    if not tracks:
        return
    
    choices = [i for i in range(len(tracks)) if i != last_track_idx]
    idx = random.choice(choices)
    last_track_idx = idx
    play(tracks[idx])


    
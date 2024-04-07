from tkinter import *
from tkinter import filedialog
import pygame.mixer as mixer  # pip install pygame
import os
import threading

# Initializing the mixer
mixer.init()

# Play, Stop, Load and Pause & Resume functions
def play_song(song_name: StringVar, songs_list: Listbox, status: StringVar, timeline_scale: Scale):
    try:
        song_name.set(songs_list.get(ACTIVE))

        mixer.music.load(songs_list.get(ACTIVE))
        mixer.music.play()

        status.set("Song PLAYING")
        update_timeline(timeline_scale)
    except Exception as e:
        status.set("Error: " + str(e))


def stop_song(status: StringVar):
    try:
        mixer.music.stop()
        status.set("Song STOPPED")
    except Exception as e:
        status.set("Error: " + str(e))


def load_directory(listbox):
    try:
        directory = filedialog.askdirectory(title='Open a songs directory')
        if directory:
            os.chdir(directory)

            tracks = os.listdir()

            for track in tracks:
                listbox.insert(END, track)
    except Exception as e:
        print("Error:", e)


def load(listbox):
    threading.Thread(target=load_directory, args=(listbox,)).start()


def pause_song(status: StringVar):
    try:
        mixer.music.pause()
        status.set("Song PAUSED")
    except Exception as e:
        status.set("Error: " + str(e))


def resume_song(status: StringVar):
    try:
        mixer.music.unpause()
        status.set("Song RESUMED")
    except Exception as e:
        status.set("Error: " + str(e))


def increase_volume(volume_label: Label):
    current_volume = mixer.music.get_volume()
    new_volume = min(current_volume + 0.1, 1.0)
    mixer.music.set_volume(new_volume)
    update_volume_label(volume_label, new_volume)


def decrease_volume(volume_label: Label):
    current_volume = mixer.music.get_volume()
    new_volume = max(current_volume - 0.1, 0.0)
    mixer.music.set_volume(new_volume)
    update_volume_label(volume_label, new_volume)


def update_volume_label(volume_label: Label, volume):
    volume_percent = int(volume * 100)
    volume_label.config(text=f"Volume: {volume_percent}%")


def update_timeline(timeline_scale: Scale):
    if mixer.music.get_busy():
        current_pos = mixer.music.get_pos() / 1000  # Convert to seconds
        timeline_scale.set(current_pos)
        timeline_scale.after(1000, lambda: update_timeline(timeline_scale))


# Creating the master GUI
root = Tk()
root.geometry('700x300')  #
root.title('PythonGeeks Music Player')
root.resizable(0, 0)

# All the frames
song_frame = LabelFrame(root, text='Current Song', bg='LightBlue', width=400, height=80)
song_frame.place(x=0, y=0)

button_frame = LabelFrame(root, text='Control Buttons', bg='Turquoise', width=400, height=120)
button_frame.place(y=80)

listbox_frame = LabelFrame(root, text='Playlist', bg='RoyalBlue')
listbox_frame.place(x=400, y=0, height=200, width=300)

volume_frame = LabelFrame(root, text='Volume', bg='LightGreen')
volume_frame.place(x=0, y=180, width=700, height=70)

timeline_frame = Frame(root, bg='LightYellow')
timeline_frame.place(x=0, y=250, width=700, height=50)

# All StringVar variables
current_song = StringVar(root, value='<Not selected>')

song_status = StringVar(root, value='<Not Available>')

# Playlist ListBox
playlist = Listbox(listbox_frame, font=('Helvetica', 11), selectbackground='Gold')

scroll_bar = Scrollbar(listbox_frame, orient=VERTICAL)
scroll_bar.pack(side=RIGHT, fill=BOTH)

playlist.config(yscrollcommand=scroll_bar.set)

scroll_bar.config(command=playlist.yview)

playlist.pack(fill=BOTH, padx=5, pady=5)

# SongFrame Labels
Label(song_frame, text='CURRENTLY PLAYING:', bg='LightBlue', font=('Times', 10, 'bold')).place(x=5, y=20)

song_lbl = Label(song_frame, textvariable=current_song, bg='Goldenrod', font=("Times", 12), width=25)
song_lbl.place(x=150, y=20)

# Volume control buttons
increase_volume_btn = Button(volume_frame, text='Increase Volume', command=lambda: increase_volume(volume_label), cursor='hand2')
increase_volume_btn.pack(side=LEFT, padx=10, pady=10)

decrease_volume_btn = Button(volume_frame, text='Decrease Volume', command=lambda: decrease_volume(volume_label), cursor='hand2')
decrease_volume_btn.pack(side=LEFT, padx=10, pady=10)

# Volume label
initial_volume = mixer.music.get_volume()
initial_volume_percent = int(initial_volume * 100)
volume_label = Label(volume_frame, text=f"Volume: {initial_volume_percent}%", font=("Helvetica", 10), bg='LightGreen')
volume_label.pack(side=LEFT, padx=10)

# Timeline scale
timeline_scale = Scale(timeline_frame, from_=0, to=100, orient=HORIZONTAL, length=700)
timeline_scale.pack(fill=X, padx=5, pady=5)

# Buttons in the main screen
pause_btn = Button(button_frame, text='Pause', bg='Aqua', font=("Georgia", 13), width=7,
                    command=lambda: pause_song(song_status), cursor='hand2')
pause_btn.place(x=15, y=10)

stop_btn = Button(button_frame, text='Stop', bg='Aqua', font=("Georgia", 13), width=7,
                  command=lambda: stop_song(song_status), cursor='hand2')
stop_btn.place(x=105, y=10)

play_btn = Button(button_frame, text='Play', bg='Aqua', font=("Georgia", 13), width=7,
                  command=lambda: play_song(current_song, playlist, song_status, timeline_scale), cursor='hand2')
play_btn.place(x=195, y=10)

resume_btn = Button(button_frame, text='Resume', bg='Aqua', font=("Georgia", 13), width=7,
                    command=lambda: resume_song(song_status), cursor='hand2')
resume_btn.place(x=285, y=10)

load_btn = Button(button_frame, text='Load Directory', bg='Aqua', font=("Georgia", 13), width=35,
                  command=lambda: load(playlist), cursor='hand2')
load_btn.place(x=10, y=55)

# Label at the bottom that displays the state of the music
Label(root, textvariable=song_status, bg='SteelBlue', font=('Times', 9), justify=LEFT).pack(side=BOTTOM)

# Finalizing the GUI
root.mainloop()

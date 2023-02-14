import sys, serial, time, wave, os, contextlib, win32api, tkinter.messagebox, serial.tools.list_ports
from tkinter.filedialog import askopenfilename
from pygame import mixer
from mutagen.mp3 import MP3
import tkinter as tk
import customtkinter as ctk

mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

nButtons = 20 # Number of buttons in the 2D-keyboard matrix
width, height = 900, 560 # Choose width and height of tkinter program
app = ctk.CTk() # Create the main app class
app.title(string="SusBoard") # Title of the app
app.geometry(f"{width}x{height}") # Set the start size of the window

dataList = ["None"] * nButtons # Create a "Empty" list which has a placeholder "None"

arduino = None
for port, desc, hwid in sorted(serial.tools.list_ports.comports()):
    print("{}: {} [{}]".format(port, desc, hwid))
    if "Arduino Uno" in desc:
        arduino = serial.Serial(port=port, baudrate=9600)
if arduino == None:
    tkinter.messagebox.showinfo("Soundboard", "Please connect the Soundboard with one of the USB ports")
# If data already exists, we read it
if os.path.exists("./data.txt"):
    print("Loading old data from data.txt...")
    data = open("./data.txt", "r").read()
    dataList = data.split("\n")
    print(dataList)
    print("Done loading!")
else:
    data = "\n".join(dataList)
    f = open("./data.txt", "w")
    f.write(data)
    f.close()
    print("New data file was created because old one did not exists")

VK_MEDIA_PLAY_PAUSE = 0xB3
VK_MEDIA_NEXT_TRACK = 0xB0
VK_MEDIA_PREV_TRACK = 0xB1
VK_VOLUME_UP = 0xAF
VK_VOLUME_DOWN = 0xAE

class BTN:
    def __init__(self, number):
        self.functionCommand = None
        self.number = number
        self.cmdOutput = "Empty"
        self.button = ctk.CTkButton(master=app, width=120, height=120, text=f"{self.number}", command=lambda:button_event(self.number))
        self.button.grid(row=self.number//5, column=self.number-(self.number//5)*5, padx=(10, 10), pady=(10, 10))
 
def get_length(path):
    if path.split("/")[-1].split(".")[-1] == "mp3":
        musicDuration = round(MP3(path).info.length, 1)
    else:
        with contextlib.closing(wave.open(path, "r")) as f:
            musicDuration = round(f.getnframes() / float(f.getframerate()), 1)
    return musicDuration

def button_event(n):
    global playingDuration
    label.configure(text=f"Selected {n}")
    musicLocation = dataList[n]
    
    slider.set(0)
    playingDuration = 0.0001
    
    for i in range(20):
        buttons[i].button.configure(fg_color=["#3B8ED0", "#1F6AA5"])
        buttons[i].button.configure(hover_color=["#36719F", "#144870"])
    buttons[n].button.configure(fg_color=["#36719F", "#144870"])
    buttons[n].button.configure(hover_color=["#3B8ED0", "#1F6AA5"])
    
    if musicLocation != "None":
        musicName = musicLocation.split("/")[-1]
        musicDuration = get_length(musicLocation)
        musicNameDisplay = " ".join(musicName.split(" ")[:2])
        musiclabel.configure(text=f"{musicNameDisplay}\n\n\n\n\n\n\n\n{musicDuration} seconds")
        slider.place(x=720, y=250)
    else:
        musiclabel.configure(text="")
        slider.place_forget()
    selectfileobject = ctk.CTkButton(master=app, text="Select audio file", command=lambda:openFile(n))
    selectfileobject.place(x=730, y=200)

def openFile(n):
    musicLocation = askopenfilename(filetypes=(("*.wav", "*.mp3"), ("all files", "*.*")))
    musicName = musicLocation.split("/")[-1]
    dataList[n] = musicLocation
    musicDuration = get_length(musicLocation)
    musicNameDisplay = " ".join(musicName.split(" ")[:2])
    slider.place(x=720, y=250)
    musiclabel.configure(text=f"{musicNameDisplay}\n\n\n\n\n\n\n\n{musicDuration} seconds")
    print(f'Button {n} has sound "{musicName}"')

buttons = []
for i in range(20):
    buttons.append(BTN(i))
    
label = ctk.CTkLabel(master=app, text="")
label.place(x=730, y=100)

savedlabel = ctk.CTkLabel(master=app, text="")
savedlabel.configure(font=("Helvetica bold", 26))
savedlabelwidth, savedlabelheight = savedlabel.cget("width"), savedlabel.cget("height")
savedlabel.place(x=730, y=400)

musiclabel = ctk.CTkLabel(master=app, text="")
musiclabel.place(x=730, y=150)

slider = ctk.CTkSlider(master=app, width=160, state="disabled")

def pressed(event):
    global t2
    t2 = time.time()
    savedlabel.configure(text="Saved")
    f = open("./data.txt", "w")
    f.write("\n".join(dataList))
    f.close()
    print(dataList)
    print("Saved")

audioBegin = 0
playingDuration = 1
def playAudio(thing):
    global audioBegin, playingDuration
    if thing == "1": thing = 0
    if thing == "2": thing = 1
    if thing == "3": thing = 2
    if thing == "4": thing = 3
    if thing == "5": thing = 4
    if thing == "6": thing = 5
    if thing == "7": thing = 6
    if thing == "8": thing = 7
    if thing == "9": thing = 8
    if thing == "A": thing = 9
    if thing == "B": thing = 10
    if thing == "C": thing = 11
    if thing == "D": thing = 12
    if thing == "E": thing = 13
    if thing == "F": thing = 14
    if thing == "G": thing = 15
    if thing == "H": thing = 16
    if thing == "I": thing = 17
    if thing == "J": thing = 18
    if thing == "K": thing = 19
    
    sound = dataList[int(thing)]
    if sound != "None":
        button_event(int(thing))
        print(sound)
        mixer.music.load(sound)
        mixer.music.play()
        slider.set(0)
        audioBegin = time.time()
        playingDuration = get_length(sound)
    

t2 = -1
musicDuration = 1
running = True
def on_close():
    global running
    app.destroy()
    running = False
   
while running:
    app.protocol("WM_DELETE_WINDOW", on_close)
   
    t = time.time()
    
    app.bind("<Control-s>", pressed)
    
    if t2 + 2 < t:
        savedlabel.configure(text="")
        t2 = -1
        
    if (time.time()-audioBegin) / playingDuration <= 1:
        slider.set((time.time()-audioBegin) / playingDuration)
    
    arduinoInput = str(arduino.readline()).split("&")
    arduinoInput[0] = arduinoInput[0].replace("b'", "")
    arduinoInput[-1] = arduinoInput[-1].replace("\\r\\n'", "")
    if arduinoInput[-1] != "":
        print(str(arduino.readline()))
        playAudio(arduinoInput[-1])
    mixer.music.set_volume(float(arduinoInput[-2]))
    #hwcode = win32api.MapVirtualKey(VK_MEDIA_PLAY_PAUSE, 0)
    #win32api.keybd_event(VK_MEDIA_PLAY_PAUSE, hwcode)
    app.update_idletasks()
    app.update()
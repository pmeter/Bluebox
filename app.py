import tkinter as tk
from tkinter import ttk
import random
from PIL import Image, ImageTk
import platform
from app_logic import *

GUI_UPDATE_DELAY = 600

class Main(tk.Tk):

    def __init__(self, parent=None):
        tk.Tk.__init__(self, parent)
        self.configure(background="black")
        self.parent = parent
        self.geometry('1024x600')
        self.title("Bluebox")

        self.status = Status()
        self.control = Control(self.status)

        self.bind("<Escape>", exit)

        self.setframes()
        
    def setframes(self):

        self.frame1 = Frame1(self, self.status, self.control)
        self.frame2 = Frame2(self, self.status, self.control)
        self.frame3 = Frame3(self, self.status, self.control)
        self.frame4 = Frame4(self, self.status, self.control)
        
        self.frame1.grid(row=0, column=0, sticky=tk.NW+tk.SE, padx=10, pady=10)
        self.frame2.grid(row=1, column=0, sticky=tk.NW+tk.SE, padx=10, pady=10)
        self.frame3.grid(row=2, column=0, sticky=tk.NW+tk.SE, padx=0, pady=0) 
        self.frame4.grid(row=3, column=0, sticky=tk.NW+tk.SE, padx=10, pady=10)

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=0)
        
        self.grid_columnconfigure(0, weight=1)
        
class Frame1(tk.Frame): # (Bluebox, Spotify, MP3, RADIO)
    def __init__(self, parent, status, control):
        tk.Frame.__init__(self, parent, bg="black", highlightbackground="#ff9900",  \
            highlightcolor="#ff9900", highlightthickness=2, bd= 0)
        self.parent = parent
        self.status = status
        self.control = control
        self.widgets()

    def widgets(self):
        def quit():
            Main.quit(self)

        self.bluebox = tk.Button(self, command=quit, width="10", height="0", bg="black", fg="grey", font=('', 18), relief=tk.FLAT, highlightthickness=0)
        self.bluebox.configure(text="BLUEBOX")
        self.bluebox.grid(row=0, column=0, padx=0, pady=0, sticky=tk.NW+tk.SE)

        self.spotify = tk.Label(self, width="10", height="0", bg="black", fg="grey", font=('', 18), relief=tk.FLAT)
        self.spotify.configure(text="Spotify")
        self.spotify.grid(row=0, column=1, padx=0, pady=0, sticky=tk.NW+tk.SE)
        
        if self.status.mp3_on() is True: mp3_foregroundcolor = "#FFF8DC"
        else: mp3_foregroundcolor = "grey"
        self.mp3 = tk.Label(self, width="10", height="0", bg="black", fg=mp3_foregroundcolor, font=('', 18), relief=tk.FLAT)
        self.mp3.configure(text="MP3")
        self.mp3.grid(row=0, column=2, padx=0, pady=0, sticky=tk.NW+tk.SE)

        if self.status.radio_on() is True: radio_foregroundcolor = "#FFF8DC"
        else: radio_foregroundcolor = "grey"
        self.radio = tk.Label(self, width="10", height="0", bg="black", fg=radio_foregroundcolor, font=('', 18), relief=tk.FLAT)
        self.radio.configure(text="RADIO")
        self.radio.grid(row=0, column=3, padx=0, pady=0, sticky=tk.NW+tk.SE)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)

        self.after(GUI_UPDATE_DELAY, self.update)
        
    def update(self):
        if self.status.mp3_on() is True: mp3_foregroundcolor = "#FFF8DC"
        else: mp3_foregroundcolor = "grey"
        if self.status.radio_on() is True: radio_foregroundcolor = "#FFF8DC"
        else: radio_foregroundcolor = "grey"
        if self.status.spotify_on() is True: spotify_foregroundcolor = "#FFF8DC"
        else: spotify_foregroundcolor = "grey"
        self.mp3.configure(text="MP3", fg=mp3_foregroundcolor)
        self.radio.configure(text="RADIO", fg=radio_foregroundcolor)
        self.spotify.configure(text="Spotify", fg=spotify_foregroundcolor)
        self.after(GUI_UPDATE_DELAY, self.update)

class Frame2(tk.Frame): # PLAYING
    def __init__(self, parent, status, control):
        tk.Frame.__init__(self, parent, bg="black", highlightbackground="#ff9900",  \
            highlightcolor="#ff9900", highlightthickness=2, bd= 0)
        self.parent = parent
        self.status = status
        self.control = control   
        self.service = "PLAYING"
        self.widgets()

    def widgets(self):
        self.playing = tk.Label(self, height="1", bg="black", fg="#FFF8DC", font=('', 14), anchor=tk.W)
        self.playing.configure(text="")
        self.playing.pack(side=tk.LEFT)

        self.playing = tk.Label(self, height="1", bg="black", fg="#FFF8DC", font=('', 14), anchor=tk.W)
        self.playing.configure(text="PLAYING")
        self.playing.place(x=5, y=0, width=110, relheight=1)

        self.line = tk.Label(self, width="2", height="2", bg="#ff9900", fg="#ff9900", text="")
        self.line.place(x=110, y=0, width=2, relheight=1)

        self.DIR = tk.Label(self, height="2", bg="black", fg="#FFF8DC", font=('', 14), anchor=tk.W)
        self.DIR.configure(text="")
        self.DIR.place(x=117, y=0, relwidth=1, relheight=1, width=-117)

        self.update()

    def update(self):
        if self.status.mp3_on() is True:
            playing_dir_and_file = self.status.check_playing_dir_and_file()
            playing_dir_and_file = playing_dir_and_file.replace("__", "_")
            self.DIR.configure(text=playing_dir_and_file)
        if self.status.radio_on() is True:
            self.DIR.configure(text=self.status.check_radiostation())
        if self.status.spotify_on() is True:
            self.DIR.configure(text=self.status.check_artist() + " - " + self.status.check_album() + \
                " - " + self.status.check_songname())
        
        self.after(GUI_UPDATE_DELAY, self.update)

class Frame3(tk.Frame):
    def __init__(self, parent, status, control):
        tk.Frame.__init__(self, parent, bg="black")
        self.parent = parent
        self.status = status
        self.control = control      
        self.setsubframes3L()

    def setsubframes3L(self):

        self.frame3L1A = Frame3L1A(self, self.status, self.control)
        self.frame3L1B = Frame3L1B(self, self.status, self.control)
        self.frame3L2 = Frame3L2(self, self.status, self.control)
        self.frame3L3 = Frame3L3(self, self.status, self.control)
        self.frame3R = Frame3R(self, self.status, self.control)
        
        self.frame3L1A.place(relx=0.5, rely=0, relheight=0, width=302, height=302, x=-312, y=10)
        self.frame3L1B.place(relx=0, rely=0, relwidth=0.25, relheight=0, width=-87, height=302, x=10, y=10)

        self.frame3L2.place(relx=0, rely=1, relwidth=0.5, width=-20, height=40, x=10, y=-85)
        self.frame3L3.place(relx=0, rely=1, relwidth=0.5, width=-20, height=40, x=10, y=-50)
        self.frame3R.place(relx=0.5, rely=0, relwidth=0.5, relheight=1, width=-20, height=-20, x=10, y=10)

class Frame3L1A(tk.Frame): # Image
    def __init__(self, parent, status, control):
        tk.Frame.__init__(self, parent, bg="black", highlightbackground="#ff9900",  \
            highlightcolor="#ff9900", highlightthickness=2, bd= 0)
        self.img_label = tk.Label(self, bg="black")
        self.img_label.pack(fill = "both", expand = True)
        self.currentimage_link = ""
        self.currentsong = ""
        self.currentradiosong= ""
        self.parent = Frame3
        self.status = status
        self.control = control
        self.albumart = Albumart(self.status)
        self.threading_image_update()

    def threading_image_update(self):
        threadObj = threading.Thread(target=self.display_new_image_if_needed)
        threadObj.start()
        
    def display_new_image_if_needed(self):
        if self.status.check_songname() != self.currentsong \
                or self.status.check_radio_title_playing() != self.currentradiosong:
            if self.albumart.return_image_link() != False:
                self.currentimage_link = self.albumart.return_image_link()
                self.currentsong = self.status.check_songname()
                self.currentradiosong = self.status.check_radio_title_playing()

                if self.albumart.return_image_link() != False:
                    print("Image location: " + self.albumart.return_image_link())

                if self.albumart.return_image_link().startswith("http"):
                    img = Image.open(urllib.request.urlopen(self.albumart.return_image_link()))
                else:
                    img = Image.open(self.albumart.return_image_link())
                basewidth = 320
                wpercent = (basewidth/float(img.size[0]))
                hsize = int((float(img.size[1])*float(wpercent)))
                img_resized = img.resize((basewidth,hsize), Image.ANTIALIAS)
                render = ImageTk.PhotoImage(img_resized)
                self.img_label.configure(image=render)
                self.img_label.image = render
                img.close()
            else: 
                print("False, want geen image link")
        self.after(1000, self.threading_image_update)

class Frame3L1B(tk.Frame):
    def __init__(self, parent, status, control):
        tk.Frame.__init__(self, parent, bg="black", highlightbackground="#ff9900",  \
            highlightcolor="#ff9900", highlightthickness=2, bd= 0)
        self.parent = Frame3
        self.status = status
        self.control = control  
        self.widgets()

    def widgets(self):
        
        def callback():
            print("click!")

        def callback2():
            Playlist()

        self.pause_button = tk.Button(self, text="Pause", command=self.control.pause, bg="black", fg="#ff9900", relief=tk.FLAT, highlightthickness=0)
        if os.path.exists(path + "APP_images/music.png"): 
            self.pause_button_image = tk.PhotoImage(file=path + "APP_images/pause.png")
            self.pause_button.config(image=self.pause_button_image)
        self.pause_button.place(x=0, y=0, relwidth=0.5, relheight=1/3)

        self.play_button = tk.Button(self, text="Play", command=self.control.play, bg="black", fg="#ff9900", relief=tk.FLAT, highlightthickness=0)
        if os.path.exists(path + "APP_images/music.png"): 
            self.play_button_image = tk.PhotoImage(file=path + "APP_images/play.png")
            self.play_button.config(image=self.play_button_image)
        self.play_button.place(relx=0.5, y=0, relwidth=0.5, relheight=1/3)      

        self.rewind_button = tk.Button(self, text="Rewind", command=self.control.seekbackward, fg="#ff9900", bg="black", relief=tk.FLAT, highlightthickness=0)
        if os.path.exists(path + "APP_images/music.png"): 
            self.rewind_button_image = tk.PhotoImage(file=path + "APP_images/rewind.png")
            self.rewind_button.config(image=self.rewind_button_image)
        self.rewind_button.place(x=0, rely=1/3, relwidth=0.5, relheight=1/3)
    
        self.forward_button = tk.Button(self, text="Forward", command=self.control.seekforward, fg="#ff9900", bg="black", relief=tk.FLAT, highlightthickness=0)
        if os.path.exists(path + "APP_images/music.png"): 
            self.forward_button_image = tk.PhotoImage(file=path + "APP_images/forward.png")
            self.forward_button.config(image=self.forward_button_image)        
        self.forward_button.place(relx=0.5, rely=1/3, relwidth=0.5, relheight=1/3)

        self.prevous_button = tk.Button(self, text="Previous", command=self.control.previous, fg="#ff9900", bg="black", relief=tk.FLAT, highlightthickness=0)
        if os.path.exists(path + "APP_images/music.png"): 
            self.prevous_button_image = tk.PhotoImage(file=path + "APP_images/previous.png")
            self.prevous_button.config(image=self.prevous_button_image)        
        self.prevous_button.place(x=0, rely=2/3, relwidth=0.5, relheight=1/3)

        self.next_button = tk.Button(self, text="Next", command=self.control.next, bg="black", fg="#ff9900", relief=tk.FLAT, highlightthickness=0)
        if os.path.exists(path + "APP_images/music.png"): 
            self.next_button_image = tk.PhotoImage(file=path + "APP_images/next.png")
            self.next_button.config(image=self.next_button_image)
        self.next_button.place(relx=0.5, rely=2/3, relwidth=0.5, relheight=1/3)

        self.linev1 = tk.Label(self, bg="#ff9900", fg="#ff9900", text="")
        self.linev2 = tk.Label(self, bg="#ff9900", fg="#ff9900", text="")
        self.linev3 = tk.Label(self, bg="#ff9900", fg="#ff9900", text="")
        self.lineh1 = tk.Label(self, bg="#ff9900", fg="#ff9900", text="")
        self.lineh2 = tk.Label(self, bg="#ff9900", fg="#ff9900", text="")
                
        self.linev1.place(relx=0.5, rely=0, width=2, relheight=1/3)
        self.linev2.place(relx=0.5, rely=1/3, width=2, relheight=1/3)
        self.linev3.place(relx=0.5, rely=2/3, width=2, relheight=1/3)

        self.lineh1.place(x=0, rely=1/3, relwidth=1, height=2)
        self.lineh2.place(x=0, rely=2/3, relwidth=1, height=2)
        

class Frame3L2(tk.Frame): # quality, repeat, shuffle
    def __init__(self, parent, status, control):
        tk.Frame.__init__(self, parent, bg="black")
        self.parent = Frame3
        self.status = status
        self.control = control   
        self.setsubframes3L2()

    def setsubframes3L2(self):   

        self.frame3L2Q = Frame3L2Q(self, self.status, self.control)
        self.frame3L2R = Frame3L2R(self, self.status, self.control)
        self.frame3L2S = Frame3L2S(self, self.status, self.control)
 
        self.frame3L2Q.place(relx=0, rely=0, width=180, height=40, x=0, y=0) 
        self.frame3L2R.place(relx=0.5, rely=0, width=180, height=40, x=-90, y=0)
        self.frame3L2S.place(relx=1, rely=0, width=180, height=40, x=-180, y=0)

class Frame3L2Q(tk.Frame): # quality
    def __init__(self, parent, status, control):
        tk.Frame.__init__(self, parent, bg="black", highlightbackground="#ff9900",  \
            highlightcolor="#ff9900", highlightthickness=2, bd= 0)
        self.parent = Frame3L2
        self.status = status
        self.control = control  
        self.widgets()

    def widgets(self):
        self.q = tk.Label(self)
        self.q.status = tk.Label(self, bg="black", fg="#FFF8DC", font=('', 12))
        self.q.status.configure(text="Q: " + self.status.check_quality())
        self.q.status.place(x=0, y=0, rely=0, relwidth=1, relheight=1, height=0)

        self.update()

    def update(self):
        self.q.status.configure(text="Q: " + self.status.check_quality())
        self.after(GUI_UPDATE_DELAY, self.update)


class Frame3L2R(tk.Frame): # repeat
    def __init__(self, parent, status, control):
        tk.Frame.__init__(self, parent, bg="black", highlightbackground="#ff9900",  \
            highlightcolor="#ff9900", highlightthickness=2, bd= 0)
        self.parent = Frame3L2
        self.status = status
        self.control = control  
        self.widgets()

    def widgets(self):
        self.r = tk.Button(self)
        self.r.status = tk.Button(self, command=self.control.repeattoggle, bg="black", fg="#FFF8DC", font=('', 12), relief=tk.FLAT, highlightthickness=0)
        self.r.status.configure(text="R: " + self.status.check_repeat())
        self.r.status.place(x=0, y=0, rely=0, relwidth=1, relheight=1, height=0)

        self.update()

    def update(self):
        self.r.status.configure(text="R: " + self.status.check_repeat())
        self.after(GUI_UPDATE_DELAY, self.update)  

class Frame3L2S(tk.Frame): # shuffle
    def __init__(self, parent, status, control):
        tk.Frame.__init__(self, parent, bg="black", highlightbackground="#ff9900",  \
            highlightcolor="#ff9900", highlightthickness=2, bd= 0)
        self.parent = Frame3L2
        self.status = status
        self.control = control  
        self.widgets()

    def widgets(self):
        self.s = tk.Label(self)
        self.s.status = tk.Label(self, bg="black", fg="#FFF8DC", font=('', 12))
        self.s.status.configure(text="S: " + self.status.check_shuffle())
        self.s.status.place(x=0, y=0, rely=0, relwidth=1, relheight=1, height=0)

        self.update()

    def update(self):
        self.s.status.configure(text="S: " + self.status.check_shuffle())
        self.after(GUI_UPDATE_DELAY, self.update)     

class Frame3L3(tk.Frame): # Control
    def __init__(self, parent, status, control):
        tk.Frame.__init__(self, parent, bg="black", highlightbackground="#ff9900",  \
            highlightcolor="#ff9900", highlightthickness=2, bd= 0)
        self.parent = Frame3
        self.status = status
        self.control = control  
        self.widgets()

    def widgets(self):
        def callback(getypt):
            Keyb_input_processor(self.control_input.get(), self.status, self.control)
            self.control_input.delete(0, 'end')

        self.control_input = tk.Entry(self, bg="black", fg="#00FF00", font=('', 16), relief=tk.FLAT)
        self.control_input.place(x=156, y=0, height=35, relwidth=1, width=-156)
        self.control_input.focus_set()
        self.control_input.bind("<Return>", (lambda event: callback(self.control_input.get())))
        self.control_input.bind("<KP_Enter>", (lambda event: callback(self.control_input.get())))

        self.control_title = tk.Label(self, bg="black", fg="#FFF8DC", font=('', 14), anchor=tk.W)
        self.control_title.configure(text="CONTROL")
        self.control_title.place(x=5, y=0, width=150, height=35)

        self.linev1 = tk.Label(self, bg="#ff9900", fg="#ff9900", text="")
        self.linev1.place(x=154, y=0, width=2, height=35)

class Frame3R(tk.Frame): # Playlist
    def __init__(self, parent, status, control):
        tk.Frame.__init__(self, parent, bg="black", highlightbackground="#ff9900",  \
            highlightcolor="#ff9900", highlightthickness=2, bd= 0)
        self.parent = Frame3
        self.status = status
        self.control = control 
        self.playlist_logic = Playlist(self.status)
        self.playlistwidget()
        self.playlist_click_commands()
        self.get_and_order_playlist()
        self.updateplaylist()

    def playlistwidget(self):

        self.playlist_nr_list = []
        self.playlist_entry_list = []

        for i in range (0,plG_length):
            
            self.playlist_nr = tk.Button(self, bg="black", font=("", 14), relief=tk.FLAT, highlightthickness=0)
            self.playlist_entry = tk.Button(self, bg="black",font=("", 14), relief=tk.FLAT, anchor=tk.W, highlightthickness=0)
        
            self.playlist_nr_list.append(self.playlist_nr)
            self.playlist_entry_list.append(self.playlist_entry)
        
            self.playlist_nr.grid(row=i, column=0, padx=0, pady=0, sticky=tk.W)
            self.playlist_entry.grid(row=i, column=1, padx=0, pady=0, sticky=tk.W+tk.E)
            
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

    def playlist_click_commands(self):
        try:
            self.playlist_nr_list[0].config(command= lambda: Bluesound_goto_specified_playlist_position(1))
            self.playlist_entry_list[0].config(command= lambda: self.playlist_click_command_translate(1))
            self.playlist_entry_list[1].config(command= lambda: self.playlist_click_command_translate(2))
            self.playlist_entry_list[2].config(command= lambda: self.playlist_click_command_translate(3))
            self.playlist_entry_list[3].config(command= lambda: self.playlist_click_command_translate(4))
            self.playlist_entry_list[4].config(command= lambda: self.playlist_click_command_translate(5))
            self.playlist_entry_list[5].config(command= lambda: self.playlist_click_command_translate(6))
            self.playlist_entry_list[6].config(command= lambda: self.playlist_click_command_translate(7))
            self.playlist_entry_list[7].config(command= lambda: self.playlist_click_command_translate(8))
            self.playlist_entry_list[8].config(command= lambda: self.playlist_click_command_translate(9))
            self.playlist_entry_list[9].config(command= lambda: self.playlist_click_command_translate(10))
            self.playlist_entry_list[10].config(command= lambda: self.playlist_click_command_translate(11))
            self.playlist_entry_list[11].config(command= lambda: self.playlist_click_command_translate(12))
            self.playlist_entry_list[12].config(command= lambda: self.playlist_click_command_translate(13))
            self.playlist_entry_list[13].config(command= lambda: self.playlist_click_command_translate(14))
        except IndexError as error:
            None
    
    def playlist_click_command_translate(self, input):
        Bluesound_goto_specified_playlist_position(self.begin + input)
         
    def get_and_order_playlist(self):

        self.playing_0strt = self.playlist_logic.check_songid()
        self.playing_1strt = self.playing_0strt + 1

        self.playlist = self.playlist_logic.check_playlist()

        lastpage = False
        if self.playing_1strt > len(self.playlist) - plG_length: # als playing_1strt in de laatste 14 zit
            lastpage = True

        if len(self.playlist) <= plG_length: # korte playlist blijft zo
            self.playlist_to_display = self.playlist[0:]
            self.first_in_playlist_is_song_id = 0

        if len(self.playlist) > plG_length: # Langere playlist wordt ingekort
            if self.playing_1strt <= 2: # als 1e of 2e nr speelt, dan 1e bovenaan
                self.begin = 0
                self.end = self.begin + plG_length
            if self.playing_1strt > 2 and lastpage is False: # als 3e of later nr speelt, dan die ervoor bovenaan
                self.begin = self.playing_1strt -2
                self.end = self.begin + plG_length
            if self.playing_1strt > 2 and lastpage is True:    
                self.begin = len(self.playlist) - plG_length
                self.end = len(self.playlist)
            self.playlist_to_display = self.playlist[self.begin:self.end]

        self.dict = {}

        self.dict = { i : self.playlist_to_display[i] for i in range(0, len(self.playlist_to_display) ) }

        self.GUI_nr_list = []
        self.greenkey = None

        for key in self.dict:

            if len(self.playlist) <= plG_length: # bij korte playlist staat GUI-nr gelijk aan key + 1
                GUI_nr = key + 1 # displaynr

                if key == self.playing_0strt: # bij korte playlist bovenste groen
                    self.greenkey = key

            if len(self.playlist) > plG_length: # bij lange playlist staat GUI-nr gelijk aan:
                if self.playing_1strt <= 2: # als 1e of 2e nr speelt, dan die bovenaan
                    GUI_nr = key + 1

                    if key == self.playing_0strt:
                        self.greenkey = key

                if self.playing_1strt > 2 and lastpage is False: # als 3e of later nr speelt, dan die ervoor bovenaan
                    GUI_nr = key + self.playing_1strt -1

                    if key == 1:
                        self.greenkey = key

                if self.playing_1strt > 2 and lastpage is True: # laatste pagina anders
                    GUI_nr = key + len(self.playlist) - plG_length + 1
                    if key == plG_length - (len(self.playlist) - self.playing_1strt) -1:
                        self.greenkey = key
        
            self.GUI_nr_list.append(GUI_nr)

    def updateplaylist(self):

        foregroundcolor="#FFF8DC"

        self.get_and_order_playlist()

        times = 0

        for key in self.dict:
            
            times = times + 1

            if key == self.greenkey:
                foregroundcolor = "#00FF00" # green
            else:
                foregroundcolor = "#FFF8DC"

            self.playlist_nr_list[key].config(text=self.GUI_nr_list[key], fg=foregroundcolor)
            self.playlist_entry_list[key].config(text=self.dict[key], fg=foregroundcolor)   
  
        # Bij korte playlist (na weergave langere) de oude balken overschrijven met niets
        if times < plG_length:
            for i in range (times,plG_length):
                self.playlist_nr_list[i].config(text="", fg=foregroundcolor)
                self.playlist_entry_list[i].config(text="", fg=foregroundcolor)

        self.after(GUI_UPDATE_DELAY, self.updateplaylist)

    def goto_item(self, input):
        print(str(self.command_list[input]))

class Frame4(tk.Frame): # Progress
    def __init__(self, parent, status, control):
        tk.Frame.__init__(self, parent, bg="black", highlightbackground="#ff9900",  \
            highlightcolor="#ff9900", highlightthickness=2, bd= 0)
        self.parent = Frame3
        self.status = status
        self.control = control      
        self.widgets()

    def widgets(self):
        self.hight = tk.Label(self, height="1", bg="black", fg="#FFF8DC", font=('', 20), anchor=tk.W)
        self.hight.configure(text="")
        self.hight.pack(side=tk.LEFT)

        self.timer = tk.Label(self, width="15", height="1", bg="black", fg="#00FF00", font=('', 18), anchor=tk.W)
        self.timer.configure(text=self.status.check_progress_converted() + " / " + \
                    self.status.check_totlen_converted())
        self.timer.place(x=5, y=0, width=160, relheight=1)

        self.line = tk.Label(self, width="2", height="2", bg="#ff9900", fg="#ff9900", text="")
        self.line.place(x=160, y=0, width=2, relheight=1)

        s = ttk.Style()
        s.theme_use('clam')
        s.configure("mystyle.Horizontal.TProgressbar", background="#006600", bordercolor="black", \
            lightcolor="#009900", darkcolor="#004d00", troughcolor="black")

        self.progressbar = ttk.Progressbar(self, style="mystyle.Horizontal.TProgressbar", orient="horizontal", \
             length=1000, mode="determinate")
        self.progressbar.place(x=164, rely=0.25, relwidth=1, relheight=0.5, width=-166)
        self.progressbar["maximum"] = 1000
        self.progressbar_update()

    def progressbar_update(self):
        self.timer.configure(text=self.status.check_progress_converted() + " / " + \
                    self.status.check_totlen_converted())
        
        self.progressbar["value"] = self.status.check_rel_progress()
        self.after(GUI_UPDATE_DELAY, self.progressbar_update)

if __name__=="__main__":
    app = Main(None)
    app.mainloop()
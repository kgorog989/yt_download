import customtkinter as ctk
from settings import *
from pytubefix import YouTube, Playlist

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        #setup
        self.title(" ")
        self.geometry(f"{APP_SIZE[0]}x{APP_SIZE[1]}")
        self.resizable(False, False)
        self.iconbitmap("empty.ico")
        
        #creating variables
        task_type_variable = ctk.StringVar(value="single")
        streaming_type_variable = ctk.StringVar(value="audio")
        quality_type_variable = ctk.StringVar(value="best")
        
        #creating fonts
        title_font = ctk.CTkFont(family=FONT, size=TITLE_FONT_SIZE, weight=TITLE_FONT_WEIGHT)
        main_font = ctk.CTkFont(family=FONT, size=MAIN_FONT_SIZE)
        
        #creating widgets
        label = TitleLabel(self, text="YouTube Downloader", font=title_font)
        frame = OptionsFrame(self, main_font, task_type_variable, streaming_type_variable, quality_type_variable)
        entry = LinkEntry(self, width=LINK_WIDTH, font=main_font)
        button = DownloadButton(self, font=main_font, command=lambda: self.download(entry, task_type_variable, streaming_type_variable, quality_type_variable))    
        
        # packing the widgets
        label.place(relx=0.5, rely=0.2, anchor="center")
        frame.place(relx=0.5, rely=0.5, anchor="center")
        entry.place(relx=0.5, rely=0.8, anchor="center")
        button.place(relx=0.5, rely=0.9, anchor="center")
        
    def download(self, entry, task_type_variable, streaming_type_variable, quality_type_variable):
        #getting the yt link
        link = entry.get()
        
        if task_type_variable.get() == "single":
            try:
                yt = YouTube(link)
                
                #filtering streams
                if streaming_type_variable.get() == "audio":
                    streams_available = yt.streams.filter(only_audio=True)
                    print(streams_available)
                elif streaming_type_variable.get() == "video":
                    streams_available = yt.streams.filter(only_video=True)
                    print(streams_available)
                else: #when streaming_type_variable is "both"
                    streams_available = yt.streams.filter(progressive=True)
                    print(streams_available)
                
                
                
                stream = streams_available.first()
                print(stream)

                #stream.download()
                print('Task Completed!')
            except:
                print("single error")
        else:
            try:
                playlist = Playlist(link)
                
                for video in playlist.videos:
                    ys = video.streams.get_audio_only()
                    ys.download(mp3=True)
            except:
                print("playlist error")
        

class OptionsFrame(ctk.CTkFrame):
    def __init__(self, parent, font, task_type_variable, streaming_type_variable, quality_type_variable):
        super().__init__(parent, fg_color="transparent")
        
        self.columnconfigure((0,1,2), weight=1, uniform="a")
        self.rowconfigure(0, weight=1, uniform="a")
        
        task_type_frame = TaskTypeFrame(self, font, task_type_variable)
        streaming_type_frame = StreamingTypeFrame(self, font, streaming_type_variable)
        quality_type_frame = QualityTypeFrame(self, font, quality_type_variable)
        
        task_type_frame.grid(column=0, row=0, sticky="nsew", padx=20, pady=20)
        streaming_type_frame.grid(column=1, row=0, sticky="nsew", padx=20, pady=20)
        quality_type_frame.grid(column=2, row=0, sticky="nsew", padx=20, pady=20)
        
class TaskTypeFrame(ctk.CTkFrame):
    def __init__(self, parent, font, variable):
        super().__init__(parent, fg_color="transparent")
        
        label = TitleLabel(self, text="Select Type", font=font)
        radio1 = RadioButton(self, text="Single Video", font=font, value="single", variable=variable, command=lambda : print(variable.get()))
        radio2 = RadioButton(self, text="Playlist", font=font,value="playlist", variable=variable, command=lambda : print(variable.get()))
        
        label.pack()
        radio1.pack()
        radio2.pack()
      
class StreamingTypeFrame(ctk.CTkFrame):
    def __init__(self, parent, font, variable):
        super().__init__(parent, fg_color="transparent")
        
        label = TitleLabel(self, text="Download Type", font=font)
        radio1 = RadioButton(self, text="Audio", font=font, value="audio", variable=variable, command=lambda : print(variable.get()))
        radio2 = RadioButton(self, text="Video", font=font, value="video", variable=variable, command=lambda : print(variable.get()))
        radio3 = RadioButton(self, text="Both", font=font, value="both", variable=variable, command=lambda : print(variable.get()))
        
        label.pack()
        radio1.pack()
        radio2.pack()
        radio3.pack()
           
class QualityTypeFrame(ctk.CTkFrame):
    def __init__(self, parent, font, variable):
        super().__init__(parent, fg_color="transparent")
        
        label = TitleLabel(self, text="Quality Type", font=(FONT, MAIN_FONT_SIZE))
        radio1 = RadioButton(self, text="Best", font=font, value="best", variable=variable, command=lambda: print(variable.get()))
        radio2 = RadioButton(self, text="Worst", font=font, value="worst", variable=variable, command=lambda: print(variable.get()))
        
        label.pack()
        radio1.pack()
        radio2.pack()

class TitleLabel(ctk.CTkLabel):
    def __init__(self, parent, text, font):
        super().__init__(parent, 
                          text = text, 
                          font = font)

class RadioButton(ctk.CTkRadioButton):
    def __init__(self, parent, text, font, value, variable, command):
        super().__init__(parent, 
                          text = text, 
                          font = font, 
                          value = value, 
                          variable = variable, 
                          command = command, 
                          fg_color=RED, 
                          hover_color=BLACK)

class LinkEntry(ctk.CTkEntry):
    def __init__(self, parent, width, font):
        super().__init__(parent, 
                         width=width,
                         font=font, 
                         border_color=BLACK)

class DownloadButton(ctk.CTkButton):
    def __init__(self, parent, font, command):
        super().__init__(parent, 
                         text="Download", 
                         width=DOWNLOAD_WIDTH, 
                         font=font, 
                         fg_color=RED, 
                         hover_color=BLACK, 
                         command=command)
        
   
if __name__=='__main__':
    app = App()
    app.mainloop()
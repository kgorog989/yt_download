import os
import subprocess

import customtkinter as ctk
import ffmpeg
from pytubefix import YouTube, Playlist

from settings import *

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        #setup
        self.title(" ")
        self.geometry(f"{APP_SIZE[0]}x{APP_SIZE[1]}")
        self.resizable(False, False)
        self.iconbitmap("empty.ico")
        
        #creating variables
        self.task_type_variable = ctk.StringVar(value="single")
        self.streaming_type_variable = ctk.StringVar(value="audio")
        self.quality_type_variable = ctk.StringVar(value="best")
        
        #creating fonts
        title_font = ctk.CTkFont(family=FONT, size=TITLE_FONT_SIZE, weight=TITLE_FONT_WEIGHT)
        main_font = ctk.CTkFont(family=FONT, size=MAIN_FONT_SIZE)
        
        #creating widgets
        label = TitleLabel(self, text="YouTube Downloader", font=title_font)
        frame = OptionsFrame(self, main_font, self.task_type_variable, self.streaming_type_variable, self.quality_type_variable)
        self.entry = LinkEntry(self, width=LINK_WIDTH, font=main_font)
        button = DownloadButton(self, font=main_font, command=self.download)    
        
        # packing the widgets
        label.place(relx=0.5, rely=0.2, anchor="center")
        frame.place(relx=0.5, rely=0.5, anchor="center")
        self.entry.place(relx=0.5, rely=0.8, anchor="center")
        button.place(relx=0.5, rely=0.9, anchor="center")
        
    def download(self):
        #getting the yt link
        link = self.entry.get()
        
        popup_font = ctk.CTkFont(family=FONT, size=POPUP_FONT_SIZE)
        
        if self.task_type_variable.get() == "single":
            try:
                yt = YouTube(link)
                
                #filtering streams
                if self.streaming_type_variable.get() == "audio":
                    streams_available = yt.streams.filter(only_audio=True)
                    target_stream = self.filter_audio_streams(streams_available)
                    target_stream.download(output_path="downloads")
                elif self.streaming_type_variable.get() == "video":
                    streams_available = yt.streams.filter(only_video=True)
                    target_stream = self.filter_video_streams(streams_available)
                    target_stream.download(output_path="downloads")
                else: #when streaming_type_variable is "both"
                    #audio part
                    streams_available = yt.streams.filter(only_audio=True)
                    target_stream = self.filter_audio_streams(streams_available)
                    audio_string = target_stream.download(output_path="downloads")
                    
                    #video part
                    streams_available = yt.streams.filter(only_video=True)
                    target_stream = self.filter_video_streams(streams_available)
                    video_string = target_stream.download(output_path="downloads")
                    
                    subprocess.run([
                        "ffmpeg",
                        "-i", video_string,
                        "-i", audio_string,
                        "-c:v", "copy",
                        "-c:a", "aac",
                        f"{video_string.split('.')[0]}_merged.mp4"
                    ])
                    
                    for f in [video_string, audio_string]:
                        try:
                            os.remove(f)
                        except FileNotFoundError:
                            pass
                
                PopupMessage(self,font=popup_font, text="Download complete!")
                self.entry.delete(0, "end")
            except:
                PopupMessage(self,font=popup_font, text="Incorrect link input!")
        else: #when it is a playlist
            try:
                playlist = Playlist(link)
                
                for video in playlist.videos:
                    if self.streaming_type_variable.get() == "audio":
                        streams_available = video.streams.filter(only_audio=True)
                        target_stream = self.filter_audio_streams(streams_available)
                        #downloading the target
                        target_stream.download(output_path="downloads")
                    elif self.streaming_type_variable.get() == "video":
                        streams_available = video.streams.filter(only_video=True)
                        target_stream = self.filter_video_streams(streams_available)
                        #downloading the target
                        target_stream.download(output_path="downloads")
                    else: #when streaming_type_variable is "both"
                        streams_available = video.streams.filter(progressive=True)
                        target_stream = self.filter_progressive_streams(streams_available)
                        #downloading the target
                        target_stream.download(output_path="downloads")
                    
                #full download complete
                PopupMessage(self,font=popup_font, text="Download complete!")
                self.entry.delete(0, "end")
            except:
                PopupMessage(self,font=popup_font, text="Incorrect link input!")

    def filter_audio_streams(self, streams_available):
        if self.quality_type_variable.get() == "best":
            best = streams_available.first()
            for stream in streams_available:
                if int(best.abr.rstrip("kbps")) < int(stream.abr.rstrip("kbps")):
                    best = stream
            target_stream = best
        else: #worst quality
            worst = streams_available.first()
            for stream in streams_available:
                if int(worst.abr.rstrip("kbps")) > int(stream.abr.rstrip("kbps")):
                    worst = stream 
            target_stream = worst
        return target_stream
            
    def filter_video_streams(self, streams_available):
        if self.quality_type_variable.get() == "best":
            best = streams_available.first()
            for stream in streams_available:
                if int(best.resolution.rstrip("p")) < int(stream.resolution.rstrip("p")):
                    best = stream
            target_stream = best
        else: #worst quality
            worst = streams_available.first()
            for stream in streams_available:
                if int(worst.resolution.rstrip("p")) > int(stream.resolution.rstrip("p")):
                    worst = stream 
            target_stream = worst
        return target_stream
            
    def filter_progressive_streams(self, streams_available):
        if self.quality_type_variable.get() == "best":
            best = streams_available.get_highest_resolution()
            target_stream = best
        else: #when its the worst
            worst = streams_available.get_lowest_resolution()
            target_stream = worst
        return target_stream

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
        radio1 = RadioButton(self, text="Single Video", font=font, value="single", variable=variable)
        radio2 = RadioButton(self, text="Playlist", font=font,value="playlist", variable=variable)
        
        label.pack()
        radio1.pack()
        radio2.pack()
      
class StreamingTypeFrame(ctk.CTkFrame):
    def __init__(self, parent, font, variable):
        super().__init__(parent, fg_color="transparent")
        
        label = TitleLabel(self, text="Download Type", font=font)
        radio1 = RadioButton(self, text="Audio", font=font, value="audio", variable=variable)
        radio2 = RadioButton(self, text="Video", font=font, value="video", variable=variable)
        radio3 = RadioButton(self, text="Both", font=font, value="both", variable=variable)
        
        label.pack()
        radio1.pack()
        radio2.pack()
        radio3.pack()
           
class QualityTypeFrame(ctk.CTkFrame):
    def __init__(self, parent, font, variable):
        super().__init__(parent, fg_color="transparent")
        
        label = TitleLabel(self, text="Quality Type", font=(FONT, MAIN_FONT_SIZE))
        radio1 = RadioButton(self, text="Best", font=font, value="best", variable=variable)
        radio2 = RadioButton(self, text="Worst", font=font, value="worst", variable=variable)
        
        label.pack()
        radio1.pack()
        radio2.pack()

class TitleLabel(ctk.CTkLabel):
    def __init__(self, parent, text, font):
        super().__init__(parent, 
                          text = text, 
                          font = font)

class RadioButton(ctk.CTkRadioButton):
    def __init__(self, parent, text, font, value, variable):
        super().__init__(parent, 
                          text = text, 
                          font = font, 
                          value = value, 
                          variable = variable, 
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

class PopupMessage(ctk.CTkToplevel):
    def __init__(self, parent, font, text):
        super().__init__(parent)     
        
        self.title(" ")
        self.geometry(f"{POPUP_SIZE[0]}x{POPUP_SIZE[1]}")
        self.resizable(False, False)
        self.iconbitmap("empty.ico")
        
        self.columnconfigure(0, weight=1, uniform='b')
        self.rowconfigure((0,1), weight=1, uniform='b')
        
        label = ctk.CTkLabel(self, text=text, font=font)
        button = ctk.CTkButton(self, 
                               font=font, 
                               fg_color=RED, 
                               hover_color=BLACK, 
                               text="Close", 
                               command=self.destroy)
        
        label.grid(column=0, row=0, sticky="sew", padx=20, pady=20)
        button.grid(column=0, row=1, sticky="nsew", padx=30, pady=30)
        
        #settings
        self.transient(parent)
        self.grab_set()
        parent.wait_window(self)
   
if __name__=='__main__':
    app = App()
    app.mainloop()
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pytubefix import YouTube
import threading

class YouTubeDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Video Downloader")
        self.root.geometry("600x400")
        self.root.configure(padx=20, pady=20)

        # URL Entry
        self.url_frame = ttk.LabelFrame(root, text="Video URL", padding="10")
        self.url_frame.pack(fill="x", pady=(0, 10))
        
        self.url_var = tk.StringVar()
        self.url_entry = ttk.Entry(self.url_frame, textvariable=self.url_var, width=50)
        self.url_entry.pack(side="left", padx=(0, 10))
        
        self.fetch_btn = ttk.Button(self.url_frame, text="Fetch Video Info", command=self.fetch_video)
        self.fetch_btn.pack(side="left")

        # Video Information
        self.info_frame = ttk.LabelFrame(root, text="Video Information", padding="10")
        self.info_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        self.title_label = ttk.Label(self.info_frame, text="Title: ")
        self.title_label.pack(anchor="w")
        
        self.length_label = ttk.Label(self.info_frame, text="Length: ")
        self.length_label.pack(anchor="w")
        
        # Resolution Selection
        self.resolution_var = tk.StringVar()
        self.resolution_combo = ttk.Combobox(self.info_frame, textvariable=self.resolution_var, state="disabled")
        self.resolution_combo.pack(pady=10)

        # Progress
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(root, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill="x", pady=(0, 10))
        
        self.status_label = ttk.Label(root, text="")
        self.status_label.pack()

        # Download Button
        self.download_btn = ttk.Button(root, text="Download", command=self.start_download, state="disabled")
        self.download_btn.pack()

        # Store streams for later use
        self.streams = []

    def fetch_video(self):
        try:
            self.url = self.url_var.get()
            if not self.url:
                messagebox.showerror("Error", "Please enter a YouTube URL")
                return
                
            self.status_label["text"] = "Fetching video information..."
            self.fetch_btn["state"] = "disabled"
            
            def fetch():
                try:
                    self.yt = YouTube(self.url)
                    
                    # Update UI in the main thread
                    self.root.after(0, self.update_video_info)
                except Exception as e:
                    self.root.after(0, lambda: self.handle_error(f"Error fetching video: {str(e)}"))
                
            thread = threading.Thread(target=fetch)
            thread.daemon = True
            thread.start()
            
        except Exception as e:
            self.handle_error(f"Error: {str(e)}")

    def update_video_info(self):
        try:
            # Update video information
            self.title_label["text"] = f"Title: {self.yt.title}"
            duration = f"{int(self.yt.length / 60)}:{str(self.yt.length % 60).zfill(2)}"
            self.length_label["text"] = f"Length: {duration}"
            
            # Get available streams
            # Include both progressive and adaptive streams for higher resolutions
            self.streams = self.yt.streams.filter(type="video").order_by('resolution').desc()
            
            # Create a list of unique resolutions with format
            resolutions = []
            added_resolutions = set()
            
            for stream in self.streams:
                stream_info = f"{stream.resolution} - {stream.mime_type}"
                if stream_info not in added_resolutions:
                    resolutions.append(stream_info)
                    added_resolutions.add(stream_info)
            
            self.resolution_combo["values"] = resolutions
            self.resolution_combo.set(resolutions[0] if resolutions else "")
            self.resolution_combo["state"] = "readonly"
            
            self.download_btn["state"] = "normal"
            self.fetch_btn["state"] = "normal"
            self.status_label["text"] = "Ready to download"
            
        except Exception as e:
            self.handle_error(f"Error updating video info: {str(e)}")

    def start_download(self):
        try:
            # Get selected resolution
            selected = self.resolution_combo.get()
            if not selected:
                messagebox.showerror("Error", "Please select a resolution")
                return
            
            resolution = selected.split()[0]  # Get just the resolution part (e.g., "1080p")
            
            # Ask for save location
            file_path = filedialog.asksaveasfilename(
                defaultextension=".mp4",
                filetypes=[("MP4 files", "*.mp4")],
                initialfile=f"{self.yt.title}.mp4"
            )
            
            if not file_path:
                return
                
            self.download_btn["state"] = "disabled"
            self.status_label["text"] = "Downloading..."
            
            def download():
                try:
                    # Find the best stream for the selected resolution
                    selected_stream = None
                    for stream in self.streams:
                        if stream.resolution == resolution:
                            selected_stream = stream
                            break
                    
                    if selected_stream is None:
                        raise Exception("Could not find selected resolution stream")
                    
                    # Download the video
                    selected_stream.download(filename=file_path)
                    
                    # Update UI in main thread
                    self.root.after(0, self.download_complete)
                    
                except Exception as e:
                    self.root.after(0, lambda: self.handle_error(f"Download error: {str(e)}"))
            
            thread = threading.Thread(target=download)
            thread.daemon = True
            thread.start()
            
        except Exception as e:
            self.handle_error(f"Error: {str(e)}")

    def download_complete(self):
        self.status_label["text"] = "Download completed!"
        self.download_btn["state"] = "normal"
        self.progress_var.set(100)
        messagebox.showinfo("Success", "Video downloaded successfully!")
        self.progress_var.set(0)

    def handle_error(self, message):
        self.status_label["text"] = message
        self.fetch_btn["state"] = "normal"
        self.download_btn["state"] = "normal"
        messagebox.showerror("Error", message)

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloaderGUI(root)
    root.mainloop()
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pydub import AudioSegment
import os
import subprocess

class AudioConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio Format Converter")
        self.root.geometry("600x400")
        
        # Input file variables
        self.input_file = ""
        self.output_format = tk.StringVar()
        
        # Format-specific options
        self.mp3_bitrate = tk.StringVar(value="192")
        self.mp3_mode = tk.StringVar(value="CBR")
        self.flac_compression = tk.StringVar(value="5")
        self.ogg_quality = tk.StringVar(value="5")
        self.aac_bitrate = tk.StringVar(value="128")
        
        self.create_widgets()
        
    def create_widgets(self):
        # File selection
        input_frame = ttk.LabelFrame(self.root, text="Input File", padding=10)
        input_frame.pack(fill="x", padx=10, pady=5)
        
        self.file_label = ttk.Label(input_frame, text="No file selected")
        self.file_label.pack(side="left", expand=True)
        
        select_btn = ttk.Button(input_frame, text="Select File", command=self.select_file)
        select_btn.pack(side="right")
        
        # Output format selection
        format_frame = ttk.LabelFrame(self.root, text="Output Format", padding=10)
        format_frame.pack(fill="x", padx=10, pady=5)
        
        formats = ["mp3", "flac", "wav", "aac", "ogg"]
        for fmt in formats:
            ttk.Radiobutton(format_frame, text=fmt, value=fmt, 
                            variable=self.output_format, 
                            command=self.update_options).pack(side="left", padx=10)
        
        # Options frame
        self.options_frame = ttk.LabelFrame(self.root, text="Conversion Options", padding=10)
        self.options_frame.pack(fill="x", padx=10, pady=5)
        
        # MP3 options
        self.mp3_frame = ttk.Frame(self.options_frame)
        ttk.Label(self.mp3_frame, text="Bitrate (kbps):").grid(row=0, column=0, padx=5, pady=5)
        mp3_bitrate_values = ["128", "192", "256", "320"]
        self.mp3_bitrate_combo = ttk.Combobox(self.mp3_frame, textvariable=self.mp3_bitrate, 
                                             values=mp3_bitrate_values)
        self.mp3_bitrate_combo.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self.mp3_frame, text="Mode:").grid(row=1, column=0, padx=5, pady=5)
        mp3_mode_values = ["CBR", "ABR", "VBR"]
        self.mp3_mode_combo = ttk.Combobox(self.mp3_frame, textvariable=self.mp3_mode,
                                          values=mp3_mode_values)
        self.mp3_mode_combo.grid(row=1, column=1, padx=5, pady=5)

        # FLAC options
        self.flac_frame = ttk.Frame(self.options_frame)
        ttk.Label(self.flac_frame, text="Compression Level (0-8) [Higher = Smaller File]:").grid(row=0, column=0, padx=5, pady=5)
        flac_compression_values = [str(i) for i in range(9)]
        self.flac_compression_combo = ttk.Combobox(self.flac_frame, textvariable=self.flac_compression,
                                                values=flac_compression_values)
        self.flac_compression_combo.grid(row=0, column=1, padx=5, pady=5)   

        # OGG options
        self.ogg_frame = ttk.Frame(self.options_frame)
        ttk.Label(self.ogg_frame, text="Quality (-1 to 10) [Higher = Better Quality]:").grid(row=0, column=0, padx=5, pady=5)
        ogg_quality_values = [str(i) for i in range(-1, 11)]
        self.ogg_quality_combo = ttk.Combobox(self.ogg_frame, textvariable=self.ogg_quality,
                                            values=ogg_quality_values)
        self.ogg_quality_combo.grid(row=0, column=1, padx=5, pady=5)   

        # AAC options
        self.aac_frame = ttk.Frame(self.options_frame)
        ttk.Label(self.aac_frame, text="Bitrate (kbps):").grid(row=0, column=0, padx=5, pady=5)
        aac_bitrate_values = ["64", "96", "128", "192", "256"]
        self.aac_bitrate_combo = ttk.Combobox(self.aac_frame, textvariable=self.aac_bitrate,
                                            values=aac_bitrate_values)
        self.aac_bitrate_combo.grid(row=0, column=1, padx=5, pady=5)
        
        # Convert button
        convert_btn = ttk.Button(self.root, text="Convert", command=self.convert_audio)
        convert_btn.pack(pady=20)
        
        # Progress bar
        self.progress = ttk.Progressbar(self.root, length=400, mode='determinate')
        self.progress.pack(pady=10)
        
    def update_options(self):
        # Hide all option frames
        for frame in [self.mp3_frame, self.flac_frame, self.ogg_frame, self.aac_frame]:
            frame.pack_forget()
        
        # Show relevant options based on format
        format = self.output_format.get()
        if format == "mp3":
            self.mp3_frame.pack(fill="x")
        elif format == "flac":
            self.flac_frame.pack(fill="x")
        elif format == "ogg":
            self.ogg_frame.pack(fill="x")
        elif format == "aac":
            self.aac_frame.pack(fill="x")
    
    def select_file(self):
        filetypes = (
            ('Audio files', '*.mp3 *.m4a *.flac *.wav *.aac *.ogg'),
            ('All files', '*.*')
        )
        
        self.input_file = filedialog.askopenfilename(filetypes=filetypes)
        if self.input_file:
            self.file_label.config(text=os.path.basename(self.input_file))
            
    def convert_audio(self):
        if not self.input_file:
            messagebox.showerror("Error", "Please select an input file")
            return
            
        if not self.output_format.get():
            messagebox.showerror("Error", "Please select an output format")
            return
            
        try:
            output_format = self.output_format.get()
            
            # Get output filename with appropriate extension
            if output_format == "aac":
                extension = ".m4a"
            else:
                extension = f".{output_format}"
                
            output_file = filedialog.asksaveasfilename(
                defaultextension=extension,
                filetypes=[(f"{output_format.upper()} files", f"*{extension}")])
            
            if not output_file:
                return
                
            self.progress["value"] = 0
            self.root.update_idletasks()
            
            if output_format == "aac":
                # Use QAAC for AAC encoding
                ffmpeg_cmd = [
                    "ffmpeg", "-i", self.input_file,
                    "-f", "wav", "-bitexact", "-"
                ]
                
                qaac_path = os.path.join(os.path.dirname(__file__), "qaac", "qaac64.exe")
                qaac_cmd = [
                    qaac_path,
                    "-v", self.aac_bitrate.get(),
                    "-o", output_file,
                    "-"
                ]
                
                # Create the pipeline
                ffmpeg_process = subprocess.Popen(
                    ffmpeg_cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                
                qaac_process = subprocess.Popen(
                    qaac_cmd,
                    stdin=ffmpeg_process.stdout,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                
                # Allow ffmpeg_process to receive a SIGPIPE if qaac_process exits
                ffmpeg_process.stdout.close()
                
                # Wait for completion
                qaac_output, qaac_error = qaac_process.communicate()
                
                if qaac_process.returncode != 0:
                    raise Exception(f"QAAC Error: {qaac_error.decode()}")
                    
            else:
                # Load the audio file
                audio = AudioSegment.from_file(self.input_file)
                
                # Format specific settings
                if output_format == "mp3":
                    mp3_mode = self.mp3_mode.get()
                    
                    if mp3_mode in ["CBR", "ABR"]:
                        params = [
                            "-c:a", "libmp3lame",
                            "-b:a", f"{self.mp3_bitrate.get()}k",
                            "-f", "mp3"
                        ]
                        if mp3_mode == "ABR":
                            params.extend(["-abr", "1"])
                    else:  # VBR
                        params = [
                            "-c:a", "libmp3lame",
                            "-V", "0",
                            "-f", "mp3"
                        ]
                    
                elif output_format == "flac":
                    params = [
                        "-c:a", "flac",
                        "-compression_level", self.flac_compression.get(),
                        "-f", "flac"
                    ]
                    
                elif output_format == "ogg":
                    params = [
                        "-c:a", "libvorbis",
                        "-q:a", self.ogg_quality.get(),
                        "-f", "ogg"
                    ]
                    
                elif output_format == "wav":
                    params = ["-f", "wav"]
                
                # Export the file
                audio.export(output_file, format=output_format, parameters=params)
            
            self.progress["value"] = 100
            self.root.update_idletasks()
            
            messagebox.showinfo("Success", "Conversion completed successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AudioConverterGUI(root)
    root.mainloop()
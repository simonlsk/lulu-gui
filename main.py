import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

from slider import CustomSlider


class VideoSectionApp:
    def __init__(self, root):
        self.root = root
        self.setup_ui()
        self.video_file = ""
        self.sections = []

    def setup_ui(self):
        # Set window title and size
        self.root.title("Video Section Selector")
        self.root.geometry("480x320")

        # Input Frame
        input_frame = tk.LabelFrame(self.root, text="Input", padx=10, pady=10)
        input_frame.pack(padx=10, pady=5, fill="x")

        # Browse Button
        self.browse_button = tk.Button(input_frame, text="Browse", command=self.browse_file)
        self.browse_button.pack(side="right")

        # Start and End Time Entries
        self.start_time_entry = tk.Entry(input_frame, width=10)
        self.start_time_entry.pack(side="left", padx=(0, 10))
        self.end_time_entry = tk.Entry(input_frame, width=10)
        self.end_time_entry.pack(side="left")

        # Add Section Button
        add_section_button = tk.Button(input_frame, text="Add section", command=self.add_section)
        add_section_button.pack(side="left", padx=10)

        # Custom Slider Frame
        self.slider_frame = tk.Frame(self.root)
        self.slider_frame.pack(fill="x", padx=20, pady=10)

        # Custom Slider
        self.slider = CustomSlider(self.slider_frame, 1000, 30)
        self.slider.pack(fill="x", expand=True)

        # Add buttons for setting start and end points
        self.set_start_button = tk.Button(self.slider_frame, text="Set Start", command=self.set_start)
        self.set_start_button.pack(side="left", padx=5)

        self.set_end_button = tk.Button(self.slider_frame, text="Set End", command=self.set_end)
        self.set_end_button.pack(side="right", padx=5)

        # Section List Frame
        section_list_frame = tk.LabelFrame(self.root, text="Sections", padx=10, pady=10)
        section_list_frame.pack(padx=10, pady=5, fill="both", expand=True)

        # Sections Listbox
        self.sections_listbox = tk.Listbox(section_list_frame)
        self.sections_listbox.pack(padx=5, pady=5, fill="both", expand=True)

        # Process Button
        process_button = tk.Button(self.root, text="Process", command=self.process_sections)
        process_button.pack(pady=5)

    def set_start(self):
        # Record the start value from the slider
        start_timecode = self.slider.get_smpte()
        # You can update the UI or internal state with this value
        print("Start timecode set to:", start_timecode)

    def set_end(self):
        # Record the end value from the slider
        end_timecode = self.slider.get_smpte()
        # You can update the UI or internal state with this value
        print("End timecode set to:", end_timecode)

    def browse_file(self):
        self.video_file = filedialog.askopenfilename(
            title="Select a video file",
            filetypes=(("Video files", "*.mp4 *.avi *.mov"), ("All files", "*.*")))
        if self.video_file:
            messagebox.showinfo("File Selected", f"Video file selected: {self.video_file}")

    def add_section(self):
        start = self.start_time_entry.get()
        end = self.end_time_entry.get()
        if start and end:
            section = f"{start}-{end}"
            self.sections.append(section)
            self.sections_listbox.insert(tk.END, section)
            self.start_time_entry.delete(0, tk.END)
            self.end_time_entry.delete(0, tk.END)

    def process_sections(self):
        if not self.sections:
            messagebox.showwarning("No Sections", "No sections have been added.")
            return
        if not self.video_file:
            messagebox.showwarning("No Video", "No video file has been selected.")
            return
        # Process sections (placeholder for actual processing)
        messagebox.showinfo("Processing", "The sections will be processed.")


root = tk.Tk()
app = VideoSectionApp(root)
root.mainloop()

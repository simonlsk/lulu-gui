import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox


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

        # Section List Frame
        section_list_frame = tk.LabelFrame(self.root, text="Sections", padx=10, pady=10)
        section_list_frame.pack(padx=10, pady=5, fill="both", expand=True)

        # Sections Listbox
        self.sections_listbox = tk.Listbox(section_list_frame)
        self.sections_listbox.pack(padx=5, pady=5, fill="both", expand=True)

        # Process Button
        process_button = tk.Button(self.root, text="Process", command=self.process_sections)
        process_button.pack(pady=5)

        # Section Time Range Frame
        time_range_frame = tk.LabelFrame(self.root, text="Time Range", padx=10, pady=10)
        time_range_frame.pack(padx=10, pady=5, fill="x")

        # Start Time Slider
        self.start_time_slider = tk.Scale(time_range_frame, from_=0, to=100, orient='horizontal', label='Start Time', length=200)
        self.start_time_slider.pack(side="left", padx=(0, 10))

        # End Time Slider
        self.end_time_slider = tk.Scale(time_range_frame, from_=0, to=100, orient='horizontal', label='End Time', length=200)
        self.end_time_slider.pack(side="left")

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

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
        self.current_start = None
        self.current_end = None

    def setup_ui(self):
        # Set window title and size
        self.root.title("Video Section Selector")
        self.root.geometry("480x480")

        # Input Frame
        input_frame = tk.LabelFrame(self.root, text="Input", padx=10, pady=10)
        input_frame.pack(padx=10, pady=5, fill="x")

        # File Path Entry
        self.file_path_entry = tk.Entry(input_frame)
        self.file_path_entry.pack(side='left', expand=True, padx=(0, 5), fill='x')

        # Open File Button
        self.open_file_button = tk.Button(input_frame, text="Open Video File", command=self.open_file)
        self.open_file_button.pack(side='right')

        # Start and End Time Entries
        # self.start_time_entry = tk.Entry(input_frame, width=10)
        # self.start_time_entry.pack(side="left", padx=(0, 10))
        # self.end_time_entry = tk.Entry(input_frame, width=10)
        # self.end_time_entry.pack(side="left")

        # Add Section Button
        # add_section_button = tk.Button(input_frame, text="Add section", command=self.add_section)
        # add_section_button.pack(side="left", padx=10)

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

        # Bind delete key
        self.sections_listbox.bind_all("<BackSpace>", self.delete_element)

        # Process Button
        process_button = tk.Button(self.root, text="Process", command=self.process_sections)
        process_button.pack(pady=5)

    def set_start(self):
        # Record the start value from the slider
        start_timecode = self.slider.get_smpte()
        # You can update the UI or internal state with this value
        previous_start = self.current_start
        self.current_start = start_timecode
        if previous_start is None:
            self.sections.append(f"{self.current_start}-<waiting for end selection>")
        else:
            self.sections[-1] = f"{self.current_start}-<waiting for end selection>"
            self.sections_listbox.delete(tk.END)
        self.sections_listbox.insert(tk.END, self.sections[-1])
        print("Start timecode set to:", start_timecode)

    def set_end(self):
        # Record the end value from the slider
        end_timecode = self.slider.get_smpte()
        # You can update the UI or internal state with this value
        self.current_end = end_timecode
        if self.current_end > self.current_start:
            self.add_section()
        print("End timecode set to:", end_timecode)

    def browse_file(self):
        self.video_file = filedialog.askopenfilename(
            title="Select a video file",
            filetypes=(("Video files", "*.mp4 *.avi *.mov"), ("All files", "*.*")))
        if self.video_file:
            messagebox.showinfo("File Selected", f"Video file selected: {self.video_file}")

    def add_section(self):
        start = self.current_start
        end = self.current_end
        if start and end:
            section = f"{start}-{end}"
            self.sections[-1] = section
            self.sections_listbox.delete(tk.END)
            self.sections_listbox.insert(tk.END, section)
            self.current_start = None
            self.current_end = None

    def process_sections(self):
        if not self.sections:
            messagebox.showwarning("No Sections", "No sections have been added.")
            return
        if not self.video_file:
            messagebox.showwarning("No Video", "No video file has been selected.")
            return
        # Process sections (placeholder for actual processing)
        messagebox.showinfo("Processing", "The sections will be processed.")

    def open_file(self):
        # Open a dialog to choose an .mp4 file
        file_path = filedialog.askopenfilename(
            title="Select a video file",
            filetypes=[("MP4 files", "*.mp4")],
            defaultextension=".mp4"
        )
        # If a file is selected, update the entry with the file path
        if file_path:
            self.file_path_entry.delete(0, tk.END)
            self.file_path_entry.insert(0, file_path)
            self.load_video(file_path)  # Load the video using the previously defined method

    def delete_element(self, arg):
        selected_indices = self.sections_listbox.curselection()
        # remove selected item from listbox and sections
        self.sections_listbox.delete(selected_indices[0], selected_indices[-1])
        self.sections = self.sections[:selected_indices[0]] + self.sections[selected_indices[-1] + 1:]


root = tk.Tk()
app = VideoSectionApp(root)
root.mainloop()

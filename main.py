import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import cv2
from PIL import ImageTk, Image

from slider import CustomSlider


class VideoSectionApp:
    def __init__(self, root):
        self.root = root
        self.setup_ui()
        self.video_file = ""
        self.sections = []
        self.current_start = None
        self.current_end = None
        self.video_length = None
        self.framerate = None
        self.cap = None

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

        # Video Display
        self.video_display = tk.Label(self.root)
        self.video_display.pack(padx=10, pady=10)

        # Custom Slider Frame
        self.slider_frame = tk.Frame(self.root)
        self.slider_frame.pack(fill="x", padx=20, pady=10)

        # Custom Slider
        self.slider = CustomSlider(self.slider_frame, 1000, 30, self.update_video_display)
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
        start_frame = self.slider.position
        # You can update the UI or internal state with this value
        previous_start = self.current_start
        self.current_start = start_timecode, start_frame
        if previous_start is None:
            self.sections.append((f"{self.current_start[0]}-<waiting for end selection>", (start_frame,)))
        else:
            self.sections[-1] = (f"{self.current_start[0]}-<waiting for end selection>", (start_frame,))
            self.sections_listbox.delete(tk.END)
        self.sections_listbox.insert(tk.END, self.sections[-1][0])
        print("Start timecode set to:", start_timecode)

    def set_end(self):
        # Record the end value from the slider
        end_timecode = self.slider.get_smpte()
        end_frame = self.slider.position
        # You can update the UI or internal state with this value
        self.current_end = end_timecode, end_frame
        if self.current_end[1] > self.current_start[1]:
            self.add_section()
        print("End timecode set to:", end_timecode)

    def add_section(self):
        start = self.current_start
        end = self.current_end
        if start and end:
            section = (f"{start[0]}-{end[0]}", (start[1], end[1]))
            self.sections[-1] = section
            self.sections_listbox.delete(tk.END)
            self.sections_listbox.insert(tk.END, section[0])
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
        messagebox.showinfo("Processing", f"The following sections will be processed: \n{self.sections}")

    def open_file(self):
        # Open a dialog to choose an .mp4 file
        file_path = filedialog.askopenfilename(
            title="Select a video file",
            filetypes=[("MP4 files", "*.mp4")],
            defaultextension=".mp4"
        )
        if self.cap is not None:
            self.cap.release()
            self.cap = None

        # If a file is selected, update the entry with the file path
        if file_path:
            self.file_path_entry.delete(0, tk.END)
            self.file_path_entry.insert(0, file_path)
            # todo: calculate framerate and length
            self.video_file = file_path
            # self.load_video(file_path)  # Load the video using the previously defined method
            self.video_length, self.framerate = self.get_video_info(file_path)
            self.reset_slider()
            # Open the video file using OpenCV
            self.cap = cv2.VideoCapture(self.video_file)


    def delete_element(self, arg):
        selected_indices = self.sections_listbox.curselection()
        # remove selected item from listbox and sections
        self.sections_listbox.delete(selected_indices[0], selected_indices[-1])
        self.sections = self.sections[:selected_indices[0]] + self.sections[selected_indices[-1] + 1:]

    def reset_slider(self):
        self.slider.set_video_length(self.video_length, self.framerate)
        self.sections = []
        self.sections_listbox.delete(0, tk.END)

    def get_video_info(self, video_path):
        # Open the video file using OpenCV
        cap = cv2.VideoCapture(video_path)

        # Check if the video file was opened successfully
        if not cap.isOpened():
            return None  # Unable to open the video

        # Get the total number of frames in the video
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # Get the framerate of the video
        framerate = cap.get(cv2.CAP_PROP_FPS)

        # Release the video capture object
        cap.release()
        return total_frames, framerate

    def update_video_display(self, frame):
        cap = self.cap
        if cap is None:
            return

        # Set the video capture to the specified frame
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame)

        # Read the frame from the video capture
        ret, frame_data = cap.read()

        # Check if the frame was read successfully
        if ret:
            # Convert the frame data to a PhotoImage object for tkinter
            frame_image = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(frame_data, cv2.COLOR_BGR2RGB)))
            self.video_display.config(image=frame_image)
            self.video_display.image = frame_image  # Keep a reference to prevent garbage collection


root = tk.Tk()
app = VideoSectionApp(root)
root.mainloop()

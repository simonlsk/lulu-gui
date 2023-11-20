import tkinter as tk


class CustomSlider(tk.Canvas):
    HANDLE_RADIUS = 5
    LINE_WIDTH = 4
    PAD_X = 20

    def __init__(self, parent, **kwargs):
        tk.Canvas.__init__(self, parent, **kwargs)
        self.config(bg="white", height=50)
        self.bind("<Configure>", self.on_resize)
        self.bind("<Button-1>", self.click)
        self.bind("<B1-Motion>", self.drag)
        self.length = 0
        self.framerate = 30  # Default framerate, can be changed later
        self.start_position = 0
        self.end_position = 0
        self.start_handle = None
        self.end_handle = None
        self.selected_handle = None

    def on_resize(self, event):
        self.config(width=event.width)
        self.draw_slider()

    def draw_slider(self):
        self.delete("slider")
        width = self.winfo_width()
        # Draw the line for the slider track
        self.create_line(self.PAD_X, 25, width - self.PAD_X, 25, fill="gray", width=self.LINE_WIDTH, tags="slider")
        # Draw the start and end draggable points
        self.start_handle = self.create_oval(self.PAD_X - self.HANDLE_RADIUS, 20, self.PAD_X + self.HANDLE_RADIUS, 30, fill="black", tags=("slider", "start"))
        self.end_handle = self.create_oval(width - self.PAD_X - self.HANDLE_RADIUS, 20, width - self.PAD_X + self.HANDLE_RADIUS, 30, fill="black", tags=("slider", "end"))

    def click(self, event):
        # Identify the handle clicked on
        self.selected_handle = None
        if self.start_handle == self.find_closest(event.x, event.y)[0]:
            self.selected_handle = "start"
        elif self.end_handle == self.find_closest(event.x, event.y)[0]:
            self.selected_handle = "end"

    def drag(self, event):
        # Drag the selected handle
        if self.selected_handle:
            new_x = min(max(event.x, self.PAD_X), self.winfo_width() - self.PAD_X)
            if self.selected_handle == "start":
                self.coords(self.start_handle, new_x - self.HANDLE_RADIUS, 20, new_x + self.HANDLE_RADIUS, 30)
                self.start_position = self.position_to_frames(new_x)
            elif self.selected_handle == "end":
                self.coords(self.end_handle, new_x - self.HANDLE_RADIUS, 20, new_x + self.HANDLE_RADIUS, 30)
                self.end_position = self.position_to_frames(new_x)

    def position_to_frames(self, x):
        # Convert the x position to frames
        range_width = self.winfo_width() - 2 * self.PAD_X
        return int((x - self.PAD_X) / range_width * self.length)

    def frames_to_position(self, frames):
        # Convert frames to x position
        range_width = self.winfo_width() - 2 * self.PAD_X
        return int(frames / self.length * range_width + self.PAD_X)

    def set_start(self, frames):
        # Set the start position handle based on frames
        self.start_position = frames
        start_x = self.frames_to_position(frames)
        self.coords(self.start_handle, start_x - self.HANDLE_RADIUS, 20, start_x + self.HANDLE_RADIUS, 30)

    def set_end(self, frames):
        # Set the end position handle based on frames
        self.end_position = frames
        end_x = self.frames_to_position(frames)
        self.coords(self.end_handle, end_x - self.HANDLE_RADIUS, 20, end_x + self.HANDLE_RADIUS, 30)

    def get_smpte_timecode(self, frames):
        # Convert frame number to SMPTE timecode
        hours = frames // (3600 * self.framerate)
        minutes = (frames // (60 * self.framerate)) % 60
        seconds = (frames // self.framerate) % 60
        frame_number = frames % self.framerate
        return f"{hours:02}:{minutes:02}:{seconds:02}:{frame_number:02}"

    def get_start_smpte(self):
        # Get SMPTE timecode for start position
        return self.get_smpte_timecode(self.start_position)

    def get_end_smpte(self):
        # Get SMPTE timecode for end position
        return self.get_smpte_timecode(self.end_position)

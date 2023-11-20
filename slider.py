import tkinter as tk


class CustomSlider(tk.Canvas):
    HANDLE_RADIUS = 5
    LINE_WIDTH = 4
    PAD_X = 20
    TEXT_PAD_Y = 20

    def __init__(self, parent, total_frames, framerate, **kwargs):
        tk.Canvas.__init__(self, parent, **kwargs)
        self.config(height=50)
        self.bind("<Configure>", self.on_resize)
        self.bind("<Button-1>", self.click)
        self.bind("<B1-Motion>", self.drag)
        self.length = total_frames
        self.framerate = framerate  # Default framerate, can be changed later
        self.position = 0
        self.cursor_handle = None
        self.timecode_text = None
        self.bind_all("<Left>", self.move_left)  # Bind to all instances of the application
        self.bind_all("<Right>", self.move_right)  # Bind to all instances of the application

    def on_resize(self, event):
        self.config(width=event.width)
        self.draw_slider()

    def draw_slider(self):
        self.delete("slider")
        width = self.winfo_width()
        # Draw the line for the slider track
        self.create_line(self.PAD_X, 25, width - self.PAD_X, 25, fill="gray", width=self.LINE_WIDTH, tags="slider")
        # Draw the cursor as a draggable point
        cursor_x = self.frames_to_position(self.position)
        self.cursor_handle = self.create_oval(cursor_x - self.HANDLE_RADIUS, 20, cursor_x + self.HANDLE_RADIUS, 30, fill="black", tags="slider")
        # Draw the timecode text
        self.timecode_text = self.create_text(cursor_x, 45, text=self.get_smpte_timecode(self.position), tags="slider")

    def click(self, event):
        self.drag(event)

    def drag(self, event):
        # Drag the cursor handle and update timecode text
        new_x = min(max(event.x, self.PAD_X), self.winfo_width() - self.PAD_X)
        self.coords(self.cursor_handle, new_x - self.HANDLE_RADIUS, 20, new_x + self.HANDLE_RADIUS, 30)
        self.coords(self.timecode_text, new_x, 45)
        self.position = self.position_to_frames(new_x)
        self.itemconfig(self.timecode_text, text=self.get_smpte_timecode(self.position))

    def position_to_frames(self, x):
        # Convert the x position to frames
        range_width = self.winfo_width() - 2 * self.PAD_X
        return int((x - self.PAD_X) / range_width * self.length)

    def frames_to_position(self, frames):
        # Convert frames to x position
        range_width = self.winfo_width() - 2 * self.PAD_X
        return int(frames / self.length * range_width + self.PAD_X)

    # def set_start(self, frames):
    #     # Set the start position handle based on frames
    #     self.start_position = frames
    #     start_x = self.frames_to_position(frames)
    #     self.coords(self.start_handle, start_x - self.HANDLE_RADIUS, 20, start_x + self.HANDLE_RADIUS, 30)
    #
    # def set_end(self, frames):
    #     # Set the end position handle based on frames
    #     self.end_position = frames
    #     end_x = self.frames_to_position(frames)
    #     self.coords(self.end_handle, end_x - self.HANDLE_RADIUS, 20, end_x + self.HANDLE_RADIUS, 30)

    def get_smpte_timecode(self, frames):
        # Convert frame number to SMPTE timecode
        hours = frames // (3600 * self.framerate)
        minutes = (frames // (60 * self.framerate)) % 60
        seconds = (frames // self.framerate) % 60
        frame_number = frames % self.framerate
        return f"{hours:02}:{minutes:02}:{seconds:02}:{frame_number:02}"

    def get_smpte(self):
        # Get SMPTE timecode for start position
        return self.get_smpte_timecode(self.position)

    def set_video_length(self, length, framerate):
        # Update the slider's length and framerate based on the new video
        self.length = length
        self.framerate = framerate
        self.position = 0  # Reset the position to the start
        self.draw_slider()  # Redraw the slider to reflect the new length

    def move_left(self, event):
        if self.position > 0:
            self.set_position(self.position - 1)  # Move left by one frame

    def move_right(self, event):
        if self.position < self.length:
            self.set_position(self.position + 1)  # Move right by one frame

    def set_position(self, frame):
        self.position = frame
        cursor_x = self.frames_to_position(frame)
        self.coords(self.cursor_handle, cursor_x - self.HANDLE_RADIUS, 20, cursor_x + self.HANDLE_RADIUS, 30)
        self.coords(self.timecode_text, cursor_x, 45)
        self.itemconfig(self.timecode_text, text=self.get_smpte_timecode(frame))


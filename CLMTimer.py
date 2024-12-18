import tkinter as tk
from tkinter import font
from tkinter import ttk
import math
from turtle import color
import os
from PIL import Image, ImageTk
import pygame # Used for sound playback

class MultiTimerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("CLM Timer")
        
        # Set window icon
        script_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(script_dir, "stopwatch.png")
        if os.path.exists(icon_path):
            icon = Image.open(icon_path)
            icon = ImageTk.PhotoImage(icon)
            self.master.iconphoto(True, icon)
        
        self.timer_font = font.Font(size=9)
        self.timers = []
        
        # Create top frame for dropdown and bell button
        top_frame = tk.Frame(master)
        top_frame.pack(fill=tk.X, pady=10)
        
        # Create dropdown for number of timers
        self.timer_count = tk.StringVar()
        self.timer_count.set("9")  # Set default to 9
        self.dropdown = ttk.Combobox(top_frame, textvariable=self.timer_count, values=[str(i) for i in range(7, 10)])
        self.dropdown.pack(side=tk.LEFT, padx=(15, 0))
        self.dropdown.bind("<<ComboboxSelected>>", self.update_timers)
        
        # Create bell button
        bell_icon_path = os.path.join(script_dir, "bell_icon.png")
        if os.path.exists(bell_icon_path):
            bell_icon = Image.open(bell_icon_path)
            bell_icon = bell_icon.resize((24, 24), Image.LANCZOS)
            bell_icon = ImageTk.PhotoImage(bell_icon)
            self.bell_button = tk.Button(top_frame, image=bell_icon, command=self.play_bell_sound, bg='red')
            self.bell_button.image = bell_icon
        else:
            self.bell_button = tk.Button(top_frame, text="🔔", command=self.play_bell_sound, bg='red')
        self.bell_button.pack(side=tk.RIGHT, padx=(0, 10))
        
        # Initialize pygame mixer for sound
        pygame.mixer.init()
        bell_sound_path = os.path.join(script_dir, "bell.wav")
        if os.path.exists(bell_sound_path):
            try:
                pygame.mixer.music.load(bell_sound_path)
                self.bell_sound = True
            except pygame.error as e:
                print(f"Error loading sound file: {e}")
                self.bell_sound = False
        else:
            print(f"Warning: Bell sound file not found at {bell_sound_path}")
            self.bell_sound = None
        
        # Create canvas with scrollbars
        self.canvas = tk.Canvas(master)
        self.scrollbar_y = ttk.Scrollbar(master, orient="vertical", command=self.canvas.yview)
        self.scrollbar_x = ttk.Scrollbar(master, orient="horizontal", command=self.canvas.xview)
        self.timer_frame = tk.Frame(self.canvas)

        # Configure canvas
        self.canvas.configure(yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)
        
        # Pack scrollbars and canvas
        self.scrollbar_y.pack(side="right", fill="y")
        self.scrollbar_x.pack(side="bottom", fill="x")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        # Create window inside canvas
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.timer_frame, anchor="nw")
        
        # Bind events
        self.timer_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        self.master.bind("<Configure>", self.on_window_resize)
        
        # Initial timers (10 by default)
        self.default_titles = [
            "Treasures Talk - 10m",
            "Spiritual Gems - 10m",
            "Bible Reading - 4m",
            "Student Talk 1",
            "Student Talk 2",
            "Student Talk 3",
            "LAC Part 1",
            "LAC Part 2",
            "Bible Study - 30m"
        ]
        for i in range(9):
            self.add_timer(self.default_titles[i])

        # Set initial window size based on number of rows
        timer_count = len(self.timers)
        cols = min(3, timer_count)  # Max 3 columns
        rows = math.ceil(timer_count / cols)
        
        # Calculate window dimensions
        window_width = cols * 160  # space for 3 timers per row
        window_height = rows * 150  # space for 3 timers per column
        
        # Get screen dimensions
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        
        # Ensure window isn't larger than screen
        window_width = min(window_width, screen_width - 100)
        window_height = min(window_height, screen_height - 100)
        
        # Set window size and position it at center
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.master.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    def play_bell_sound(self):
        if self.bell_sound:
            pygame.mixer.music.play()
        else:
            print("Bell sound not available")
    def update_timers(self, event):
        count = int(self.timer_count.get())
        current_count = len(self.timers)
        
        if count == 8:
            # Special handling for 8 timers
            # Save Bible Study timer if it exists
            bible_study_timer = self.timers[-1] if self.timers else None
            
            # Remove all existing timers
            for timer in self.timers[:]:
                timer.destroy()
            self.timers.clear()
            
            # Add the specific 8 timer configuration
            titles = [
                "Treasures Talk - 10m",
                "Spiritual Gems - 10m",
                "Bible Reading - 4m",
                "Student Talk 1",
                "Student Talk 2",
                "Student Talk 3",
                "LAC Part 1",
                "Bible Study - 30m"
            ]
            for title in titles:
                self.add_timer(title)
                
        elif count == 7:
            # Special handling for 7 timers
            bible_study_timer = self.timers[-1] if self.timers else None
            
            # Remove all existing timers
            for timer in self.timers[:]:
                timer.destroy()
            self.timers.clear()
            
            # Add the specific 7 timer configuration
            titles = [
                "Treasures Talk - 10m",
                "Spiritual Gems - 10m",
                "Bible Reading - 4m",
                "Student Talk 1",
                "Student Talk 2",
                "LAC Part 1",
                "Bible Study - 30m"
            ]
            for title in titles:
                self.add_timer(title)
                
        elif count == 9:
            # Special handling for 9 timers
            bible_study_timer = self.timers[-1] if self.timers else None
            
            # Remove all existing timers
            for timer in self.timers[:]:
                timer.destroy()
            self.timers.clear()
            
            # Add all default titles
            for title in self.default_titles:
                self.add_timer(title)
        
        self.arrange_timers()

    def add_timer(self, title):
        timer = TimerWidget(self.timer_frame, title, self.timer_font)
        self.timers.append(timer)
        self.arrange_timers()
    
    def on_frame_configure(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event):
        # Update the width of the canvas window when the canvas is resized
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_frame, width=canvas_width)
        self.arrange_timers()

    def on_window_resize(self, event=None):
        # Only handle if it's the main window being resized
        if event.widget == self.master:
            self.arrange_timers()

    def arrange_timers(self):
        for timer in self.timers:
            timer.grid_forget()
        
        if not self.timers:
            return

        # Get available width and calculate how many timers can fit per row
        canvas_width = self.canvas.winfo_width()
        timer_width = 130  # Approximate width of each timer widget
        padding = 20  # Total horizontal padding between timers
        
        cols = max(1, canvas_width // (timer_width + padding))
        rows = math.ceil(len(self.timers) / cols)
        
        for i, timer in enumerate(self.timers):
            row = i // cols
            col = i % cols
            timer.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            
        # Configure grid columns to be equal width
        for i in range(cols):
            self.timer_frame.grid_columnconfigure(i, weight=1)

class TimerWidget(tk.Frame):
    def __init__(self, parent, title, timer_font):
        super().__init__(parent)
        
        self.is_running = False
        self.time = 0
        
        # Title entry
        self.title_entry = tk.Entry(self, font=timer_font, width=17)
        self.title_entry.insert(0, title)
        self.title_entry.pack()
        
        # Time display
        timer_time_font = font.Font(size=24)  # Increase font size
        self.time_label = tk.Label(self, text="00:00:00", font=timer_time_font)
        self.time_label.pack()
        
        # Control buttons
        button_frame = tk.Frame(self)
        button_frame.pack()
        
        # Get the directory of the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Function to load and resize image safely
        def load_image(filename):
            try:
                img_path = os.path.join(script_dir, filename)
                img = Image.open(img_path)
                # Calculate new size (50% of original)
                new_size = tuple(dim // 2 for dim in img.size)
                img = img.resize(new_size, Image.LANCZOS)
                return ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"Error loading {filename}: {e}")
                return None

        play_icon = load_image("play_icon.png")
        stop_icon = load_image("stop_icon.png")
        reset_icon = load_image("reset_icon.png")

        # Create buttons with fallback to text if image loading fails
        self.start_button = tk.Button(button_frame, command=self.start_timer)
        if play_icon:
            self.start_button.config(image=play_icon)
            self.start_button.image = play_icon
        else:
            self.start_button.config(text="▶", fg="white", font=("Arial", 12, "bold"))
        self.start_button.pack(side=tk.LEFT, padx=2)

        self.stop_button = tk.Button(button_frame, command=self.stop_timer, state=tk.DISABLED)
        if stop_icon:
            self.stop_button.config(image=stop_icon)
            self.stop_button.image = stop_icon
        else:
            self.stop_button.config(text="⏹", fg="white", font=("Arial", 12, "bold"))
        self.stop_button.pack(side=tk.LEFT, padx=2)

        self.reset_button = tk.Button(button_frame, command=self.reset_timer)
        if reset_icon:
            self.reset_button.config(image=reset_icon)
            self.reset_button.image = reset_icon
        else:
            self.reset_button.config(text="⟳", fg="white", font=("Arial", 12, "bold"))
        self.reset_button.pack(side=tk.LEFT, padx=2)
    
    def start_timer(self):
        self.is_running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.update_timer()
    
    def stop_timer(self):
        self.is_running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
    
    def reset_timer(self):
        self.is_running = False
        self.time = 0
        self.update_display()
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
    
    def update_timer(self):
        if self.is_running:
            self.time += 1
            self.update_display()
            self.after(1000, self.update_timer)
    
    def update_display(self):
        hours, remainder = divmod(self.time, 3600)
        minutes, seconds = divmod(remainder, 60)
        time_string = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        self.time_label.config(text=time_string)

# Update the main app creation
root = tk.Tk()
app = MultiTimerApp(root)
root.mainloop()
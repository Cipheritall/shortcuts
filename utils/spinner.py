import customtkinter as ctk
from typing import Optional
import threading
import time

class Spinner(ctk.CTkLabel):
    SPINNER_CHARS = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(text="", font=("Courier", 20))
        self.running = False
        self.thread: Optional[threading.Thread] = None
        
    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._animate)
            self.thread.daemon = True
            self.thread.start()
            
    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
        self.configure(text="")
            
    def _animate(self):
        idx = 0
        while self.running:
            self.configure(text=self.SPINNER_CHARS[idx])
            idx = (idx + 1) % len(self.SPINNER_CHARS)
            time.sleep(0.1)

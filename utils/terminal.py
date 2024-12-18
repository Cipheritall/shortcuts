import customtkinter as ctk
import sys
from datetime import datetime
import queue
import threading

class Terminal(ctk.CTkTextbox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Configuration du terminal
        self.configure(
            font=("Courier", 12),
            text_color="#00FF00",  # Vert terminal
            fg_color="#1a1a1a",    # Fond noir
            border_color="#333333",
            border_width=1,
            wrap="word"
        )
        
        # File d'attente pour les messages
        self.queue = queue.Queue()
        
        # Démarrer le thread de traitement
        self.running = True
        self.thread = threading.Thread(target=self._process_queue)
        self.thread.daemon = True
        self.thread.start()
        
    def _process_queue(self):
        while self.running:
            try:
                msg = self.queue.get(timeout=0.1)
                self.write(msg)
            except queue.Empty:
                continue
                
    def write(self, text: str):
        """Écrire dans le terminal avec timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.configure(state="normal")
        self.insert("end", f"[{timestamp}] {text}\n")
        self.configure(state="disabled")
        self.see("end")
        
    def clear(self):
        """Effacer le terminal"""
        self.configure(state="normal")
        self.delete("1.0", "end")
        self.configure(state="disabled")
        
    def stop(self):
        """Arrêter le thread de traitement"""
        self.running = False
        if self.thread.is_alive():
            self.thread.join()

class TerminalOutput:
    """Classe pour rediriger stdout vers le terminal"""
    def __init__(self, terminal: Terminal):
        self.terminal = terminal
        self.stdout = sys.stdout
        
    def write(self, text: str):
        if text.strip():  # Ignorer les lignes vides
            self.terminal.queue.put(text.strip())
        self.stdout.write(text)
        
    def flush(self):
        self.stdout.flush()

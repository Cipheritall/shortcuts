# features/slow_task.py
import time
from features.base_feature import BaseFeature
import customtkinter as ctk
from typing import Dict, Any
import threading

class SlowTaskFeature(BaseFeature):
    @property
    def name(self) -> str:
        return "Slow Task"
    
    @property
    def icon(self) -> str:
        return "time"
    
    def init(self) -> None:
        self.iterations = 60
        self.delay = 60
    
    def main(self, **kwargs) -> None:
        iterations = int(kwargs.get('iterations', self.iterations))
        delay = float(kwargs.get('delay', self.delay))
        stop_event: threading.Event = kwargs.get('stop_event')
        
        for i in range(iterations):
            if stop_event and stop_event.is_set():
                return
                
            print(f"Step {i+1}/{iterations}")
            
            # Check for stop during sleep
            for _ in range(int(delay * 10)):
                if stop_event and stop_event.is_set():
                    return
                time.sleep(0.1)
    
    def options(self, parent: ctk.CTkFrame) -> Dict[str, Any]:
        frame = ctk.CTkFrame(parent)
        
        ctk.CTkLabel(frame, text="Iterations:").pack(pady=5)
        iterations = ctk.CTkEntry(frame)
        iterations.insert(0, str(self.iterations))
        iterations.pack(pady=5)
        
        ctk.CTkLabel(frame, text="Delay (seconds):").pack(pady=5)
        delay = ctk.CTkEntry(frame)
        delay.insert(0, str(self.delay))
        delay.pack(pady=5)
        
        return {
            "widget": frame,
            "values": lambda: {
                "iterations": int(iterations.get()),
                "delay": float(delay.get())
            }
        }

    def exit(self) -> None:
        """Cleanup method called when feature is stopped"""
        pass
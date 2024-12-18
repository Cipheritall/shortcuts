from features.base_feature import BaseFeature
import customtkinter as ctk
from typing import Dict, Any

import time
import pyautogui

class HelloWorldFeature(BaseFeature):
    @property
    def name(self) -> str:
        return "Hello BRB"
        
    @property
    def icon(self) -> str:
        return "chat-bubble"  # CTk icon name
    
    def init(self) -> None:
        self.message = "Hello BRB!"
        
    def main(self, **kwargs) -> None:
        message = kwargs.get('message', self.message)
        print(message)
        start_time = time.asctime()
        i = 0
        occ = 30
        print(f"Started at : {start_time} / {occ}s")
        while 1:
            elapsed_hours = int(occ*i/60/60)
            elapsed_min = (occ*i/60/60-elapsed_hours)*60
            print(f"ONGOING \t\t: {elapsed_hours}:{elapsed_min}")
            time.sleep(occ)
            pyautogui.press("fn")
            i+=1
        
    def exit(self) -> None:
        pass
        
    def options(self, parent: ctk.CTkFrame) -> Dict[str, Any]:
        options_frame = ctk.CTkFrame(parent)
        
        # Message input
        message_label = ctk.CTkLabel(options_frame, text="Message:")
        message_label.pack(pady=5)
        
        message_entry = ctk.CTkEntry(options_frame)
        message_entry.insert(0, self.message)
        message_entry.pack(pady=5)
        
        return {
            "widget": options_frame,
            "values": lambda: {"message": message_entry.get()}
        }

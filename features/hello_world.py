from features.base_feature import BaseFeature
import customtkinter as ctk
from typing import Dict, Any

class HelloWorldFeature(BaseFeature):
    @property
    def name(self) -> str:
        return "Hello World"
        
    @property
    def icon(self) -> str:
        return "chat-bubble"  # CTk icon name
    
    def init(self) -> None:
        self.message = "Hello World!"
        
    def main(self, **kwargs) -> None:
        message = kwargs.get('message', self.message)
        print(message)
        
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

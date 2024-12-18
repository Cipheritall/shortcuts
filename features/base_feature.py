from abc import ABC, abstractmethod
from typing import Dict, Any
import customtkinter as ctk

class BaseFeature(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass
        
    @property
    @abstractmethod
    def icon(self) -> str:
        """Return icon name from CTk or a path to custom icon"""
        pass
    
    @abstractmethod
    def init(self) -> None:
        """Initialize feature"""
        pass
        
    @abstractmethod
    def main(self, **kwargs) -> None:
        """Main feature execution"""
        pass
        
    @abstractmethod
    def exit(self) -> None:
        """Cleanup"""
        pass
        
    @abstractmethod
    def options(self, parent: ctk.CTkFrame) -> Dict[str, Any]:
        """Return options widget and their values"""
        pass

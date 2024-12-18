import customtkinter as ctk
from typing import Callable, Dict, Type
import importlib
import os
import inspect
import sys
from features.base_feature import BaseFeature
from utils.logger import Logger
from utils.terminal import Terminal, TerminalOutput

class MainPage(ctk.CTkFrame):
    def __init__(self, parent, config, logout_callback: Callable):
        super().__init__(parent)
        self.config = config
        self.logout_callback = logout_callback
        self.logger = Logger("MainPage")
        
        self.features: Dict[str, BaseFeature] = {}
        self.current_feature = None
        self.current_options = None
        
        self.init_ui()
        self.load_features()
        
    def init_ui(self):
        # Main container
        self.main_container = ctk.CTkFrame(self)
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Left panel (features list)
        self.left_panel = ctk.CTkFrame(self.main_container)
        self.left_panel.pack(side="left", fill="y", padx=10)
        
        # Features list frame
        self.features_frame = ctk.CTkFrame(self.left_panel)
        self.features_frame.pack(fill="x", pady=10)
        
        # Features label
        self.features_label = ctk.CTkLabel(
            self.features_frame,
            text="Features",
            font=("Helvetica", 16, "bold")
        )
        self.features_label.pack(pady=5)
        
        # Right panel (options and terminal)
        self.right_panel = ctk.CTkFrame(self.main_container)
        self.right_panel.pack(side="right", fill="both", expand=True, padx=10)
        
        # Options frame
        self.options_frame = ctk.CTkFrame(self.right_panel)
        self.options_frame.pack(fill="x", pady=10)
        
        # Terminal frame
        self.terminal_frame = ctk.CTkFrame(self.right_panel)
        self.terminal_frame.pack(fill="both", expand=True, pady=10)
        
        # Terminal label
        self.terminal_label = ctk.CTkLabel(
            self.terminal_frame,
            text="Terminal Output",
            font=("Helvetica", 16, "bold")
        )
        self.terminal_label.pack(pady=5)
        
        # Terminal
        self.terminal = Terminal(self.terminal_frame, height=200)
        self.terminal.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Redirect stdout to terminal
        sys.stdout = TerminalOutput(self.terminal)
        
        # Buttons frame
        self.buttons_frame = ctk.CTkFrame(self.right_panel)
        self.buttons_frame.pack(fill="x", pady=10)
        
        # Run button
        self.run_button = ctk.CTkButton(
            self.buttons_frame,
            text="Run Feature",
            command=self.run_feature
        )
        self.run_button.pack(side="left", padx=5)
        
        # Clear button
        self.clear_button = ctk.CTkButton(
            self.buttons_frame,
            text="Clear Terminal",
            command=self.terminal.clear,
            fg_color="#555555",
            hover_color="#666666"
        )
        self.clear_button.pack(side="left", padx=5)
        
     
    def load_features(self):
        features_dir = "features"
        self.logger.info("Loading features...")
        
        for file in os.listdir(features_dir):
            if file.endswith(".py") and file not in ["__init__.py", "base_feature.py"]:
                module_name = file[:-3]
                try:
                    module = importlib.import_module(f"features.{module_name}")
                    
                    # Find feature class in module
                    for name, obj in inspect.getmembers(module):
                        if (inspect.isclass(obj) and 
                            issubclass(obj, BaseFeature) and 
                            obj != BaseFeature):
                            
                            feature = obj()
                            feature.init()
                            self.features[feature.name] = feature
                            
                            # Create button for feature
                            btn = ctk.CTkButton(
                                self.features_frame,
                                text=feature.name,
                                command=lambda f=feature: self.select_feature(f)
                            )
                            btn.pack(pady=5, padx=10)
                            
                            self.logger.info(f"Loaded feature: {feature.name}")
                            
                except Exception as e:
                    self.logger.error(f"Error loading feature {module_name}: {str(e)}")
    
        
    def select_feature(self, feature: BaseFeature):
        self.current_feature = feature
        
        # Clear previous options
        for widget in self.options_frame.winfo_children():
            widget.destroy()
            
        # Show new options
        options = feature.options(self.options_frame)
        self.current_options = options
        options["widget"].pack(fill="both", expand=True, pady=10)
        
        # Update run button
        self.run_button.configure(text=f"Run {feature.name}")
        
    def run_feature(self):
        if self.current_feature and self.current_options:
            try:
                # Print feature execution
                print(f"Executing feature: {self.current_feature.name}")
                
                # Get values from options
                values = self.current_options["values"]()
                
                # Run feature
                self.current_feature.main(**values)
                print(f"Feature {self.current_feature.name} completed successfully")
                
            except Exception as e:
                error_msg = f"Error running feature {self.current_feature.name}: {str(e)}"
                print(error_msg)
                self.logger.error(error_msg)
                
    def on_closing(self):
        """Appelé quand l'application se ferme"""
        self.terminal.stop()
        sys.stdout = sys.__stdout__  # Restaurer stdout

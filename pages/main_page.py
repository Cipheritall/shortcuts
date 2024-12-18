import customtkinter as ctk
from typing import Callable, Dict
import importlib
import os
import inspect
import sys
import threading
import queue
from features.base_feature import BaseFeature
from utils.logger import Logger
from utils.terminal import Terminal, TerminalOutput
import tkinter as tk
from PIL import Image, ImageTk
import qtawesome as qta

class FeatureButton(ctk.CTkButton):
    def __init__(self, parent, feature: BaseFeature, command: Callable):
        # Create icon
        try:
            if feature.icon.startswith('fa'):
                # QtAwesome icon
                qta_icon = qta.icon(feature.icon, color='white')
                icon = ImageTk.PhotoImage(qta_icon.to_image(32, 32))
            else:
                # Custom image icon
                icon_path = os.path.join('icons', f"{feature.icon}.png")
                if os.path.exists(icon_path):
                    img = Image.open(icon_path)
                    img = img.resize((24, 24), Image.Resampling.LANCZOS)
                    icon = ImageTk.PhotoImage(img)
                else:
                    icon = None
        except Exception:
            icon = None

        super().__init__(
            parent,
            text=feature.name,
            image=icon if icon else None,
            compound="left",
            command=command,
            anchor="w",
            width=180
        )
        # Keep a reference to prevent garbage collection
        self.icon = icon

class TaskFrame(ctk.CTkFrame):
    def __init__(self, parent, task_id: int, name: str, icon: str, stop_callback: Callable):
        super().__init__(parent)
        self.task_id = task_id
        
        # Task info
        self.info_frame = ctk.CTkFrame(self)
        self.info_frame.pack(side="left", fill="x", expand=True)
        
        # Try to create icon
        try:
            if icon.startswith('fa'):
                qta_icon = qta.icon(icon, color='white')
                task_icon = ImageTk.PhotoImage(qta_icon.to_image(24, 24))
            else:
                icon_path = os.path.join('icons', f"{icon}.png")
                if os.path.exists(icon_path):
                    img = Image.open(icon_path)
                    img = img.resize((20, 20), Image.Resampling.LANCZOS)
                    task_icon = ImageTk.PhotoImage(img)
                else:
                    task_icon = None
        except Exception:
            task_icon = None
        
        # Icon label if icon exists
        if task_icon:
            self.icon_label = ctk.CTkLabel(
                self.info_frame,
                text="",
                image=task_icon
            )
            self.icon_label.pack(side="left", padx=5)
            self.icon_label.image = task_icon  # Keep reference
        
        self.name_label = ctk.CTkLabel(
            self.info_frame,
            text=f"Task {task_id}: {name}",
            anchor="w"
        )
        self.name_label.pack(side="left", padx=5)
        
        self.status_label = ctk.CTkLabel(
            self.info_frame,
            text="Running",
            text_color="yellow"
        )
        self.status_label.pack(side="left", padx=5)
        
        # Stop button
        self.stop_button = ctk.CTkButton(
            self,
            text="Stop",
            command=lambda: stop_callback(task_id),
            width=60,
            fg_color="#DC2626",
            hover_color="#B91C1C"
        )
        self.stop_button.pack(side="right", padx=5, pady=2)
    
    def update_status(self, status: str, color: str):
        self.status_label.configure(text=status, text_color=color)

class MainPage(ctk.CTkFrame):
    def __init__(self, parent, config, logout_callback: Callable):
        super().__init__(parent)
        self.config = config
        self.logout_callback = logout_callback
        self.logger = Logger("MainPage")
        
        self.features: Dict[str, BaseFeature] = {}
        self.current_feature = None
        self.current_options = None
        
        # Task management
        self.tasks = {}
        self.next_task_id = 1
        
        self.init_ui()
        self.load_features()

    def init_ui(self):
        # Main container
        self.main_container = ctk.CTkFrame(self)
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Left panel (features list)
        self.left_panel = ctk.CTkFrame(self.main_container, width=200)
        self.left_panel.pack(side="left", fill="y", padx=10)
        self.left_panel.pack_propagate(False)
        
        # Features label
        self.features_label = ctk.CTkLabel(
            self.left_panel,
            text="Features",
            font=("Helvetica", 16, "bold")
        )
        self.features_label.pack(pady=5)
        
        # Features list frame
        self.features_frame = ctk.CTkFrame(self.left_panel)
        self.features_frame.pack(fill="both", expand=True, pady=5)
        
        # Right panel
        self.right_panel = ctk.CTkFrame(self.main_container)
        self.right_panel.pack(side="left", fill="both", expand=True, padx=10)
        
        # Options frame
        self.options_frame = ctk.CTkFrame(self.right_panel)
        self.options_frame.pack(fill="x", pady=10)
        
        # Tasks frame
        self.tasks_frame = ctk.CTkFrame(self.right_panel)
        self.tasks_frame.pack(fill="x", pady=5)
        
        # Tasks label
        self.tasks_label = ctk.CTkLabel(
            self.tasks_frame,
            text="Running Tasks",
            font=("Helvetica", 12, "bold")
        )
        self.tasks_label.pack(pady=2)
        
        # Tasks list
        self.tasks_list = ctk.CTkScrollableFrame(self.tasks_frame, height=100)
        self.tasks_list.pack(fill="x", expand=True, padx=5, pady=5)
        
        # Terminal frame
        self.terminal_frame = ctk.CTkFrame(self.right_panel)
        self.terminal_frame.pack(fill="both", expand=True, pady=10)
        
        # Terminal label
        self.terminal_label = ctk.CTkLabel(
            self.terminal_frame,
            text="Output",
            font=("Helvetica", 12, "bold")
        )
        self.terminal_label.pack(pady=2)
        
        # Terminal
        self.terminal = Terminal(self.terminal_frame, height=100)
        self.terminal.pack(fill="both", expand=True, padx=5, pady=5)
        
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
        
        # Clear terminal button
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
                    
                    for name, obj in inspect.getmembers(module):
                        if (inspect.isclass(obj) and 
                            issubclass(obj, BaseFeature) and 
                            obj != BaseFeature):
                            
                            feature = obj()
                            feature.init()
                            self.features[feature.name] = feature
                            
                            # Create feature button with icon
                            btn = FeatureButton(
                                self.features_frame,
                                feature,
                                lambda f=feature: self.select_feature(f)
                            )
                            btn.pack(pady=5, padx=10, fill="x")
                            
                            self.logger.info(f"Loaded feature: {feature.name}")
                            
                except Exception as e:
                    self.logger.error(f"Error loading feature {module_name}: {str(e)}")

    def select_feature(self, feature: BaseFeature):
        self.current_feature = feature
        
        for widget in self.options_frame.winfo_children():
            widget.destroy()
        
        options = feature.options(self.options_frame)
        self.current_options = options
        options["widget"].pack(fill="both", expand=True, pady=10)
        
        self.run_button.configure(text=f"Run {feature.name}")

    def run_feature(self):
        if self.current_feature and self.current_options:
            try:
                values = self.current_options["values"]()
                
                task_id = self.next_task_id
                self.next_task_id += 1
                
                # Create stop event
                stop_event = threading.Event()
                
                # Create task frame with icon
                task_frame = TaskFrame(
                    self.tasks_list,
                    task_id,
                    self.current_feature.name,
                    self.current_feature.icon,
                    self.stop_task
                )
                task_frame.pack(fill="x", padx=5, pady=2)
                
                # Store task info
                self.tasks[task_id] = {
                    'frame': task_frame,
                    'stop_event': stop_event,
                    'feature': self.current_feature.name
                }
                
                # Add stop_event to values
                values['stop_event'] = stop_event
                
                # Start thread
                thread = threading.Thread(
                    target=self._run_task,
                    args=(task_id, self.current_feature, values),
                    daemon=True
                )
                thread.start()
                
                print(f"Started task {task_id}: {self.current_feature.name}")
                
            except Exception as e:
                error_msg = f"Error starting feature: {str(e)}"
                print(error_msg)
                self.logger.error(error_msg)

    def _run_task(self, task_id: int, feature: BaseFeature, values: dict):
        try:
            print(f"[Task {task_id}] Starting {feature.name}")
            feature.main(**values)
            
            if task_id in self.tasks:
                if self.tasks[task_id]['stop_event'].is_set():
                    print(f"[Task {task_id}] Stopped {feature.name}")
                    self.after(0, lambda: self._update_task_status(task_id, "Stopped", "gray"))
                else:
                    print(f"[Task {task_id}] Completed {feature.name}")
                    self.after(0, lambda: self._update_task_status(task_id, "Completed", "green"))
                    
        except Exception as e:
            error_msg = f"[Task {task_id}] Error in {feature.name}: {str(e)}"
            print(error_msg)
            self.logger.error(error_msg)
            self.after(0, lambda: self._update_task_status(task_id, "Error", "red"))

    def stop_task(self, task_id: int):
        if task_id in self.tasks:
            print(f"Stopping task {task_id}...")
            self.tasks[task_id]['stop_event'].set()
            self._update_task_status(task_id, "Stopping", "orange")

    def _update_task_status(self, task_id: int, status: str, color: str):
        if task_id in self.tasks:
            self.tasks[task_id]['frame'].update_status(status, color)

    def on_closing(self):
        """Called when application closes"""
        # Stop all running tasks
        for task_id in list(self.tasks.keys()):
            self.stop_task(task_id)
        
        self.terminal.stop()
        sys.stdout = sys.__stdout__

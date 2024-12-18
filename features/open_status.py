import os
import threading
from datetime import datetime
from typing import Dict, Any
import customtkinter as ctk
from features.base_feature import BaseFeature
from PIL import ImageGrab
import pygetwindow as gw
import pyautogui

class GetStatusScreenFeature(BaseFeature):
    @property
    def name(self) -> str:
        return "Get Status Screen"

    @property
    def icon(self) -> str:
        return "fas.camera"

    def init(self) -> None:
        self.window_name = None
        self.output_dir = "share/screen_shots"
        self.interval = 60  # seconds for periodic screenshots
        self.occurrences = 1  # number of times to take screenshots
        self.stop_event = threading.Event()
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def main(self, **kwargs) -> None:
        window_name = kwargs.get('window_name', self.window_name)
        self.interval = int(kwargs.get('interval', self.interval))
        self.occurrences = int(kwargs.get('occurrences', self.occurrences))
        self.stop_event = kwargs.get('stop_event', threading.Event())
        if not window_name:
            print("No window selected.")
            return
        print(f"Capturing screenshots from window: {window_name}")
        try:
            self._take_screenshot_periodically(window_name, self.occurrences)
        except Exception as e:
            print(f"Error: {str(e)}")
            raise

    def _take_screenshot(self, window_name):
        window = gw.getWindowsWithTitle(window_name)
        if window:
            window = window[0]
            bbox = (window.left, window.top, window.right, window.bottom)
            screenshot = pyautogui.screenshot(region=bbox)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
            filepath = os.path.join(self.output_dir, filename)
            screenshot.save(filepath)
            print(f"Screenshot saved: {filepath}")
        else:
            print(f"Window '{window_name}' not found.")

    def _take_screenshot_periodically(self, window_name, occurrences):
        if not self.stop_event.is_set() and occurrences > 0:
            self._take_screenshot(window_name)
            occurrences -= 1
            threading.Timer(self.interval, self._take_screenshot_periodically, [window_name, occurrences]).start()

    def exit(self) -> None:
        self.stop_event.set()

    def options(self, parent: ctk.CTkFrame) -> Dict[str, Any]:
        frame = ctk.CTkFrame(parent)
        
        window_label = ctk.CTkLabel(frame, text="Select Window:")
        window_label.pack(pady=5)
        
        self.window_combobox = ctk.CTkComboBox(frame, width=300)
        self.window_combobox.pack(pady=5)
        
        interval_label = ctk.CTkLabel(frame, text="Interval (seconds):")
        interval_label.pack(pady=5)
        interval_entry = ctk.CTkEntry(frame)
        interval_entry.insert(0, str(self.interval))
        interval_entry.pack(pady=5)
        
        occurrences_label = ctk.CTkLabel(frame, text="Number of Occurrences:")
        occurrences_label.pack(pady=5)
        occurrences_entry = ctk.CTkEntry(frame)
        occurrences_entry.insert(0, str(self.occurrences))
        occurrences_entry.pack(pady=5)
        
        output_label = ctk.CTkLabel(
            frame,
            text=f"Screenshots will be saved in: {self.output_dir}",
            text_color="gray"
        )
        output_label.pack(pady=10)
        
        self._update_window_list()
        
        return {
            "widget": frame,
            "values": lambda: {
                "window_name": self.window_combobox.get(),
                "interval": int(interval_entry.get()),
                "occurrences": int(occurrences_entry.get())
            }
        }

    def _get_open_windows(self):
        windows = [window.title for window in gw.getAllWindows() if window.title]
        return windows

    def _update_window_list(self):
        windows = self._get_open_windows()
        self.window_combobox.configure(values=windows)
        self.window_combobox.after(1000, self._update_window_list)

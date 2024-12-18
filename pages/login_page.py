import customtkinter as ctk
from typing import Callable
from utils.logger import Logger

class LoginPage(ctk.CTkFrame):
    def __init__(self, parent, switch_to_main: Callable):
        super().__init__(parent)
        self.switch_to_main = switch_to_main
        self.logger = Logger("LoginPage")
        self.logger.info("Initializing login page")
        
        # Login frame
        self.login_frame = ctk.CTkFrame(self)
        self.login_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Title
        self.title = ctk.CTkLabel(
            self.login_frame, 
            text="Login", 
            font=("Helvetica", 24)
        )
        self.title.pack(pady=20)
        
        # Username
        self.username = ctk.CTkEntry(
            self.login_frame,
            placeholder_text="Username"
        )
        self.username.pack(pady=10, padx=40)
        
        # Password
        self.password = ctk.CTkEntry(
            self.login_frame,
            placeholder_text="Password",
            show="*"
        )
        self.password.pack(pady=10, padx=40)
        
        # Login button
        self.login_button = ctk.CTkButton(
            self.login_frame,
            text="Login",
            command=self.login
        )
        self.login_button.pack(pady=20)
        
        # Error message
        self.error_label = ctk.CTkLabel(
            self.login_frame,
            text="",
            text_color="red"
        )
        self.error_label.pack(pady=10)
    
    def login(self):
        username = self.username.get()
        self.logger.info(f"Login attempt for user: {username}")
        
        password = self.password.get()
        
        # Simple validation (replace with your auth logic)
        if username == "admin" and password == "admin":
            self.logger.info(f"Successful login for user: {username}")
            self.switch_to_main()
        else:
            self.logger.warning(f"Failed login attempt for user: {username}")
            self.error_label.configure(text="Invalid credentials!")

 
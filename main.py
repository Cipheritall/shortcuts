import customtkinter as ctk
from config import Config
from pages.login_page import LoginPage
from pages.main_page import MainPage
from utils.logger import Logger

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Initialize logger
        self.logger = Logger("App")
        self.logger.info("Starting application")
        
        # Load configuration
        self.config = Config.load_config()
        self.logger.info(f"Loaded configuration: {self.config}")
        
        # Configure window
        self.title(f"{self.config.app_title} v{self.config.version}")
        self.geometry("800x600")
        
        # Set theme
        ctk.set_appearance_mode(self.config.theme)
        ctk.set_default_color_theme("blue")
        self.logger.info(f"Theme set to: {self.config.theme}")
        
        # Initialize pages
        self.current_page = None
        self.show_login_page()
        
    def show_login_page(self):
        self.logger.info("Switching to login page")
        if self.current_page:
            self.current_page.destroy()
        self.current_page = LoginPage(self, self.show_main_page)
        self.current_page.pack(fill="both", expand=True)
        
    def show_main_page(self):
        self.logger.info("Switching to main page")
        if self.current_page:
            self.current_page.destroy()
        self.current_page = MainPage(self, self.config, self.show_login_page)
        self.current_page.pack(fill="both", expand=True)

def main():
    logger = Logger("Main")
    try:
        logger.info("Application startup")
        app = App()
        app.mainloop()
    except Exception as e:
        logger.critical(f"Application crashed: {str(e)}")
        raise e
    finally:
        logger.info("Application shutdown")

if __name__ == "__main__":
    main()

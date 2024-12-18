from features.base_feature import BaseFeature
import customtkinter as ctk
from typing import Dict, Any
import threading
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def click_pki(browser):
    # connect_1_PKI
    # Wait for the PKI button to be present and click it
    pki_button = WebDriverWait(browser, 20).until(
        EC.presence_of_element_located((By.ID, "connect_1_PKI"))
    )
    pki_button.click()

def login(browser):
    try:
        # Wait for the username input field to be present

        username_input = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.ID, "discovery_username"))
        )
        # Enter the username
        username_input.send_keys("sami.ezzerouali.ext@orange.com")
        # Submit the form (if applicable)
        username_input.send_keys(Keys.RETURN)
        click_pki(browser)
    except Exception as e:
        print(f"Login error: {str(e)}")

class GetStatusScreenFeature(BaseFeature):
    @property
    def name(self) -> str:
        return "Get Status Screen"

    @property
    def icon(self) -> str:
        return "fas.camera"  # Font Awesome icon

    def init(self) -> None:
        self.url = "https://de.www.mgmt.cloud.vmware.com/automation/#/service/catalog/consume/deployment/f75b95b1-9f41-4702-9a53-5fdc9089c64a"
        self.wait_time = 10  # seconds
        self.output_dir = "share/screen_shots"

        # Create output directory if it doesn't exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def main(self, **kwargs) -> None:
        url = kwargs.get('url', self.url)
        wait_time = int(kwargs.get('wait_time', self.wait_time))
        stop_event: threading.Event = kwargs.get('stop_event')

        print(f"Opening URL: {url}")
        try:
            # Configure Firefox options
            firefox_options = Options()
            #firefox_options.add_argument("--headless")  # Run in headless mode

            # Initialize driver
            driver = webdriver.Firefox(options=firefox_options)

            try:
                # Load page
                print("Loading page...")
                driver.get(url)

                # Wait for page to load
                print(f"Waiting {wait_time} seconds for page to load...")
                WebDriverWait(driver, wait_time).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )

                # Login
                click_pki(driver)

                if stop_event and stop_event.is_set():
                    print("Task stopped by user")
                    return

                # Take screenshot
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"screenshot_{timestamp}.png"
                filepath = os.path.join(self.output_dir, filename)

                print("Taking screenshot...")
                driver.save_screenshot(filepath)
                print(f"Screenshot saved: {filepath}")

            finally:
                driver.quit()

        except Exception as e:
            print(f"Error: {str(e)}")
            raise

    def exit(self) -> None:
        pass

    def options(self, parent: ctk.CTkFrame) -> Dict[str, Any]:
        frame = ctk.CTkFrame(parent)

        # URL input
        url_label = ctk.CTkLabel(frame, text="URL:")
        url_label.pack(pady=5)

        url_entry = ctk.CTkEntry(frame, width=300)
        url_entry.insert(0, self.url)
        url_entry.pack(pady=5)

        # Wait time input
        wait_label = ctk.CTkLabel(frame, text="Wait time (seconds):")
        wait_label.pack(pady=5)

        wait_entry = ctk.CTkEntry(frame)
        wait_entry.insert(0, str(self.wait_time))
        wait_entry.pack(pady=5)

        # Output directory label
        output_label = ctk.CTkLabel(
            frame,
            text=f"Screenshots will be saved in: {self.output_dir}",
            text_color="gray"
        )
        output_label.pack(pady=10)

        return {
            "widget": frame,
            "values": lambda: {
                "url": url_entry.get(),
                "wait_time": int(wait_entry.get())
            }
        }

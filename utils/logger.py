import logging
from datetime import datetime
import os

class Logger:
    def __init__(self, name: str):
        # Créer le dossier logs s'il n'existe pas
        if not os.path.exists('logs'):
            os.makedirs('logs')
            
        # Configuration du logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Format du log
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Handler pour fichier
        file_handler = logging.FileHandler(
            f'logs/{datetime.now().strftime("%Y-%m-%d")}.log'
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        
        # Handler pour console
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
    
    def debug(self, message: str):
        self.logger.debug(message)
        
    def info(self, message: str):
        self.logger.info(message)
        
    def warning(self, message: str):
        self.logger.warning(message)
        
    def error(self, message: str):
        self.logger.error(message)
        
    def critical(self, message: str):
        self.logger.critical(message)

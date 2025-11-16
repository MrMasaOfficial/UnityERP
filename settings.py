import json
import os
from themes import ThemeMode
from translations import translator

SETTINGS_FILE = 'app_settings.json'

DEFAULT_SETTINGS = {
    'language': 'ar',
    'theme': 'light',
    'window_geometry': None,
    'window_state': None,
}

class SettingsManager:
    def __init__(self):
        self.settings = self.load_settings()
    
    def load_settings(self):
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading settings: {e}")
                return DEFAULT_SETTINGS.copy()
        return DEFAULT_SETTINGS.copy()
    
    def save_settings(self):
        try:
            with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving settings: {e}")
    
    def get(self, key, default=None):
        return self.settings.get(key, default if default is not None else DEFAULT_SETTINGS.get(key))
    
    def set(self, key, value):
        self.settings[key] = value
        self.save_settings()
    
    def get_language(self):
        return self.get('language', 'ar')
    
    def set_language(self, lang):
        self.set('language', lang)
        translator.set_language(lang)
    
    def get_theme(self):
        return self.get('theme', 'light')
    
    def set_theme(self, theme):
        self.set('theme', theme)
    
    def get_window_geometry(self):
        return self.get('window_geometry')
    
    def set_window_geometry(self, geometry):
        self.set('window_geometry', geometry)
    
    def get_window_state(self):
        return self.get('window_state')
    
    def set_window_state(self, state):
        self.set('window_state', state)
    
    def reset_to_defaults(self):
        self.settings = DEFAULT_SETTINGS.copy()
        self.save_settings()

settings_manager = SettingsManager()

def get_language():
    return settings_manager.get_language()

def set_language(lang):
    settings_manager.set_language(lang)

def get_theme():
    return settings_manager.get_theme()

def set_theme(theme):
    settings_manager.set_theme(theme)

def get_setting(key, default=None):
    return settings_manager.get(key, default)

def set_setting(key, value):
    settings_manager.set(key, value)

import sys
from PySide6.QtCore import QObject, Signal
from pynput import keyboard

def to_pynput_format(hotkey_str):
    """Converts a hotkey string like 'ctrl+shift+o' to pynput format '<ctrl>+<shift>+o'."""
    parts = hotkey_str.lower().split('+')
    pynput_parts = []
    for part in parts:
        part = part.strip()
        if part in ["ctrl", "alt", "shift", "win", "up", "down", "left", "right"]:
            pynput_parts.append(f"<{part}>")
        else:
            pynput_parts.append(part)
    return "+".join(pynput_parts)

class HotkeyManager(QObject):
    # Thread-safe Qt signals
    toggle_overlay_signal = Signal()
    toggle_crosshair_signal = Signal()
    opacity_up_signal = Signal()
    opacity_down_signal = Signal()

    def __init__(self, config_manager):
        super().__init__()
        self.config_manager = config_manager
        self.listener = None

    def start(self):
        self.stop()
        
        hotkeys_cfg = self.config_manager.get("hotkeys", {})
        mapping = {}
        
        # Mapping configurations to triggers
        if "toggle_overlay" in hotkeys_cfg and hotkeys_cfg["toggle_overlay"]:
            key_str = to_pynput_format(hotkeys_cfg["toggle_overlay"])
            mapping[key_str] = self.toggle_overlay_signal.emit
            
        if "toggle_crosshair" in hotkeys_cfg and hotkeys_cfg["toggle_crosshair"]:
            key_str = to_pynput_format(hotkeys_cfg["toggle_crosshair"])
            mapping[key_str] = self.toggle_crosshair_signal.emit
            
        if "increase_opacity" in hotkeys_cfg and hotkeys_cfg["increase_opacity"]:
            key_str = to_pynput_format(hotkeys_cfg["increase_opacity"])
            mapping[key_str] = self.opacity_up_signal.emit
            
        if "decrease_opacity" in hotkeys_cfg and hotkeys_cfg["decrease_opacity"]:
            key_str = to_pynput_format(hotkeys_cfg["decrease_opacity"])
            mapping[key_str] = self.opacity_down_signal.emit

        if not mapping:
            return

        try:
            self.listener = keyboard.GlobalHotKeys(mapping)
            self.listener.start()
            print(f"Global hotkeys listener started with: {mapping}")
        except Exception as e:
            print(f"Failed to start global hotkeys listener: {e}")

    def stop(self):
        if self.listener:
            try:
                self.listener.stop()
            except Exception as e:
                print(f"Error stopping hotkeys listener: {e}")
            self.listener = None

import ctypes
import os
import time
from PySide6.QtCore import QThread, Signal
import psutil

class ProcessMonitor(QThread):
    # Signals whether a target game is active in the foreground
    game_active_signal = Signal(bool)

    def __init__(self, config_manager):
        super().__init__()
        self.config_manager = config_manager
        self.running = True
        self.last_state = None

    def run(self):
        user32 = ctypes.windll.user32
        
        while self.running:
            # If auto-trigger is disabled, we do nothing and sleep
            if not self.config_manager.get("auto_trigger_enabled", True):
                self.last_state = None  # Reset state so it updates immediately when re-enabled
                time.sleep(1.5)
                continue

            hwnd = user32.GetForegroundWindow()
            if not hwnd:
                time.sleep(1.0)
                continue

            pid = ctypes.c_ulong()
            user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
            
            try:
                # If process ID is valid, get the executable name and path
                if pid.value > 0:
                    proc = psutil.Process(pid.value)
                    proc_name = proc.name().lower()
                    try:
                        proc_path = proc.exe().lower()
                    except Exception:
                        proc_path = ""
                else:
                    proc_name = ""
                    proc_path = ""
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                proc_name = ""
                proc_path = ""

            game_list = [g.strip().lower() for g in self.config_manager.get("game_processes", []) if g.strip()]
            
            # Check if current foreground process is in the monitor list, or if it is a Steam game
            is_game_active = False
            if proc_name:
                if proc_name in game_list:
                    is_game_active = True
                elif proc_name not in ["steam.exe", "steamwebhelper.exe"]:
                    if "steamapps" in proc_path or "steamlibrary" in proc_path:
                        is_game_active = True
            
            if is_game_active != self.last_state:
                self.game_active_signal.emit(is_game_active)
                self.last_state = is_game_active
                
            time.sleep(1.5)

    def stop(self):
        self.running = False
        self.wait()

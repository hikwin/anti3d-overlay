import sys
import os
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PySide6.QtGui import QIcon, QPixmap, QPainter, QRadialGradient, QColor
from PySide6.QtCore import Qt, QObject

from config import ConfigManager
from overlay_window import OverlayWindow
from control_panel import ControlPanel
from hotkey_manager import HotkeyManager
from process_monitor import ProcessMonitor

def create_tray_icon():
    """Generates a high-quality circular glowing QIcon dynamically."""
    pixmap = QPixmap(32, 32)
    pixmap.fill(Qt.GlobalColor.transparent)
    
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
    
    # Outer glow (radial gradient)
    grad = QRadialGradient(16, 16, 14)
    grad.setColorAt(0.0, QColor("#00F5FF"))
    grad.setColorAt(0.7, QColor("#00A3AA"))
    grad.setColorAt(1.0, QColor(0, 0, 0, 0))
    
    painter.setBrush(grad)
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawEllipse(2, 2, 28, 28)
    
    # Center core dot
    painter.setBrush(QColor(255, 255, 255, 220))
    painter.drawEllipse(13, 13, 6, 6)
    
    painter.end()
    return QIcon(pixmap)

class Anti3DApp(QObject):
    def __init__(self):
        super().__init__()
        # Load configuration
        self.config_manager = ConfigManager()
        
        # Create UI components
        self.overlay_window = OverlayWindow(self.config_manager)
        self.control_panel = ControlPanel(self.config_manager)
        
        # Initialize tray icon
        self.setup_tray_icon()
        
        # Share tray icon handle with control panel for minimize notifications
        self.control_panel.tray_icon = self.tray_icon
        
        # Initialize background services
        self.hotkey_manager = HotkeyManager(self.config_manager)
        self.process_monitor = ProcessMonitor(self.config_manager)
        
        # Connect signals
        self.connect_signals()
        
        # Start services
        self.hotkey_manager.start()
        self.process_monitor.start()
        
        # Set initial visibility of overlay
        self.update_overlay_visibility()
        
        # Show control panel on initial launch
        self.control_panel.show()

    def connect_signals(self):
        # Control panel updates settings
        self.control_panel.settings_changed.connect(self.update_overlay_visibility)
        self.control_panel.settings_changed.connect(self.refresh_overlay_geometry)
        self.control_panel.screen_changed.connect(self.overlay_window.set_screen_index)
        self.control_panel.exit_requested.connect(self.exit_app)
        self.control_panel.language_changed.connect(self.retranslate_tray_menu)
        
        # Hotkeys trigger actions
        self.hotkey_manager.toggle_overlay_signal.connect(self.on_toggle_overlay)
        self.hotkey_manager.toggle_crosshair_signal.connect(self.on_toggle_crosshair)
        self.hotkey_manager.opacity_up_signal.connect(self.on_opacity_up)
        self.hotkey_manager.opacity_down_signal.connect(self.on_opacity_down)
        
        # Process monitor triggers overlay state
        self.process_monitor.game_active_signal.connect(self.on_game_active_changed)

    def setup_tray_icon(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(create_tray_icon())
        self.tray_icon.setToolTip(self.config_manager.tr("tray_tooltip"))
        
        # Context Menu
        self.tray_menu = QMenu()
        
        self.act_show = self.tray_menu.addAction(self.config_manager.tr("tray_open_panel"))
        self.act_show.triggered.connect(self.show_control_panel)
        
        self.act_toggle = self.tray_menu.addAction(self.config_manager.tr("tray_toggle_overlay"))
        self.act_toggle.triggered.connect(self.on_toggle_overlay)
        
        # Presets submenu in tray
        self.presets_menu = self.tray_menu.addMenu(self.config_manager.tr("tray_load_preset"))
        self.presets_menu.aboutToShow.connect(self.populate_tray_presets)
        
        self.tray_menu.addSeparator()
        self.act_exit = self.tray_menu.addAction(self.config_manager.tr("tray_exit"))
        self.act_exit.triggered.connect(self.exit_app)
        
        self.tray_icon.setContextMenu(self.tray_menu)
        
        # Handle double click on tray icon
        self.tray_icon.activated.connect(self.on_tray_activated)
        self.tray_icon.show()
        
        # Call retranslate once initially to sync state
        self.retranslate_tray_menu()

    def populate_tray_presets(self):
        self.presets_menu.clear()
        presets = self.config_manager.get_presets()
        active_preset = self.config_manager.get("active_preset", "默认模式")
        
        for name in presets.keys():
            action = self.presets_menu.addAction(name)
            action.setCheckable(True)
            action.setChecked(name == active_preset)
            # Use default binding closure
            action.triggered.connect(lambda checked=False, p_name=name: self.apply_preset_from_tray(p_name))

    def apply_preset_from_tray(self, preset_name):
        if self.config_manager.apply_preset(preset_name):
            self.control_panel.load_settings_into_ui()
            self.update_overlay_visibility()
            display_name = self.config_manager.tr("preset_default_mode") if preset_name == "默认模式" else preset_name
            self.tray_icon.showMessage(
                self.config_manager.tr("preset_applied"),
                self.config_manager.tr("preset_applied_desc", display_name),
                self.tray_icon.MessageIcon.Information,
                2000
            )

    def on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.show_control_panel()

    def show_control_panel(self):
        self.control_panel.show()
        self.control_panel.raise_()
        self.control_panel.activateWindow()

    def refresh_overlay_geometry(self):
        """Recalculate overlay window geometry applying current top/bottom margins."""
        screens = QApplication.screens()
        screen_idx = getattr(self.overlay_window, '_current_screen_index', 0)
        screen = screens[screen_idx] if 0 <= screen_idx < len(screens) else QApplication.primaryScreen()
        if screen:
            self.overlay_window.setGeometry(
                self.overlay_window._get_margin_geometry(screen.geometry())
            )

    def update_overlay_visibility(self):

        is_on = self.config_manager.get("overlay_enabled", True)
        if is_on:
            self.overlay_window.show()
            self.overlay_window.update()
        else:
            self.overlay_window.hide()
            
        # Synchronize context menu label
        state_text = "暂停叠加层" if is_on else "开启叠加层"
        self.act_toggle.setText(state_text)

    def on_toggle_overlay(self):
        is_on = not self.config_manager.get("overlay_enabled", True)
        self.config_manager.set("overlay_enabled", is_on)
        self.control_panel.load_settings_into_ui()
        self.update_overlay_visibility()

    def on_toggle_crosshair(self):
        is_on = not self.config_manager.get("crosshair_enabled", True)
        self.config_manager.set("crosshair_enabled", is_on)
        self.control_panel.load_settings_into_ui()
        self.overlay_window.update()

    def on_opacity_up(self):
        opac = self.config_manager.get("mask_opacity", 0.70)
        opac = min(1.0, opac + 0.05)
        self.config_manager.set("mask_opacity", opac)
        self.control_panel.load_settings_into_ui()
        self.overlay_window.update()

    def on_opacity_down(self):
        opac = self.config_manager.get("mask_opacity", 0.70)
        opac = max(0.0, opac - 0.05)
        self.config_manager.set("mask_opacity", opac)
        self.control_panel.load_settings_into_ui()
        self.overlay_window.update()

    def on_game_active_changed(self, is_game_active):
        """Called when process monitor detects foreground game state transition."""
        if self.config_manager.get("auto_trigger_enabled", True):
            self.config_manager.set("overlay_enabled", is_game_active)
            self.control_panel.update_toggle_button_ui()
            self.update_overlay_visibility()
            # Show a brief notification on auto trigger
            status = self.config_manager.tr("status_auto_on") if is_game_active else self.config_manager.tr("status_auto_off")
            self.tray_icon.showMessage(
                self.config_manager.tr("auto_trigger"),
                self.config_manager.tr("auto_trigger_desc", status),
                self.tray_icon.MessageIcon.Information,
                1500
            )

    def retranslate_tray_menu(self):
        tr = self.config_manager.tr
        self.tray_icon.setToolTip(tr("tray_tooltip"))
        self.act_show.setText(tr("tray_open_panel"))
        
        is_on = self.config_manager.get("overlay_enabled", True)
        self.act_toggle.setText(tr("btn_toggle_running") if is_on else tr("btn_toggle_paused"))
        
        self.presets_menu.setTitle(tr("tray_load_preset"))
        self.act_exit.setText(tr("tray_exit"))

    def exit_app(self):
        # Stop background threads
        self.hotkey_manager.stop()
        self.process_monitor.stop()
        
        # Close windows
        self.overlay_window.close()
        self.control_panel.close()
        
        # Quit Qt Application
        QApplication.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Avoid closing application when setting window is hidden
    app.setQuitOnLastWindowClosed(False)
    
    main_app = Anti3DApp()
    
    sys.exit(app.exec())

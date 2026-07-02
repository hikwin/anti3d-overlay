import os
import json
import ctypes
import locale

def get_windows_locale():
    try:
        # Get User Default Locale Name (e.g. "zh-CN", "zh-TW", "en-US")
        buf = ctypes.create_unicode_buffer(85)
        if ctypes.windll.kernel32.GetUserDefaultLocaleName(buf, 85) > 0:
            locale_name = buf.value.lower()
            if locale_name.startswith("zh"):
                return "zh"
    except Exception:
        pass
    
    # Fallback to standard Python locale detection
    try:
        loc = locale.getlocale()[0] or locale.getdefaultlocale()[0]
        if loc and loc.lower().startswith("zh"):
            return "zh"
    except Exception:
        pass
        
    return "en"

TRANSLATIONS = {
    "zh": {
        # Tray Menu
        "tray_tooltip": "Anti3D-Overlay (3D晕动症缓解工具)",
        "tray_open_panel": "打开设置面板",
        "tray_toggle_overlay": "开启/暂停叠加层",
        "tray_load_preset": "载入方案预设",
        "tray_exit": "退出软件",
        "preset_applied": "方案应用成功",
        "preset_applied_desc": "已切换至防眩晕方案: {}",
        "auto_trigger": "Anti3D 智能触发",
        "auto_trigger_desc": "监测到游戏前台切换，已{}防晕遮罩。",
        "status_auto_on": "自动开启",
        "status_auto_off": "自动暂停",
        "tray_minimized_title": "Anti3D-Overlay 已最小化",
        "tray_minimized_desc": "设置面板已隐藏到系统托盘，双击托盘图标可再次打开。",
        
        # Telemetry
        "telemetry_stats": "CPU: {}%  RAM: {}%",
        
        # UI Titles & Common
        "window_title": "Anti3D-Overlay 控制面板 (Mulmiyac Pro)",
        "btn_toggle_running": " 防眩晕叠加层：运行中 ",
        "btn_toggle_paused": " 防眩晕叠加层：已暂停 ",
        "btn_exit": " 退出整个软件 ",
        "btn_save": " 保存 ",
        "btn_delete": " 删除 ",
        "btn_add": " 添加 ",
        "btn_del_selected": " 删除选中 ",
        "btn_choose_color": " 选择颜色 ",
        "msg_confirm_exit_title": "确认退出",
        "msg_confirm_exit_text": "您确定要彻底退出防眩晕叠加层软件吗？",
        "msg_info": "信息",
        "msg_warning": "警告",
        "msg_success": "成功",
        "msg_preset_exists": "该进程已经存在于列表中。",
        "msg_enter_preset_name": "请输入预设方案的名称。",
        "msg_preset_saved": "成功保存预设方案: {}",
        "msg_preset_delete_confirm": "您确定要删除预设方案 '{}' 吗？",
        "msg_preset_delete_default_warning": "默认模式是系统预设，无法删除。",
        "msg_preset_deleted": "成功删除预设: {}",
        
        # Tabs
        "tab_mask": " 边缘遮罩 ",
        "tab_crosshair": " 中心准星 ",
        "tab_auxiliary": " 辅助与状态 ",
        "tab_hotkeys": " 快捷键与自动 ",
        "tab_presets": " 方案预设 ",
        
        # Tab 1: Mask
        "mask_title": "边缘遮罩 (屏蔽余光高速移动)",
        "mask_enabled": "启用边缘遮罩",
        "mask_shape": "遮罩形状:",
        "mask_size": "清晰区大小:",
        "mask_opacity": "遮罩不透明度:",
        "mask_feather": "边缘羽化度:",
        "mask_color": "遮罩颜色:",
        "shape_circle": "圆形",
        "shape_ellipse": "椭圆形",
        "shape_rectangle": "方形",
        "shape_diamond": "菱形",
        
        # Tab 2: Crosshair
        "crosshair_title": "屏幕中心准星 (视觉聚焦锚点)",
        "crosshair_enabled": "启用中心准星",
        "crosshair_shape": "准星形状:",
        "crosshair_size": "准星大小:",
        "crosshair_thick": "线条粗细:",
        "crosshair_color": "准星颜色:",
        "crosshair_opacity": "不透明度:",
        "crosshair_outline": "启用深色边缘描边 (增强复杂背景可见度)",
        "crosshair_outline_color": "描边颜色:",
        
        # Tab 3: Auxiliary
        "aux_screen_title": "物理显示屏幕选择",
        "aux_screen_label": "叠加屏幕:",
        "aux_margin_top": "顶部间距:",
        "aux_margin_bottom": "底部间距:",
        "aux_margin_desc": "（适用于窗口化游戏，用于收缩遮罩叠加区域）",
        "aux_split_title": "分屏引导线 (减少单次光流范围)",
        "aux_split_enabled": "启用分屏引导线",
        "aux_split_type": "分屏方式:",
        "aux_split_thick": "线条粗细:",
        "aux_split_opacity": "不透明度:",
        "aux_split_color": "线段颜色:",
        "split_v": "垂直单线",
        "split_h": "水平单线",
        "split_cross": "十字十字线",
        
        "aux_edge_title": "边缘十字标 (强中心引导锚点)",
        "aux_edge_enabled": "启用边缘十字标",
        "aux_edge_style": "十字标样式:",
        "aux_edge_width": "标线宽度:",
        "aux_edge_length": "标线长度:",
        "aux_edge_arrow": "箭头大小:",
        "aux_edge_opacity": "不透明度:",
        "aux_edge_color": "十字标颜色:",
        "edge_style_arrow": "箭头标",
        "edge_style_bar": "直条标",
        "edge_style_semi": "半圆标",
        
        "aux_tel_title": "角落信息叠加 (低干扰参考锚点)",
        "aux_tel_clock": "显示角落时钟",
        "aux_tel_stats": "显示系统负载指标 (CPU / RAM 占用率)",
        "aux_tel_pos": "信息位置:",
        "aux_tel_size": "字体大小:",
        "aux_tel_opacity": "不透明度:",
        "aux_tel_color": "文字颜色:",
        
        # Tab 4: Hotkeys & Auto
        "auto_title": "智能进程自动激活 (免手动切换)",
        "auto_enabled": "启用自动检测激活",
        "auto_desc": "当以下列表中的游戏进程处于前台时，自动开启防晕叠加层；否则自动关闭。",
        "auto_tip": "提示：大部分 Steam 游戏可被智能识别。若游戏运行中未显示遮罩，请确保游戏设置中显示模式为“无边框窗口”或“窗口化”（非独占全屏）。",
        "auto_input_placeholder": "例如: Cyberpunk2077.exe",
        
        "hk_title": "全局系统快捷键 (重启软件后生效)",
        "hk_tip": "使用快捷键格式：ctrl+alt+字母 或 ctrl+shift+字母",
        "hk_toggle_overlay": "开启/暂停叠加层:",
        "hk_toggle_crosshair": "开启/隐藏中心准星:",
        "hk_inc_opacity": "增加遮罩透明度:",
        "hk_dec_opacity": "减少遮罩透明度:",
        
        # Tab 5: Presets
        "preset_title": "预设配置管理 (一键载入不同场景)",
        "preset_select": "选择预设方案:",
        "preset_save_new": "保存为新方案:",
        "preset_btn_save": " 保存当前配置为新预设 ",
        "preset_btn_delete": " 删除当前预设 ",
        "preset_btn_reset": " 恢复默认设置 ",
        "msg_confirm_reset_title": "确认恢复默认",
        "msg_confirm_reset_text": "确定要将所有设置恢复为程序默认配置吗？该操作不会删除您已保存的预设方案。",
        "msg_reset_done": "已成功恢复全部默认设置。",
        
        # Language Setting Group
        "lang_title": "界面语言设置 (Language Settings)",
        "lang_label": "选择语言:",
        "lang_auto": "自动检测 (Auto)",
        "lang_zh": "简体/繁体中文 (Chinese)",
        "lang_en": "English",
        
        # Screens Label
        "screen_primary_suffix": " (主屏)",
        "screen_label_pattern": "显示器 {}{}[{}x{}]"
    },
    "en": {
        # Tray Menu
        "tray_tooltip": "Anti3D-Overlay (Motion Sickness Relief)",
        "tray_open_panel": "Open Settings Panel",
        "tray_toggle_overlay": "Toggle Overlay On/Off",
        "tray_load_preset": "Load Preset Scheme",
        "tray_exit": "Exit Program",
        "preset_applied": "Preset Applied Successfully",
        "preset_applied_desc": "Switched to preset scheme: {}",
        "auto_trigger": "Anti3D Smart Trigger",
        "auto_trigger_desc": "Detected game foreground switch, overlay has been {}.",
        "status_auto_on": "auto activated",
        "status_auto_off": "auto suspended",
        "tray_minimized_title": "Anti3D-Overlay Minimized",
        "tray_minimized_desc": "Settings panel hidden to tray. Double click the icon to open again.",
        
        # Telemetry
        "telemetry_stats": "CPU: {}%  RAM: {}%",
        
        # UI Titles & Common
        "window_title": "Anti3D-Overlay Control Panel (Mulmiyac Pro)",
        "btn_toggle_running": " Overlay: Running ",
        "btn_toggle_paused": " Overlay: Suspended ",
        "btn_exit": " Exit Entire Program ",
        "btn_save": " Save ",
        "btn_delete": " Delete ",
        "btn_add": " Add ",
        "btn_del_selected": " Delete Selected ",
        "btn_choose_color": " Choose Color ",
        "msg_confirm_exit_title": "Confirm Exit",
        "msg_confirm_exit_text": "Are you sure you want to completely exit Anti3D-Overlay?",
        "msg_info": "Information",
        "msg_warning": "Warning",
        "msg_success": "Success",
        "msg_preset_exists": "This process already exists in the list.",
        "msg_enter_preset_name": "Please enter a name for the new preset.",
        "msg_preset_saved": "Preset saved successfully: {}",
        "msg_preset_delete_confirm": "Are you sure you want to delete preset '{}'?",
        "msg_preset_delete_default_warning": "Default mode is built-in and cannot be deleted.",
        "msg_preset_deleted": "Preset deleted successfully: {}",
        
        # Tabs
        "tab_mask": " Edge Mask ",
        "tab_crosshair": " Center Crosshair ",
        "tab_auxiliary": " Auxiliary & Stats ",
        "tab_hotkeys": " Hotkeys & Auto ",
        "tab_presets": " Presets ",
        
        # Tab 1: Mask
        "mask_title": "Edge Mask (Blocks peripheral optical flow)",
        "mask_enabled": "Enable Edge Mask",
        "mask_shape": "Mask Shape:",
        "mask_size": "Clear Area Size:",
        "mask_opacity": "Mask Opacity:",
        "mask_feather": "Edge Feathering:",
        "mask_color": "Mask Color:",
        "shape_circle": "Circle",
        "shape_ellipse": "Ellipse",
        "shape_rectangle": "Rectangle",
        "shape_diamond": "Diamond",
        
        # Tab 2: Crosshair
        "crosshair_title": "Center Crosshair (Visual focal anchor)",
        "crosshair_enabled": "Enable Center Crosshair",
        "crosshair_shape": "Crosshair Shape:",
        "crosshair_size": "Crosshair Size:",
        "crosshair_thick": "Line Thickness:",
        "crosshair_color": "Crosshair Color:",
        "crosshair_opacity": "Opacity:",
        "crosshair_outline": "Enable dark outline contour (High-contrast backgrounds)",
        "crosshair_outline_color": "Outline Color:",
        
        # Tab 3: Auxiliary
        "aux_screen_title": "Physical Display Selection",
        "aux_screen_label": "Overlay Screen:",
        "aux_margin_top": "Top Margin:",
        "aux_margin_bottom": "Bottom Margin:",
        "aux_margin_desc": "(Useful for windowed games — shrinks overlay coverage area)",
        "aux_split_title": "Split Screen Lines (Reduce single optical flow region)",
        "aux_split_enabled": "Enable Split Lines",
        "aux_split_type": "Split Type:",
        "aux_split_thick": "Line Thickness:",
        "aux_split_opacity": "Opacity:",
        "aux_split_color": "Lines Color:",
        "split_v": "Vertical Single Line",
        "split_h": "Horizontal Single Line",
        "split_cross": "Cross split lines",
        
        "aux_edge_title": "Edge Crosshair / Arrows (Peripheral center anchor)",
        "aux_edge_enabled": "Enable Edge Crosshair",
        "aux_edge_style": "Crosshair Style:",
        "aux_edge_width": "Lines Width:",
        "aux_edge_length": "Lines Length:",
        "aux_edge_arrow": "Arrow Size:",
        "aux_edge_opacity": "Opacity:",
        "aux_edge_color": "Crosshair Color:",
        "edge_style_arrow": "Arrowhead",
        "edge_style_bar": "Solid Bar",
        "edge_style_semi": "Semicircle",
        
        "aux_tel_title": "Corner Telemetry Overlay (Low-distraction reference points)",
        "aux_tel_clock": "Show Corner Clock",
        "aux_tel_stats": "Show System Metrics (CPU / RAM Usage)",
        "aux_tel_pos": "Info Position:",
        "aux_tel_size": "Font Size:",
        "aux_tel_opacity": "Opacity:",
        "aux_tel_color": "Text Color:",
        
        # Tab 4: Hotkeys & Auto
        "auto_title": "Smart Process Auto-Trigger",
        "auto_enabled": "Enable Auto-Detection Trigger",
        "auto_desc": "When target games in the list run in the foreground, auto open overlay; else auto hide.",
        "auto_tip": "Tip: Most Steam games are detected automatically. If not showing in game, ensure Display Mode is Borderless Windowed or Windowed (not Exclusive Fullscreen).",
        "auto_input_placeholder": "e.g., Cyberpunk2077.exe",
        
        "hk_title": "Global System Hotkeys (Takes effect after restart)",
        "hk_tip": "Hotkey syntax: ctrl+alt+char or ctrl+shift+char",
        "hk_toggle_overlay": "Toggle Overlay:",
        "hk_toggle_crosshair": "Toggle Center Crosshair:",
        "hk_inc_opacity": "Increase Opacity:",
        "hk_dec_opacity": "Decrease Opacity:",
        
        # Tab 5: Presets
        "preset_title": "Configuration Presets Management",
        "preset_select": "Select Preset Scheme:",
        "preset_save_new": "Save Current as New:",
        "preset_btn_save": " Save Preset ",
        "preset_btn_delete": " Delete Preset ",
        "preset_btn_reset": " Restore Defaults ",
        "msg_confirm_reset_title": "Confirm Reset",
        "msg_confirm_reset_text": "Reset all settings to program defaults? Your saved presets will NOT be deleted.",
        "msg_reset_done": "All settings have been restored to defaults.",
        
        # Language Setting Group
        "lang_title": "Language Settings",
        "lang_label": "Select Language:",
        "lang_auto": "Auto-Detect",
        "lang_zh": "简体/繁体中文 (Chinese)",
        "lang_en": "English",
        
        # Screens Label
        "screen_primary_suffix": " (Primary)",
        "screen_label_pattern": "Monitor {}{}[{}x{}]"
    }
}

DEFAULT_CONFIG = {
    "language": "auto",               # "auto", "zh", "en"
    "overlay_enabled": True,
    "mask_enabled": True,             # Whether the edge mask is enabled
    "mask_shape": "ellipse",          # "circle", "ellipse", "rectangle", "diamond"
    "mask_size": 90,                 # 10 to 90 (represents the transparent center size %)
    "mask_opacity": 0.70,            # 0.0 to 1.0
    "mask_feather": 0.35,            # 0.0 to 1.0 (gradient smoothness)
    "mask_color": "#000000",         # Hex color of the mask
    
    "crosshair_enabled": True,
    "crosshair_shape": "dot",        # "dot", "cross", "circle_dot", "diamond", "chevron"
    "crosshair_size": 12,            # size in pixels
    "crosshair_thickness": 2,        # stroke thickness
    "crosshair_color": "#00FF00",    # Hex color
    "crosshair_opacity": 0.6,
    "crosshair_outline": True,
    "crosshair_outline_color": "#000000",
    
    "clock_enabled": True,
    "clock_position": "top_right",   # "top_right", "top_left", "bottom_right", "bottom_left"
    "clock_size": 14,
    "clock_opacity": 0.6,
    "clock_color": "#FFFFFF",
    
    "telemetry_enabled": False,       # System stats: CPU, RAM
    "telemetry_show_fps": False,      # Show FPS (approximate/overlay refresh rate or custom measurement)
    
    "split_lines_enabled": False,
    "split_lines_type": "vertical",  # "vertical", "horizontal", "cross"
    "split_lines_thickness": 1,
    "split_lines_opacity": 0.3,
    "split_lines_color": "#FFFFFF",
    
    "edge_crosshair_enabled": False,
    "edge_crosshair_style": "arrow",  # "arrow", "bar", "semicircle"
    "edge_crosshair_color": "#FF5B55",
    "edge_crosshair_opacity": 0.60,
    "edge_crosshair_width": 40,
    "edge_crosshair_length": 250,
    "edge_crosshair_arrow_size": 25,
    
    "overlay_margin_top": 0,           # Pixels to shrink overlay from top (for windowed games)
    "overlay_margin_bottom": 0,        # Pixels to shrink overlay from bottom (for windowed games)
    
    "hotkeys": {
        "toggle_overlay": "ctrl+alt+o",
        "toggle_crosshair": "ctrl+alt+c",
        "increase_opacity": "ctrl+alt+up",
        "decrease_opacity": "ctrl+alt+down"
    },
    
    "auto_trigger_enabled": True,
    "game_processes": [
        "notepad.exe",
        "Cyberpunk2077.exe",
        "cs2.exe",
        "GTA5.exe"
    ],
    
    "active_preset": "默认模式",
    "presets": {}
}

# Add default presets
DEFAULT_CONFIG["presets"] = {
    "默认模式": {
        "mask_enabled": True,
        "mask_shape": "ellipse",
        "mask_size": 90,
        "mask_opacity": 0.70,
        "mask_feather": 0.35,
        "mask_color": "#000000",
        "crosshair_enabled": True,
        "crosshair_shape": "dot",
        "crosshair_color": "#00FF00",
        "split_lines_enabled": False
    },
    "极度晕机缓解": {
        "mask_shape": "ellipse",
        "mask_size": 40,
        "mask_opacity": 0.85,
        "mask_feather": 0.20,
        "mask_color": "#05050a", # Very dark blue
        "crosshair_enabled": True,
        "crosshair_shape": "circle_dot",
        "crosshair_color": "#00FF00",
        "split_lines_enabled": True,
        "split_lines_type": "cross"
    },
    "FPS竞技": {
        "mask_shape": "circle",
        "mask_size": 65,
        "mask_opacity": 0.50,
        "mask_feather": 0.40,
        "mask_color": "#000000",
        "crosshair_enabled": True,
        "crosshair_shape": "cross",
        "crosshair_color": "#FF0000",
        "split_lines_enabled": False
    },
    "赛车极速": {
        "mask_shape": "rectangle",
        "mask_size": 50,
        "mask_opacity": 0.75,
        "mask_feather": 0.30,
        "mask_color": "#0a0000", # Very dark red
        "crosshair_enabled": True,
        "crosshair_shape": "chevron",
        "crosshair_color": "#FFFF00",
        "split_lines_enabled": True,
        "split_lines_type": "horizontal" # Horizon visual anchor
    }
}

import sys

if getattr(sys, 'frozen', False):
    CONFIG_DIR = os.path.dirname(sys.executable)
else:
    CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

class ConfigManager:
    def __init__(self):
        self.config = {}
        self.load()

    def load(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    self.config = json.load(f)
                # Ensure all default keys exist
                self._merge_with_defaults(self.config, DEFAULT_CONFIG)
            except Exception as e:
                print(f"Error loading config, resetting to default: {e}")
                self.config = DEFAULT_CONFIG.copy()
                self.save()
        else:
            self.config = DEFAULT_CONFIG.copy()
            self.save()

    def _merge_with_defaults(self, target, defaults):
        """Recursively merge default keys to prevent errors when loading older configs."""
        for key, val in defaults.items():
            if key not in target:
                target[key] = val
            elif isinstance(val, dict) and isinstance(target[key], dict):
                # Don't overwrite the presets entirely, just merge default presets
                if key == "presets":
                    for p_name, p_val in val.items():
                        if p_name not in target[key]:
                            target[key][p_name] = p_val
                else:
                    self._merge_with_defaults(target[key], val)

    def save(self):
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving config: {e}")

    def get(self, key, default=None):
        return self.config.get(key, default)

    def set(self, key, value):
        self.config[key] = value
        self.save()

    def get_presets(self):
        return self.config.get("presets", {})

    def save_preset(self, name):
        """Save the current active parameters as a preset."""
        # We only save visual overlay parameters, not application configurations like hotkeys or process lists
        preset_keys = [
            "mask_enabled", "mask_shape", "mask_size", "mask_opacity", "mask_feather", "mask_color",
            "crosshair_enabled", "crosshair_shape", "crosshair_size", "crosshair_thickness",
            "crosshair_color", "crosshair_opacity", "crosshair_outline", "crosshair_outline_color",
            "clock_enabled", "clock_position", "clock_size", "clock_opacity", "clock_color",
            "telemetry_enabled", "telemetry_show_fps",
            "split_lines_enabled", "split_lines_type", "split_lines_thickness", "split_lines_opacity", "split_lines_color",
            "edge_crosshair_enabled", "edge_crosshair_style", "edge_crosshair_color", "edge_crosshair_opacity",
            "edge_crosshair_width", "edge_crosshair_length", "edge_crosshair_arrow_size"
        ]
        
        preset_data = {}
        for key in preset_keys:
            preset_data[key] = self.config[key]
            
        self.config["presets"][name] = preset_data
        self.config["active_preset"] = name
        self.save()

    def apply_preset(self, name):
        """Apply settings from a preset name."""
        if name in self.config["presets"]:
            preset_data = self.config["presets"][name]
            for key, val in preset_data.items():
                self.config[key] = val
            self.config["active_preset"] = name
            self.save()
            return True
        return False

    def delete_preset(self, name):
        if name in self.config["presets"] and name != "默认模式":
            del self.config["presets"][name]
            if self.config["active_preset"] == name:
                self.config["active_preset"] = "默认模式"
                self.apply_preset("默认模式")
            self.save()
            return True
        return False

    def get_language(self):
        lang_config = self.get("language", "auto")
        if lang_config == "auto":
            return get_windows_locale()
        return lang_config

    def tr(self, key, *args):
        lang = self.get_language()
        string = TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, key)
        if args:
            try:
                return string.format(*args)
            except Exception:
                pass
        return string

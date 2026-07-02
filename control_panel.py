from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
    QTabWidget, QLabel, QSlider, QComboBox, QCheckBox, QPushButton, 
    QLineEdit, QListWidget, QGroupBox, QColorDialog, QMessageBox, QFormLayout,
    QApplication
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QScreen


# Stylized Modern Dark Theme Stylesheet (QSS)
QSS_THEME = """
QMainWindow {
    background-color: #121216;
    color: #E0E0E6;
    font-family: "Segoe UI", "Microsoft YaHei", "Arial", sans-serif;
}

QWidget#central {
    background-color: #121216;
}

QTabWidget::pane {
    border: 1px solid #252530;
    background-color: #1A1A22;
    border-radius: 8px;
    padding: 10px;
}

QTabBar::tab {
    background-color: #15151C;
    color: #8E8E9F;
    border: 1px solid #252530;
    border-bottom: none;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    padding: 8px 16px;
    margin-right: 4px;
    font-weight: bold;
    font-size: 12px;
}

QTabBar::tab:hover {
    background-color: #20202B;
    color: #00F5FF;
}

QTabBar::tab:selected {
    background-color: #1A1A22;
    color: #00F5FF;
    border: 1px solid #00F5FF;
    border-bottom: 1px solid #1A1A22;
}

QGroupBox {
    border: 1px solid #252530;
    border-radius: 6px;
    margin-top: 12px;
    padding-top: 15px;
    font-weight: bold;
    color: #00F5FF;
    font-size: 13px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 10px;
    padding: 0 5px;
}

QLabel {
    color: #C0C0D0;
    font-size: 13px;
}

QCheckBox {
    color: #C0C0D0;
    spacing: 8px;
    font-size: 13px;
}

QCheckBox::indicator {
    width: 16px;
    height: 16px;
    border: 2px solid #3A3A4A;
    border-radius: 4px;
    background-color: #15151C;
}

QCheckBox::indicator:hover {
    border-color: #00F5FF;
}

QCheckBox::indicator:checked {
    background-color: #00F5FF;
    border-color: #00F5FF;
}

QPushButton {
    background-color: #252535;
    color: #E0E0E6;
    border: 1px solid #3A3A4A;
    border-radius: 6px;
    padding: 6px 14px;
    font-size: 12px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #303045;
    border-color: #00F5FF;
    color: #00F5FF;
}

QPushButton:pressed {
    background-color: #1A1A28;
}

QSlider::groove:horizontal {
    border: 1px solid #252530;
    height: 6px;
    background: #15151C;
    border-radius: 3px;
}

QSlider::handle:horizontal {
    background: #00F5FF;
    border: 1px solid #00D2DD;
    width: 14px;
    height: 14px;
    margin: -4px 0;
    border-radius: 7px;
}

QSlider::handle:horizontal:hover {
    background: #33F7FF;
    border-color: #00F5FF;
}

QComboBox {
    background-color: #15151C;
    border: 1px solid #252530;
    border-radius: 6px;
    padding: 4px 8px;
    color: #E0E0E6;
    font-size: 12px;
}

QComboBox:hover {
    border-color: #00F5FF;
}

QComboBox QAbstractItemView {
    background-color: #15151C;
    border: 1px solid #252530;
    selection-background-color: #252535;
    selection-color: #00F5FF;
    color: #E0E0E6;
}

QLineEdit {
    background-color: #15151C;
    border: 1px solid #252530;
    border-radius: 6px;
    padding: 4px 8px;
    color: #E0E0E6;
    font-size: 12px;
}

QLineEdit:focus {
    border-color: #00F5FF;
}

QListWidget {
    background-color: #15151C;
    border: 1px solid #252530;
    border-radius: 6px;
    padding: 4px;
    color: #E0E0E6;
    font-size: 12px;
}

QListWidget::item:hover {
    background-color: #20202B;
    color: #00F5FF;
}

QListWidget::item:selected {
    background-color: #252535;
    color: #00F5FF;
}

QMessageBox {
    background-color: #1A1A22;
}
QMessageBox QLabel {
    color: #E0E0E6;
    font-size: 13px;
}
QMessageBox QPushButton {
    background-color: #252535;
    color: #E0E0E6;
    border: 1px solid #3A3A4A;
    border-radius: 6px;
    padding: 5px 15px;
    min-width: 70px;
    font-size: 12px;
}
QMessageBox QPushButton:hover {
    background-color: #303045;
    border-color: #00F5FF;
    color: #00F5FF;
}
"""

class ControlPanel(QMainWindow):
    # Emitted when any overlay parameter changes, requesting screen redraw
    settings_changed = Signal()
    # Emitted when a screen/monitor index is selected
    screen_changed = Signal(int)
    # Emitted when exit is requested
    exit_requested = Signal()
    # Emitted when interface language changes
    language_changed = Signal()

    def __init__(self, config_manager):
        super().__init__()
        self.config_manager = config_manager
        
        self.setWindowTitle("Anti3D-Overlay 控制面板 (Mulmiyac Pro)")
        self.resize(780, 560)
        self.setStyleSheet(QSS_THEME)
        
        # Central widget setup
        central = QWidget(self)
        central.setObjectName("central")
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        
        # Master Toggle Button
        self.btn_toggle = QPushButton(" 开启防眩晕叠加层 ", self)
        self.btn_toggle.setCheckable(True)
        self.btn_toggle.setFixedHeight(40)
        self.btn_toggle.setStyleSheet("""
            QPushButton {
                background-color: #FF3B30;
                color: white;
                font-size: 15px;
                border: none;
                border-radius: 8px;
            }
            QPushButton:checked {
                background-color: #34C759;
            }
        """)
        self.btn_toggle.clicked.connect(self.toggle_overlay)
        main_layout.addWidget(self.btn_toggle)
        
        # Tab view widget
        self.tabs = QTabWidget(self)
        main_layout.addWidget(self.tabs)
        
        # Create different tabs
        self.init_mask_tab()
        self.init_crosshair_tab()
        self.init_auxiliary_tab()
        self.init_hotkey_auto_tab()
        self.init_preset_tab()
        
        # Initialize UI elements from stored configuration
        self.load_settings_into_ui()
        
        # Bottom exit notice
        self.lbl_notice = QLabel("本软件在后台运行，点击关闭将隐藏至托盘，在托盘右键可退出软件。")
        self.lbl_notice.setStyleSheet("font-size: 11px; color: #666; font-style: italic;")
        self.lbl_notice.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.lbl_notice)
        
        # Bottom row layout
        bottom_layout = QHBoxLayout()
        bottom_layout.setContentsMargins(0, 5, 0, 0)
        bottom_layout.setSpacing(10)
        
        # Exit Button
        self.btn_exit_app = QPushButton(" 退出整个软件 ", self)
        self.btn_exit_app.setStyleSheet("""
            QPushButton {
                background-color: #252535;
                color: #FF3B30;
                border: 1px solid #FF3B30;
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #FF3B30;
                color: white;
            }
        """)
        self.btn_exit_app.clicked.connect(self.request_exit)
        bottom_layout.addWidget(self.btn_exit_app)
        
        # Language Switch Button (Text button)
        self.btn_lang_toggle = QPushButton(self)
        self.btn_lang_toggle.setFixedHeight(28) # Perfectly align with exit button height
        self.btn_lang_toggle.setStyleSheet("""
            QPushButton {
                background-color: #252535;
                color: #00F5FF;
                border: 1px solid #00F5FF;
                border-radius: 6px;
                padding: 4px 12px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #00F5FF;
                color: #1E1E2A;
            }
        """)
        self.btn_lang_toggle.clicked.connect(self.toggle_language)
        bottom_layout.addWidget(self.btn_lang_toggle)
        
        bottom_layout.addStretch()
        
        main_layout.addLayout(bottom_layout)
        
        # Retranslate initial UI to match locale
        self.retranslate_ui()

    def toggle_overlay(self):
        is_on = self.btn_toggle.isChecked()
        self.config_manager.set("overlay_enabled", is_on)
        self.btn_toggle.setText(self.config_manager.tr("btn_toggle_running") if is_on else self.config_manager.tr("btn_toggle_paused"))
        self.settings_changed.emit()

    def update_toggle_button_ui(self):
        is_on = self.config_manager.get("overlay_enabled", True)
        self.btn_toggle.blockSignals(True)
        self.btn_toggle.setChecked(is_on)
        self.btn_toggle.setText(self.config_manager.tr("btn_toggle_running") if is_on else self.config_manager.tr("btn_toggle_paused"))
        self.btn_toggle.blockSignals(False)

    # ----------------------------------------------------
    # TAB 1: MASK SETTINGS
    # ----------------------------------------------------
    def init_mask_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        self.group_mask = QGroupBox("边缘遮罩 (屏蔽余光高速移动)")
        g_layout = QFormLayout(self.group_mask)
        g_layout.setVerticalSpacing(15)
        
        # Mask Enable Toggle
        self.chk_mask_enabled = QCheckBox("启用边缘遮罩")
        self.chk_mask_enabled.toggled.connect(self.save_mask_settings)
        g_layout.addRow("", self.chk_mask_enabled)
        
        # Shape
        self.lbl_mask_shape_title = QLabel("遮罩形状:")
        self.cb_mask_shape = QComboBox()
        self.cb_mask_shape.addItems(["圆形", "椭圆形", "方形", "菱形"])
        self.cb_mask_shape.currentIndexChanged.connect(self.save_mask_settings)
        g_layout.addRow(self.lbl_mask_shape_title, self.cb_mask_shape)
        
        # Size (transparent central region diameter)
        self.lbl_mask_size_title = QLabel("清晰区大小:")
        self.lbl_mask_size = QLabel()
        self.slider_mask_size = QSlider(Qt.Orientation.Horizontal)
        self.slider_mask_size.setRange(10, 90)
        self.slider_mask_size.valueChanged.connect(self.save_mask_settings)
        h_layout_size = QHBoxLayout()
        h_layout_size.addWidget(self.slider_mask_size)
        h_layout_size.addWidget(self.lbl_mask_size)
        g_layout.addRow(self.lbl_mask_size_title, h_layout_size)
        
        # Opacity
        self.lbl_mask_opacity_title = QLabel("遮罩不透明度:")
        self.lbl_mask_opacity = QLabel()
        self.slider_mask_opacity = QSlider(Qt.Orientation.Horizontal)
        self.slider_mask_opacity.setRange(0, 100)
        self.slider_mask_opacity.valueChanged.connect(self.save_mask_settings)
        h_layout_opacity = QHBoxLayout()
        h_layout_opacity.addWidget(self.slider_mask_opacity)
        h_layout_opacity.addWidget(self.lbl_mask_opacity)
        g_layout.addRow(self.lbl_mask_opacity_title, h_layout_opacity)
        
        # Feather
        self.lbl_mask_feather_title = QLabel("边缘羽化度:")
        self.lbl_mask_feather = QLabel()
        self.slider_mask_feather = QSlider(Qt.Orientation.Horizontal)
        self.slider_mask_feather.setRange(0, 100)
        self.slider_mask_feather.valueChanged.connect(self.save_mask_settings)
        h_layout_feather = QHBoxLayout()
        h_layout_feather.addWidget(self.slider_mask_feather)
        h_layout_feather.addWidget(self.lbl_mask_feather)
        g_layout.addRow(self.lbl_mask_feather_title, h_layout_feather)
        
        # Mask Color
        self.lbl_mask_color_title = QLabel("遮罩颜色:")
        self.btn_mask_color = QPushButton(" 选择颜色 ")
        self.btn_mask_color.clicked.connect(self.choose_mask_color)
        g_layout.addRow(self.lbl_mask_color_title, self.btn_mask_color)
        
        layout.addWidget(self.group_mask)
        layout.addStretch()
        self.tabs.addTab(tab, " 边缘遮罩 ")

    def choose_mask_color(self):
        current_hex = self.config_manager.get("mask_color", "#000000")
        color = QColorDialog.getColor(QColor(current_hex), self, "选择遮罩颜色")
        if color.isValid():
            self.config_manager.set("mask_color", color.name())
            self.update_color_button_ui(self.btn_mask_color, color.name())
            self.settings_changed.emit()

    def save_mask_settings(self):
        enabled = self.chk_mask_enabled.isChecked()
        shapes = ["circle", "ellipse", "rectangle", "diamond"]
        shape = shapes[self.cb_mask_shape.currentIndex()]
        size = self.slider_mask_size.value()
        opacity = self.slider_mask_opacity.value() / 100.0
        feather = self.slider_mask_feather.value() / 100.0
        
        self.config_manager.set("mask_enabled", enabled)
        self.config_manager.set("mask_shape", shape)
        self.config_manager.set("mask_size", size)
        self.config_manager.set("mask_opacity", opacity)
        self.config_manager.set("mask_feather", feather)
        
        self.lbl_mask_size.setText(f"{size}%")
        self.lbl_mask_opacity.setText(f"{int(opacity * 100)}%")
        self.lbl_mask_feather.setText(f"{int(feather * 100)}%")
        
        # Premium touch: Disable/Enable settings when mask is disabled
        self.cb_mask_shape.setEnabled(enabled)
        self.slider_mask_size.setEnabled(enabled)
        self.lbl_mask_size.setEnabled(enabled)
        self.slider_mask_opacity.setEnabled(enabled)
        self.lbl_mask_opacity.setEnabled(enabled)
        self.slider_mask_feather.setEnabled(enabled)
        self.lbl_mask_feather.setEnabled(enabled)
        self.btn_mask_color.setEnabled(enabled)
        
        self.settings_changed.emit()

    # ----------------------------------------------------
    # TAB 2: CROSSHAIR SETTINGS
    # ----------------------------------------------------
    def init_crosshair_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        self.group_crosshair = QGroupBox("屏幕中心准星 (视觉聚焦锚点)")
        g_layout = QFormLayout(self.group_crosshair)
        g_layout.setVerticalSpacing(12)
        
        # Enable
        self.chk_crosshair_enabled = QCheckBox("启用中心准星")
        self.chk_crosshair_enabled.toggled.connect(self.save_crosshair_settings)
        g_layout.addRow("", self.chk_crosshair_enabled)
        
        # Shape
        self.lbl_crosshair_shape_title = QLabel("准星形状:")
        self.cb_crosshair_shape = QComboBox()
        self.cb_crosshair_shape.addItems(["圆点 (Dot)", "经典十字 (Cross)", "圆点十字 (Circle Dot)", "菱形 (Diamond)", "V形 (Chevron)"])
        self.cb_crosshair_shape.currentIndexChanged.connect(self.save_crosshair_settings)
        g_layout.addRow(self.lbl_crosshair_shape_title, self.cb_crosshair_shape)
        
        # Size
        self.lbl_crosshair_size_title = QLabel("准星大小:")
        self.lbl_crosshair_size = QLabel()
        self.slider_crosshair_size = QSlider(Qt.Orientation.Horizontal)
        self.slider_crosshair_size.setRange(4, 256)
        self.slider_crosshair_size.valueChanged.connect(self.save_crosshair_settings)
        h_layout_size = QHBoxLayout()
        h_layout_size.addWidget(self.slider_crosshair_size)
        h_layout_size.addWidget(self.lbl_crosshair_size)
        g_layout.addRow(self.lbl_crosshair_size_title, h_layout_size)
        
        # Thickness
        self.lbl_crosshair_thick_title = QLabel("线条粗细:")
        self.lbl_crosshair_thick = QLabel()
        self.slider_crosshair_thick = QSlider(Qt.Orientation.Horizontal)
        self.slider_crosshair_thick.setRange(1, 30)
        self.slider_crosshair_thick.valueChanged.connect(self.save_crosshair_settings)
        h_layout_thick = QHBoxLayout()
        h_layout_thick.addWidget(self.slider_crosshair_thick)
        h_layout_thick.addWidget(self.lbl_crosshair_thick)
        g_layout.addRow(self.lbl_crosshair_thick_title, h_layout_thick)
        
        # Color
        self.lbl_crosshair_color_title = QLabel("准星颜色:")
        self.btn_crosshair_color = QPushButton(" 选择颜色 ")
        self.btn_crosshair_color.clicked.connect(self.choose_crosshair_color)
        g_layout.addRow(self.lbl_crosshair_color_title, self.btn_crosshair_color)
        
        # Opacity
        self.lbl_crosshair_opacity_title = QLabel("不透明度:")
        self.lbl_crosshair_opacity = QLabel()
        self.slider_crosshair_opacity = QSlider(Qt.Orientation.Horizontal)
        self.slider_crosshair_opacity.setRange(10, 100)
        self.slider_crosshair_opacity.valueChanged.connect(self.save_crosshair_settings)
        h_layout_opacity = QHBoxLayout()
        h_layout_opacity.addWidget(self.slider_crosshair_opacity)
        h_layout_opacity.addWidget(self.lbl_crosshair_opacity)
        g_layout.addRow(self.lbl_crosshair_opacity_title, h_layout_opacity)
        
        # Outline
        self.chk_crosshair_outline = QCheckBox("启用深色边缘描边 (增强复杂背景可见度)")
        self.chk_crosshair_outline.toggled.connect(self.save_crosshair_settings)
        g_layout.addRow("", self.chk_crosshair_outline)
        
        # Outline Color
        self.lbl_outline_color_title = QLabel("描边颜色:")
        self.btn_outline_color = QPushButton(" 选择颜色 ")
        self.btn_outline_color.clicked.connect(self.choose_outline_color)
        g_layout.addRow(self.lbl_outline_color_title, self.btn_outline_color)
        
        layout.addWidget(self.group_crosshair)
        layout.addStretch()
        self.tabs.addTab(tab, " 中心准星 ")

    def choose_crosshair_color(self):
        current_hex = self.config_manager.get("crosshair_color", "#00FF00")
        color = QColorDialog.getColor(QColor(current_hex), self, "选择准星颜色")
        if color.isValid():
            self.config_manager.set("crosshair_color", color.name())
            self.update_color_button_ui(self.btn_crosshair_color, color.name())
            self.settings_changed.emit()

    def choose_outline_color(self):
        current_hex = self.config_manager.get("crosshair_outline_color", "#000000")
        color = QColorDialog.getColor(QColor(current_hex), self, "选择描边颜色")
        if color.isValid():
            self.config_manager.set("crosshair_outline_color", color.name())
            self.update_color_button_ui(self.btn_outline_color, color.name())
            self.settings_changed.emit()

    def save_crosshair_settings(self):
        shapes = ["dot", "cross", "circle_dot", "diamond", "chevron"]
        shape = shapes[self.cb_crosshair_shape.currentIndex()]
        size = self.slider_crosshair_size.value()
        thick = self.slider_crosshair_thick.value()
        opacity = self.slider_crosshair_opacity.value() / 100.0
        enabled = self.chk_crosshair_enabled.isChecked()
        outline = self.chk_crosshair_outline.isChecked()
        
        self.config_manager.set("crosshair_enabled", enabled)
        self.config_manager.set("crosshair_shape", shape)
        self.config_manager.set("crosshair_size", size)
        self.config_manager.set("crosshair_thickness", thick)
        self.config_manager.set("crosshair_opacity", opacity)
        self.config_manager.set("crosshair_outline", outline)
        
        self.lbl_crosshair_size.setText(f"{size}px")
        self.lbl_crosshair_thick.setText(f"{thick}px")
        self.lbl_crosshair_opacity.setText(f"{int(opacity * 100)}%")
        
        self.settings_changed.emit()

    # ----------------------------------------------------
    # TAB 3: AUXILIARY & SYSTEM SETTINGS
    # ----------------------------------------------------
    def init_auxiliary_tab(self):
        tab = QWidget()
        main_layout = QHBoxLayout(tab)
        main_layout.setSpacing(15)
        
        left_col = QWidget()
        left_layout = QVBoxLayout(left_col)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(10)
        
        right_col = QWidget()
        right_layout = QVBoxLayout(right_col)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(10)
        
        # 1. Screen selection (Left Column)
        self.group_screen = QGroupBox("物理显示屏幕选择")
        screen_form = QFormLayout(self.group_screen)
        screen_row = QHBoxLayout()
        self.lbl_screen_title = QLabel("叠加屏幕:")
        self.cb_screen = QComboBox()
        self.refresh_screens()
        self.cb_screen.currentIndexChanged.connect(self.on_screen_changed)
        screen_row.addWidget(self.lbl_screen_title)
        screen_row.addWidget(self.cb_screen)
        screen_form.addRow(screen_row)
        
        # Margin top slider
        self.lbl_margin_top_title = QLabel("顶部间距:")
        self.lbl_margin_top = QLabel("0px")
        self.slider_margin_top = QSlider(Qt.Orientation.Horizontal)
        self.slider_margin_top.setRange(0, 500)
        self.slider_margin_top.setValue(0)
        self.slider_margin_top.valueChanged.connect(self.save_margin_settings)
        h_margin_top = QHBoxLayout()
        h_margin_top.addWidget(self.slider_margin_top)
        h_margin_top.addWidget(self.lbl_margin_top)
        screen_form.addRow(self.lbl_margin_top_title, h_margin_top)
        
        # Margin bottom slider
        self.lbl_margin_bottom_title = QLabel("底部间距:")
        self.lbl_margin_bottom = QLabel("0px")
        self.slider_margin_bottom = QSlider(Qt.Orientation.Horizontal)
        self.slider_margin_bottom.setRange(0, 500)
        self.slider_margin_bottom.setValue(0)
        self.slider_margin_bottom.valueChanged.connect(self.save_margin_settings)
        h_margin_bottom = QHBoxLayout()
        h_margin_bottom.addWidget(self.slider_margin_bottom)
        h_margin_bottom.addWidget(self.lbl_margin_bottom)
        screen_form.addRow(self.lbl_margin_bottom_title, h_margin_bottom)
        
        # Hint label
        self.lbl_margin_desc = QLabel("（适用于窗口化游戏，用于收缩遮罩叠加区域）")
        self.lbl_margin_desc.setStyleSheet("color: #6E6E7E; font-size: 11px;")
        screen_form.addRow(self.lbl_margin_desc)
        
        left_layout.addWidget(self.group_screen)
        
        # 2. Split Lines (Left Column)
        self.group_split = QGroupBox("分屏引导线 (减少单次光流范围)")
        split_layout = QFormLayout(self.group_split)
        
        self.chk_split_enabled = QCheckBox("启用分屏引导线")
        self.chk_split_enabled.toggled.connect(self.save_auxiliary_settings)
        split_layout.addRow("", self.chk_split_enabled)
        
        self.lbl_split_type_title = QLabel("分屏方式:")
        self.cb_split_type = QComboBox()
        self.cb_split_type.addItems(["垂直单线", "水平单线", "十字十字线"])
        self.cb_split_type.currentIndexChanged.connect(self.save_auxiliary_settings)
        split_layout.addRow(self.lbl_split_type_title, self.cb_split_type)
        
        self.lbl_split_thick_title = QLabel("线条粗细:")
        self.lbl_split_thick = QLabel()
        self.slider_split_thick = QSlider(Qt.Orientation.Horizontal)
        self.slider_split_thick.setRange(1, 5)
        self.slider_split_thick.valueChanged.connect(self.save_auxiliary_settings)
        h_layout_s_thick = QHBoxLayout()
        h_layout_s_thick.addWidget(self.slider_split_thick)
        h_layout_s_thick.addWidget(self.lbl_split_thick)
        split_layout.addRow(self.lbl_split_thick_title, h_layout_s_thick)
        
        self.lbl_split_opacity_title = QLabel("不透明度:")
        self.lbl_split_opacity = QLabel()
        self.slider_split_opacity = QSlider(Qt.Orientation.Horizontal)
        self.slider_split_opacity.setRange(0, 100)
        self.slider_split_opacity.valueChanged.connect(self.save_auxiliary_settings)
        h_layout_s_opac = QHBoxLayout()
        h_layout_s_opac.addWidget(self.slider_split_opacity)
        h_layout_s_opac.addWidget(self.lbl_split_opacity)
        split_layout.addRow(self.lbl_split_opacity_title, h_layout_s_opac)
        
        self.lbl_split_color_title = QLabel("线段颜色:")
        self.btn_split_color = QPushButton(" 选择颜色 ")
        self.btn_split_color.clicked.connect(self.choose_split_color)
        split_layout.addRow(self.lbl_split_color_title, self.btn_split_color)
        
        left_layout.addWidget(self.group_split)
        left_layout.addStretch()
        
        # 3. Edge Crosshair Group (Right Column)
        self.group_edge = QGroupBox("边缘十字标 (强中心引导锚点)")
        edge_layout = QFormLayout(self.group_edge)
        
        self.chk_edge_enabled = QCheckBox("启用边缘十字标")
        self.chk_edge_enabled.toggled.connect(self.save_edge_settings)
        edge_layout.addRow("", self.chk_edge_enabled)
        
        self.lbl_edge_style_title = QLabel("十字标样式:")
        self.cb_edge_style = QComboBox()
        self.cb_edge_style.addItems(["箭头标", "直条标", "半圆标"])
        self.cb_edge_style.currentIndexChanged.connect(self.save_edge_settings)
        edge_layout.addRow(self.lbl_edge_style_title, self.cb_edge_style)
        
        self.lbl_edge_width_title = QLabel("标线宽度:")
        self.lbl_edge_width = QLabel()
        self.slider_edge_width = QSlider(Qt.Orientation.Horizontal)
        self.slider_edge_width.setRange(10, 100)
        self.slider_edge_width.valueChanged.connect(self.save_edge_settings)
        h_layout_e_width = QHBoxLayout()
        h_layout_e_width.addWidget(self.slider_edge_width)
        h_layout_e_width.addWidget(self.lbl_edge_width)
        edge_layout.addRow(self.lbl_edge_width_title, h_layout_e_width)
        
        self.lbl_edge_length_title = QLabel("标线长度:")
        self.lbl_edge_length = QLabel()
        self.slider_edge_length = QSlider(Qt.Orientation.Horizontal)
        self.slider_edge_length.setRange(50, 600)
        self.slider_edge_length.valueChanged.connect(self.save_edge_settings)
        h_layout_e_length = QHBoxLayout()
        h_layout_e_length.addWidget(self.slider_edge_length)
        h_layout_e_length.addWidget(self.lbl_edge_length)
        edge_layout.addRow(self.lbl_edge_length_title, h_layout_e_length)
        
        self.lbl_edge_arrow_title = QLabel("箭头大小:")
        self.lbl_edge_arrow_size = QLabel()
        self.slider_edge_arrow_size = QSlider(Qt.Orientation.Horizontal)
        self.slider_edge_arrow_size.setRange(5, 100)
        self.slider_edge_arrow_size.valueChanged.connect(self.save_edge_settings)
        h_layout_e_arrow = QHBoxLayout()
        h_layout_e_arrow.addWidget(self.slider_edge_arrow_size)
        h_layout_e_arrow.addWidget(self.lbl_edge_arrow_size)
        edge_layout.addRow(self.lbl_edge_arrow_title, h_layout_e_arrow)
        
        self.lbl_edge_opacity_title = QLabel("不透明度:")
        self.lbl_edge_opacity = QLabel()
        self.slider_edge_opacity = QSlider(Qt.Orientation.Horizontal)
        self.slider_edge_opacity.setRange(10, 100)
        self.slider_edge_opacity.valueChanged.connect(self.save_edge_settings)
        h_layout_e_opac = QHBoxLayout()
        h_layout_e_opac.addWidget(self.slider_edge_opacity)
        h_layout_e_opac.addWidget(self.lbl_edge_opacity)
        edge_layout.addRow(self.lbl_edge_opacity_title, h_layout_e_opac)
        
        self.lbl_edge_color_title = QLabel("十字标颜色:")
        self.btn_edge_color = QPushButton(" 选择颜色 ")
        self.btn_edge_color.clicked.connect(self.choose_edge_color)
        edge_layout.addRow(self.lbl_edge_color_title, self.btn_edge_color)
        
        right_layout.addWidget(self.group_edge)
        
        # 4. Telemetry & Clock (Right Column)
        self.group_telemetry = QGroupBox("角落信息叠加 (低干扰参考锚点)")
        tel_layout = QFormLayout(self.group_telemetry)
        
        self.chk_clock_enabled = QCheckBox("显示角落时钟")
        self.chk_clock_enabled.toggled.connect(self.save_auxiliary_settings)
        tel_layout.addRow("", self.chk_clock_enabled)
        
        self.chk_telemetry_enabled = QCheckBox("显示系统负载指标 (CPU / RAM 占用率)")
        self.chk_telemetry_enabled.toggled.connect(self.save_auxiliary_settings)
        tel_layout.addRow("", self.chk_telemetry_enabled)
        
        self.lbl_clock_pos_title = QLabel("信息位置:")
        self.cb_clock_pos = QComboBox()
        self.cb_clock_pos.addItems(["右上角", "左上角", "右下角", "左下角"])
        self.cb_clock_pos.currentIndexChanged.connect(self.save_auxiliary_settings)
        tel_layout.addRow(self.lbl_clock_pos_title, self.cb_clock_pos)
        
        self.lbl_clock_size_title = QLabel("字体大小:")
        self.lbl_clock_size = QLabel()
        self.slider_clock_size = QSlider(Qt.Orientation.Horizontal)
        self.slider_clock_size.setRange(8, 36)
        self.slider_clock_size.valueChanged.connect(self.save_auxiliary_settings)
        h_layout_c_size = QHBoxLayout()
        h_layout_c_size.addWidget(self.slider_clock_size)
        h_layout_c_size.addWidget(self.lbl_clock_size)
        tel_layout.addRow(self.lbl_clock_size_title, h_layout_c_size)
        
        self.lbl_clock_opacity_title = QLabel("不透明度:")
        self.lbl_clock_opacity = QLabel()
        self.slider_clock_opacity = QSlider(Qt.Orientation.Horizontal)
        self.slider_clock_opacity.setRange(0, 100)
        self.slider_clock_opacity.valueChanged.connect(self.save_auxiliary_settings)
        h_layout_c_opac = QHBoxLayout()
        h_layout_c_opac.addWidget(self.slider_clock_opacity)
        h_layout_c_opac.addWidget(self.lbl_clock_opacity)
        tel_layout.addRow(self.lbl_clock_opacity_title, h_layout_c_opac)
        
        self.lbl_clock_color_title = QLabel("文字颜色:")
        self.btn_clock_color = QPushButton(" 选择颜色 ")
        self.btn_clock_color.clicked.connect(self.choose_clock_color)
        tel_layout.addRow(self.lbl_clock_color_title, self.btn_clock_color)
        
        right_layout.addWidget(self.group_telemetry)
        right_layout.addStretch()
        
        main_layout.addWidget(left_col)
        main_layout.addWidget(right_col)
        self.tabs.addTab(tab, " 辅助与状态 ")

    def refresh_screens(self):
        self.cb_screen.blockSignals(True)
        self.cb_screen.clear()
        screens = QApplication.screens()
        for i, s in enumerate(screens):
            primary = self.config_manager.tr("screen_primary_suffix") if s == QApplication.primaryScreen() else ""
            geometry = f" [{s.geometry().width()}x{s.geometry().height()}]"
            self.cb_screen.addItem(self.config_manager.tr("screen_label_pattern", i+1, primary, s.geometry().width(), s.geometry().height()))
        self.cb_screen.blockSignals(False)

    def on_screen_changed(self, index):
        if index >= 0:
            self.screen_changed.emit(index)

    def choose_edge_color(self):
        current_hex = self.config_manager.get("edge_crosshair_color", "#FF5B55")
        color = QColorDialog.getColor(QColor(current_hex), self, "选择边缘十字标颜色")
        if color.isValid():
            self.config_manager.set("edge_crosshair_color", color.name())
            self.update_color_button_ui(self.btn_edge_color, color.name())
            self.settings_changed.emit()

    def save_edge_settings(self):
        enabled = self.chk_edge_enabled.isChecked()
        styles = ["arrow", "bar", "semicircle"]
        style = styles[self.cb_edge_style.currentIndex()]
        width = self.slider_edge_width.value()
        length = self.slider_edge_length.value()
        arrow_size = self.slider_edge_arrow_size.value()
        opacity = self.slider_edge_opacity.value() / 100.0
        
        self.config_manager.set("edge_crosshair_enabled", enabled)
        self.config_manager.set("edge_crosshair_style", style)
        self.config_manager.set("edge_crosshair_width", width)
        self.config_manager.set("edge_crosshair_length", length)
        self.config_manager.set("edge_crosshair_arrow_size", arrow_size)
        self.config_manager.set("edge_crosshair_opacity", opacity)
        
        self.lbl_edge_width.setText(f"{width}px")
        self.lbl_edge_length.setText(f"{length}px")
        self.lbl_edge_arrow_size.setText(f"{arrow_size}px")
        self.lbl_edge_opacity.setText(f"{int(opacity * 100)}%")
        
        # Premium touch: Disable arrow size slider for non-arrow styles
        is_arrow = (style == "arrow")
        self.slider_edge_arrow_size.setEnabled(is_arrow)
        self.lbl_edge_arrow_size.setEnabled(is_arrow)
        
        self.settings_changed.emit()

    def choose_split_color(self):
        current_hex = self.config_manager.get("split_lines_color", "#FFFFFF")
        color = QColorDialog.getColor(QColor(current_hex), self, "选择分屏线颜色")
        if color.isValid():
            self.config_manager.set("split_lines_color", color.name())
            self.update_color_button_ui(self.btn_split_color, color.name())
            self.settings_changed.emit()

    def choose_clock_color(self):
        current_hex = self.config_manager.get("clock_color", "#FFFFFF")
        color = QColorDialog.getColor(QColor(current_hex), self, "选择文本颜色")
        if color.isValid():
            self.config_manager.set("clock_color", color.name())
            self.update_color_button_ui(self.btn_clock_color, color.name())
            self.settings_changed.emit()

    def save_margin_settings(self):
        margin_top = self.slider_margin_top.value()
        margin_bottom = self.slider_margin_bottom.value()
        self.config_manager.set("overlay_margin_top", margin_top)
        self.config_manager.set("overlay_margin_bottom", margin_bottom)
        self.lbl_margin_top.setText(f"{margin_top}px")
        self.lbl_margin_bottom.setText(f"{margin_bottom}px")
        self.settings_changed.emit()

    def save_auxiliary_settings(self):
        split_enabled = self.chk_split_enabled.isChecked()
        split_types = ["vertical", "horizontal", "cross"]
        split_type = split_types[self.cb_split_type.currentIndex()]
        split_thick = self.slider_split_thick.value()
        split_opacity = self.slider_split_opacity.value() / 100.0
        
        clock_enabled = self.chk_clock_enabled.isChecked()
        telemetry_enabled = self.chk_telemetry_enabled.isChecked()
        clock_positions = ["top_right", "top_left", "bottom_right", "bottom_left"]
        clock_pos = clock_positions[self.cb_clock_pos.currentIndex()]
        clock_size = self.slider_clock_size.value()
        clock_opacity = self.slider_clock_opacity.value() / 100.0
        
        self.config_manager.set("split_lines_enabled", split_enabled)
        self.config_manager.set("split_lines_type", split_type)
        self.config_manager.set("split_lines_thickness", split_thick)
        self.config_manager.set("split_lines_opacity", split_opacity)
        
        self.config_manager.set("clock_enabled", clock_enabled)
        self.config_manager.set("telemetry_enabled", telemetry_enabled)
        self.config_manager.set("clock_position", clock_pos)
        self.config_manager.set("clock_size", clock_size)
        self.config_manager.set("clock_opacity", clock_opacity)
        
        self.lbl_split_thick.setText(f"{split_thick}px")
        self.lbl_split_opacity.setText(f"{int(split_opacity * 100)}%")
        self.lbl_clock_size.setText(f"{clock_size}pt")
        self.lbl_clock_opacity.setText(f"{int(clock_opacity * 100)}%")
        
        self.settings_changed.emit()

    # ----------------------------------------------------
    # TAB 4: HOTKEYS & AUTO-TRIGGER SETTINGS
    # ----------------------------------------------------
    def init_hotkey_auto_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Auto Trigger
        self.group_auto = QGroupBox("智能进程自动激活 (免手动切换)")
        auto_layout = QVBoxLayout(self.group_auto)
        
        self.chk_auto_enabled = QCheckBox("启用自动检测激活")
        self.chk_auto_enabled.toggled.connect(self.save_auto_trigger_enabled)
        auto_layout.addWidget(self.chk_auto_enabled)
        
        self.lbl_info = QLabel("当以下列表中的游戏进程处于前台时，自动开启防晕叠加层；否则自动关闭。")
        self.lbl_info.setWordWrap(True)
        self.lbl_info.setStyleSheet("font-size: 11px; color: #888;")
        auto_layout.addWidget(self.lbl_info)
        
        self.lbl_tip = QLabel("提示：大部分 Steam 游戏可被智能识别。若游戏运行中未显示遮罩，请确保游戏设置中显示模式为“无边框窗口”或“窗口化”（非独占全屏）。")
        self.lbl_tip.setWordWrap(True)
        self.lbl_tip.setStyleSheet("font-size: 11px; color: #00F5FF; font-style: italic;")
        auto_layout.addWidget(self.lbl_tip)
        
        # List of processes
        self.list_processes = QListWidget()
        self.list_processes.setMaximumHeight(120)
        auto_layout.addWidget(self.list_processes)
        
        h_layout_proc = QHBoxLayout()
        self.txt_process_input = QLineEdit()
        self.txt_process_input.setPlaceholderText("例如: Cyberpunk2077.exe")
        h_layout_proc.addWidget(self.txt_process_input)
        
        self.btn_add_proc = QPushButton(" 添加 ")
        self.btn_add_proc.clicked.connect(self.add_process)
        h_layout_proc.addWidget(self.btn_add_proc)
        
        self.btn_del_proc = QPushButton(" 删除选中 ")
        self.btn_del_proc.clicked.connect(self.delete_process)
        h_layout_proc.addWidget(self.btn_del_proc)
        
        auto_layout.addLayout(h_layout_proc)
        layout.addWidget(self.group_auto)
        
        # Hotkeys
        self.group_hotkey = QGroupBox("全局系统快捷键 (重启软件后生效)")
        hk_layout = QFormLayout(self.group_hotkey)
        hk_layout.setVerticalSpacing(8)
        
        self.lbl_hk_tip = QLabel("使用快捷键格式：ctrl+alt+字母 或 ctrl+shift+字母")
        self.lbl_hk_tip.setStyleSheet("font-size: 11px; color: #888; font-style: italic;")
        hk_layout.addRow("", self.lbl_hk_tip)
        
        self.txt_hk_toggle_overlay = QLineEdit()
        self.txt_hk_toggle_overlay.editingFinished.connect(self.save_hotkeys)
        self.lbl_hk_toggle_overlay = QLabel("开启/暂停叠加层:")
        hk_layout.addRow(self.lbl_hk_toggle_overlay, self.txt_hk_toggle_overlay)
        
        self.txt_hk_toggle_crosshair = QLineEdit()
        self.txt_hk_toggle_crosshair.editingFinished.connect(self.save_hotkeys)
        self.lbl_hk_toggle_crosshair = QLabel("开启/隐藏中心准星:")
        hk_layout.addRow(self.lbl_hk_toggle_crosshair, self.txt_hk_toggle_crosshair)
        
        self.txt_hk_inc_opacity = QLineEdit()
        self.txt_hk_inc_opacity.editingFinished.connect(self.save_hotkeys)
        self.lbl_hk_inc_opacity = QLabel("增加遮罩透明度:")
        hk_layout.addRow(self.lbl_hk_inc_opacity, self.txt_hk_inc_opacity)
        
        self.txt_hk_dec_opacity = QLineEdit()
        self.txt_hk_dec_opacity.editingFinished.connect(self.save_hotkeys)
        self.lbl_hk_dec_opacity = QLabel("减少遮罩透明度:")
        hk_layout.addRow(self.lbl_hk_dec_opacity, self.txt_hk_dec_opacity)
        
        layout.addWidget(self.group_hotkey)
        layout.addStretch()
        self.tabs.addTab(tab, " 快捷键与自动 ")

    def save_auto_trigger_enabled(self):
        self.config_manager.set("auto_trigger_enabled", self.chk_auto_enabled.isChecked())

    def add_process(self):
        text = self.txt_process_input.text().strip()
        if text:
            # Basic validation: ensure it ends with .exe if a file extension
            if "." not in text:
                text += ".exe"
            
            current_list = self.config_manager.get("game_processes", [])
            if text.lower() not in [p.lower() for p in current_list]:
                current_list.append(text)
                self.config_manager.set("game_processes", current_list)
                self.list_processes.addItem(text)
                self.txt_process_input.clear()
            else:
                QMessageBox.information(self, self.config_manager.tr("msg_info"), self.config_manager.tr("msg_preset_exists"))

    def delete_process(self):
        selected_items = self.list_processes.selectedItems()
        if not selected_items:
            return
            
        current_list = self.config_manager.get("game_processes", [])
        for item in selected_items:
            proc_name = item.text()
            if proc_name in current_list:
                current_list.remove(proc_name)
            # Remove from list widget
            self.list_processes.takeItem(self.list_processes.row(item))
            
        self.config_manager.set("game_processes", current_list)

    def save_hotkeys(self):
        hotkeys = {
            "toggle_overlay": self.txt_hk_toggle_overlay.text().strip().lower(),
            "toggle_crosshair": self.txt_hk_toggle_crosshair.text().strip().lower(),
            "increase_opacity": self.txt_hk_inc_opacity.text().strip().lower(),
            "decrease_opacity": self.txt_hk_dec_opacity.text().strip().lower()
        }
        self.config_manager.set("hotkeys", hotkeys)

    # ----------------------------------------------------
    # TAB 5: PRESETS SETTINGS
    # ----------------------------------------------------
    def init_preset_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        self.group_preset = QGroupBox("预设配置管理 (一键载入不同场景)")
        g_layout = QFormLayout(self.group_preset)
        g_layout.setVerticalSpacing(15)
        
        # Select active preset
        self.cb_active_preset = QComboBox()
        self.cb_active_preset.currentIndexChanged.connect(self.on_preset_selected)
        self.lbl_preset_select = QLabel("选择预设方案:")
        g_layout.addRow(self.lbl_preset_select, self.cb_active_preset)
        
        # New preset name
        self.txt_new_preset = QLineEdit()
        self.txt_new_preset.setPlaceholderText("请输入新预设的名称")
        self.lbl_preset_save_new = QLabel("保存为新方案:")
        g_layout.addRow(self.lbl_preset_save_new, self.txt_new_preset)
        
        h_layout_btns = QHBoxLayout()
        self.btn_save_preset = QPushButton(" 保存当前配置为新预设 ")
        self.btn_save_preset.clicked.connect(self.save_new_preset)
        h_layout_btns.addWidget(self.btn_save_preset)
        
        self.btn_del_preset = QPushButton(" 删除当前预设 ")
        self.btn_del_preset.clicked.connect(self.delete_current_preset)
        h_layout_btns.addWidget(self.btn_del_preset)
        
        g_layout.addRow("", h_layout_btns)
        
        # Reset to defaults button (separate row, prominent warning style)
        self.btn_reset_preset = QPushButton(" 恢复默认设置 ")
        self.btn_reset_preset.setStyleSheet("""
            QPushButton {
                background-color: #252535;
                color: #FF9500;
                border: 1px solid #FF9500;
                border-radius: 6px;
                padding: 6px 14px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #FF9500;
                color: #1A1A22;
            }
        """)
        self.btn_reset_preset.clicked.connect(self.reset_to_defaults)
        g_layout.addRow("", self.btn_reset_preset)
        
        layout.addWidget(self.group_preset)
        layout.addStretch()
        self.tabs.addTab(tab, " 方案预设 ")

    def refresh_presets_combobox(self):
        self.cb_active_preset.blockSignals(True)
        self.cb_active_preset.clear()
        
        presets = self.config_manager.get_presets()
        for name in presets.keys():
            display_name = self.config_manager.tr("preset_default_mode") if name == "默认模式" else name
            self.cb_active_preset.addItem(display_name, name)
            
        active = self.config_manager.get("active_preset", "默认模式")
        index = self.cb_active_preset.findData(active)
        if index >= 0:
            self.cb_active_preset.setCurrentIndex(index)
            
        # "默认模式" is built-in and cannot be deleted
        self.btn_del_preset.setEnabled(active != "默认模式")
        self.cb_active_preset.blockSignals(False)

    def on_preset_selected(self, index):
        if index < 0:
            return
        name = self.cb_active_preset.itemData(index)
        if not name:
            name = self.cb_active_preset.currentText()
        if self.config_manager.apply_preset(name):
            # Load new settings values into UI sliders and comboboxes
            self.load_settings_into_ui()
            # Notify overlay window to redraw
            self.settings_changed.emit()
            
            # Update delete button availability
            self.btn_del_preset.setEnabled(name != "默认模式")

    def save_new_preset(self):
        name = self.txt_new_preset.text().strip()
        if not name:
            QMessageBox.warning(self, self.config_manager.tr("msg_warning"), self.config_manager.tr("msg_enter_preset_name"))
            return
            
        self.config_manager.save_preset(name)
        self.txt_new_preset.clear()
        self.refresh_presets_combobox()
        QMessageBox.information(self, self.config_manager.tr("msg_success"), self.config_manager.tr("msg_preset_saved", name))

    def delete_current_preset(self):
        index = self.cb_active_preset.currentIndex()
        name = self.cb_active_preset.itemData(index) or self.cb_active_preset.currentText()
        if name == "默认模式":
            QMessageBox.warning(self, self.config_manager.tr("msg_warning"), self.config_manager.tr("msg_preset_delete_default_warning"))
            return
            
        reply = QMessageBox.question(
            self, self.config_manager.tr("msg_confirm_exit_title"), self.config_manager.tr("msg_preset_delete_confirm", name),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.config_manager.delete_preset(name)
            self.refresh_presets_combobox()
            self.load_settings_into_ui()
            self.settings_changed.emit()
            QMessageBox.information(self, self.config_manager.tr("msg_success"), self.config_manager.tr("msg_preset_deleted", name))

    def reset_to_defaults(self):
        """Reset all visual/overlay settings to program defaults, preserving language, hotkeys, and presets."""
        reply = QMessageBox.question(
            self,
            self.config_manager.tr("msg_confirm_reset_title"),
            self.config_manager.tr("msg_confirm_reset_text"),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply != QMessageBox.StandardButton.Yes:
            return

        from config import DEFAULT_CONFIG
        # Keys to preserve (user-specific, non-visual settings except active_preset)
        preserve_keys = {"language", "hotkeys", "game_processes", "auto_trigger_enabled",
                         "presets"}

        for key, value in DEFAULT_CONFIG.items():
            if key not in preserve_keys:
                self.config_manager.config[key] = value

        # Also reset the active preset selection back to built-in default
        self.config_manager.config["active_preset"] = "默认模式"

        self.config_manager.save()
        self.load_settings_into_ui()
        self.settings_changed.emit()
        QMessageBox.information(
            self,
            self.config_manager.tr("msg_success"),
            self.config_manager.tr("msg_reset_done")
        )

    # ----------------------------------------------------
    # DATA BINDING HELPERS
    # ----------------------------------------------------
    def update_color_button_ui(self, button, hex_color):
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {hex_color};
                color: {"#000000" if QColor(hex_color).lightness() > 130 else "#FFFFFF"};
                border: 1px solid #555566;
                border-radius: 4px;
                padding: 4px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                border-color: #00F5FF;
            }}
        """)
        # Display the hex code on the button
        button.setText(hex_color.upper())

    def load_settings_into_ui(self):
        """Loads values from the config manager into UI widgets, blocking signals temporarily to avoid change cascades."""
        # Block signals for all input widgets to prevent recursive update loops
        widgets_to_block = [
            self.chk_mask_enabled, self.cb_mask_shape, self.slider_mask_size, self.slider_mask_opacity, self.slider_mask_feather,
            self.chk_crosshair_enabled, self.cb_crosshair_shape, self.slider_crosshair_size, self.slider_crosshair_thick,
            self.slider_crosshair_opacity, self.chk_crosshair_outline,
            self.chk_split_enabled, self.cb_split_type, self.slider_split_thick, self.slider_split_opacity,
            self.chk_clock_enabled, self.chk_telemetry_enabled, self.cb_clock_pos, self.slider_clock_size,
            self.slider_clock_opacity, self.chk_auto_enabled,
            self.chk_edge_enabled, self.cb_edge_style, self.slider_edge_width, self.slider_edge_length, self.slider_edge_arrow_size, self.slider_edge_opacity
        ]
        for w in widgets_to_block:
            w.blockSignals(True)
            
        # 1. Overlay state
        self.update_toggle_button_ui()

        # 2. Mask settings
        mask_enabled = self.config_manager.get("mask_enabled", True)
        self.chk_mask_enabled.setChecked(mask_enabled)
        
        shapes = ["circle", "ellipse", "rectangle", "diamond"]
        shape = self.config_manager.get("mask_shape", "ellipse")
        if shape in shapes:
            self.cb_mask_shape.setCurrentIndex(shapes.index(shape))
        
        size = self.config_manager.get("mask_size", 90)
        self.slider_mask_size.setValue(size)
        self.lbl_mask_size.setText(f"{size}%")
        
        opacity = self.config_manager.get("mask_opacity", 0.70)
        self.slider_mask_opacity.setValue(int(opacity * 100))
        self.lbl_mask_opacity.setText(f"{int(opacity * 100)}%")
        
        feather = self.config_manager.get("mask_feather", 0.35)
        self.slider_mask_feather.setValue(int(feather * 100))
        self.lbl_mask_feather.setText(f"{int(feather * 100)}%")
        
        self.update_color_button_ui(self.btn_mask_color, self.config_manager.get("mask_color", "#000000"))
        
        # Enable state update
        self.cb_mask_shape.setEnabled(mask_enabled)
        self.slider_mask_size.setEnabled(mask_enabled)
        self.lbl_mask_size.setEnabled(mask_enabled)
        self.slider_mask_opacity.setEnabled(mask_enabled)
        self.lbl_mask_opacity.setEnabled(mask_enabled)
        self.slider_mask_feather.setEnabled(mask_enabled)
        self.lbl_mask_feather.setEnabled(mask_enabled)
        self.btn_mask_color.setEnabled(mask_enabled)

        # 3. Crosshair settings
        self.chk_crosshair_enabled.setChecked(self.config_manager.get("crosshair_enabled", True))
        
        c_shapes = ["dot", "cross", "circle_dot", "diamond", "chevron"]
        c_shape = self.config_manager.get("crosshair_shape", "dot")
        if c_shape in c_shapes:
            self.cb_crosshair_shape.setCurrentIndex(c_shapes.index(c_shape))
            
        c_size = self.config_manager.get("crosshair_size", 12)
        self.slider_crosshair_size.setValue(c_size)
        self.lbl_crosshair_size.setText(f"{c_size}px")
        
        c_thick = self.config_manager.get("crosshair_thickness", 2)
        self.slider_crosshair_thick.setValue(c_thick)
        self.lbl_crosshair_thick.setText(f"{c_thick}px")
        
        c_opac = self.config_manager.get("crosshair_opacity", 1.0)
        self.slider_crosshair_opacity.setValue(int(c_opac * 100))
        self.lbl_crosshair_opacity.setText(f"{int(c_opac * 100)}%")
        
        self.update_color_button_ui(self.btn_crosshair_color, self.config_manager.get("crosshair_color", "#00FF00"))
        
        self.chk_crosshair_outline.setChecked(self.config_manager.get("crosshair_outline", True))
        self.update_color_button_ui(self.btn_outline_color, self.config_manager.get("crosshair_outline_color", "#000000"))

        # 4. Split screen settings
        self.chk_split_enabled.setChecked(self.config_manager.get("split_lines_enabled", False))
        
        split_types = ["vertical", "horizontal", "cross"]
        split_type = self.config_manager.get("split_lines_type", "vertical")
        if split_type in split_types:
            self.cb_split_type.setCurrentIndex(split_types.index(split_type))
            
        s_thick = self.config_manager.get("split_lines_thickness", 1)
        self.slider_split_thick.setValue(s_thick)
        self.lbl_split_thick.setText(f"{s_thick}px")
        
        s_opac = self.config_manager.get("split_lines_opacity", 0.3)
        self.slider_split_opacity.setValue(int(s_opac * 100))
        self.lbl_split_opacity.setText(f"{int(s_opac * 100)}%")
        
        self.update_color_button_ui(self.btn_split_color, self.config_manager.get("split_lines_color", "#FFFFFF"))

        # 4b. Edge crosshair settings
        self.chk_edge_enabled.setChecked(self.config_manager.get("edge_crosshair_enabled", False))
        
        edge_styles = ["arrow", "bar", "semicircle"]
        edge_style = self.config_manager.get("edge_crosshair_style", "arrow")
        if edge_style in edge_styles:
            self.cb_edge_style.setCurrentIndex(edge_styles.index(edge_style))
        
        edge_width = self.config_manager.get("edge_crosshair_width", 40)
        self.slider_edge_width.setValue(edge_width)
        self.lbl_edge_width.setText(f"{edge_width}px")
        
        edge_length = self.config_manager.get("edge_crosshair_length", 250)
        self.slider_edge_length.setValue(edge_length)
        self.lbl_edge_length.setText(f"{edge_length}px")
        
        edge_arrow_size = self.config_manager.get("edge_crosshair_arrow_size", 25)
        self.slider_edge_arrow_size.setValue(edge_arrow_size)
        self.lbl_edge_arrow_size.setText(f"{edge_arrow_size}px")
        
        edge_opacity = self.config_manager.get("edge_crosshair_opacity", 0.60)
        self.slider_edge_opacity.setValue(int(edge_opacity * 100))
        self.lbl_edge_opacity.setText(f"{int(edge_opacity * 100)}%")
        
        self.update_color_button_ui(self.btn_edge_color, self.config_manager.get("edge_crosshair_color", "#FF5B55"))
        
        # Premium touch: Update arrow size slider state initially
        is_arrow = (edge_style == "arrow")
        self.slider_edge_arrow_size.setEnabled(is_arrow)
        self.lbl_edge_arrow_size.setEnabled(is_arrow)

        # 5. Telemetry / Corner Clock
        self.chk_clock_enabled.setChecked(self.config_manager.get("clock_enabled", True))
        self.chk_telemetry_enabled.setChecked(self.config_manager.get("telemetry_enabled", False))
        
        c_positions = ["top_right", "top_left", "bottom_right", "bottom_left"]
        c_pos = self.config_manager.get("clock_position", "top_right")
        if c_pos in c_positions:
            self.cb_clock_pos.setCurrentIndex(c_positions.index(c_pos))
            
        c_pt = self.config_manager.get("clock_size", 14)
        self.slider_clock_size.setValue(c_pt)
        self.lbl_clock_size.setText(f"{c_pt}pt")
        
        c_pt_opac = self.config_manager.get("clock_opacity", 0.6)
        self.slider_clock_opacity.setValue(int(c_pt_opac * 100))
        self.lbl_clock_opacity.setText(f"{int(c_pt_opac * 100)}%")
        
        self.update_color_button_ui(self.btn_clock_color, self.config_manager.get("clock_color", "#FFFFFF"))

        # Overlay margins
        margin_top = self.config_manager.get("overlay_margin_top", 0)
        self.slider_margin_top.setValue(int(margin_top))
        self.lbl_margin_top.setText(f"{int(margin_top)}px")
        
        margin_bottom = self.config_manager.get("overlay_margin_bottom", 0)
        self.slider_margin_bottom.setValue(int(margin_bottom))
        self.lbl_margin_bottom.setText(f"{int(margin_bottom)}px")

        # 6. Auto-activation
        self.chk_auto_enabled.setChecked(self.config_manager.get("auto_trigger_enabled", True))
        
        # Populate game process list
        self.list_processes.clear()
        processes = self.config_manager.get("game_processes", [])
        for p in processes:
            if p.strip():
                self.list_processes.addItem(p)

        # Hotkeys strings
        hks = self.config_manager.get("hotkeys", {})
        self.txt_hk_toggle_overlay.setText(hks.get("toggle_overlay", "ctrl+alt+o"))
        self.txt_hk_toggle_crosshair.setText(hks.get("toggle_crosshair", "ctrl+alt+c"))
        self.txt_hk_inc_opacity.setText(hks.get("increase_opacity", "ctrl+alt+up"))
        self.txt_hk_dec_opacity.setText(hks.get("decrease_opacity", "ctrl+alt+down"))

        # 7. Preset
        self.refresh_presets_combobox()

        # Unblock signals
        for w in widgets_to_block:
            w.blockSignals(False)

    def request_exit(self):
        reply = QMessageBox.question(
            self, self.config_manager.tr("msg_confirm_exit_title"), self.config_manager.tr("msg_confirm_exit_text"),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.is_exiting = True
            self.exit_requested.emit()

    def toggle_language(self):
        current = self.config_manager.get_language()
        next_lang = "en" if current == "zh" else "zh"
        self.config_manager.set("language", next_lang)
        self.config_manager.save()
        self.retranslate_ui()
        self.language_changed.emit()

    def closeEvent(self, event):
        """Override close event to hide the window and run in the system tray, rather than exiting."""
        # If we are intentionally exiting the app, accept the event
        if getattr(self, 'is_exiting', False):
            event.accept()
            return
            
        # If we have a system tray icon active, hide and notify the user
        if hasattr(self, 'tray_icon') and self.tray_icon and self.tray_icon.isVisible():
            self.hide()
            # Suppress multiple messages to avoid spamming the user
            if not getattr(self, '_notified_minimize', False):
                self.tray_icon.showMessage(
                    self.config_manager.tr("tray_minimized_title"),
                    self.config_manager.tr("tray_minimized_desc"),
                    icon=self.tray_icon.MessageIcon.Information,
                    msecs=3000
                )
                self._notified_minimize = True
            event.ignore()
        else:
            event.accept()

    def retranslate_ui(self):
        tr = self.config_manager.tr
        
        # Main Window
        self.setWindowTitle(tr("window_title"))
        
        # Toggle Overlay button
        is_on = self.btn_toggle.isChecked()
        self.btn_toggle.setText(tr("btn_toggle_running") if is_on else tr("btn_toggle_paused"))
        
        # Tab titles
        self.tabs.setTabText(0, tr("tab_mask"))
        self.tabs.setTabText(1, tr("tab_crosshair"))
        self.tabs.setTabText(2, tr("tab_auxiliary"))
        self.tabs.setTabText(3, tr("tab_hotkeys"))
        self.tabs.setTabText(4, tr("tab_presets"))
        
        # Tab 1: Mask
        self.group_mask.setTitle(tr("mask_title"))
        self.chk_mask_enabled.setText(tr("mask_enabled"))
        self.lbl_mask_shape_title.setText(tr("mask_shape"))
        self.lbl_mask_size_title.setText(tr("mask_size"))
        self.lbl_mask_opacity_title.setText(tr("mask_opacity"))
        self.lbl_mask_feather_title.setText(tr("mask_feather"))
        self.lbl_mask_color_title.setText(tr("mask_color"))
        self.btn_mask_color.setText(tr("btn_choose_color"))
        
        self.cb_mask_shape.blockSignals(True)
        current_mask_shape = self.cb_mask_shape.currentIndex()
        self.cb_mask_shape.clear()
        self.cb_mask_shape.addItems([tr("shape_circle"), tr("shape_ellipse"), tr("shape_rectangle"), tr("shape_diamond")])
        self.cb_mask_shape.setCurrentIndex(current_mask_shape)
        self.cb_mask_shape.blockSignals(False)
        
        # Tab 2: Crosshair
        self.group_crosshair.setTitle(tr("crosshair_title"))
        self.chk_crosshair_enabled.setText(tr("crosshair_enabled"))
        self.lbl_crosshair_shape_title.setText(tr("crosshair_shape"))
        self.lbl_crosshair_size_title.setText(tr("crosshair_size"))
        self.lbl_crosshair_thick_title.setText(tr("crosshair_thick"))
        self.lbl_crosshair_color_title.setText(tr("crosshair_color"))
        self.lbl_crosshair_opacity_title.setText(tr("crosshair_opacity"))
        self.chk_crosshair_outline.setText(tr("crosshair_outline"))
        self.lbl_outline_color_title.setText(tr("crosshair_outline_color"))
        self.btn_crosshair_color.setText(tr("btn_choose_color"))
        self.btn_outline_color.setText(tr("btn_choose_color"))
        
        self.cb_crosshair_shape.blockSignals(True)
        current_crosshair_shape = self.cb_crosshair_shape.currentIndex()
        self.cb_crosshair_shape.clear()
        self.cb_crosshair_shape.addItems([
            tr("shape_circle") + " (Dot)", 
            tr("split_cross").split("单")[0] + " (Cross)", 
            tr("shape_circle") + "+" + tr("split_cross").split("单")[0] + " (Circle Dot)", 
            tr("shape_diamond") + " (Diamond)", 
            "V-" + tr("shape_rectangle").replace("方形", "形") + " (Chevron)"
        ])
        self.cb_crosshair_shape.setCurrentIndex(current_crosshair_shape)
        self.cb_crosshair_shape.blockSignals(False)
        
        # Tab 3: Auxiliary
        self.group_screen.setTitle(tr("aux_screen_title"))
        self.lbl_screen_title.setText(tr("aux_screen_label"))
        self.lbl_margin_top_title.setText(tr("aux_margin_top"))
        self.lbl_margin_bottom_title.setText(tr("aux_margin_bottom"))
        self.lbl_margin_desc.setText(tr("aux_margin_desc"))
        
        self.group_split.setTitle(tr("aux_split_title"))
        self.chk_split_enabled.setText(tr("aux_split_enabled"))
        self.lbl_split_type_title.setText(tr("aux_split_type"))
        self.lbl_split_thick_title.setText(tr("aux_split_thick"))
        self.lbl_split_opacity_title.setText(tr("aux_split_opacity"))
        self.lbl_split_color_title.setText(tr("aux_split_color"))
        self.btn_split_color.setText(tr("btn_choose_color"))
        
        self.cb_split_type.blockSignals(True)
        current_split_type = self.cb_split_type.currentIndex()
        self.cb_split_type.clear()
        self.cb_split_type.addItems([tr("split_v"), tr("split_h"), tr("split_cross")])
        self.cb_split_type.setCurrentIndex(current_split_type)
        self.cb_split_type.blockSignals(False)
        
        self.group_edge.setTitle(tr("aux_edge_title"))
        self.chk_edge_enabled.setText(tr("aux_edge_enabled"))
        self.lbl_edge_style_title.setText(tr("aux_edge_style"))
        self.lbl_edge_width_title.setText(tr("aux_edge_width"))
        self.lbl_edge_length_title.setText(tr("aux_edge_length"))
        self.lbl_edge_arrow_title.setText(tr("aux_edge_arrow"))
        self.lbl_edge_opacity_title.setText(tr("aux_edge_opacity"))
        self.lbl_edge_color_title.setText(tr("aux_edge_color"))
        self.btn_edge_color.setText(tr("btn_choose_color"))
        
        self.cb_edge_style.blockSignals(True)
        current_edge_style = self.cb_edge_style.currentIndex()
        self.cb_edge_style.clear()
        self.cb_edge_style.addItems([tr("edge_style_arrow"), tr("edge_style_bar"), tr("edge_style_semi")])
        self.cb_edge_style.setCurrentIndex(current_edge_style)
        self.cb_edge_style.blockSignals(False)
        
        self.group_telemetry.setTitle(tr("aux_tel_title"))
        self.chk_clock_enabled.setText(tr("aux_tel_clock"))
        self.chk_telemetry_enabled.setText(tr("aux_tel_stats"))
        self.lbl_clock_pos_title.setText(tr("aux_tel_pos"))
        self.lbl_clock_size_title.setText(tr("aux_tel_size"))
        self.lbl_clock_opacity_title.setText(tr("aux_tel_opacity"))
        self.lbl_clock_color_title.setText(tr("aux_tel_color"))
        self.btn_clock_color.setText(tr("btn_choose_color"))
        
        self.cb_clock_pos.blockSignals(True)
        current_clock_pos = self.cb_clock_pos.currentIndex()
        self.cb_clock_pos.clear()
        self.cb_clock_pos.addItems([
            "Top Right" if tr("lang_en") == "English" else "右上角",
            "Top Left" if tr("lang_en") == "English" else "左上角",
            "Bottom Right" if tr("lang_en") == "English" else "右下角",
            "Bottom Left" if tr("lang_en") == "English" else "左下角"
        ])
        self.cb_clock_pos.setCurrentIndex(current_clock_pos)
        self.cb_clock_pos.blockSignals(False)
        
        self.btn_lang_toggle.setToolTip("Switch Language / 切换语言")
        current_lang = self.config_manager.get_language()
        self.btn_lang_toggle.setText("English" if current_lang == "zh" else "中文")
        
        # Tab 4: Hotkeys
        self.group_auto.setTitle(tr("auto_title"))
        self.chk_auto_enabled.setText(tr("auto_enabled"))
        self.lbl_info.setText(tr("auto_desc"))
        self.lbl_tip.setText(tr("auto_tip"))
        self.txt_process_input.setPlaceholderText(tr("auto_input_placeholder"))
        self.btn_add_proc.setText(tr("btn_add"))
        self.btn_del_proc.setText(tr("btn_del_selected"))
        
        self.group_hotkey.setTitle(tr("hk_title"))
        self.lbl_hk_tip.setText(tr("hk_tip"))
        self.lbl_hk_toggle_overlay.setText(tr("hk_toggle_overlay"))
        self.lbl_hk_toggle_crosshair.setText(tr("hk_toggle_crosshair"))
        self.lbl_hk_inc_opacity.setText(tr("hk_inc_opacity"))
        self.lbl_hk_dec_opacity.setText(tr("hk_dec_opacity"))
        
        # Tab 5: Presets
        self.group_preset.setTitle(tr("preset_title"))
        self.lbl_preset_select.setText(tr("preset_select"))
        self.lbl_preset_save_new.setText(tr("preset_save_new"))
        self.btn_save_preset.setText(tr("preset_btn_save"))
        self.btn_del_preset.setText(tr("preset_btn_delete"))
        self.btn_reset_preset.setText(tr("preset_btn_reset"))
        
        # Main exit button & notice
        self.lbl_notice.setText("This application runs in the background. Closing hides it to the tray; right-click tray to exit." if tr("lang_en") == "English" else "本软件在后台运行，点击关闭将隐藏至托盘，在托盘右键可退出软件。")
        self.btn_exit_app.setText(tr("btn_exit"))
        
        # Suffix labels
        self.lbl_mask_size.setText(f"{self.slider_mask_size.value()}%")
        self.lbl_mask_opacity.setText(f"{self.slider_mask_opacity.value()}%")
        self.lbl_mask_feather.setText(f"{self.slider_mask_feather.value()}%")
        
        self.lbl_crosshair_size.setText(f"{self.slider_crosshair_size.value()}px")
        self.lbl_crosshair_thick.setText(f"{self.slider_crosshair_thick.value()}px")
        self.lbl_crosshair_opacity.setText(f"{self.slider_crosshair_opacity.value()}%")
        
        self.lbl_split_thick.setText(f"{self.slider_split_thick.value()}px")
        self.lbl_split_opacity.setText(f"{self.slider_split_opacity.value()}%")
        
        self.lbl_edge_width.setText(f"{self.slider_edge_width.value()}px")
        self.lbl_edge_length.setText(f"{self.slider_edge_length.value()}px")
        self.lbl_edge_arrow_size.setText(f"{self.slider_edge_arrow_size.value()}px")
        self.lbl_edge_opacity.setText(f"{self.slider_edge_opacity.value()}%")
        
        self.lbl_clock_size.setText(f"{self.slider_clock_size.value()}pt")
        self.lbl_clock_opacity.setText(f"{self.slider_clock_opacity.value()}%")
        
        self.refresh_screens()
        self.refresh_presets_combobox()

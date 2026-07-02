import ctypes
import os
from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QPolygonF, QFont, QRadialGradient
from PySide6.QtCore import Qt, QPointF, QRectF, QTimer, QTime
import psutil

# Windows API constants
GWL_EXSTYLE = -20
GWL_HWNDPARENT = -8
WS_EX_TRANSPARENT = 0x00000020
WS_EX_LAYERED = 0x00080000

try:
    SetWindowLongPtr = ctypes.windll.user32.SetWindowLongPtrW
    GetWindowLongPtr = ctypes.windll.user32.GetWindowLongPtrW
except AttributeError:
    SetWindowLongPtr = ctypes.windll.user32.SetWindowLongW
    GetWindowLongPtr = ctypes.windll.user32.GetWindowLongW

def set_click_through(hwnd):
    """Applies mouse click-through, topmost, no-activate, and transparency styles to HWND."""
    try:
        style = GetWindowLongPtr(hwnd, GWL_EXSTYLE)
        # GWL_EXSTYLE = -20
        # WS_EX_TRANSPARENT = 0x00000020
        # WS_EX_LAYERED = 0x00080000
        # WS_EX_TOPMOST = 0x00000008
        # WS_EX_NOACTIVATE = 0x08000000
        new_style = style | 0x00080000 | 0x00000020 | 0x00000008 | 0x08000000
        SetWindowLongPtr(hwnd, GWL_EXSTYLE, new_style)
    except Exception as e:
        print(f"Error applying click-through style: {e}")

class OverlayWindow(QWidget):
    def __init__(self, config_manager):
        super().__init__()
        self.config_manager = config_manager
        
        # Configure window: Frameless, always on top, tool window (using ToolTip flags for maximum Z-order)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnTopHint | 
            Qt.WindowType.ToolTip
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        
        # Stats Cache
        self.cpu_usage = 0
        self.ram_usage = 0
        
        # Setup Timers
        self.metrics_timer = QTimer(self)
        self.metrics_timer.timeout.connect(self.update_metrics)
        self.metrics_timer.start(2000) # Every 2s
        
        self.clock_timer = QTimer(self)
        self.clock_timer.timeout.connect(self.update) # Trigger repaint for clock every 1s
        self.clock_timer.start(1000)
        
        # Enforce topmost periodically to prevent fullscreen games from covering it
        self.topmost_timer = QTimer(self)
        self.topmost_timer.timeout.connect(self.enforce_topmost)
        self.topmost_timer.start(500)
        
        # Fit to screen
        self.update_geometry()
        
    def update_geometry(self):
        screen = QApplication.primaryScreen()
        if screen:
            self._current_screen_index = 0
            self.setGeometry(self._get_margin_geometry(screen.geometry()))
            
    def _get_margin_geometry(self, screen_geom):
        """Returns the screen geometry with top/bottom margins applied."""
        margin_top = int(self.config_manager.get("overlay_margin_top", 0))
        margin_bottom = int(self.config_manager.get("overlay_margin_bottom", 0))
        from PySide6.QtCore import QRect
        return QRect(
            screen_geom.x(),
            screen_geom.y() + margin_top,
            screen_geom.width(),
            screen_geom.height() - margin_top - margin_bottom
        )
            
    def set_screen_index(self, index):
        """Sets overlay geometry to the chosen screen index."""
        screens = QApplication.screens()
        if 0 <= index < len(screens):
            self._current_screen_index = index
            self.setGeometry(self._get_margin_geometry(screens[index].geometry()))
            self.update()
    def update_metrics(self):
        """Poll CPU and RAM stats from psutil in a lightweight manner."""
        if self.config_manager.get("telemetry_enabled", False) and self.isVisible():
            try:
                # cpu_percent(interval=None) is non-blocking and returns CPU usage since last call
                self.cpu_usage = int(psutil.cpu_percent())
                self.ram_usage = int(psutil.virtual_memory().percent)
            except Exception:
                pass

    def showEvent(self, event):
        super().showEvent(event)
        # Apply window styling so clicks pass through
        set_click_through(int(self.winId()))
        self.enforce_topmost()
        
    def enforce_topmost(self):
        """Enforces that the window is topmost, visible, and restored without stealing focus."""
        if self.config_manager.get("overlay_enabled", True):
            try:
                # 1. Force restore if minimized by OS
                if self.isMinimized():
                    self.showNormal()
                
                # 2. Force show if hidden by OS/Fullscreen transition
                if not self.isVisible():
                    self.show()
                    
                # 3. Synchronize geometry if screen resolution changed (common in fullscreen games)
                screens = QApplication.screens()
                screen_idx = getattr(self, '_current_screen_index', 0)
                screen = screens[screen_idx] if 0 <= screen_idx < len(screens) else QApplication.primaryScreen()
                if screen:
                    target_geom = self._get_margin_geometry(screen.geometry())
                    if self.geometry() != target_geom:
                        self.setGeometry(target_geom)

                        
                # 4. Handle cross-process window ownership to stay on top of fullscreen games
                hwnd = int(self.winId())
                fg_hwnd = ctypes.windll.user32.GetForegroundWindow()
                if fg_hwnd and fg_hwnd != hwnd:
                    pid = ctypes.c_ulong()
                    ctypes.windll.user32.GetWindowThreadProcessId(fg_hwnd, ctypes.byref(pid))
                    is_game = False
                    if pid.value > 0:
                        proc_name = ""
                        proc_path = ""
                        h_process = ctypes.windll.kernel32.OpenProcess(0x1000, False, pid.value) # PROCESS_QUERY_LIMITED_INFORMATION
                        if h_process:
                            try:
                                buf_size = 1024
                                buf = ctypes.create_unicode_buffer(buf_size)
                                size = ctypes.c_ulong(buf_size)
                                if ctypes.windll.kernel32.QueryFullProcessImageNameW(h_process, 0, buf, ctypes.byref(size)):
                                    proc_path = buf.value.lower()
                                    proc_name = os.path.basename(proc_path)
                            except Exception:
                                pass
                            finally:
                                ctypes.windll.kernel32.CloseHandle(h_process)
                        
                        # Fallback to psutil
                        if not proc_name:
                            try:
                                proc = psutil.Process(pid.value)
                                proc_name = proc.name().lower()
                                proc_path = proc.exe().lower()
                            except Exception:
                                pass
                        
                        game_list = [g.strip().lower() for g in self.config_manager.get("game_processes", []) if g.strip()]
                        if proc_name:
                            if proc_name in game_list:
                                is_game = True
                            elif proc_name not in ["steam.exe", "steamwebhelper.exe"]:
                                if "steamapps" in proc_path or "steamlibrary" in proc_path:
                                    is_game = True
                                    
                    if is_game:
                        # Set owner of our overlay window to the game window
                        current_owner = GetWindowLongPtr(hwnd, GWL_HWNDPARENT)
                        if current_owner != fg_hwnd:
                            SetWindowLongPtr(hwnd, GWL_HWNDPARENT, fg_hwnd)
                    else:
                        # Reset owner if foreground is not a game
                        current_owner = GetWindowLongPtr(hwnd, GWL_HWNDPARENT)
                        if current_owner != 0:
                            SetWindowLongPtr(hwnd, GWL_HWNDPARENT, 0)
                            
                # 5. Assert topmost window layer via SetWindowPos
                # HWND_TOPMOST = -1
                # SWP_NOMOVE = 0x0002, SWP_NOSIZE = 0x0001, SWP_NOACTIVATE = 0x0010, SWP_NOOWNERZORDER = 0x0200
                flags = 0x0002 | 0x0001 | 0x0010 | 0x0200
                ctypes.windll.user32.SetWindowPos(hwnd, -1, 0, 0, 0, 0, flags)
            except Exception as e:
                print(f"Error enforcing topmost: {e}")
        
    def paintEvent(self, event):
        # Do not paint if the overlay is disabled or configuration says so
        if not self.config_manager.get("overlay_enabled", True):
            return
            
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        
        w = self.width()
        h = self.height()
        cx = w / 2.0
        cy = h / 2.0
        
        # 1. Draw edge mask (vignette)
        self.draw_edge_mask(painter, w, h, cx, cy)
        
        # 2. Draw split lines
        self.draw_split_lines(painter, w, h, cx, cy)
        
        # 3. Draw edge crosshair (arrows pointing to center)
        self.draw_edge_crosshair(painter, w, h, cx, cy)
        
        # 4. Draw clock and system stats
        self.draw_telemetry(painter, w, h)
        
        # 5. Draw center crosshair
        self.draw_crosshair(painter, cx, cy)

    def draw_edge_crosshair(self, painter, w, h, cx, cy):
        if not self.config_manager.get("edge_crosshair_enabled", False):
            return
            
        style = self.config_manager.get("edge_crosshair_style", "arrow").lower()
        width = self.config_manager.get("edge_crosshair_width", 40)
        length = self.config_manager.get("edge_crosshair_length", 250)
        arrow_size = self.config_manager.get("edge_crosshair_arrow_size", 25)
        opacity = self.config_manager.get("edge_crosshair_opacity", 0.60)
        color_str = self.config_manager.get("edge_crosshair_color", "#FF5B55")
        
        color = QColor(color_str)
        color.setAlphaF(opacity)
        
        painter.setBrush(QBrush(color))
        painter.setPen(Qt.PenStyle.NoPen)
        
        if style == "arrow":
            # Top Arrow (pointing down)
            # Stem
            painter.drawRect(QRectF(cx - width / 2.0, 0, width, length - arrow_size))
            # Arrowhead
            top_arrowhead = QPolygonF()
            top_arrowhead.append(QPointF(cx - width / 2.0 - arrow_size, length - arrow_size))
            top_arrowhead.append(QPointF(cx + width / 2.0 + arrow_size, length - arrow_size))
            top_arrowhead.append(QPointF(cx, length))
            painter.drawPolygon(top_arrowhead)
            
            # Bottom Arrow (pointing up)
            # Stem
            painter.drawRect(QRectF(cx - width / 2.0, h - length + arrow_size, width, length - arrow_size))
            # Arrowhead
            bottom_arrowhead = QPolygonF()
            bottom_arrowhead.append(QPointF(cx - width / 2.0 - arrow_size, h - length + arrow_size))
            bottom_arrowhead.append(QPointF(cx + width / 2.0 + arrow_size, h - length + arrow_size))
            bottom_arrowhead.append(QPointF(cx, h - length))
            painter.drawPolygon(bottom_arrowhead)
            
            # Left Arrow (pointing right)
            # Stem
            painter.drawRect(QRectF(0, cy - width / 2.0, length - arrow_size, width))
            # Arrowhead
            left_arrowhead = QPolygonF()
            left_arrowhead.append(QPointF(length - arrow_size, cy - width / 2.0 - arrow_size))
            left_arrowhead.append(QPointF(length - arrow_size, cy + width / 2.0 + arrow_size))
            left_arrowhead.append(QPointF(length, cy))
            painter.drawPolygon(left_arrowhead)
            
            # Right Arrow (pointing left)
            # Stem
            painter.drawRect(QRectF(w - length + arrow_size, cy - width / 2.0, length - arrow_size, width))
            # Arrowhead
            right_arrowhead = QPolygonF()
            right_arrowhead.append(QPointF(w - length + arrow_size, cy - width / 2.0 - arrow_size))
            right_arrowhead.append(QPointF(w - length + arrow_size, cy + width / 2.0 + arrow_size))
            right_arrowhead.append(QPointF(w - length, cy))
            painter.drawPolygon(right_arrowhead)
            
        elif style == "bar":
            # Top Bar
            painter.drawRect(QRectF(cx - width / 2.0, 0, width, length))
            # Bottom Bar
            painter.drawRect(QRectF(cx - width / 2.0, h - length, width, length))
            # Left Bar
            painter.drawRect(QRectF(0, cy - width / 2.0, length, width))
            # Right Bar
            painter.drawRect(QRectF(w - length, cy - width / 2.0, length, width))
            
        elif style == "semicircle":
            # Draw semi-ellipses centered on the edges of the screen
            # Top
            painter.drawEllipse(QRectF(cx - width / 2.0, -length, width, length * 2))
            # Bottom
            painter.drawEllipse(QRectF(cx - width / 2.0, h - length, width, length * 2))
            # Left
            painter.drawEllipse(QRectF(-length, cy - width / 2.0, length * 2, width))
            # Right
            painter.drawEllipse(QRectF(w - length, cy - width / 2.0, length * 2, width))

    def draw_raw_shape(self, painter, shape, cx, cy, w, h, color):
        """Draws the raw geometric shape centered at (cx, cy)."""
        painter.setBrush(QBrush(color))
        painter.setPen(Qt.PenStyle.NoPen)
        
        if shape == "circle":
            r = w / 2.0
            painter.drawEllipse(QPointF(cx, cy), r, r)
        elif shape == "ellipse":
            painter.drawEllipse(QRectF(cx - w/2.0, cy - h/2.0, w, h))
        elif shape == "rectangle":
            painter.drawRect(QRectF(cx - w/2.0, cy - h/2.0, w, h))
        elif shape == "diamond":
            poly = QPolygonF()
            poly.append(QPointF(cx, cy - h/2.0))
            poly.append(QPointF(cx + w/2.0, cy))
            poly.append(QPointF(cx, cy + h/2.0))
            poly.append(QPointF(cx - w/2.0, cy))
            painter.drawPolygon(poly)

    def draw_edge_mask(self, painter, w, h, cx, cy):
        if not self.config_manager.get("mask_enabled", True):
            return
            
        shape = self.config_manager.get("mask_shape", "ellipse").lower()
        size_pct = self.config_manager.get("mask_size", 55)
        opacity = self.config_manager.get("mask_opacity", 0.70)
        feather = self.config_manager.get("mask_feather", 0.35)
        color_str = self.config_manager.get("mask_color", "#000000")
        
        # Base background color
        mask_color = QColor(color_str)
        mask_color.setAlphaF(opacity)
        
        # Fill the entire window first with the solid overlay color
        painter.fillRect(0, 0, w, h, mask_color)
        
        # Set composition mode to cut a hole in the filled region
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_DestinationOut)
        
        # Calculate transparent core dimensions
        target_w = w * (size_pct / 100.0)
        target_h = h * (size_pct / 100.0)
        
        if shape == "circle":
            target_h = target_w  # Circle must be uniform
            
        steps = 40
        if feather <= 0.01:
            # Hard cutout, no feathering
            self.draw_raw_shape(painter, shape, cx, cy, target_w, target_h, QColor(255, 255, 255, 255))
        else:
            # Multi-pass concentric overlay (smoothly clears destination from inside out)
            inner_fraction = 1.0 - feather
            core_w = target_w * inner_fraction
            core_h = target_h * inner_fraction
            
            # Solid inner core (fully transparent in final display)
            self.draw_raw_shape(painter, shape, cx, cy, core_w, core_h, QColor(255, 255, 255, 255))
            
            # Transition region (progressively clears less, creating a smooth gradient)
            for i in range(steps):
                t = i / float(steps)
                current_w = target_w - (target_w - core_w) * t
                current_h = target_h - (target_h - core_h) * t
                # Alpha increases as we move inward (closer core has higher subtraction value)
                alpha = int(255 * t)
                self.draw_raw_shape(painter, shape, cx, cy, current_w, current_h, QColor(255, 255, 255, alpha))
                
        # Reset composition mode to normal drawing
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceOver)

    def draw_split_lines(self, painter, w, h, cx, cy):
        if not self.config_manager.get("split_lines_enabled", False):
            return
            
        line_type = self.config_manager.get("split_lines_type", "vertical").lower()
        thickness = self.config_manager.get("split_lines_thickness", 1)
        opacity = self.config_manager.get("split_lines_opacity", 0.3)
        color_str = self.config_manager.get("split_lines_color", "#FFFFFF")
        
        pen_color = QColor(color_str)
        pen_color.setAlphaF(opacity)
        pen = QPen(pen_color, thickness, Qt.PenStyle.SolidLine)
        painter.setPen(pen)
        
        if line_type in ["vertical", "cross"]:
            painter.drawLine(cx, 0, cx, h)
        if line_type in ["horizontal", "cross"]:
            painter.drawLine(0, cy, w, cy)

    def draw_crosshair(self, painter, cx, cy):
        if not self.config_manager.get("crosshair_enabled", True):
            return
            
        shape = self.config_manager.get("crosshair_shape", "dot").lower()
        size = self.config_manager.get("crosshair_size", 12)
        thickness = self.config_manager.get("crosshair_thickness", 2)
        color_str = self.config_manager.get("crosshair_color", "#00FF00")
        opacity = self.config_manager.get("crosshair_opacity", 1.0)
        outline = self.config_manager.get("crosshair_outline", True)
        outline_color_str = self.config_manager.get("crosshair_outline_color", "#000000")
        
        main_color = QColor(color_str)
        main_color.setAlphaF(opacity)
        out_color = QColor(outline_color_str)
        out_color.setAlphaF(opacity)
        
        def draw_shape_helper(pen_c, brush_c, t_offset=0):
            pen = QPen(pen_c, thickness + t_offset, Qt.PenStyle.SolidLine)
            painter.setPen(pen)
            
            if brush_c:
                painter.setBrush(QBrush(brush_c))
            else:
                painter.setBrush(Qt.BrushStyle.NoBrush)
                
            if shape == "dot":
                r = size / 2.0
                painter.drawEllipse(QPointF(cx, cy), r, r)
            elif shape == "cross":
                gap = size / 4.0
                length = size / 2.0
                painter.drawLine(cx - gap - length, cy, cx - gap, cy)
                painter.drawLine(cx + gap, cy, cx + gap + length, cy)
                painter.drawLine(cx, cy - gap - length, cx, cy - gap)
                painter.drawLine(cx, cy + gap, cx, cy + gap + length)
            elif shape == "circle_dot":
                # Central tiny dot
                r_dot = max(1.5, thickness / 2.0)
                painter.setBrush(QBrush(pen_c))
                painter.drawEllipse(QPointF(cx, cy), r_dot, r_dot)
                # Outer ring
                painter.setBrush(Qt.BrushStyle.NoBrush)
                r_ring = size / 2.0
                painter.drawEllipse(QPointF(cx, cy), r_ring, r_ring)
            elif shape == "diamond":
                poly = QPolygonF()
                poly.append(QPointF(cx, cy - size/2.0))
                poly.append(QPointF(cx + size/2.0, cy))
                poly.append(QPointF(cx, cy + size/2.0))
                poly.append(QPointF(cx - size/2.0, cy))
                painter.drawPolygon(poly)
            elif shape == "chevron":
                # ^ chevron shape
                painter.drawLine(cx - size/2.0, cy + size/4.0, cx, cy - size/2.0)
                painter.drawLine(cx, cy - size/2.0, cx + size/2.0, cy + size/4.0)

        # Draw black backdrop contour first
        if outline:
            draw_shape_helper(out_color, out_color if shape in ["dot", "diamond"] else None, t_offset=2)
            
        # Draw high-contrast primary shape
        draw_shape_helper(main_color, main_color if shape in ["dot", "diamond"] else None, t_offset=0)

    def draw_telemetry(self, painter, w, h):
        clock_enabled = self.config_manager.get("clock_enabled", True)
        telemetry_enabled = self.config_manager.get("telemetry_enabled", False)
        
        if not (clock_enabled or telemetry_enabled):
            return
            
        pos = self.config_manager.get("clock_position", "top_right").lower()
        size = self.config_manager.get("clock_size", 14)
        opacity = self.config_manager.get("clock_opacity", 0.6)
        color_str = self.config_manager.get("clock_color", "#FFFFFF")
        
        font = QFont("Consolas", size)
        painter.setFont(font)
        
        text_color = QColor(color_str)
        text_color.setAlphaF(opacity)
        painter.setPen(text_color)
        
        lines = []
        if clock_enabled:
            current_time = QTime.currentTime().toString("HH:mm:ss")
            lines.append(current_time)
        if telemetry_enabled:
            stats = self.config_manager.tr("telemetry_stats", self.cpu_usage, self.ram_usage)
            lines.append(stats)
            
        if not lines:
            return
            
        fm = painter.fontMetrics()
        line_height = fm.height()
        margin = 25
        
        max_w = max(fm.horizontalAdvance(line) for line in lines)
        total_h = len(lines) * line_height
        
        # Calculate Y position
        if "top" in pos:
            y = margin + line_height
        else: # bottom
            y = h - total_h - margin + line_height
            
        # Calculate X position
        if "left" in pos:
            x = margin
        else: # right
            x = w - max_w - margin
            
        # Draw all text lines
        for i, line in enumerate(lines):
            line_y = y + (i * line_height)
            
            # Subtle drop shadow
            painter.save()
            shadow = QColor(0, 0, 0, int(opacity * 255 * 0.7))
            painter.setPen(shadow)
            painter.drawText(x + 1, line_y + 1, line)
            painter.restore()
            
            painter.drawText(x, line_y, line)

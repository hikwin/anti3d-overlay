# Anti3D-Overlay (防 3D 晕动症叠加引导工具) | [English Version](#anti3d-overlay-anti-3d-motion-sickness-helper)

Anti3D-Overlay 是一款专为 3D 游戏玩家设计的轻量级屏幕辅助工具。通过在游戏窗口上方叠加动态可定制的**边缘减速遮罩**、**多形态中心准星**、**分屏引导线**以及**角落参考信息**，帮助降低视觉光流刺激，建立强有力的中心参考锚点，从而有效缓解 3D 晕动症（游戏眩晕）。

> 📦 **快捷下载**：可以直接在 [GitHub Releases](https://github.com/hikwin/anti3d-overlay/releases) 页面直接下载已打包好的独立绿色免安装版运行包。

---

## 🌟 核心功能 | [English Version](#-core-features)

1. **边缘动态遮罩（Edge Mask）**：
   * 锁定游戏余光区域的高速运动，提供圆形、椭圆、矩形、菱形等多种遮罩形状。
   * 支持透明中心范围（默认 90% 大范围）、透明度、羽化渐变程度、以及遮罩颜色的自由调节。
   * 支持一键开启/关闭边缘遮罩。

2. **多样式中心准星（Crosshair Options）**：
   * 建立视觉中心锚点，提供圆点（Dot）、十字（Cross）、圆点十字（Circle Dot）、菱形（Diamond）以及 V 形折线（Chevron）五种高级样式。
   * 尺寸（支持 4-256px）、线条粗细（支持 1-30px）、颜色及透明度大范围精细微调。
   * 提供描边（Outline）开关及描边颜色自定义，确保在任何游戏背景下准星都清晰醒目。

3. **分屏引导线（Split Lines）**：
   * 提供垂直单线、水平单线、十字线三种分屏参考线样式，分割屏幕视觉区域，降低单次光流横扫的眼球负荷。
   * 粗细、透明度及线条颜色可自定义。

4. **边缘十字锚点（Edge Crosshairs）**：
   * 拥有带箭头的、直条的、或者是半圆款式的边缘十字标遮罩，有效形成强烈的中心视线汇聚感。
   * 标线宽度、标线长度、箭头大小、不透明度及十字标颜色可配置。

5. **角落参考信息叠加（Corner Telemetry & Clock）**：
   * 可选在屏幕四个角落（左上、右上、左下、右下）渲染小干扰时钟及系统负载（CPU / RAM 占用率）。
   * 字体大小、不透明度、文字颜色完全可调。

6. **全局快捷键控制（Global Hotkeys）**：
   * 支持全局系统快捷键（如 `Ctrl + Alt + O` 开启/暂停叠加层，`Ctrl + Alt + C` 隐藏/显示准星，`Ctrl + Alt + 向上/向下箭头` 微调遮罩透明度）。

7. **智能进程自动激活（Auto Trigger）**：
   * 玩家可自由添加游戏进程名称（如 `Cyberpunk2077.exe`）。
   * 开启自动检测后，当目标游戏切到前台时自动开启防晕叠加，游戏最小化或退出时自动暂停，实现零干扰无缝体验。
   * 优化对 Steam 全屏游戏的防丢失遮罩机制。

8. **预设管理系统（Preset Settings）**：
   * 支持将当前所有滑块、颜色和开关保存为自定义的“预设方案”，并在多套方案间一键应用或删除。

9. **中英文多语言即时切换（Dynamic Bilingual Switcher）**：
   * **系统语言自适应**：启动时自动识别 Windows 区域设置（中文系统自适应显示中文，其它语言默认显示英文）。
   * **一键免重启切换**：点击界面左下角（退出按钮旁）的语言文本按钮（`中文` / `English`），界面上所有选项卡、滑块单位、通知以及气泡弹窗文本将会即时无缝重载。

---

## 🛠️ 安装与依赖 | [English Version](#-installation-and-dependencies)

本软件使用 **Python 3** 和 **PySide6 (Qt for Python)** 编写。

### 1. 依赖库安装
在项目根目录下，使用 pip 安装运行依赖：
```bash
pip install -r requirements.txt
```

> ⚠️ **重要提示**：
> 由于本软件注册了全局系统快捷键以方便玩家在游戏内进行盲操，在 Windows 系统下可能需要以 **管理员权限** 运行终端才能使键盘钩子（`pynput` 库）正常拦截到全局按键。

---

## 🚀 运行与使用说明 | [English Version](#-usage-instructions)

### 启动软件
在管理员终端执行：
```bash
python main.py
```

### 使用指南
1. **主控制面板**：启动后展示 `780x560` 的双栏暗色科技风控制面板。
2. **多显示器适配**：在“辅助与状态”标签页中选择投射遮罩的具体显示器。
3. **关闭与隐藏**：点击控制面板窗口的“关闭”按钮会安全缩至系统右下角的**托盘图标**中运行。
4. **彻底退出**：
   * 方案 A：点击控制面板左下角的红色“退出整个软件”按钮。
   * 方案 B：在右下角托盘图标上右键，选择“退出软件”。

---
---

# Anti3D-Overlay (Anti-3D Motion Sickness Helper) | [中文版](#anti3d-overlay-防-3d-晕动症叠加引导工具-english-version)

Anti3D-Overlay is a lightweight screen overlay assistant designed for 3D gamers. By rendering a customizable **peripheral speed-reducing mask**, **multi-style central crosshairs**, **screen split guides**, and **corner reference stats**, it helps reduce optical flow stimulation, build a strong visual center of focus, and effectively alleviate 3D motion sickness (simulator sickness).

> 📦 **Quick Download**: You can directly download the pre-packaged standalone executable from [GitHub Releases](https://github.com/hikwin/anti3d-overlay/releases).

---

## 🌟 Core Features | [中文版](#-核心功能-english-version)

1. **Dynamic Peripheral Mask (Edge Mask)**:
   * Masks high-speed motion in peripheral vision. Provides multiple mask shapes: Circle, Ellipse, Rectangle, and Diamond.
   * Adjustable clear central area (default is 90% wide clear region), opacity, feathering gradients, and solid mask color.
   * Master checkbox to quickly enable or disable the edge mask.

2. **Multi-Style Central Crosshair**:
   * Creates a solid visual anchor at the center. Offers 5 premium styles: Dot, Cross, Circle Dot, Diamond, and Chevron.
   * High-precision slider adjustments for size (4-256px), thickness (1-30px), opacity, and color.
   * Optional outline styling with customizable outline color to guarantee readability under any gaming scene.

3. **Screen Split Guides (Split Lines)**:
   * Split reference lines (Vertical, Horizontal, Cross) to divide visual zones and lower eye-strain caused by high-speed panning.
   * Adjustable thickness, opacity, and line colors.

4. **Edge Crosshair Anchors**:
   * Features arrowed, straight, or semi-circular edge markers to guide visual focus toward the screen center.
   * Customizable line width, line length, arrow size, opacity, and color.

5. **Corner Telemetry & Clock Overlay**:
   * Renders a clock and hardware indicators (CPU / RAM utilization) in one of the screen corners (Top Right, Top Left, Bottom Right, Bottom Left).
   * Fully customizable text color, font size, and opacity.

6. **Global Shortcut Controls (Global Hotkeys)**:
   * Global system hotkeys (e.g. `Ctrl + Alt + O` to toggle overlay, `Ctrl + Alt + C` to toggle crosshair, `Ctrl + Alt + Up/Down Arrow` to adjust mask opacity).

7. **Smart Foreground Auto Trigger**:
   * Easily input game process executable filenames (e.g., `Cyberpunk2077.exe`).
   * When enabled, the overlay automatically turns on when the game window is in the foreground, and pauses when minimized or closed.
   * Fully optimized to prevent overlays from getting hidden under Steam fullscreen games.

8. **Preset Management (Presets)**:
   * Save all current sliders, colors, and switches into custom presets. Instantly load different presets or delete them.

9. **Bilingual Dynamic Switcher**:
   * **System Locale Auto-Detection**: Chinese is shown by default on Chinese systems, and English is loaded on all other locales.
   * **Dynamic Text Retranslation**: Click the language switcher text button (`中文` / `English`) at the bottom-left of the panel to instantly translate all tabs, labels, suffixes, messages, and tray menus without restarting.

---

## 🛠️ Installation and Dependencies | [中文版](#-安装与依赖-english-version)

This utility is built using **Python 3** and **PySide6 (Qt for Python)**.

### 1. Install Dependencies
Run the pip installer in your project directory:
```bash
pip install -r requirements.txt
```

> ⚠️ **Important Notice**:
> Because the application hooks global hotkeys to allow adjustments during gameplay, you may need to run your terminal or IDE with **Administrator privileges** on Windows for the key hooks (`pynput` library) to intercept keyboard inputs.

---

## 🚀 Usage Instructions | [中文版](#-运行与使用说明-english-version)

### Running the App
Execute in an Administrator console:
```bash
python main.py
```

### Quick Guide
1. **Control Panel**: Shows a double-column dark-mode dashboard sized `780x560`. A master overlay switch resides at the top.
2. **Multi-Monitor Display**: Pick the specific monitor in the "Auxiliary & Stats" tab to project the overlay.
3. **Minimize to Tray**: Closing the window hides the setting panel into the system tray.
4. **Exiting Application**:
   * Option A: Click the red "Exit App" (退出整个软件) button in the bottom-left.
   * Option B: Right-click the system tray icon and select "Exit" (退出软件).

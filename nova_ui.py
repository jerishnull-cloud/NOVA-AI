import math
import random

from PySide6.QtCore import (
    Qt,
    QTimer,
    Signal,
    QPointF,
    QRectF,
)

from PySide6.QtGui import (
    QColor,
    QPainter,
    QPen,
    QBrush,
    QLinearGradient,
    QFont,
)

from PySide6.QtWidgets import (
    QWidget,
    QFrame,
    QLabel,
    QPushButton,
    QLineEdit,
    QVBoxLayout,
    QHBoxLayout,
    QScrollArea,
)


# ============================================================
# NOVA COLORS
# ============================================================

BACKGROUND = QColor("#020812")

CYAN = QColor("#00E5FF")
BLUE = QColor("#1687FF")
LIGHT_BLUE = QColor("#54E8FF")

WHITE = QColor("#EAFBFF")

GREEN = QColor("#4DFFC7")

RED = QColor("#FF5577")

MUTED = QColor("#6E9DB5")


# ============================================================
# NEON PANEL
# ============================================================

class NeonPanel(QFrame):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setObjectName("NeonPanel")

        self.setStyleSheet("""
            QFrame#NeonPanel {
                background-color: rgba(2, 12, 28, 225);
                border: 1px solid #087EA5;
                border-radius: 14px;
            }
        """)


# ============================================================
# STARFIELD BACKGROUND
# ============================================================

class NovaBackground(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.stars = []

        for _ in range(320):

            self.stars.append({
                "x": random.random(),
                "y": random.random(),
                "size": random.uniform(0.5, 2.4),
                "speed": random.uniform(0.2, 1.3),
                "phase": random.uniform(
                    0,
                    math.pi * 2
                ),
            })

        self.time = 0

        self.motion_x = 0

        self.motion_y = 0

        self.timer = QTimer(self)

        self.timer.timeout.connect(
            self.animate
        )

        self.timer.start(16)

        self.setAttribute(
            Qt.WidgetAttribute.WA_TransparentForMouseEvents
        )

    # --------------------------------------------------------
    # ANIMATION
    # --------------------------------------------------------

    def animate(self):

        self.time += 0.035

        for star in self.stars:

            star["y"] += (
                0.00015 *
                star["speed"]
            )

            if star["y"] > 1:

                star["y"] = 0

                star["x"] = random.random()

        self.motion_x *= 0.94

        self.motion_y *= 0.94

        self.update()

    # --------------------------------------------------------
    # HAND MOTION
    # --------------------------------------------------------

    def set_motion(
        self,
        dx,
        dy
    ):

        self.motion_x += dx * 1.5

        self.motion_y += dy * 1.5

        self.update()

    # --------------------------------------------------------
    # DRAW
    # --------------------------------------------------------

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing
        )

        width = self.width()

        height = self.height()

        # ----------------------------------------------------
        # BACKGROUND
        # ----------------------------------------------------

        painter.fillRect(
            self.rect(),
            BACKGROUND
        )

        # ----------------------------------------------------
        # BLUE SPACE GLOW
        # ----------------------------------------------------

        gradient = QLinearGradient(
            width * 0.5,
            0,
            width * 0.5,
            height
        )

        gradient.setColorAt(
            0,
            QColor(
                0,
                50,
                110,
                50
            )
        )

        gradient.setColorAt(
            0.45,
            QColor(
                0,
                30,
                80,
                30
            )
        )

        gradient.setColorAt(
            1,
            QColor(
                0,
                0,
                0,
                0
            )
        )

        painter.fillRect(
            self.rect(),
            gradient
        )

        # ----------------------------------------------------
        # STARS
        # ----------------------------------------------------

        for star in self.stars:

            x = (
                star["x"] * width
                +
                self.motion_x *
                star["speed"]
            )

            y = (
                star["y"] * height
                +
                self.motion_y *
                star["speed"]
            )

            x %= width

            y %= height

            pulse = (
                math.sin(
                    self.time *
                    star["speed"]
                    +
                    star["phase"]
                )
                +
                1
            ) / 2

            alpha = int(
                65 +
                pulse * 170
            )

            painter.setPen(
                Qt.PenStyle.NoPen
            )

            painter.setBrush(
                QColor(
                    25,
                    210,
                    255,
                    alpha
                )
            )

            size = star["size"]

            painter.drawEllipse(
                QPointF(
                    x,
                    y
                ),
                size,
                size
            )

        painter.end()


# ============================================================
# NOVA CORE
# ============================================================

class NovaCore(QWidget):

    def __init__(
        self,
        parent=None
    ):

        super().__init__(
            parent
        )

        self.angle = 0

        self.timer = QTimer(
            self
        )

        self.timer.timeout.connect(
            self.animate
        )

        self.timer.start(16)

    # --------------------------------------------------------
    # ANIMATION
    # --------------------------------------------------------

    def animate(self):

        self.angle += 0.7

        if self.angle >= 360:

            self.angle = 0

        self.update()

    # --------------------------------------------------------
    # DRAW
    # --------------------------------------------------------

    def paintEvent(
        self,
        event
    ):

        painter = QPainter(
            self
        )

        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing
        )

        width = self.width()

        height = self.height()

        cx = width / 2

        cy = height / 2

        # ----------------------------------------------------
        # GLOW
        # ----------------------------------------------------

        glow_layers = [
            (110, 8),
            (95, 14),
            (80, 23),
        ]

        for radius, alpha in glow_layers:

            painter.setPen(
                Qt.PenStyle.NoPen
            )

            painter.setBrush(
                QColor(
                    0,
                    140,
                    255,
                    alpha
                )
            )

            painter.drawEllipse(
                QPointF(
                    cx,
                    cy
                ),
                radius,
                radius
            )

        # ----------------------------------------------------
        # ORBIT RINGS
        # ----------------------------------------------------

        painter.setBrush(
            Qt.BrushStyle.NoBrush
        )

        for index in range(4):

            painter.save()

            painter.translate(
                cx,
                cy
            )

            direction = (
                1
                if index % 2 == 0
                else -1
            )

            painter.rotate(
                self.angle *
                direction
            )

            ring_width = (
                135 +
                index * 20
            )

            ring_height = (
                48 +
                index * 13
            )

            painter.setPen(
                QPen(
                    QColor(
                        0,
                        220,
                        255,
                        120 -
                        index * 20
                    ),
                    1
                )
            )

            painter.drawEllipse(
                QRectF(
                    -ring_width / 2,
                    -ring_height / 2,
                    ring_width,
                    ring_height
                )
            )

            # Orbit particle

            orbit_angle = math.radians(
                self.angle *
                direction
            )

            particle_x = (
                math.cos(
                    orbit_angle
                )
                *
                ring_width /
                2
            )

            particle_y = (
                math.sin(
                    orbit_angle
                )
                *
                ring_height /
                2
            )

            painter.setPen(
                Qt.PenStyle.NoPen
            )

            painter.setBrush(
                LIGHT_BLUE
            )

            painter.drawEllipse(
                QPointF(
                    particle_x,
                    particle_y
                ),
                4,
                4
            )

            painter.restore()

        # ----------------------------------------------------
        # CENTRAL SPHERE
        # ----------------------------------------------------

        sphere_gradient = QLinearGradient(
            cx - 60,
            cy - 65,
            cx + 60,
            cy + 65
        )

        sphere_gradient.setColorAt(
            0,
            QColor(
                180,
                255,
                255
            )
        )

        sphere_gradient.setColorAt(
            0.25,
            QColor(
                50,
                210,
                255
            )
        )

        sphere_gradient.setColorAt(
            0.6,
            QColor(
                10,
                90,
                255
            )
        )

        sphere_gradient.setColorAt(
            1,
            QColor(
                3,
                20,
                65
            )
        )

        painter.setBrush(
            sphere_gradient
        )

        painter.setPen(
            QPen(
                CYAN,
                2
            )
        )

        painter.drawEllipse(
            QPointF(
                cx,
                cy
            ),
            58,
            58
        )

        # ----------------------------------------------------
        # NOVA TEXT
        # ----------------------------------------------------

        painter.setPen(
            WHITE
        )

        painter.setFont(
            QFont(
                "Segoe UI",
                23,
                QFont.Weight.Bold
            )
        )

        text = "NOVA"

        metrics = painter.fontMetrics()

        text_width = metrics.horizontalAdvance(
            text
        )

        painter.drawText(
            int(
                cx -
                text_width / 2
            ),
            int(
                cy + 8
            ),
            text
        )

        painter.end()


# ============================================================
# MESSAGE WIDGET
# ============================================================

class MessageWidget(QFrame):

    def __init__(
        self,
        sender,
        message,
        parent=None
    ):

        super().__init__(
            parent
        )

        self.setStyleSheet("""
            QFrame {
                background-color: rgba(3, 25, 48, 220);
                border: 1px solid rgba(0, 190, 255, 110);
                border-radius: 12px;
            }
        """)

        layout = QVBoxLayout(
            self
        )

        layout.setContentsMargins(
            15,
            10,
            15,
            10
        )

        layout.setSpacing(
            5
        )

        # ----------------------------------------------------
        # SENDER
        # ----------------------------------------------------

        sender_label = QLabel(
            sender.upper()
        )

        sender_label.setStyleSheet("""
            color: #00E5FF;
            font-size: 11px;
            font-weight: bold;
            background: transparent;
            border: none;
            letter-spacing: 2px;
        """)

        # ----------------------------------------------------
        # MESSAGE
        # ----------------------------------------------------

        message_label = QLabel(
            str(message)
        )

        message_label.setWordWrap(
            True
        )

        message_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        message_label.setStyleSheet("""
            color: #EAFBFF;
            font-size: 14px;
            background: transparent;
            border: none;
        """)

        layout.addWidget(
            sender_label
        )

        layout.addWidget(
            message_label
        )


# ============================================================
# NOVA MAIN UI
# ============================================================

class NovaUI(QWidget):

    # ========================================================
    # SIGNALS
    # ========================================================

    command_signal = Signal(str)

    send_signal = Signal(str)

    voice_signal = Signal()

    web_search_signal = Signal()

    # Compatibility alias expected by main.py
    search_signal = Signal()

    screenshot_signal = Signal()

    power_signal = Signal(bool)

    motion_signal = Signal(bool)

    # Hand movement signal
    # dx = left/right movement
    # dy = up/down movement
    hand_movement = Signal(float, float)

    # ========================================================
    # INIT
    # ========================================================

    def __init__(self):

        super().__init__()

        self.nova_enabled = True

        self.motion_enabled = True

        self.setWindowTitle(
            "NOVA AI"
        )

        self.setMinimumSize(
            1100,
            700
        )

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
        )

        # ====================================================
        # BACKGROUND
        # ====================================================

        self.background = NovaBackground(
            self
        )

        self.background.setGeometry(
            self.rect()
        )

        # ====================================================
        # ROOT
        # ====================================================

        self.root_layout = QVBoxLayout(
            self
        )

        self.root_layout.setContentsMargins(
            18,
            16,
            18,
            14
        )

        self.root_layout.setSpacing(
            12
        )

        # ====================================================
        # HEADER
        # ====================================================

        header = self.create_header()

        self.root_layout.addWidget(
            header,
            0
        )

        # ====================================================
        # MAIN CONTENT
        # ====================================================

        main_layout = QHBoxLayout()

        main_layout.setSpacing(
            14
        )

        # ====================================================
        # LEFT
        # ====================================================

        left_panel = self.create_left_panel()

        main_layout.addWidget(
            left_panel,
            0
        )

        # ====================================================
        # CENTER
        # ====================================================

        center_layout = QVBoxLayout()

        center_layout.setSpacing(
            10
        )

        self.core = NovaCore()

        self.core.setMinimumHeight(
            170
        )

        self.core.setMaximumHeight(
            215
        )

        center_layout.addWidget(
            self.core,
            0
        )

        self.chat_panel = self.create_chat_panel()

        center_layout.addWidget(
            self.chat_panel,
            1
        )

        main_layout.addLayout(
            center_layout,
            1
        )

        # ====================================================
        # RIGHT
        # ====================================================

        right_panel = self.create_right_panel()

        main_layout.addWidget(
            right_panel,
            0
        )

        self.root_layout.addLayout(
            main_layout,
            1
        )

        # ====================================================
        # BOTTOM
        # ====================================================

        bottom = self.create_bottom()

        self.root_layout.addWidget(
            bottom,
            0
        )

        # ====================================================
        # COMPATIBILITY WIRING
        # (keeps nova_ui.py aligned with main.py's expected API)
        # ====================================================

        # main.py connects hand_thread.movement -> self.hand_movement,
        # so wire that signal to the starfield motion handler here.
        self.hand_movement.connect(
            self.update_hand_motion
        )

        # main.py connects self.ui.search_signal -> its web_search()
        # handler. Forward the existing web_search_signal into it.
        self.web_search_signal.connect(
            self.search_signal.emit
        )

        self.background.lower()

    # ========================================================
    # HEADER
    # ========================================================

    def create_header(self):

        panel = NeonPanel()

        panel.setMinimumHeight(
            90
        )

        layout = QHBoxLayout(
            panel
        )

        layout.setContentsMargins(
            20,
            10,
            16,
            10
        )

        # ----------------------------------------------------
        # LOGO
        # ----------------------------------------------------

        logo_layout = QVBoxLayout()

        logo = QLabel(
            "NOVA"
        )

        logo.setStyleSheet("""
            color: #F0FFFF;
            font-size: 40px;
            font-weight: bold;
            letter-spacing: 8px;
        """)

        subtitle = QLabel(
            "NEURAL OPERATING VIRTUAL ASSISTANT"
        )

        subtitle.setStyleSheet("""
            color: #35DFFF;
            font-size: 10px;
            letter-spacing: 2px;
        """)

        logo_layout.addWidget(
            logo
        )

        logo_layout.addWidget(
            subtitle
        )

        layout.addLayout(
            logo_layout
        )

        layout.addStretch()

        # ----------------------------------------------------
        # INFO
        # ----------------------------------------------------

        info = QLabel(
            "YOUR VOICE\n"
            "YOUR COMMAND\n"
            "MY MISSION"
        )

        info.setStyleSheet("""
            color: #45DFFF;
            font-size: 11px;
            background: transparent;
            border: none;
        """)

        layout.addWidget(
            info
        )

        layout.addStretch()

        # ----------------------------------------------------
        # ONLINE
        # ----------------------------------------------------

        self.online_label = QLabel(
            "●  ONLINE"
        )

        self.online_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.online_label.setMinimumWidth(
            135
        )

        self.online_label.setStyleSheet("""
            QLabel {
                color: #50FFC7;
                font-size: 14px;
                font-weight: bold;
                background: rgba(0, 80, 70, 70);
                border: 1px solid #0786A5;
                border-radius: 10px;
                padding: 12px;
            }
        """)

        layout.addWidget(
            self.online_label
        )

        return panel

    # ========================================================
    # LEFT PANEL
    # ========================================================

    def create_left_panel(self):

        panel = NeonPanel()

        panel.setMinimumWidth(
            175
        )

        panel.setMaximumWidth(
            215
        )

        layout = QVBoxLayout(
            panel
        )

        layout.setContentsMargins(
            12,
            16,
            12,
            16
        )

        layout.setSpacing(
            6
        )

        title = QLabel(
            "NAVIGATION"
        )

        title.setStyleSheet("""
            color: #00E5FF;
            font-size: 10px;
            font-weight: bold;
            letter-spacing: 2px;
        """)

        layout.addWidget(
            title
        )

        # ----------------------------------------------------
        # NAV BUTTONS
        # ----------------------------------------------------

        navigation = [
            ("⌂", "HOME"),
            ("▣", "CHAT"),
            ("◉", "SYSTEM"),
            ("☷", "SETTINGS"),
            ("ⓘ", "ABOUT"),
        ]

        for icon, text in navigation:

            button = QPushButton(
                f"{icon}    {text}"
            )

            button.setMinimumHeight(
                46
            )

            button.setCursor(
                Qt.CursorShape.PointingHandCursor
            )

            button.setStyleSheet("""
                QPushButton {
                    text-align: left;
                    color: #B7EFFF;
                    background: transparent;
                    border: 1px solid transparent;
                    border-radius: 8px;
                    padding-left: 12px;
                    font-size: 13px;
                    font-weight: bold;
                }

                QPushButton:hover {
                    color: white;
                    background: rgba(0, 150, 220, 60);
                    border: 1px solid #00BFEA;
                }
            """)

            layout.addWidget(
                button
            )

        layout.addStretch()

        # ----------------------------------------------------
        # MISSION
        # ----------------------------------------------------

        mission = QLabel(
            "MY MISSION\n\n"
            "Assist.\n"
            "Protect.\n"
            "Automate."
        )

        mission.setWordWrap(
            True
        )

        mission.setStyleSheet("""
            color: #67A5BE;
            font-size: 11px;
            padding: 12px;
            background: rgba(0, 20, 40, 100);
            border: 1px solid #075579;
            border-radius: 10px;
        """)

        layout.addWidget(
            mission
        )

        return panel

    # ========================================================
    # CHAT PANEL
    # ========================================================

    def create_chat_panel(self):

        panel = NeonPanel()

        layout = QVBoxLayout(
            panel
        )

        layout.setContentsMargins(
            16,
            12,
            16,
            14
        )

        layout.setSpacing(
            9
        )

        # ----------------------------------------------------
        # STATUS
        # ----------------------------------------------------

        self.status_label = QLabel(
            "NOVA // ONLINE"
        )

        self.status_label.setStyleSheet("""
            color: #00E5FF;
            font-size: 12px;
            font-weight: bold;
            letter-spacing: 3px;
        """)

        layout.addWidget(
            self.status_label
        )

        # Compatibility alias: main.py sets text directly via
        # self.ui.chat_title.setText(...)
        self.chat_title = self.status_label

        # ----------------------------------------------------
        # NOTICE LABEL (compatibility)
        # main.py sets text directly via
        # self.ui.chat_label.setText(...) for quick notices
        # such as voice errors or "didn't catch that" messages.
        # ----------------------------------------------------

        self.chat_label = QLabel(
            ""
        )

        self.chat_label.setWordWrap(
            True
        )

        self.chat_label.setStyleSheet("""
            color: #7FE3FF;
            font-size: 11px;
            font-style: italic;
            letter-spacing: 1px;
        """)

        layout.addWidget(
            self.chat_label
        )

        # ----------------------------------------------------
        # SCROLL AREA
        # ----------------------------------------------------

        self.scroll = QScrollArea()

        self.scroll.setWidgetResizable(
            True
        )

        self.scroll.setFrameShape(
            QFrame.Shape.NoFrame
        )

        self.scroll.setStyleSheet("""
            QScrollArea {
                background: transparent;
                border: none;
            }

            QScrollBar:vertical {
                width: 5px;
                background: transparent;
            }

            QScrollBar::handle:vertical {
                background: #087EA5;
                border-radius: 3px;
            }
        """)

        self.messages_widget = QWidget()

        self.messages_layout = QVBoxLayout(
            self.messages_widget
        )

        self.messages_layout.setContentsMargins(
            2,
            2,
            8,
            2
        )

        self.messages_layout.setSpacing(
            9
        )

        self.messages_layout.addStretch()

        self.scroll.setWidget(
            self.messages_widget
        )

        layout.addWidget(
            self.scroll,
            1
        )

        # ----------------------------------------------------
        # INPUT
        # ----------------------------------------------------

        input_layout = QHBoxLayout()

        input_layout.setSpacing(
            8
        )

        self.input = QLineEdit()

        # Compatibility alias: main.py reads/writes
        # self.ui.input_box directly (setText, setFocus, etc.)
        self.input_box = self.input

        self.input.setPlaceholderText(
            "Type your message..."
        )

        self.input.setMinimumHeight(
            50
        )

        self.input.returnPressed.connect(
            self.send_text
        )

        self.input.setStyleSheet("""
            QLineEdit {
                color: #EAFBFF;
                background: rgba(3, 25, 50, 235);
                border: 1px solid #078DB8;
                border-radius: 10px;
                padding-left: 15px;
                font-size: 14px;
            }

            QLineEdit:focus {
                border: 1px solid #00E5FF;
            }
        """)

        input_layout.addWidget(
            self.input,
            1
        )

        # ----------------------------------------------------
        # SEND
        # ----------------------------------------------------

        send_button = QPushButton(
            "➤"
        )

        send_button.setFixedSize(
            52,
            50
        )

        send_button.clicked.connect(
            self.send_text
        )

        send_button.setStyleSheet("""
            QPushButton {
                color: white;
                background: #078FC2;
                border: 1px solid #00E5FF;
                border-radius: 25px;
                font-size: 21px;
                font-weight: bold;
            }

            QPushButton:hover {
                background: #00BDE8;
            }
        """)

        input_layout.addWidget(
            send_button
        )

        layout.addLayout(
            input_layout
        )

        return panel

    # ========================================================
    # RIGHT PANEL
    # ========================================================

    def create_right_panel(self):

        panel = NeonPanel()

        panel.setMinimumWidth(
            245
        )

        panel.setMaximumWidth(
            295
        )

        layout = QVBoxLayout(
            panel
        )

        layout.setContentsMargins(
            15,
            15,
            15,
            15
        )

        layout.setSpacing(
            12
        )

        # ----------------------------------------------------
        # TITLE
        # ----------------------------------------------------

        title = QLabel(
            "MOTION CONTROL"
        )

        title.setStyleSheet("""
            color: #00E5FF;
            font-size: 13px;
            font-weight: bold;
            letter-spacing: 2px;
        """)

        layout.addWidget(
            title
        )

        # ----------------------------------------------------
        # MOTION BUTTON
        # ----------------------------------------------------

        self.motion_button = QPushButton(
            "●  MOTION ON"
        )

        self.motion_button.setCheckable(
            True
        )

        self.motion_button.setChecked(
            True
        )

        self.motion_button.setMinimumHeight(
            45
        )

        self.motion_button.clicked.connect(
            self.motion_clicked
        )

        self.motion_button.setStyleSheet("""
            QPushButton {
                color: #52FFC9;
                background: rgba(0, 100, 90, 80);
                border: 1px solid #00BFA5;
                border-radius: 10px;
                font-weight: bold;
            }

            QPushButton:checked {
                color: #06151C;
                background: #4EFFC5;
            }
        """)

        layout.addWidget(
            self.motion_button
        )

        # ----------------------------------------------------
        # DESCRIPTION
        # ----------------------------------------------------

        description = QLabel(
            "Move your hand to control the stars.\n\n"
            "← Left / Right →\n"
            "↑ Up / Down ↓"
        )

        description.setWordWrap(
            True
        )

        description.setStyleSheet("""
            color: #81A8BD;
            font-size: 12px;
            padding: 13px;
            border: 1px solid #075579;
            border-radius: 10px;
            background: rgba(2, 15, 30, 160);
        """)

        layout.addWidget(
            description
        )

        # ----------------------------------------------------
        # WAVEFORM
        # ----------------------------------------------------

        self.waveform = QLabel(
            "▁▂▄▆█▆▄▂▁▃▅▇▅▃▁▂▄▆▄▂▁"
        )

        self.waveform.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.waveform.setStyleSheet("""
            color: #00E5FF;
            font-size: 17px;
            padding: 10px;
        """)

        layout.addWidget(
            self.waveform
        )

        # ----------------------------------------------------
        # CAMERA
        # ----------------------------------------------------

        self.camera_label = QLabel(
            "● CAMERA READY"
        )

        self.camera_label.setStyleSheet("""
            color: #51FFC9;
            font-size: 11px;
            font-weight: bold;
            padding: 11px;
            border-top: 1px solid #075579;
        """)

        layout.addWidget(
            self.camera_label
        )

        layout.addStretch()

        # ----------------------------------------------------
        # HAND TRACKING
        # ----------------------------------------------------

        self.hand_label = QLabel(
            "HAND TRACKING\n\n"
            "● ACTIVE"
        )

        self.hand_label.setStyleSheet("""
            color: #51FFC9;
            font-size: 12px;
            font-weight: bold;
            padding: 13px;
            border: 1px solid #087B9E;
            border-radius: 10px;
            background: rgba(0, 70, 70, 50);
        """)

        layout.addWidget(
            self.hand_label
        )

        return panel

    # ========================================================
    # BOTTOM BAR
    # ========================================================

    def create_bottom(self):

        frame = QWidget()

        layout = QHBoxLayout(
            frame
        )

        layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        layout.setSpacing(
            8
        )

        # ----------------------------------------------------
        # HAND STATUS
        # ----------------------------------------------------

        self.hand_status = QLabel(
            "●  HAND TRACKING  ACTIVE"
        )

        self.hand_status.setStyleSheet("""
            color: #50FFC7;
            font-size: 10px;
            font-weight: bold;
            letter-spacing: 1px;
        """)

        layout.addWidget(
            self.hand_status
        )

        layout.addStretch(
            1
        )

        # ----------------------------------------------------
        # NOVA STATUS
        # ----------------------------------------------------

        self.bottom_status = QLabel(
            "NOVA // ONLINE"
        )

        self.bottom_status.setStyleSheet("""
            color: #00E5FF;
            font-size: 13px;
            font-weight: bold;
            letter-spacing: 3px;
        """)

        layout.addWidget(
            self.bottom_status
        )

        layout.addStretch(
            1
        )

        # ----------------------------------------------------
        # VOICE
        # ----------------------------------------------------

        voice_button = self.make_bottom_button(
            "🎙 VOICE"
        )

        voice_button.clicked.connect(
            self.voice_signal.emit
        )

        layout.addWidget(
            voice_button
        )

        # ----------------------------------------------------
        # WEB
        # ----------------------------------------------------

        web_button = self.make_bottom_button(
            "◎ WEB SEARCH"
        )

        web_button.clicked.connect(
            self.web_search_signal.emit
        )

        layout.addWidget(
            web_button
        )

        # ----------------------------------------------------
        # SCREENSHOT
        # ----------------------------------------------------

        screenshot_button = self.make_bottom_button(
            "▣ SCREENSHOT"
        )

        screenshot_button.clicked.connect(
            self.screenshot_signal.emit
        )

        layout.addWidget(
            screenshot_button
        )

        # ----------------------------------------------------
        # POWER
        # ----------------------------------------------------

        self.power_button = QPushButton(
            "● ON"
        )

        self.power_button.setCheckable(
            True
        )

        self.power_button.setChecked(
            True
        )

        self.power_button.setMinimumSize(
            80,
            40
        )

        self.power_button.clicked.connect(
            self.power_clicked
        )

        self.power_button.setStyleSheet("""
            QPushButton {
                color: #06151C;
                background: #4EFFC5;
                border: 1px solid #00E5FF;
                border-radius: 9px;
                font-weight: bold;
            }

            QPushButton:!checked {
                color: #FF6680;
                background: rgba(100,20,40,150);
                border: 1px solid #FF5577;
            }
        """)

        layout.addWidget(
            self.power_button
        )

        return frame

    # ========================================================
    # BOTTOM BUTTON
    # ========================================================

    def make_bottom_button(
        self,
        text
    ):

        button = QPushButton(
            text
        )

        button.setMinimumSize(
            112,
            40
        )

        button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        button.setStyleSheet("""
            QPushButton {
                color: #C7F8FF;
                background: rgba(2,20,38,230);
                border: 1px solid #087B9E;
                border-radius: 9px;
                font-size: 9px;
                font-weight: bold;
            }

            QPushButton:hover {
                color: white;
                background: rgba(0,140,200,100);
                border: 1px solid #00E5FF;
            }
        """)

        return button

    # ========================================================
    # SEND TEXT
    # ========================================================

    def send_text(self):

        text = self.input.text().strip()

        if not text:
            return

        if not self.nova_enabled:
            return

        self.input.clear()

        self.add_message(
            "YOU",
            text
        )

        # IMPORTANT
        # main.py expects this
        self.command_signal.emit(
            text
        )

        # Older code compatibility
        self.send_signal.emit(
            text
        )

    # ========================================================
    # ADD MESSAGE
    # ========================================================

    def add_message(
        self,
        sender,
        message
    ):

        # Remove final stretch temporarily
        if self.messages_layout.count() > 0:

            last_item = self.messages_layout.itemAt(
                self.messages_layout.count() - 1
            )

            if (
                last_item is not None
                and last_item.spacerItem()
            ):

                self.messages_layout.takeAt(
                    self.messages_layout.count() - 1
                )

        widget = MessageWidget(
            sender,
            message
        )

        self.messages_layout.addWidget(
            widget
        )

        self.messages_layout.addStretch()

        QTimer.singleShot(
            50,
            self.scroll_to_bottom
        )

    # ========================================================
    # NOVA MESSAGE
    # ========================================================

    def add_nova_message(
        self,
        message
    ):

        self.add_message(
            "NOVA",
            message
        )

    # ========================================================
    # IMPORTANT COMPATIBILITY METHOD
    #
    # Your main.py uses:
    #
    # self.ui.show_nova_message(...)
    #
    # ========================================================

    def show_nova_message(
        self,
        message
    ):

        self.add_nova_message(
            message
        )

    # ========================================================
    # USER MESSAGE COMPATIBILITY
    # ========================================================

    def show_user_message(
        self,
        message
    ):

        self.add_message(
            "YOU",
            message
        )

    # ========================================================
    # CLEAR CHAT
    # ========================================================

    def clear_chat(self):

        while self.messages_layout.count():

            item = self.messages_layout.takeAt(
                0
            )

            widget = item.widget()

            if widget is not None:

                widget.deleteLater()

        self.messages_layout.addStretch()

    # ========================================================
    # SCROLL
    # ========================================================

    def scroll_to_bottom(self):

        scrollbar = (
            self.scroll.verticalScrollBar()
        )

        scrollbar.setValue(
            scrollbar.maximum()
        )

    # ========================================================
    # STATUS
    # ========================================================

    def set_status(
        self,
        text
    ):

        text = str(
            text
        ).upper()

        self.status_label.setText(
            f"NOVA // {text}"
        )

        self.bottom_status.setText(
            f"NOVA // {text}"
        )

    # --------------------------------------------------------
    # Compatibility
    # --------------------------------------------------------

    def update_status(
        self,
        text
    ):

        self.set_status(
            text
        )

    # ========================================================
    # LISTENING
    # ========================================================

    def set_listening(
        self,
        active=True
    ):

        if active:

            self.set_status(
                "LISTENING"
            )

            self.waveform.setText(
                "▁▂▄▆█▇▅▃▅▇█▆▄▂▁"
            )

        else:

            self.set_status(
                "ONLINE"
            )

            self.waveform.setText(
                "▁▂▄▆█▆▄▂▁▃▅▇▅▃▁"
            )

    # ========================================================
    # PROCESSING
    # ========================================================

    def set_processing(
        self,
        active=True
    ):

        if active:

            self.set_status(
                "PROCESSING"
            )

        else:

            self.set_status(
                "ONLINE"
            )

    # ========================================================
    # HAND TRACKING STATUS
    # ========================================================

    def set_hand_status(
        self,
        active=True
    ):

        if active:

            self.hand_status.setText(
                "●  HAND TRACKING  ACTIVE"
            )

            self.hand_label.setText(
                "HAND TRACKING\n\n"
                "● ACTIVE"
            )

        else:

            self.hand_status.setText(
                "●  HAND TRACKING  OFF"
            )

            self.hand_label.setText(
                "HAND TRACKING\n\n"
                "● OFFLINE"
            )

    # ========================================================
    # CAMERA STATUS
    # ========================================================

    def set_camera_status(
        self,
        text
    ):

        self.camera_label.setText(
            f"● {str(text).upper()}"
        )

    # ========================================================
    # MOTION BUTTON
    # ========================================================

    def motion_clicked(self):

        self.motion_enabled = (
            self.motion_button.isChecked()
        )

        if self.motion_enabled:

            self.motion_button.setText(
                "●  MOTION ON"
            )

            self.set_hand_status(
                True
            )

        else:

            self.motion_button.setText(
                "○  MOTION OFF"
            )

            self.set_hand_status(
                False
            )

        self.motion_signal.emit(
            self.motion_enabled
        )

    # ========================================================
    # POWER BUTTON
    # ========================================================

    def power_clicked(self):

        self.nova_enabled = (
            self.power_button.isChecked()
        )

        if self.nova_enabled:

            self.power_button.setText(
                "● ON"
            )

            self.online_label.setText(
                "●  ONLINE"
            )

            self.set_status(
                "ONLINE"
            )

        else:

            self.power_button.setText(
                "○ OFF"
            )

            self.online_label.setText(
                "●  OFFLINE"
            )

            self.set_status(
                "OFFLINE"
            )

        self.power_signal.emit(
            self.nova_enabled
        )

    # ========================================================
    # HAND MOVEMENT
    # ========================================================

    def update_hand_motion(
        self,
        dx,
        dy
    ):

        if not self.motion_enabled:

            return

        self.background.set_motion(
            dx,
            dy
        )

    # ========================================================
    # COMPATIBILITY
    # ========================================================

    def update_motion(
        self,
        dx,
        dy
    ):

        self.update_hand_motion(
            dx,
            dy
        )

    # ========================================================
    # CAMERA ERROR
    # ========================================================

    def show_camera_error(
        self,
        message
    ):

        self.set_camera_status(
            f"CAMERA ERROR: {message}"
        )

        self.set_hand_status(
            False
        )

    # ========================================================
    # FULLSCREEN
    # ========================================================

    def show_fullscreen(self):

        self.showFullScreen()

    # ========================================================
    # WINDOW RESIZE
    # ========================================================

    def resizeEvent(
        self,
        event
    ):

        super().resizeEvent(
            event
        )

        if hasattr(
            self,
            "background"
        ):

            self.background.setGeometry(
                self.rect()
            )

    # ========================================================
    # ESCAPE
    # ========================================================

    def keyPressEvent(
        self,
        event
    ):

        if (
            event.key()
            ==
            Qt.Key.Key_Escape
        ):

            self.showNormal()

            return

        super().keyPressEvent(
            event
        )
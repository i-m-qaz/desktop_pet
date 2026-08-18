import sys
from pathlib import Path

from PyQt5.QtCore import Qt, QTimer, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QMovie, QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from pynput import keyboard


RESOURCE_DIR = Path(__file__).resolve().parent / "resources"
ASSET_PATHS = {
    "keyboard": RESOURCE_DIR / "keyboard.png",
    "standby": RESOURCE_DIR / "standby.gif",
    "left": RESOURCE_DIR / "left.gif",
    "right": RESOURCE_DIR / "right.gif",
    "blank": RESOURCE_DIR / "blank.gif",
    "del": RESOURCE_DIR / "del.gif",
}

LEFT_KEYS = "qazwsxedcrfvt"
RIGHT_KEYS = "ygbuhnijmoklp"
EXIT_KEYS = {"5", "6", "7"}

KEY_ACTIONS = {key: "left" for key in LEFT_KEYS}
KEY_ACTIONS.update({key: "right" for key in RIGHT_KEYS})
KEY_ACTIONS[" "] = "blank"
KEY_ACTIONS["backspace"] = "del"

# 坐标是相对于窗口宽高的比例，便于以后替换不同尺寸的键盘底图。
KEY_POSITIONS = {
    "q": (0.27, 0.36), "w": (0.35, 0.36), "e": (0.42, 0.36),
    "r": (0.49, 0.36), "t": (0.56, 0.36),
    "a": (0.28, 0.44), "s": (0.35, 0.44), "d": (0.43, 0.44),
    "f": (0.50, 0.44),
    "z": (0.38, 0.51), "x": (0.45, 0.51), "c": (0.53, 0.51),
    "v": (0.61, 0.51),
    "y": (0.45, 0.36), "u": (0.52, 0.36), "i": (0.59, 0.36),
    "o": (0.67, 0.36), "p": (0.75, 0.36),
    "g": (0.38, 0.44), "h": (0.46, 0.44), "j": (0.53, 0.44),
    "k": (0.61, 0.44), "l": (0.69, 0.44),
    "b": (0.48, 0.51), "n": (0.56, 0.51), "m": (0.64, 0.51),
}
BLANK_POSITION = (0.45, 0.60)
ANIMATION_DURATION_MS = 450


class DeskPet(QWidget):
    # pynput 在后台线程工作；信号会把操作安全地交给 Qt 主线程。
    key_pressed = pyqtSignal(str)
    exit_requested = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setWindowFlags(
            Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)

        self._init_background()
        self._init_animations()

        self.pressed_keys = set()
        self.key_listener = None

        self.key_pressed.connect(self._handle_key_press)
        self.exit_requested.connect(self._quit_application)
        QApplication.instance().aboutToQuit.connect(self._stop_key_listener)

        self._show_standby()
        self._start_global_key_listener()
        print("桌宠启动成功！按下字母、空格或 Backspace 触发动画，5+6+7 退出")

    def _init_background(self):
        pixmap = QPixmap(str(ASSET_PATHS["keyboard"]))
        if pixmap.isNull():
            raise FileNotFoundError(f"无法加载键盘底图：{ASSET_PATHS['keyboard']}")

        self.resize(pixmap.size())
        self.bg_label = QLabel(self)
        self.bg_label.setPixmap(pixmap)
        self.bg_label.setGeometry(0, 0, pixmap.width(), pixmap.height())

    def _init_animations(self):
        self.movies = {
            name: QMovie(str(path))
            for name, path in ASSET_PATHS.items()
            if name != "keyboard"
        }
        invalid_assets = [
            str(ASSET_PATHS[name])
            for name, movie in self.movies.items()
            if not movie.isValid()
        ]
        if invalid_assets:
            raise FileNotFoundError("无法加载动画素材：" + ", ".join(invalid_assets))

        # 所有动画共用一个标签，切换时只替换它所播放的 QMovie。
        self.pet_label = QLabel(self)
        self.pet_label.setAttribute(Qt.WA_TransparentForMouseEvents)

        self.animation_timer = QTimer(self)
        self.animation_timer.setSingleShot(True)
        self.animation_timer.timeout.connect(self._show_standby)

        self.current_movie = None

    def _start_global_key_listener(self):
        def on_press(key):
            key_char = self._get_key_char(key)
            if key_char is None:
                return

            self.pressed_keys.add(key_char)
            if EXIT_KEYS.issubset(self.pressed_keys):
                print("检测到退出快捷键 (5+6+7)，程序即将退出")
                self.exit_requested.emit()
                return

            if key_char in KEY_ACTIONS:
                self.key_pressed.emit(key_char)

        def on_release(key):
            key_char = self._get_key_char(key)
            if key_char is not None:
                self.pressed_keys.discard(key_char)

        self.key_listener = keyboard.Listener(
            on_press=on_press,
            on_release=on_release,
        )
        self.key_listener.daemon = True
        self.key_listener.start()

    @staticmethod
    def _get_key_char(key):
        if key == keyboard.Key.space:
            return " "
        if key == keyboard.Key.backspace:
            return "backspace"

        key_char = getattr(key, "char", None)
        return key_char.lower() if key_char else None

    @pyqtSlot(str)
    def _handle_key_press(self, key):
        action = KEY_ACTIONS[key]
        position = BLANK_POSITION if action in {"blank", "del"} else KEY_POSITIONS[key]
        self._show_movie(action, position)
        self.animation_timer.start(ANIMATION_DURATION_MS)

    def _show_movie(self, name, relative_position=None):
        movie = self.movies[name]
        if self.current_movie is not None and self.current_movie is not movie:
            self.current_movie.stop()

        movie.jumpToFrame(0)
        frame = movie.currentPixmap()
        if frame.isNull():
            raise RuntimeError(f"动画没有可显示的画面：{ASSET_PATHS[name]}")

        width, height = frame.width(), frame.height()
        if relative_position is None:
            # 待机动画水平居中并贴住窗口顶部。
            x = (self.width() - width) // 2
            y = 0
        else:
            center_x = int(self.width() * relative_position[0])
            center_y = int(self.height() * relative_position[1])
            x = center_x - width // 2
            y = center_y - height // 2

        self.pet_label.setMovie(movie)
        self.pet_label.setGeometry(x, y, width, height)
        self.pet_label.show()
        self.pet_label.raise_()
        movie.start()
        self.current_movie = movie

    @pyqtSlot()
    def _show_standby(self):
        self.animation_timer.stop()
        self._show_movie("standby")

    @pyqtSlot()
    def _quit_application(self):
        QApplication.instance().quit()

    @pyqtSlot()
    def _stop_key_listener(self):
        if self.key_listener is not None:
            self.key_listener.stop()
            self.key_listener = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton and hasattr(self, "drag_position"):
            self.move(event.globalPos() - self.drag_position)

    def closeEvent(self, event):
        self._stop_key_listener()
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    pet = DeskPet()
    pet.show()
    sys.exit(app.exec_())

# This Python file uses the following encoding: utf-8
import time
import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QThread


class Timer(QThread):
    def __init__(self, h, m, s):
        super(Timer, self).__init__()
        self.hour = h
        self.minutes = m
        self.seconds = s

    def reduce(self):
        if self.hour == 0 and self.minutes == 0 and self.seconds == 0:
            return
        if self.seconds == 0 and self.minutes > 0:
            self.seconds += 59
            self.minutes -= 1
        elif self.minutes == 0 and self.hour > 0:
            self.minutes += 59
            self.hour -= 1
        self.seconds -= 1

    def run(self):
        while True:
            self.reduce()
            time.sleep(0.5)
            window.ui.lbl_timer.setText(f'{self.hour}:{self.minutes}:{self.seconds}')


class Stop_watch(QThread):
    def __init__(self):
        super(Stop_watch, self).__init__()
        self.hour = 0
        self.minutes = 0
        self.seconds = 0

    def increase(self):
        self.seconds += 1
        if self.seconds >= 60:
            self.minutes += 1
            self.seconds = 0
        elif self.minutes >= 60:
            self.hour += 1
            self.minutes = 0

    def run(self):
        while True:
            self.increase()
            time.sleep(0.2)
            window.ui.lbl_stop_watch.setText(f"{self.hour}:{self.minutes}:{self.seconds}")


class Main:
    def __init__(self):
        super(Main, self).__init__()
        loader = QUiLoader()
        self.ui = loader.load("form.ui")
        self.ui.show()
        self.ui.btn_start.clicked.connect(self.start_timer)
        self.ui.btn_stop.clicked.connect(self.stop_timer)
        self.ui.btn_pause.clicked.connect(self.pause_timer)

        self.ui.btn_start_timer.clicked.connect(self.timer)

        self.stop_watch = Stop_watch()

    def timer(self):
        self.timer = Timer(self.ui.tb_hour.value(), self.ui.tb_minutes.value(), self.ui.tb_seconds.value())
        self.timer.start()

    def pause_timer(self):
        self.stop_watch.terminate()

    def stop_timer(self):
        self.stop_watch.terminate()
        self.stop_watch.hour = 0
        self.stop_watch.minutes = 0
        self.stop_watch.seconds = 0
        self.ui.lbl_stop_watch.setText('00:00:00')

    def start_timer(self):
        self.stop_watch.start()


if __name__ == "__main__":
    app = QApplication([])
    window = Main()
    sys.exit(app.exec_())

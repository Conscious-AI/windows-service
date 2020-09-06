import time
import os
import signal
import subprocess as sp

import win32.servicemanager as sm

from winservice_backbone import PyWinService

_CAI_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


class HandleLocalServer:
    def __init__(self):
        self.path = os.path.join(_CAI_DIR, "local_server", "app.py")
        self.isrunning = False

    def run(self):
        sm.LogInfoMsg("CAI: SERVICE: Starting local server...")
        self.proc = sp.Popen(["python", self.path])
        sm.LogInfoMsg(f"CAI: SERVICE: Local server started with pid {self.proc.pid}")
        self.isrunning = True

    def stop(self):
        sm.LogInfoMsg("CAI: SERVICE: Stopping local server...")
        self.proc.terminate()
        self.isrunning = False


class HandleCommandRecognizer:
    def __init__(self):
        self.dir_path = os.path.join(_CAI_DIR, "command_recognizer")
        self.script_path = os.path.join(self.dir_path, "recognize_command.py")
        self.isrunning = False

    def run(self):
        sm.LogInfoMsg("CAI: SERVICE: Starting command recognizer...")
        self.proc = sp.Popen(["python", self.script_path], cwd=self.dir_path)
        sm.LogInfoMsg(f"CAI: SERVICE: Recognizer started with pid {self.proc.pid}")
        self.isrunning = True

    def stop(self):
        sm.LogInfoMsg("CAI: SERVICE: Stopping recognizer...")
        self.proc.terminate()
        self.isrunning = False


class CAIService(PyWinService):
    _svc_name_ = "CAI Service"
    _svc_display_name_ = "CAI Service"
    _svc_description_ = "Conscious-AI startup and helper service."

    def start(self):
        self.isrunning = True
        self.server = HandleLocalServer()
        self.recognizer = HandleCommandRecognizer()

    def stop(self):
        self.isrunning = False

    def main(self):
        while self.isrunning:
            if not self.server.isrunning:
                self.server.run()
            if not self.recognizer.isrunning:
                self.recognizer.run()
            time.sleep(1)
        self.recognizer.stop()
        self.server.stop()


if __name__ == "__main__":
    CAIService.parse_command_line()

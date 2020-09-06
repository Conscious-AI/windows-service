import sys
import traceback
import socket

import win32.servicemanager as servicemanager
import win32serviceutil
import win32service
import win32event


class PyWinService(win32serviceutil.ServiceFramework):
    """Base class to create the winservice in python"""

    _svc_name_ = "Service True Name"
    _svc_display_name_ = "Service Display Name"
    _svc_description_ = "Service Description."

    @classmethod
    def parse_command_line(cls):
        """
        ClassMethod to parse the command line
        """
        win32serviceutil.HandleCommandLine(cls)

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        """
        Called when the service is asked to stop
        """
        self.stop()
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        """
        Called when the service is asked to start
        """
        self.start()
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, ""),
        )
        try:
            servicemanager.LogInfoMsg("Starting main()...")
            self.main()
        except:
            servicemanager.LogErrorMsg(traceback.format_exc())
            sys.exit(-1)

    def start(self):
        """
        Override to add logic before the start
        eg. running condition
        """
        pass

    def stop(self):
        """
        Override to add logic before the stop
        eg. invalidating running condition
        """
        pass

    def main(self):
        """
        Main class to be overridden to add logic
        """
        pass


if __name__ == "__main__":
    PyWinService.parse_command_line()

from .DebugEventHandler import *


class UserDebugger:
    def __init__(self):
        if sys.version.find("AMD64") != -1:
            self.p = os.path.join(os.path.dirname(__file__), "utils", 'x64')
        else:
            self.p = os.path.join(os.path.dirname(__file__), "utils", 'x86')
        self.dbg = None
        self.started = Event()
        self.quit = Event()
        self.handlingFault = Event()
        self.handledFault = Event()
        self.event_handler = DebugEventHandler()
        self.event_handler.pid = None
        self.event_handler.follow_forks = True
        self.event_handler.quit = self.quit
        self.event_handler.FaultOnEarlyExit = False
        self.event_handler.handlingFault = self.handlingFault
        self.event_handler.handledFault = self.handledFault
        self.event_handler.IgnoreFirstChanceGardPage = False
        self.event_handler.IgnoreSecondChanceGardPage = False
        self.event_handler.crash_name = None
        self.event_handler.crash_description = None

        self.crash_name = None
        self.crash_description = None

    def run(self, proc_args, follow_forks=True):
        proc_args = proc_args.encode("ascii", "ignore")
        self.event_handler.follow_forks = follow_forks
        self.dbg = ProcessCreator(
            command_line=proc_args,
            follow_forks=follow_forks,
            event_callbacks_sink=self.event_handler,
            output_callbacks_sink=self.event_handler,
            dbg_eng_dll_path=self.p)  # symbols_path = SymbolsPath
        self.event_handler.dbg = self.dbg
        self.started.set()
        self.dbg.event_loop_with_quit_event(self.quit)
        # when event handler loop is over
        self.crash_name = self.event_handler.crash_name
        self.crash_description = self.event_handler.crash_description

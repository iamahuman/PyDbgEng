from comtypes.gen import DbgEng
from .UserModeSession import *


class ProcessCreator(UserModeSession):
    '''
    debug a new process.
    '''

    def __init__(self,
                 command_line,
                 follow_forks=True,
                 event_callbacks_sink=None,
                 output_callbacks_sink=None,
                 dbg_eng_dll_path=None,
                 symbols_path=None):
        PyDbgEng.__init__(self, event_callbacks_sink, output_callbacks_sink,
                          dbg_eng_dll_path, symbols_path)
        # create debuggee process
        self.idebug_client.CreateProcess(
            Server=UserModeSession.NO_PROCESS_SERVER,
            CommandLine=command_line,
            CreateFlags=DbgEng.DEBUG_PROCESS if follow_forks else DbgEng.DEBUG_ONLY_THIS_PROCESS)

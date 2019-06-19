from comtypes.gen import DbgEng
from .UserModeSession import *


class ProcessCreator(UserModeSession):
    '''
    debug a new process.
    '''

    def __init__(self, command_line, follow_forks=True, *args, **kwargs):
        super(ProcessCreator, self).__init__(*args, **kwargs)
        # create debuggee process
        self.idebug_client.CreateProcess(
            Server=UserModeSession.NO_PROCESS_SERVER,
            CommandLine=command_line,
            CreateFlags=DbgEng.DEBUG_PROCESS if follow_forks else DbgEng.DEBUG_ONLY_THIS_PROCESS)

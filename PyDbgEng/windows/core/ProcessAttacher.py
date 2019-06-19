from .UserModeSession import *


class ProcessAttacher(UserModeSession):
    '''
    debug an existing process.
    '''

    def __init__(self, pid, *args, **kwargs):
        super(ProcessAttacher, self).__init__(*args, **kwargs)
        # attach to process
        self.idebug_client.AttachProcess(
            Server=UserModeSession.NO_PROCESS_SERVER,
            ProcessId=pid,
            AttachFlags=DbgEng.DEBUG_ATTACH_DEFAULT)

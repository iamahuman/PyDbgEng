
from .Defines import INFINITE
from .PyDbgEng import PyDbgEng

from comtypes.gen import DbgEng


class DumpFileOpener(PyDbgEng):
    '''
    open crash dump file
    '''

    def __init__(self, dump_file, *args, **kwargs):
        super(DumpFileOpener, self).__init__(*args, **kwargs)

        # open dump file
        self.dbg_eng_log(
            "DumpFileOpener.__init__: about to open dump file %s" % dump_file)
        self.idebug_client.OpenDumpFile(dump_file)

        # Finish initialization by waiting for the event that
        # caused the dump.  This will return immediately as the
        # dump file is considered to be at its event.
        self.idebug_control.WaitForEvent(DbgEng.DEBUG_WAIT_DEFAULT, INFINITE)

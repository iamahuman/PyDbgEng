import sys
from ctypes import *
from .PyDbgEng import *
from comtypes.gen import DbgEng
from .Defines import *
from .DebuggerException import *


class UserModeSession(PyDbgEng):
    '''
    in user mode debug session the IDebugControl.WaitForEvent() can have a non
    INFINITE timeout.
    client should NOT use this class directly.
    '''
    NO_PROCESS_SERVER = 0

    # event loop
    def wait_for_event(self, timeout_ms):
        try:
            self.idebug_control.WaitForEvent(DbgEng.DEBUG_WAIT_DEFAULT,
                                             timeout_ms)
            return True
        except COMError as e:
            status = self.idebug_control.GetExecutionStatus()

            # debuggee terminated?
            if status == DbgEng.DEBUG_STATUS_NO_DEBUGGEE:
                # ok, no harm done. leave the function.
                return False
            # some other error - re throw
            raise

    def event_loop_with_user_callback(self, user_callback,
                                      user_callback_pool_interval_ms):
        if user_callback_pool_interval_ms <= 0:
            raise DebuggerException(
                "UserModeSession.event_loop_with_user_callback(): invalid user_callback_pool_interval_ms"
            )
        while True:
            if self.wait_for_event(user_callback_pool_interval_ms) == False:
                break
            # call user callback
            if user_callback(self) == True:
                # user requested to quit event loop
                break

    def event_loop_with_quit_event(self, quit_event):
        #if not isinstance(quit_event, threading._Event):
        #    raise DebuggerException("UserModeSession.event_loop_with_quit_event(): invalid quit_event")
        while not quit_event.is_set():
            if self.wait_for_event(200) == False:
                break

    # handle functions
    def get_handle_data(self, handle):
        handle_data_size = 0
        handle_data_buffer = None
        while True:
            handle_data_size += 256
            handle_data_buffer = create_string_buffer(handle_data_size)
            try:
                self.idebug_data_spaces.ReadHandleData( handle,
                                                        DbgEng.DEBUG_HANDLE_DATA_TYPE_OBJECT_NAME,
                                                        byref(handle_data_buffer),
                                                        handle_data_size)
                if handle_data_buffer.raw.find("\x00") != -1:
                    break
            except COMError as e:
                if e[0] != int(STRSAFE_E_INSUFFICIENT_BUFFER):
                    raise
                pass
        return BUFFER_TO_ANSI_STRING(handle_data_buffer.raw)

    # thread functions
    def get_current_tid(self):
        return self.idebug_system_objects.GetCurrentThreadId()

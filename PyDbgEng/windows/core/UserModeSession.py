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
        except COMError:
            status = self.idebug_control.GetExecutionStatus()

            # debuggee terminated?
            if status != DbgEng.DEBUG_STATUS_NO_DEBUGGEE:
                # some other error - re throw
                raise
            # ok, no harm done. leave the function.
            return False

    def event_loop_with_user_callback(self, user_callback,
                                      user_callback_pool_interval_ms):
        if user_callback_pool_interval_ms <= 0:
            raise DebuggerException(
                "UserModeSession.event_loop_with_user_callback(): invalid user_callback_pool_interval_ms"
            )
        while self.wait_for_event(user_callback_pool_interval_ms) and not user_callback(self):
            pass

    def event_loop_with_quit_event(self, quit_event):
        #if not isinstance(quit_event, threading._Event):
        #    raise DebuggerException("UserModeSession.event_loop_with_quit_event(): invalid quit_event")
        while not quit_event.is_set() and self.wait_for_event(200):
            pass

    # handle functions
    def get_handle_data(self, handle):
        handle_data_buffer = create_string_buffer(256)
        while True:
            try:
                self.idebug_data_spaces.ReadHandleData( handle,
                                                        DbgEng.DEBUG_HANDLE_DATA_TYPE_OBJECT_NAME,
                                                        byref(handle_data_buffer),
                                                        sizeof(handle_data_buffer))
                buf = handle_data_buffer.value
                if len(buf) < len(handle_data_buffer):
                    return buf
                del buf
                resize(handle_data_buffer, sizeof(handle_data_buffer) + 256)
            except COMError as e:
                if e[0] != int(STRSAFE_E_INSUFFICIENT_BUFFER):
                    raise

    # thread functions
    def get_current_tid(self):
        return self.idebug_system_objects.GetCurrentThreadId()

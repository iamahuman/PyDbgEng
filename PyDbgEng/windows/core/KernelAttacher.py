import threading
from multiprocessing import *
from ctypes import *
from comtypes.gen import DbgEng

from .PyDbgEng import *


class KernelAttacher(PyDbgEng):
    '''
    used for kernel mode debugging.
    '''

    class QuitEventWaiter(threading.Thread):

        def __init__(self, quit_event, abort_event, top):
            super(QuitEventWaiter, self).__init__()
            self.daemon = True
            self.quit_event = quit_event
            self.abort_event = abort_event
            self.top = top
            self.start()

        def run(self):
            while not self.abort_event.is_set():
                self.quit_event.wait(0.02)  # wait for 200ms
                if self.quit_event.is_set():
                    self.top.force_quit_flag = True
                    self.top.idebug_control.SetInterrupt(
                        Flags=DbgEng.DEBUG_INTERRUPT_EXIT)
                    break

    def __init__(self, connection_string, set_initial_bp=True, *args, **kwargs):
        super(KernelAttacher, self).__init__(*args, **kwargs)

        self.force_quit_flag = False

        # sanity check before setting initial bp
        if (event_callbacks_sink is not None
                and isinstance(event_callbacks_sink, IDebugEventCallbacksSink)
                and set_initial_bp):
            if not (event_callbacks_sink.GetInterestMask()
                     & DbgEng.DEBUG_EVENT_EXCEPTION):
                raise DebuggerException(
                    "requested initial break, but 'exception' method is not implemented."
                )
            self.idebug_control.SetEngineOptions(
                DbgEng.DEBUG_ENGOPT_INITIAL_BREAK)

        # attach to kernel
        self.idebug_client.AttachKernel(
            ConnectOptions=connection_string,
            Flags=DbgEng.DEBUG_ATTACH_KERNEL_CONNECTION)

    def __del__(self):
        super(KernelAttacher, self).__del__(self)

        # an extra step in kenel session termination: free dbgeng.dll
        # this will make sure all handles are closed and PyDbgEng will
        # be ready for another run
        dbgeng_dll = self.dbgeng_dll
        if dbgeng_dll is not None:
            self.dbgeng_dll = None
            windll.kernel32.FreeLibrary(dbgeng_dll._handle)

    # event loop
    def event_loop_with_quit_event(self, quit_event):
        '''
        in kernel debugging session IDebugControl.WaitForEvent() must be called with an 'infinite' timeout value.
        this is why we have to create thread that checks the given given quit event. once set it will force a debugger
        break.
        '''
        # sanity check on quit_event
        #if (not isinstance(quit_event, threading._Event)):
        #   raise DebuggerException("invalid type for quit event")
        # is already set?
        if quit_event.is_set():
            # no job for us
            return

        # create abort event
        abort_quit_waiter_event = Event()

        # start quit thread
        quit_waiter = KernelAttacher.QuitEventWaiter(
            quit_event=quit_event,
            abort_event=abort_quit_waiter_event,
            top=self)

        # event loop
        self.__event_loop_with_forced_break_check(quit_event)

        # stop quit waiter thread
        abort_quit_waiter_event.set()
        quit_waiter.join()

        # dont wait for garbage collection, and force delete on self
        self.__del__()

    def __event_loop_with_forced_break_check(self, quit_event):
        while True:
            try:
                #print 'waiting for event'
                self.idebug_control.WaitForEvent(DbgEng.DEBUG_WAIT_DEFAULT,
                                                 INFINITE)
                #status = self.idebug_control.GetExecutionStatus()
                #print 'done waiting. status: '+str(status)
            except COMError:
                #print 'comerror'
                status = self.idebug_control.GetExecutionStatus()
                # forced break?
                #print 'status:' + str(status)
                if (status == DbgEng.DEBUG_STATUS_BREAK
                        and self.force_quit_flag):

                    # reset force break - so client can keep on calling event loop
                    self.force_quit_flag = False

                    # ok, no harm done. break the loop.
                    return

                # some other error - re throw
                raise

    # thread functions
    def get_current_tid(self):
        return 0

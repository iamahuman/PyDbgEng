import os
import comtypes.server.localserver
from comtypes.client import CreateObject
from comtypes.hresult import S_OK
from comtypes import CoClass, GUID

from .PyDbgEng import PyDbgEng
from .Defines import *

try:
    from comtypes.gen import DbgEng
except ImportError:
    import comtypes
    tlb = os.path.join(os.path.dirname(__file__), "..", "utils", "DbgEng.tlb")
    comtypes.client.GetModule(tlb)
    from comtypes.gen import DbgEng


class DebuggerException(Exception):
    pass


class DbgEngEventCallbacks(CoClass):

    _reg_clsid_ = GUID('{EAC5ACAA-7BD0-4f1f-8DEB-DF2862A7E85B}')
    _reg_threading_ = "Both"
    _reg_progid_ = "PyDbgEngLib.DbgEngEventCallbacks.1"
    _reg_novers_progid_ = "PyDbgEngLib.DbgEngEventCallbacks"
    _reg_desc_ = "Callback class!"
    _reg_clsctx_ = comtypes.CLSCTX_INPROC_SERVER

    _com_interfaces_ = [
        DbgEng.IDebugEventCallbacks, DbgEng.IDebugOutputCallbacks,
        comtypes.typeinfo.IProvideClassInfo2,
        comtypes.errorinfo.ISupportErrorInfo,
        comtypes.connectionpoints.IConnectionPointContainer
    ]

    def IDebugOutputCallbacks_Output(self, *args):
        if len(args) == 2:
            args = (None,) + args
        self._pyDbgEng = PyDbgEng.fuzzyWuzzy
        self._pyDbgEng.output_callbacks_sink.Output(*args)
        return S_OK

    def IDebugEventCallbacks_Breakpoint(self, *args):
        # >= v0.5.1
        if len(args) == 1:
            args = (None,) + args
        return self._pyDbgEng.Breakpoint(*args)

    def IDebugEventCallbacks_ChangeDebuggeeState(self, *args):
        # >= v0.5.1
        if len(args) == 2:
            args = (None,) + args
        return self._pyDbgEng.ChangeDebuggeeState(*args)

    def IDebugEventCallbacks_ChangeEngineState(self, *args):
        # >= v0.5.1
        if len(args) == 2:
            args = (None,) + args
        return self._pyDbgEng.ChangeEngineState(*args)

    def IDebugEventCallbacks_Exception(self, *args):
        # >= v0.5.1:
        if len(args) == 2:
            args = (None,) + args
        return self._pyDbgEng.Exception(*args)

    def IDebugEventCallbacks_GetInterestMask(self, *args):
        # Superhack!
        self._pyDbgEng = PyDbgEng.fuzzyWuzzy
        # For v0.5.1 and on
        if not args:
            return self._pyDbgEng.GetInterestMask()
        # For v0.4 and lower
        args[1][0] = self._pyDbgEng.GetInterestMask()
        return S_OK

    def IDebugEventCallbacks_LoadModule(self, *args):
        # >= v0.5.1
        if len(args) == 7:
            args = (None,) + args
        return self._pyDbgEng.LoadModule(*args)

    def IDebugEventCallbacks_UnloadModule(self, *args):
        # >= 0.5.1
        if len(args) == 2:
            args = (None,) + args
        return self._pyDbgEng.UnloadModule(*args)

    def IDebugEventCallbacks_CreateProcess(self, *args):
        # >= 0.5.1
        if len(args) == 11:
            args = (None,) + args
        return self._pyDbgEng.CreateProcess(*args)

    def IDebugEventCallbacks_ExitProcess(self, *args):
        # >= 0.5.1
        if len(args) == 1:
            args = (None,) + args
        return self._pyDbgEng.ExitProcess(*args)

    def IDebugEventCallbacks_SessionStatus(self, *args):
        # >= 0.5.1
        if len(args) == 1:
            args = (None,) + args
        return self._pyDbgEng.SessionStatus(*args)

    def IDebugEventCallbacks_ChangeSymbolState(self, *args):
        # >= 0.5.1
        if len(args) == 2:
            args = (None,) + args
        return self._pyDbgEng.ChangeSymbolState(*args)

    def IDebugEventCallbacks_SystemError(self, *args):
        # >= 0.5.1
        if len(args) == 2:
            args = (None,) + args
        return self._pyDbgEng.SystemError(*args)

    def IDebugEventCallbacks_CreateThread(self, *args):
        # >= 0.5.1
        if len(args) == 3:
            args = (None,) + args
        return self._pyDbgEng.CreateThread(*args)

    def IDebugEventCallbacks_ExitThread(self, *args):
        # >= 0.5.1
        if len(args) == 1:
            args = (None,) + args
        return self._pyDbgEng.ExitThread(*args)

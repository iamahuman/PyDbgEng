from .DebuggerException import *


class hook_container:

    def __init__(self):
        self.hooks = []

    def add(self, dbg, address, num_args, entry_hook=None, exit_hook=None):
        if entry_hook is None and exit_hook is None:
            raise DebuggerException("no entry or exit hooks")

        # create a new hook instance and activate it.
        h = hook(address, num_args, entry_hook, exit_hook)
        h.hook(dbg)

        self.hooks.append(h)


class hook:

    def __init__(self, address, num_args, entry_hook=None, exit_hook=None):
        self.address = address
        self.num_args = num_args
        self.entry_hook = entry_hook
        self.exit_hook = exit_hook
        self.arguments = {}

    def hook(self, dbg):
        dbg.bp_set(self.address, restore=True, handler=self.__proxy_on_entry)

    def __proxy_on_entry(self, dbg):
        tid = dbg.get_current_tid()
        args = []
        for i in range(1, self.num_args + 1):
            args.append(dbg.get_arg(i))
        self.arguments[tid] = args

        # if an entry point callback was specified, call it and grab the return value.
        if self.entry_hook:
            self.entry_hook(dbg, args)

        # if an exit hook callback was specified, determine the function exit.
        if self.exit_hook:
            function_exit = dbg.get_arg(0)

            # set a breakpoint on the function exit.
            dbg.bp_set(function_exit,
                       restore=False,
                       handler=self.__proxy_on_exit)

    def __proxy_on_exit(self, dbg):
        self.exit_hook(dbg, self.arguments[dbg.get_current_tid()], dbg.get_register_value("eax"))

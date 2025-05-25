import gdb

class DepthCommand(gdb.Command):
    """Print the current call stack depth"""

    def __init__(self):
        super (DepthCommand, self).__init__('depth', gdb.COMMAND_FILES)

    def invoke(self, arg, _):
        frame = gdb.selected_frame()
        if frame is None:
            gdb.write('No frame selected\n')
            return

        depth = frame.level()
        while frame.older() is not None:
            frame = frame.older()
            depth += 1

        gdb.write(f'Depth of current call stack is {depth} frames\n')

DepthCommand()


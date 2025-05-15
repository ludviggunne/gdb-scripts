import gdb
import re
from math import log, ceil

class GrepCommand(gdb.Command):
    """Search for patterns in current source file"""

    def __init__(self):
        super (GrepCommand, self).__init__('grep', gdb.COMMAND_FILES)

    def invoke(self, arg, _):

        # Parse arguments
        argv = gdb.string_to_argv(arg)
        if len(argv) == 0:
            gdb.write('Missing pattern\n')
            return

        pattern = argv[0]

        # Find name of current source file
        try:
            pc = gdb.selected_frame().pc()
            symtab_and_line = gdb.find_pc_line(pc)
            symtab = symtab_and_line.symtab
            lineno = symtab_and_line.line - 1
            filename = symtab.fullname()
        except:
            gdb.write('Failed to retrieve source file information\n')
            return

        # Read source file
        try:
            with open(filename, 'r') as file:
                lines = [line.rstrip() for line in file]
        except:
            gdb.write('Failed to open source file ' + filename + '\n')
            return

        # Only use case insensitive search if pattern is all lowercase
        flags = re.I
        for c in pattern:
            if c.isupper():
                flags = 0
                break

        padding = int(ceil(log(len(lines), 10)))

        # Match lines
        found_match = False
        for lineno, line in enumerate(lines, start=1):
            if re.search(pattern, line, flags=flags) is not None:
                gdb.write(f'{str(lineno).rjust(padding)}: {line}\n')
                found_match = True

        if not found_match:
            gdb.write('No matches\n')

GrepCommand()

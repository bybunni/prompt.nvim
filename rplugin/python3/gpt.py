import pynvim


@pynvim.plugin
class GPT:
    def __init__(self, nvim):
        self.nvim = nvim

    @pynvim.function("Selection")
    def print_selection(self, args):
        self.nvim.out_write(str(self.selection(args)) + "\n")

    def selection(self, args):
        # 2147483647 is the maximum value for a signed 32-bit integer and will be returned as cecol if we are at the end of the line
        _, csrow, cscol, _ = self.nvim.eval('getpos("\'<")')
        _, cerow, cecol, _ = self.nvim.eval('getpos("\'>")')
        if csrow < cerow or (csrow == cerow and cscol <= cecol):
            return csrow - 1, cscol - 1, cerow - 1, cecol
        else:
            return cerow - 1, cecol - 1, csrow - 1, cscol

import pynvim


@pynvim.plugin
class GPT:
    def __init__(self, nvim):
        self.nvim = nvim

    @pynvim.function("GPTHello")
    def hello(self, args):
        self.nvim.out_write("Hello from Python!\n")

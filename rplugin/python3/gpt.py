import pynvim
import os
import openai

openai.api_key = os.environ["OPENAI_API_KEY"]


@pynvim.plugin
class GPT:
    def __init__(self, nvim):
        self.nvim = nvim

    @pynvim.command("Prompt", range=True, nargs="*")
    def prompt(self, *args):
        self.nvim.out_write(str(len(args)) + str(args) + "\n")
        if len(args[0]) == 0:
            csrow, cscol, cerow, cecol = self.selection(args)
            highlighted_text = self.nvim.current.buffer[csrow : cerow + 1]
            prompt = "\n".join(highlighted_text)
        else:
            prompt = " ".join(args[0])

        # create split window for response
        self.nvim.command("vsplit")
        current_window = self.nvim.current.window
        # create new buffer for response
        response_buffer = self.nvim.api.create_buf(False, True)
        response_buffer[:] = ["Waiting for response..."]
        self.nvim.api.win_set_buf(current_window, response_buffer)

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=100,
            echo=True,
        )

        response_buffer[:] = response.choices[0].text.splitlines()
        self.nvim.api.win_set_buf(current_window, response_buffer)

    @pynvim.command("PromptChat", range=True)
    def prompt_chat(self, *args):
        self.nvim.out_write(str(len(args)) + str(args) + "\n")
        buffer_text = self.nvim.current.buffer[:]
        prompt = "\n".join(buffer_text)

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=300,
            echo=True,
        )

        self.nvim.current.buffer[:] = response.choices[0].text.splitlines()
        self.nvim.command("norm! GVgqG")

    @pynvim.function("Selection")
    def print_selction(self, args):
        self.nvim.out_write(str(self.selection(args)) + "\n")

    def selection(self, args):
        # 2147483647 is the maximum value for a signed 32-bit integer and will
        # be returned as cecol if we are at the end of the line
        # https://github.com/vim/vim/issues/4464
        _, csrow, cscol, _ = self.nvim.eval('getpos("\'<")')
        _, cerow, cecol, _ = self.nvim.eval('getpos("\'>")')
        if csrow < cerow or (csrow == cerow and cscol <= cecol):
            return csrow - 1, cscol - 1, cerow - 1, cecol
        else:
            return cerow - 1, cecol - 1, csrow - 1, cscol

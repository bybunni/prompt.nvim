import pynvim
import os
import openai

openai.api_key = os.environ["OPENAI_API_KEY"]


@pynvim.plugin
class GPT:
    def __init__(self, nvim):
        self.nvim = nvim

    @pynvim.function("SelectionWindow")
    def selection_window(self, args):
        csrow, cscol, cerow, cecol = self.selection(args)
        scratch_buffer = self.nvim.api.create_buf(True, False)
        highlighted_text = self.nvim.current.buffer[csrow : cerow + 1]
        # prompt = "Write a pragraph based on the below outline:\n\n"
        prompt = "\n".join(highlighted_text)
        # prompt += text
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=100,
            echo=True,
        )
        for line in response.choices[0].text.splitlines():
            scratch_buffer.append(line)
        # prompt = "\n\nPrompt sent to GPT3:\n" + prompt
        # for line in prompt.splitlines():
        #     scratch_buffer.append(line)
        window = self.nvim.api.open_win(
            scratch_buffer,
            False,
            {"relative": "win", "row": 0, "col": 95, "width": 88, "height": 20},
        )

    @pynvim.function("Selection")
    def print_selection(self, args):
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

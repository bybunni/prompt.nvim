import pynvim
import os
import openai

openai.api_key = os.environ["OPENAI_API_KEY"]


@pynvim.plugin
class GPT:
    def __init__(self, nvim):
        self.nvim = nvim
        self.response_buffer = None

    @pynvim.command("CodexCompile", range=True)
    def codex_compile(self, *args):
        original_code = self.nvim.current.buffer[:]
        original_code = "\n".join(original_code)
        original_window = self.nvim.current.window
        self.nvim.out_write(original_code)
        self.nvim.command(":new | read !cc #")
        compiler_output = self.nvim.current.buffer[:]
        compiler_output = "\n".join(compiler_output)
        self.nvim.out_write(compiler_output)
        prompt = (
            original_code
            + "\n\n"
            + compiler_output
            + "\n\n"
            + "Suggest a fix to the code."
        )
        self.nvim.out_write("\nWaiting for response...\n")
        response = openai.Completion.create(
            model="code-davinci-002",
            prompt=prompt,
            max_tokens=256,
            echo=True,
        )
        self.nvim.out_write(response.choices[0].text)

    @pynvim.command("Prompt", range=True, nargs="*")
    def prompt(self, *args):
        # self.nvim.out_write(str(len(args)) + str(args) + "\n")
        csrow, cerow = args[1]
        selected_text = self.nvim.current.buffer[
            csrow - 1 : (cerow + 1) if cerow != csrow else cerow
        ]
        selected_text = "\n".join(selected_text)
        ssrow, sscol, serow, secol = self.selection(args)
        # if cursor position matches visual selection use selected_text
        # [crow, ccol] == [crow-1, _, ccol-1, _]
        if (csrow - 1) != ssrow and (cerow - 1) != serow:
            selected_text = ""
        if len(args[0]) != 0:
            prompt = " ".join(args[0]) + "\n\n" + selected_text
        else:
            prompt = selected_text
        # self.nvim.out_write(str([csrow, cscol, cerow, cecol]) + "\n")
        # self.nvim.out_write(str([csrow, cerow]) + "\n")
        # self.nvim.out_write("Goodbye from Python!\n")

        if self.response_buffer is None:
            # create split window for response
            self.nvim.command("vsplit")
            self.response_buffer = self.nvim.api.create_buf(False, True)
            current_window = self.nvim.current.window
            self.nvim.api.win_set_buf(current_window, self.response_buffer)

        # self.response_buffer[:] = ["Waiting for response..."]
        self.nvim.out_write("Waiting for response...\n")
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=300,
            echo=True,
        )
        self.nvim.out_write("\n")

        self.response_buffer.append(
            response.choices[0].text.splitlines() + [""], index=0
        )
        # self.nvim.api.win_set_buf(current_window, self.response_buffer)

    @pynvim.command("PromptChat", range=True)
    def prompt_chat(self, *args):
        # self.nvim.out_write(str(len(args)) + str(args) + "\n")
        buffer_text = self.nvim.current.buffer[:]
        prompt = "\n".join(buffer_text)

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=300,
            echo=True,
        )

        self.nvim.current.buffer[:] = response.choices[0].text.splitlines()

    @pynvim.function("Selection")
    def print_selction(self, args):
        self.nvim.out_write(str(self.selection(args)) + "\n")

    def selection(self, args):
        # 2147483647 is the maximum value for a signed 32-bit integer and will
        # be returned as cecol if we are at the end of the line
        # https://github.com/vim/vim/issues/4464
        a, csrow, cscol, b = self.nvim.eval('getpos("\'<")')
        c, cerow, cecol, d = self.nvim.eval('getpos("\'>")')
        # self.nvim.out_write("ab" + str([a, csrow, cscol, b]) + "\n")
        # self.nvim.out_write("cd" + str([c, cerow, cecol, d]) + "\n")
        if csrow < cerow or (csrow == cerow and cscol <= cecol):
            return csrow - 1, cscol - 1, cerow - 1, cecol
        else:
            return cerow - 1, cecol - 1, csrow - 1, cscol

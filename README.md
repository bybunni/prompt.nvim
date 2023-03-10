# prompt.nvim

## Dependencies
1. Install [pynvim](https://github.com/neovim/pynvim): `python -m pip install pynvim`
2. Install [openai](https://github.com/openai/openai-python): `python -m pip install openai`
### Verify pynvim is detected
`:checkhealth` and verify Python 3 provider shows Python and pynvim

## Export OpenAI Key
`export OPENAI_API_KEY=YourKey`

## Install Plugin with Packer
1. Add to your `init.lua`: `use 'bybunni/llm.nvim'`
2. Run `:PackerSync`
3. Run `:UpdateRemotePlugins`
4. Quit and restart Neovim

## Use
1. In any mode prompt text completion with `:Prompt` e.g. `:Prompt write a haiku` will
   result in a response like
```
blooming morning dew
beneath azure summer sky
sparkling fresh renewal
```
2. In Visual mode highlight the desired text to send to GPT-3 as a prompt and
   invoke the `Prompt` command. After a few seconds a window will open with a
   scratch buffer containing the response. You can interact with this window
   like any other neovim window. Additional responses will be prepended to this
   buffer.
   ![Screenshot](images/window.jpg)

3. Alternatively, in Visual mode highlight the desired text to act on and 
   invoke the `Prompt` command with arguments, e.g. `:Prompt translate to
   Spanish` and the prompt command will be combined with the visual text.
   After a few seconds a window will open with a scratch buffer containing the
   response. You can interact with this window like any other neovim window.
   Additional responses will be prepended to this buffer.
   ![Screenshot](images/prompt_with_visual_selection.jpg)

4. The `PromptChat` command takes as input the entire current buffer and
   returns responses appended to the end of the current buffer to facilitate an
   iterative _chat_ style.

## Keymaps
Add a binding for the `Prompt` command e.g.

`vim.keymap.set({ 'n', 'v' }, '<leader>p', ':Prompt<CR>') -- prompt.nvim`

Custom `Prompt` commands to act on a visual selection can also be bound, e.g.

`vim.keymap.set({ 'n', 'v' }, '<leader>pt', ':Prompt translate to Spanish<CR>') -- prompt.nvim`

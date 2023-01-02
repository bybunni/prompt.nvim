# llm.nvim

## Dependencies
1. Install [pynvim](https://github.com/neovim/pynvim): `python -m pip install pynvim`
2. Install [openai](https://github.com/openai/openai-python): `python -m pip install pynvim`
### Verify pynvim is detected
`:checkhealth` and verify Python 3 provider shows Python and pynvim

## Export OpenAI Key
`export OPENAI_API_KEY=YourKey`

## Install Plugin
1. Add to your `init.lua`: `use 'bybunni/llm.nvim' -- llm.nvim local development directory`
2. Run `:PackerSync`
3. Run `:UpdateRemotePlugins`
4. Quit and restart Neovim

## Call Function
Add a binding for `SelectionWindow()` e.g., `vim.keymap.set({ 'n', 'v' }, '<leader>w', ':call SelectionWindow()<CR>') -- llm.nvim`

## Use
Highlight the desired text to send to GPT-3 as a prompt and call
`SelectionWindow()`. After a few seconds a window will open on the right with
the response.

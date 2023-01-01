# llm.nvim

## Dependencies
Install [pynvim](https://github.com/neovim/pynvim): `python -m pip install pynvim`
### Verify pynvim is detected
`:checkhealth` and verify Python 3 provider shows Python and pynvim

## Install Plugin
1. Add to your `init.lua`: `use 'bybunni/llm.nvim' -- llm.nvim local development directory`
2. Run `:PackerSync`
3. Run `:UpdateRemotePlugins`
4. Quit and restart Neovim

## Call Function
`:call Selection()`

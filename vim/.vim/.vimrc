" liukui authorized only
set nocompatible
set fileencoding=utf-8
set fileencodings=ucs-bom,utf-8,gb18030,big5,euc-jp,euc-kr,latin1
set encoding=utf-8
set termencoding=&encoding
set fileformats=unix
set display=lastline
set viewoptions=cursor,folds
set viewdir=~/.vimview
set hlsearch

au BufWinLeave * if bufname("%") != "" | mkview
au BufWinEnter * if bufname("%") != "" | silent loadview
au BufNewFile,Bufread *.ros,*.inc,*.php set keywordprg=":help"
let mapleader = ","
let g:fencview_autodetect = 1
nmap <leader>w :w!<cr>
nmap <leader>w :w!<cr> 
nmap <leader>r :!/home/work/php/bin/php %<cr>
nmap <leader>l :!/home/work/php/bin/php -ln %<cr>
nmap <leader>q :q!<cr>
nmap <silent> <F6> :set number!<CR>
nnoremap ,m :w <BAR> !lessc % > %:t:r.css<CR><space>
set autoindent
set smartindent
set tabstop=4
set softtabstop=4
set shiftwidth=4
set nonu
set list
set listchars=tab:>-,trail:-
set expandtab
set ruler
set nocp
set backspace=indent,eol,start
set paste

filetype on
runtime bundle/vim-pathogen/autoload/pathogen.vim
call pathogen#infect()
call pathogen#helptags()
syntax on
filetype plugin indent on

" Always show status line, even for one window
set laststatus=2
set statusline=%F%*\ %y[%{&fenc}]\ %2*%r%m%*\ %l,%c\ %=%l/%L\ (%p%%)%*\%{strftime('%Y-%m-%d-%H:%M')}
set viminfo='20,\"50,:20,%,n~/.viminfo

" set colorscheme
 colorscheme koehler
" colorscheme evening

let Tlist_Ctags_cmd="/usr/bin/ctags"
let Tlist_Inc_Winwidth=0

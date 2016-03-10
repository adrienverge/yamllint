Integration with text editors
=============================

Most text editors support syntax checking and highlighting, to visually report
syntax errors and warnings to the user. yamllint can be used to syntax-check
YAML source, but a bit of configuration is required depending on your favorite
text editor.

Vim
---

Assuming that the `syntastic <https://github.com/scrooloose/syntastic>`_ plugin
is installed, add to your ``.vimrc``:

::

 let g:syntastic_yaml_checkers = ['yamllint']

Neovim
------

Assuming that the `neomake <https://github.com/benekastah/neomake>`_ plugin is
installed, yamllint is supported by default. It is automatically enabled when
editing YAML files.

Other text editors
------------------

.. rubric:: Help wanted!

Your favorite text editor is not listed here? Help us improve by adding a
section (by opening a pull-request or issue on GitHub).

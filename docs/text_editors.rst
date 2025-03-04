Integration with text editors
=============================

Most text editors support syntax checking and highlighting, to visually report
syntax errors and warnings to the user. yamllint can be used to syntax-check
YAML source, but a bit of configuration is required depending on your favorite
text editor.

Vim
---

Assuming that the `ALE <https://github.com/dense-analysis/ale>`_ plugin is
installed, yamllint is supported by default. It is automatically enabled when
editing YAML files.

If you instead use the `syntastic <https://github.com/vim-syntastic/syntastic>`_
plugin, add this to your ``.vimrc``:

::

 let g:syntastic_yaml_checkers = ['yamllint']

Note that Vim >9.0 includes a so-called "compiler script" for yamllint.

- Enable the compiler:

  ::

  :compiler yamllint

- Use it on the current buffer:

  ::

  :make %

See ``:help quickfix``.

Neovim
------

Assuming that the `neomake <https://github.com/neomake/neomake>`_ plugin is
installed, yamllint is supported by default. It is automatically enabled when
editing YAML files.

Emacs
-----

If you are `flycheck <https://github.com/flycheck/flycheck>`_ user, you can use
`flycheck-yamllint <https://github.com/krzysztof-magosa/flycheck-yamllint>`_ integration.

Visual Studio Code
------------------

https://marketplace.visualstudio.com/items?itemName=fnando.linter

IntelliJ
--------

https://plugins.jetbrains.com/plugin/15349-yamllint

Other text editors
------------------

.. rubric:: Help wanted!

Your favorite text editor is not listed here? Help us improve by adding a
section (by opening a pull-request or issue on GitHub).

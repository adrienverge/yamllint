Configuration
=============

yamllint uses a set of :doc:`rules <rules>` to check source files for problems.
Each rule is independent from the others, and can be enabled, disabled or
tweaked. All these settings can be gathered in a configuration file.

To use a custom configuration file, use the ``-c`` option:

.. code:: bash

 yamllint -c /path/to/myconfig file-to-lint.yaml

If ``-c`` is not provided, yamllint will look for a configuration file in the
following locations (by order of preference):

- a file named ``.yamllint``, ``.yamllint.yaml``, or ``.yamllint.yml`` in the
  current working directory, or a parent directory (the search for this file is
  terminated at the user's home or filesystem root)
- a filename referenced by ``$YAMLLINT_CONFIG_FILE``, if set
- a file named ``$XDG_CONFIG_HOME/yamllint/config`` or
  ``~/.config/yamllint/config``, if present

Finally if no config file is found, the default configuration is applied.

Default configuration
---------------------

Unless told otherwise, yamllint uses its ``default`` configuration:

.. literalinclude:: ../yamllint/conf/default.yaml
   :language: yaml

Details on rules can be found on :doc:`the rules page <rules>`.

There is another pre-defined configuration named ``relaxed``. As its name
suggests, it is more tolerant:

.. literalinclude:: ../yamllint/conf/relaxed.yaml
   :language: yaml

It can be chosen using:

.. code:: bash

 yamllint -d relaxed file.yml

Extending the default configuration
-----------------------------------

When writing a custom configuration file, you don't need to redefine every
rule. Just extend the ``default`` configuration (or any already-existing
configuration file).

For instance, if you just want to disable the ``comments-indentation`` rule,
your file could look like this:

.. code-block:: yaml

 # This is my first, very own configuration file for yamllint!
 # It extends the default conf by adjusting some options.

 extends: default

 rules:
   comments-indentation: disable  # don't bother me with this rule

Similarly, if you want to set the ``line-length`` rule as a warning and be less
strict on block sequences indentation:

.. code-block:: yaml

 extends: default

 rules:
   # 80 chars should be enough, but don't fail if a line is longer
   line-length:
     max: 80
     level: warning

   # accept both     key:
   #                   - item
   #
   # and             key:
   #                 - item
   indentation:
     indent-sequences: whatever

Custom configuration without a config file
------------------------------------------

It is possible -- although not recommended -- to pass custom configuration
options to yamllint with the ``-d`` (short for ``--config-data``) option.

Its content can either be the name of a pre-defined conf (example: ``default``
or ``relaxed``) or a serialized YAML object describing the configuration.

For instance:

.. code:: bash

 yamllint -d "{extends: relaxed, rules: {line-length: {max: 120}}}" file.yaml

Errors and warnings
-------------------

Problems detected by yamllint can be raised either as errors or as warnings.
The CLI will output them (with different colors when using the ``colored``
output format, or ``auto`` when run from a terminal).

By default the script will exit with a return code ``1`` *only when* there is
one or more error(s).

However if strict mode is enabled with the ``-s`` (or ``--strict``) option, the
return code will be:

 * ``0`` if no errors or warnings occur
 * ``1`` if one or more errors occur
 * ``2`` if no errors occur, but one or more warnings occur

If the script is invoked with the ``--no-warnings`` option, it won't output
warning level problems, only error level ones.

YAML files extensions
---------------------

To configure what yamllint should consider as YAML files when listing
directories, set ``yaml-files`` configuration option. The default is:

.. code-block:: yaml

 yaml-files:
   - '*.yaml'
   - '*.yml'
   - '.yamllint'

The same rules as for ignoring paths apply (``.gitignore``-style path pattern,
see below).

If you need to know the exact list of files that yamllint would process,
without really linting them, you can use ``--list-files``:

.. code:: bash

 yamllint --list-files .

Ignoring paths
--------------

It is possible to exclude specific files or directories, so that the linter
doesn't process them. They can be provided either as a list of paths, or as a
bulk string.

You can either totally ignore files (they won't be looked at):

.. code-block:: yaml

 extends: default

 ignore: |
   /this/specific/file.yaml
   all/this/directory/
   *.template.yaml

 # or:

 ignore:
   - /this/specific/file.yaml
   - all/this/directory/
   - '*.template.yaml'

or ignore paths only for specific rules:

.. code-block:: yaml

 extends: default

 rules:
   trailing-spaces:
     ignore: |
       /this-file-has-trailing-spaces-but-it-is-OK.yaml
       /generated/*.yaml

 # or:

 rules:
   trailing-spaces:
     ignore:
       - /this-file-has-trailing-spaces-but-it-is-OK.yaml
       - /generated/*.yaml

Note that this ``.gitignore``-style path pattern allows complex path
exclusion/inclusion, see the `pathspec README file
<https://pypi.org/project/pathspec/>`_ for more details. Here is a more complex
example:

.. code-block:: yaml

 # For all rules
 ignore: |
   *.dont-lint-me.yaml
   /bin/
   !/bin/*.lint-me-anyway.yaml

 extends: default

 rules:
   key-duplicates:
     ignore: |
       generated
       *.template.yaml
   trailing-spaces:
     ignore: |
       *.ignore-trailing-spaces.yaml
       ascii-art/*

You can also use the ``.gitignore`` file (or any list of files) through:

.. code-block:: yaml

 ignore-from-file: .gitignore

or:

.. code-block:: yaml

 ignore-from-file: [.gitignore, .yamlignore]

.. note:: However, this is mutually exclusive with the ``ignore`` key.

If you need to know the exact list of files that yamllint would process,
without really linting them, you can use ``--list-files``:

.. code:: bash

 yamllint --list-files .

Setting the locale
------------------

It is possible to set the ``locale`` option globally. This is passed to Python's
`locale.setlocale
<https://docs.python.org/3/library/locale.html#locale.setlocale>`_,
so an empty string ``""`` will use the system default locale, while e.g.
``"en_US.UTF-8"`` will use that.

Currently this only affects the ``key-ordering`` rule. The default will order
by Unicode code point number, while locales will sort case and accents
properly as well.

.. code-block:: yaml

 extends: default

 locale: en_US.UTF-8

Configuration
=============

yamllint uses a set of *rules* to check sources files for problems. Each rule is
independent from the others, and can be enabled, disabled or tweaked. All these
settings can be gathered in a configuration file.

To use a custom configuration file, either name it ``.yamllint`` in your working
directory, or use the ``-c`` option:

.. code:: bash

 yamllint -c ~/myconfig file.yml

Default configuration
---------------------

Unless told otherwise, yamllint uses its ``default`` configuration:

.. literalinclude:: ../yamllint/conf/default.yml
   :language: yaml

Details on rules can be found on :doc:`the rules page <rules>`.

There is another pre-defined configuration named ``relaxed``. As its name
suggests, it is more tolerant.

It can be chosen using:

.. code:: bash

 yamllint -d relaxed file.yml

Extending the default configuration
-----------------------------------

When writing a custom configuration file, you don't need to redefine every rule.
Just extend the ``default`` configuration (or any already-existing configuration
file).

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

 yamllint -d "{extends: relaxed, rules: {line-length: {max: 120}}}" file.yml

Errors and warnings
-------------------

Problems detected by yamllint can be raised either as errors or as warnings.

In both cases, the script will output them (with different colors when using the
``standard`` output format), but the exit code can be different. More precisely,
the script will exit will a failure code *only when* there is one or more
error(s).

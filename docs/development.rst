Development
===========

yamllint provides both a script and a Python module. The latter can be used to
write your own linting tools.

Basic example of running the linter from Python:

.. code-block:: python

   import yamllint

   yaml_config = yamllint.config.YamlLintConfig("extends: default")
   for p in yamllint.linter.run(open("example.yaml", "r"), yaml_config):
       print(p.desc, p.line, p.rule)

.. automodule:: yamllint.linter
   :members:

Develop rule plugins
---------------------

yamllint provides a plugin mechanism using setuptools (pkg_resources) to allow
adding custom rules. So, you can extend yamllint and add rules with your own
custom yamllint rule plugins if you developed them.

yamllint plugins are Python packages installable using pip and distributed
under GPLv3+. To develop yamllint rules, it is recommended to copy the example
from ``tests/yamllint_plugin_example``, and follow its README file.  Also, the
core rules themselves in ``yamllint/rules`` are good references.

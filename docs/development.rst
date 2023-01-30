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

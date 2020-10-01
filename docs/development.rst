Development
===========

yamllint provides both a script and a Python module. The latter can be used to
write your own linting tools.

Basic example of running the linter from Python:

.. code-block:: python

   import yamllint

   yaml_config = yamllint.config.YamlLintConfig("extends: default")
   for p in yamllint.linter.run("example.yaml", yaml_config):
       print(p.desc, p.line, p.rule)

.. automodule:: yamllint.linter
   :members:

Develop rule plugins
---------------------

yamllint provides a plugin mechanism using setuptools (pkg_resources) to allow
adding custom rules. So, you can extend yamllint and add rules with your own
custom yamllint rule plugins if you developed them.

Yamllint rule plugins must satisfy the followings.

#. It must be a Python package installable using pip and distributed under
   GPLv3+ same as yamllint.
#. It must contains the entry point configuration in ``setup.cfg`` or something
   similar packaging configuration files, to make it installed and working as a
   yamllint plugin like below. (``<plugin_name>`` is that plugin name and
   ``<plugin_src_dir>`` is a dir where the rule modules exist.)
   ::

     [options.entry_points]
     yamllint.plugins.rules =
          <plugin_name> = <plugin_src_dir>

#. It must contain custom yamllint rule modules:

   - Each rule module must define a couple of global variables, ID and TYPE. ID
     must not conflicts with other rules' ID.
   - Each rule module must define a function named 'check' to test input data
     complies with the rule.
   - Each rule module may have other global variables.

     - CONF to define its configuration parameters and those types.
     - DEFAULT to provide default values for each configuration parameters.

#. It must define a global variable RULES_MAP to provide mappings of rule ID
   and rule modules to yamllint like this.
   ::

     RULES_MAP = {
         # rule ID: rule module
         a_custom_rule.ID: a_custom_rule
     }

To develop yamllint rules, the default rules themselves in yamllint may become
good references.

yamllint plugin example
=======================

This is a yamllint plugin example as a reference, contains the following rules.

- ``forbid-comments`` to forbid comments
- ``random-failure`` to fail randomly

To enable thes rules in yamllint, you must add them to your `yamllint config
file <https://yamllint.readthedocs.io/en/stable/configuration.html>`_:

.. code-block:: yaml

 extends: default

 rules:
   forbid-comments: enable
   random-failure: enable

How to develop rule plugins
---------------------------

yamllint rule plugins must satisfy the followings.

#. It must be a Python package installable using pip and distributed under
   GPLv3+ same as yamllint.

   How to make a Python package is beyond the scope of this README file. Please
   refer to the official guide (`Python Packaging User Guide
   <https://packaging.python.org/>`_ ) and related documents.

#. It must contains the entry point configuration in ``setup.cfg`` or something
   similar packaging configuration files, to make it installed and working as a
   yamllint plugin like below. (``<plugin_name>`` is that plugin name and
   ``<plugin_src_dir>`` is a dir where the rule modules exist.)
   ::

     [options.entry_points]
     yamllint.plugins.rules =
          <plugin_name> = <plugin_src_dir>

#. It must contain custom yamllint rule modules:

   - Each rule module must define a couple of global variables, ``ID`` and
     ``TYPE``. ``ID`` must not conflicts with other rules' IDs.
   - Each rule module must define a function named 'check' to test input data
     complies with the rule.
   - Each rule module may have other global variables.
     - ``CONF`` to define its configuration parameters and those types.
     - ``DEFAULT`` to provide default values for each configuration parameters.

#. It must define a global variable ``RULES`` to provide an iterable object, a
   tuple or a list for example, of tuples of rule ID and rule modules to
   yamllint like this.
   ::

     RULES = (
         # (rule module ID, rule module)
         (a_custom_rule_module.ID, a_custom_rule_module),
         (other_custom_rule_module.ID, other_custom_rule_module),
     )

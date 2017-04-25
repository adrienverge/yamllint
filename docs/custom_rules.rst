Custom Rules
============

There are times when you might like to add custom rules to your
project.  This could be because the rules you'd like to enforce are
not general enough to consider including in upstream yamllint.

yamllint will look for custom rules in ``.yamllint/rules``.  To enable
a custom rule you need to explicitly reference the rule in your
config.

Example
~~~~~~~

In this example there is a custom rule called ``truthy`` that will
complain if ambiguous truthy values are not quoted.

This is the directory structure:

.. code:: plain

   .
   |-- .yamllint
   |   |-- config
   |   `-- rules
   |       |-- __init__.py
   |       `-- truthy.py
   `-- example.yml

   2 directories, 4 files

This is an example yaml file with ambiguous truthy values:

.. code:: yaml

   ---
   a: y
   b: yes
   c: on
   d: True

This is an example config file:

.. code:: yaml

   ---
   extends: default

   rules:
     truthy: enable

Lint problems from the custom rule are now included in the yamllint
output:

.. code:: plain

   $ yamllint example.yml
   example.yml
     2:3       error    ambiguous truthy value is not quoted  (truthy)
     3:3       error    ambiguous truthy value is not quoted  (truthy)
     4:3       error    ambiguous truthy value is not quoted  (truthy)
     5:3       error    ambiguous truthy value is not quoted  (truthy)

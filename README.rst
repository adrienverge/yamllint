yamllint
========

A linter for YAML files.

.. image::
   https://travis-ci.org/adrienverge/yamllint.svg?branch=master
   :target: https://travis-ci.org/adrienverge/yamllint
.. image::
   https://coveralls.io/repos/github/adrienverge/yamllint/badge.svg?branch=master
   :target: https://coveralls.io/github/adrienverge/yamllint?branch=master

Compatible with Python 2 & 3.

Documentation
-------------

http://yamllint.readthedocs.org/

Short overview
--------------

Installation
^^^^^^^^^^^^

.. code:: bash

 pip install yamllint

Usage
^^^^^

.. code:: bash

 # Lint one or more files
 yamllint my_file.yml my_other_file.yaml ...

.. code:: bash

 # Lint all YAML files in a directory
 yamllint .

.. code:: bash

 # Use a custom lint configuration
 yamllint -c ~/myconfig file.yml

.. code:: bash

 # Output a parsable format (for syntax checking in editors like Vim, emacs...)
 yamllint -f parsable file.yml

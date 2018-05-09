Quickstart
==========

Installing yamllint
-------------------

On Fedora / CentOS:

.. code:: bash

 sudo dnf install yamllint

On Debian 8+ / Ubuntu 16.04+:

.. code:: bash

 sudo apt-get install yamllint

On Mac OS 10.11+:

.. code:: bash

 brew install yamllint

Alternatively using pip, the Python package manager:

.. code:: bash

 pip install --user yamllint

If you prefer installing from source, you can run, from the source directory:

.. code:: bash

 python setup.py sdist
 pip install --user dist/yamllint-*.tar.gz

Running yamllint
----------------

Basic usage:

.. code:: bash

 yamllint file.yml other-file.yaml

You can also lint all YAML files in a whole directory:

.. code:: bash

 yamllint .

The output will look like (colors are not displayed here):

::

 file.yml
   1:4       error    trailing spaces  (trailing-spaces)
   4:4       error    wrong indentation: expected 4 but found 3  (indentation)
   5:4       error    duplication of key "id-00042" in mapping  (key-duplicates)
   6:6       warning  comment not indented like content  (comments-indentation)
   12:6      error    too many spaces after hyphen  (hyphens)
   15:12     error    too many spaces before comma  (commas)

 other-file.yaml
   1:1       warning  missing document start "---"  (document-start)
   6:81      error    line too long (87 > 80 characters)  (line-length)
   10:1      error    too many blank lines (4 > 2)  (empty-lines)
   11:4      error    too many spaces inside braces  (braces)

Add the ``-f parsable`` arguments if you need an output format parsable by a
machine (for instance for :doc:`syntax highlighting in text editors
<text_editors>`). The output will then look like:

::

 file.yml:6:2: [warning] missing starting space in comment (comments)
 file.yml:57:1: [error] trailing spaces (trailing-spaces)
 file.yml:60:3: [error] wrong indentation: expected 4 but found 2 (indentation)

If you have a custom linting configuration file (see :doc:`how to configure
yamllint <configuration>`), it can be passed to yamllint using the ``-c``
option:

.. code:: bash

 yamllint -c ~/myconfig file.yaml

.. note::

   If you have a ``.yamllint`` file in your working directory, it will be
   automatically loaded as configuration by yamllint.

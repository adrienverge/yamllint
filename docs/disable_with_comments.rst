Disable with comments
=====================

Disabling checks for a specific line
------------------------------------

To prevent yamllint from reporting problems for a specific line, add a
directive comment (``# yamllint disable-line ...``) on that line, or on the
line above. For instance:

.. code-block:: yaml

 # The following mapping contains the same key twice,
 # but I know what I'm doing:
 - key: value 1
   key: value 2  # yamllint disable-line rule:key-duplicates

 - This line is waaaaaaaaaay too long but yamllint will not report anything about it.  # yamllint disable-line rule:line-length
 - This line will be checked by yamllint.

or:

.. code-block:: yaml

 # The following mapping contains the same key twice,
 # but I know what I'm doing:
 - key: value 1
   # yamllint disable-line rule:key-duplicates
   key: value 2

 # yamllint disable-line rule:line-length
 - This line is waaaaaaaaaay too long but yamllint will not report anything about it.
 - This line will be checked by yamllint.

It is possible, although not recommend, to disabled **all** rules for a
specific line:

.. code-block:: yaml

 # yamllint disable-line
 -  {    all : rules ,are disabled   for this line}

You can't make yamllint ignore invalid YAML syntax on a line (which generates a
`syntax error`), such as when templating a YAML file with Jinja. In some cases,
you can workaround this by putting the templating syntax in a YAML comment. See
`Putting template flow control in comments`_.

If you need to disable multiple rules, it is allowed to chain rules like this:
``# yamllint disable-line rule:hyphens rule:commas rule:indentation``.

Disabling checks for all (or part of) the file
----------------------------------------------

To prevent yamllint from reporting problems for the whole file, or for a block
of lines within the file, use ``# yamllint disable ...`` and ``# yamllint
enable ...`` directive comments. For instance:

.. code-block:: yaml

 # yamllint disable rule:colons
 - Lorem       : ipsum
   dolor       : sit amet,
   consectetur : adipiscing elit
 # yamllint enable rule:colons

 - rest of the document...

It is possible, although not recommend, to disabled **all** rules:

.. code-block:: yaml

 # yamllint disable
 - Lorem       :
         ipsum:
           dolor : [   sit,amet]
 -         consectetur : adipiscing elit
 # yamllint enable

If you need to disable multiple rules, it is allowed to chain rules like this:
``# yamllint disable rule:hyphens rule:commas rule:indentation``.

Disabling all checks for a file
-------------------------------

To prevent yamllint from reporting problems for a specific file, add the
directive comment ``# yamllint disable-file`` as the first line of the file.
For instance:

.. code-block:: yaml

 # yamllint disable-file
 # The following mapping contains the same key twice, but I know what I'm doing:
 - key: value 1
   key: value 2

 - This line is waaaaaaaaaay too long but yamllint will not report anything about it.

or:

.. code-block:: jinja

 # yamllint disable-file
 # This file is not valid YAML because it is a Jinja template
 {% if extra_info %}
 key1: value1
 {% endif %}
 key2: value2

Putting template flow control in comments
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Alternatively for templating you can wrap the template statements in comments
to make it a valid YAML file. As long as the templating language doesn't use
the same comment symbol, it should be a valid template and valid YAML (pre and
post-template processing).

Example of a Jinja2 code that cannot be parsed as YAML because it contains
invalid tokens ``{%`` and ``%}``:

.. code-block:: text

 # This file IS NOT valid YAML and will produce syntax errors
 {% if extra_info %}
 key1: value1
 {% endif %}
 key2: value2

But it can be fixed using YAML comments:

.. code-block:: yaml

 # This file IS valid YAML because the Jinja is in a YAML comment
 # {% if extra_info %}
 key1: value1
 # {% endif %}
 key2: value2

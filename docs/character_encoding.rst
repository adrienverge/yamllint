Character Encoding
==================

When yamllint reads a file (whether its a configuration file or a file to
lint), yamllint will try to automatically detect that file’s character
encoding. In order for the automatic detection to work properly, files must
follow these two rules (see `this section of the YAML specification for details
<https://yaml.org/spec/1.2.2/#52-character-encodings>`_):

* The file must be encoded in UTF-8, UTF-16 or UTF-32.

* The file must begin with either a byte order mark or an ASCII character.

Override character encoding
---------------------------

Previous versions of yamllint did not try to autodetect the character encoding
of files. Previous versions of yamllint assumed that files used the current
locale’s character encoding. This meant that older versions of yamllint would
sometimes correctly decode files that didn’t follow those two rules. For the
sake of backwards compatibility, the current version of yamllint allows you to
disable automatic character encoding detection by setting the
``YAMLLINT_FILE_ENCODING`` environment variable. If you set the
``YAMLLINT_FILE_ENCODING`` environment variable to the `the name of one of
Python’s standard character encodings
<https://docs.python.org/3/library/codecs.html#standard-encodings>`_, then
yamllint will use that character encoding instead of trying to autodetect the
character encoding.

The ``YAMLLINT_FILE_ENCODING`` environment variable should only be used as a
stopgap solution. If you need to use ``YAMLLINT_FILE_ENCODING``, then you
should really update your YAML files so that their character encoding can
automatically be detected, or else you may run into compatibility problems.
Future versions of yamllint may remove support for the
``YAMLLINT_FILE_ENCODING`` environment variable, and other YAML processors may
misinterpret your YAML files.

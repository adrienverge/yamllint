Changelog
=========

1.26.0 (2021-01-29)
-------------------

- End support for Python 2 and Python 3.4, add support for Python 3.9
- Add ``forbid: non-empty`` option to ``braces`` and ``brackets`` rules
- Fix ``quoted-strings`` for explicit octal recognition
- Add documentation for integration with Arcanist
- Fix typos in changelog and README
- Stop using deprecated ``python setup.py test`` in tests

1.25.0 (2020-09-29)
-------------------

- Run tests on Travis both with and without UTF-8 locales
- Improve documentation with default values to rules with options
- Improve documentation with a Python API usage example
- Fix documentation on ``commas`` examples
- Packaging: move setuptools' configuration from ``setup.py`` to ``setup.cfg``
- Packaging: add extra info in PyPI metadata
- Improve documentation on ``yaml-files``
- Fix ``octal-values`` to prevent detection of ``8`` and ``9`` as octal values
- Fix ``quoted-strings`` Fix detecting strings with hashtag as requiring quotes
- Add ``forbid`` configuration to the ``braces`` and ``brackets`` rules
- Fix runtime dependencies missing ``setuptools``
- Add a new output format for GitHub Annotations (``--format github``)
- Fix DOS lines messing with rule IDs in directives

1.24.2 (2020-07-16)
-------------------

- Add ``locale`` config option and make ``key-ordering`` locale-aware

1.24.1 (2020-07-15)
-------------------

- Revert ``locale`` config option from version 1.24.0 because of a bug

1.24.0 (2020-07-15)
-------------------

- Specify config with environment variable ``YAMLLINT_CONFIG_FILE``
- Fix bug with CRLF in ``new-lines`` and ``require-starting-space``
- Do not run linter on directories whose names look like YAML files
- Add ``locale`` config option and make ``key-ordering`` locale-aware

1.23.0 (2020-04-17)
-------------------

- Allow rules to validate their configuration
- Add options ``extra-required`` and ``extra-allowed`` to ``quoted-strings``

1.22.1 (2020-04-15)
-------------------

- Fix ``quoted-strings`` rule with ``only-when-needed`` on corner cases

1.22.0 (2020-04-13)
-------------------

- Add ``check-keys`` option to the ``truthy`` rule
- Fix ``quoted-strings`` rule not working on sequences items
- Sunset Python 2

1.21.0 (2020-03-24)
-------------------

- Fix ``new-lines`` rule on Python 3 with DOS line endings
- Fix ``quoted-strings`` rule not working for string values matching scalars
- Add ``required: only-when-needed`` option to the ``quoted-strings`` rule

1.20.0 (2019-12-26)
-------------------

- Add --no-warnings option to suppress warning messages
- Use 'syntax' as rule name upon syntax errors

1.19.0 (2019-11-19)
-------------------

- Allow disabling all checks for a file with ``# yamllint disable-file``

1.18.0 (2019-10-15)
-------------------

- Lint ``.yamllint`` config file by default
- Also read config from ``.yamllint.yml`` and ``.yamllint.yaml``
- Improve documentation for ``yaml-files``
- Update documentation for ``pre-commit``
- Explicitly disable ``empty-values`` and ``octal-values`` rules

1.17.0 (2019-08-12)
-------------------

- Simplify installation instructions in the README
- Add OpenBSD installation instructions
- Make YAML file extensions configurable

1.16.0 (2019-06-07)
-------------------

- Add FreeBSD installation instructions
- Fix the ``line`` rule to correctly handle DOS new lines
- Add the ``allowed-values`` option to the ``truthy`` rule
- Allow configuration options to be a list of enums

1.15.0 (2019-02-11)
-------------------

- Allow linting from standard input with ``yamllint -``

1.14.0 (2019-01-14)
-------------------

- Fix documentation code snippets
- Drop Python 2.6 and 3.3 support, add Python 3.7 support
- Update documentation and tests for ``line-length`` + Unicode + Python 2
- Allow rule configurations to lack options
- Add a new ``ignore-shebangs`` option for the ``comments`` rule

1.13.0 (2018-11-14)
-------------------

- Use ``isinstance(x, y)`` instead of ``type(x) == y``
- Add a new ``-f colored`` option
- Update documentation about colored output when run from CLI

1.12.1 (2018-10-17)
-------------------

- Fix the ``quoted-strings`` rule, broken implementation
- Fix missing documentation for the ``quoted-strings`` rule

1.12.0 (2018-10-04)
-------------------

- Add a new ``quoted-strings`` rule
- Update installation documentation for pip, CentOS, Debian, Ubuntu, Mac OS

1.11.1 (2018-04-06)
-------------------

- Handle merge keys (``<<``) in the ``key-duplicates`` rule
- Update documentation about pre-commit
- Make examples for ``ignore`` rule clearer
- Clarify documentation on the 'truthy' rule
- Fix crash in parser due to a change in PyYAML > 3.12

1.11.0 (2018-02-21)
-------------------

- Add a new ``octal-values`` rule

1.10.0 (2017-11-05)
-------------------

- Fix colored output on Windows
- Check documentation compilation on continuous integration
- Add a new ``empty-values`` rule
- Make sure test files are included in dist bundle
- Tests: Use en_US.UTF-8 locale when C.UTF-8 not available
- Tests: Dynamically detect Python executable path

1.9.0 (2017-10-16)
------------------

- Add a new ``key-ordering`` rule
- Fix indentation rule for key following empty list

1.8.2 (2017-10-10)
------------------

- Be clearer about the ``ignore`` conf type
- Update pre-commit hook file
- Add documentation for pre-commit

1.8.1 (2017-07-04)
------------------

- Require pathspec >= 0.5.3
- Support Python 2.6
- Add a changelog

1.8.0 (2017-06-28)
------------------

- Refactor argparse with mutually_exclusive_group
- Add support to ignore paths in configuration

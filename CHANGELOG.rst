Changelog
=========

1.12.0 (2018-10-04)
-------------------

- Add a new `quoted-strings` rule
- Update installation documentation for pip, CentOS, Debian, Ubuntu, Mac OS

1.11.1 (2018-04-06)
-------------------

- Handle merge keys (`<<`) in the `key-duplicates` rule
- Update documentation about pre-commit
- Make examples for `ignore` rule clearer
- Clarify documentation on the 'truthy' rule
- Fix crash in parser due to a change in PyYAML > 3.12

1.11.0 (2018-02-21)
-------------------

- Add a new `octal-values` rule

1.10.0 (2017-11-05)
-------------------

- Fix colored output on Windows
- Check documentation compilation on continuous integration
- Add a new `empty-values` rule
- Make sure test files are included in dist bundle
- Tests: Use en_US.UTF-8 locale when C.UTF-8 not available
- Tests: Dynamically detect Python executable path

1.9.0 (2017-10-16)
------------------

- Add a new `key-ordering` rule
- Fix indentation rule for key following empty list

1.8.2 (2017-10-10)
------------------

- Be clearer about the `ignore` conf type
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

Contributing
============

Pull requests are the best way to propose changes to the codebase.
Contributions are welcome, but they have to meet some criteria.

Pull Request Process
--------------------

1. Fork this Git repository and create your branch from ``master``.

2. Make sure the tests pass:

   .. code:: bash

    pip install --user .
    python -m unittest discover  # all tests...
    python -m unittest tests/rules/test_commas.py  # or just some tests (faster)

3. If you add code that should be tested, add tests.

4. Make sure the linters pass:

   .. code:: bash

    flake8 .

   If you added/modified documentation:

   .. code:: bash

    doc8 $(git ls-files '*.rst')

   If you touched YAML files:

   .. code:: bash

    yamllint --strict $(git ls-files '*.yaml' '*.yml')

5. If relevant, update documentation (either in ``docs`` directly or in rules
   files themselves).

6. Write a `good commit message
   <http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html>`_.
   If the pull request has multiple commits, each must be atomic (single
   irreducible change that makes sense on its own).

7. Then, open a pull request.

YAML Test Suite
---------------

The optional ``tests/yaml-test-suite`` submodule contains generated inputs from
`yaml/yaml-test-suite <https://github.com/yaml/yaml-test-suite>`_. Initialize it
from the repository root to include the corpus in ordinary unit tests:

.. code:: bash

   git submodule update --init tests/yaml-test-suite
   python -m unittest tests.test_yaml_test_suite

Without the data, discovery reports one explicit skipped corpus test. No test
performs downloads or generates data, and Docker is not needed. The dedicated
CI job initializes the submodule and uses the following required-data command;
missing or empty data is a failure with this command:

.. code:: bash

   python -m tests.test_yaml_test_suite

The gitlink pins data release ``data-2022-01-17`` to commit
``6e6c296ae9c9d2d5c4134b4b64d01b29ac19ff6f``. This release contains 402 inputs
(308 valid and 94 error-marked), including numbered subcases. Each input is
reported separately. All current rules, including optional rules, run with
their default options, and diagnostics are fully consumed. Style and syntax
diagnostics are accepted: this tests crash resistance, not YAML 1.2 conformance
or whether PyYAML accepts every input marked valid by the suite. No YAML
constructors or upstream generation scripts are executed.

The one known crash, ``4H7K``, is recorded in ``KNOWN_FAILURES`` with its exact
exception type and message and a link to the existing fix in PR 829. That case
still executes; a changed exception or unexpected pass fails the test so the
baseline must be reviewed. With Python 3.12 and PyYAML 6.0.3, the other
401 inputs complete without uncaught exceptions. Do not disable whole rules or
skip the corpus to accommodate a new crash.

To update the data, fetch the official repository's tags, choose a generated
``data-YYYY-MM-DD`` release, and check out its immutable commit in the
submodule.
Run both commands above and the full tests, inspect any new failures, update
the release/commit and counts here, then commit the updated gitlink. Do not
track the moving ``data`` branch or use ``git submodule update --remote``.
The corpus is MIT licensed; its notice is preserved in
``tests/yaml-test-suite.LICENSE`` (copied from the upstream source repository's
``License`` at ``da267a5c4782e7361e82889e76c0dc7df0e1e870``; the generated
release omits that file). Retain and review the notice when updating.

Source archives do not include the optional submodule data; their ordinary
tests report the same explicit skip. Use a Git checkout and initialize the
submodule to run corpus tests.

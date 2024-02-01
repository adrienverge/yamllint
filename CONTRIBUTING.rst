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

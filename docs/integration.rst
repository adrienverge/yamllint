Integration with other software
===============================

Integration with pre-commit
---------------------------

You can integrate yamllint in `pre-commit <http://pre-commit.com/>`_ tool.
Here is an example, to add in your .pre-commit-config.yaml

.. code:: yaml

  ---
  # Update the rev variable with the release version that you want, from the yamllint repo
  # You can pass your custom .yamllint with args attribute.
  - repo: https://github.com/adrienverge/yamllint.git
    rev: v1.17.0
    hooks:
      - id: yamllint
        args: [-c=/path/to/.yamllint]

Integration with GitHub Actions
-------------------------------

yamllint auto-detects when it's running inside of `GitHub
Actions<https://github.com/features/actions>` and automatically uses the suited
output format to decorate code with linting errors automatically. You can also
force the GitHub Actions output with ``yamllint --format github``.

An example workflow using GitHub Actions:

.. code:: yaml

   ---
   name: yamllint test

   on: push

   jobs:
     test:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v2

         - name: Set up Python
           uses: actions/setup-python@v2
           with:
             python-version: 3.8

         - name: Install yamllint
           run: pip install yamllint

         - name: Lint YAML files
           run: yamllint .

Integration with Arcanist
-------------------------

You can configure yamllint to run on ``arc lint``. Here is an example
``.arclint`` file that makes use of this configuration.

.. code:: json

  {
    "linters": {
      "yamllint": {
        "type": "script-and-regex",
        "script-and-regex.script": "yamllint",
        "script-and-regex.regex": "/^(?P<line>\\d+):(?P<offset>\\d+) +(?P<severity>warning|error) +(?P<message>.*) +\\((?P<name>.*)\\)$/m",
        "include": "(\\.(yml|yaml)$)"
      }
    }
  }

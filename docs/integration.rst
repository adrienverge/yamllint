Integration with other software
===============================

Integration with pre-commit
---------------------------

You can integrate yamllint in the `pre-commit <https://pre-commit.com/>`_ tool.
Here is an example, to add in your .pre-commit-config.yaml

.. code:: yaml

 ---
 # Update the rev variable with the release version that you want, from the yamllint repo
 # You can pass your custom .yamllint with args attribute.
 repos:
   - repo: https://github.com/adrienverge/yamllint.git
     rev: v1.29.0
     hooks:
       - id: yamllint
         args: [--strict, -c=/path/to/.yamllint]


Integration with GitHub Actions
-------------------------------

yamllint auto-detects when it's running inside of `GitHub
Actions <https://github.com/features/actions>`_ and automatically uses the
suited output format to decorate code with linting errors. You can also force
the GitHub Actions output with ``yamllint --format github``.

A minimal example workflow using GitHub Actions:

.. code:: yaml

 ---
 on: push  # yamllint disable-line rule:truthy

 jobs:
   lint:
     runs-on: ubuntu-latest
     steps:
       - uses: actions/checkout@v3

       - name: Install yamllint
         run: pip install yamllint

       - name: Lint YAML files
         run: yamllint .

Integration with GitLab
-----------------------

You can use the following GitLab CI/CD stage to run yamllint and get the
results as a `Code quality (Code Climate)
<https://docs.gitlab.com/ee/ci/testing/code_quality.html>` report.

.. code:: yaml

 ---
 lint:
   stage: lint
   script:
     - pip install yamllint
     - mkdir reports
     - >
       yamllint -f parsable . | tee >(awk '
       BEGIN {FS = ":"; ORS="\n"; first=1}
       {
           gsub(/^[ \t]+|[ \t]+$|"/, "", $4);
           match($4, /^\[(warning|error)\](.*)\((.*)\)$/, a);
           sev = (a[1] == "error" ? "major" : "minor");
           if (first) {
               first=0;
               printf("[");
           } else {
               printf(",");
           }
           printf("{\"location\":{\"path\":\"%s\",\"lines\":{\"begin\":%s",\
                  "\"end\":%s}},\"severity\":\"%s\",\"check_name\":\"%s\","\
                  "\"categories\":[\"Style\"],\"type\":\"issue\","\
                  "\"description\":\"%s\"}", $1, $2, $3, sev, a[3], a[2]);
       }
       END { if (!first) printf("]\n"); }' > reports/codequality.json)
   artifacts:
     when: always
     paths:
       - reports
     expire_in: 1 week
     reports:
       codequality: reports/codequality.json

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

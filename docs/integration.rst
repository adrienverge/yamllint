Integration with other software
===============================

Integration with pre-commit
---------------------------

You can integrate yamllint in `pre-commit <http://pre-commit.com/>`_ tool.
Here is an example, to add in your .pre-commit-config.yaml

.. code:: yaml

  ---
  # Update the sha variable with the release version that you want, from the yamllint repo
  - repo: https://github.com/adrienverge/yamllint.git
    sha: v1.8.1
    hooks:
      - id: yamllint

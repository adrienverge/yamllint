"""
Use this rule to forbid specific YAML types from being used as
keys in mappings.

This rule prevents the use of YAML type names as keys, which can cause
confusion or issues in some contexts. The rule is based on the YAML schema
types from https://perlpunk.github.io/YAML-PP-p5/schemas.html.

.. rubric:: Options

* ``forbid-null`` forbids keys named "null"
* ``forbid-bool`` forbids keys named "bool"
* ``forbid-int`` forbids keys named "int"
* ``forbid-float`` forbids keys named "float"
* ``forbid-str`` forbids keys named "str"

.. rubric:: Default values (when enabled)

.. code-block:: yaml

 rules:
   key-types:
     forbid-null: false
     forbid-bool: false
     forbid-int: false
     forbid-float: false
     forbid-str: false

.. rubric:: Examples

#. With ``key-types: {forbid-null: true, forbid-bool: true}``

   the following code snippet would **PASS**:
   ::

    valid_key: value
    another_key:
      - item0
      - "null"
      - item2

   the following code snippet would **FAIL**:
   ::

    null:
      valid: "somevalue"

   the following code snippet would **FAIL**:
   ::

    outer_key:
      bool:
        inner_key: value

#. With ``key-types: {forbid-int: true, forbid-float: true}``

   the following code snippet would **PASS**:
   ::

    valid_key: value
    number: 42

   the following code snippet would **FAIL**:
   ::

    int: 42

   the following code snippet would **FAIL**:
   ::

    float: 3.14
"""

import yaml

from yamllint.linter import LintProblem

ID = 'key-types'
TYPE = 'token'
CONF = {
    'forbid-null': bool,
    'forbid-bool': bool,
    'forbid-int': bool,
    'forbid-float': bool,
    'forbid-str': bool
}
DEFAULT = {
    'forbid-null': False,
    'forbid-bool': False,
    'forbid-int': False,
    'forbid-float': False,
    'forbid-str': False
}


def check(conf, token, prev, next, nextnext, context):
    if not isinstance(token, yaml.tokens.ScalarToken):
        return
    if token.style:
        return
    val = token.value

    if isinstance(token, yaml.tokens.ScalarToken):
        if conf['forbid-null'] and val == "null":
            yield LintProblem(
                token.start_mark.line + 1,
                token.start_mark.column + 1,
                'Found forbidden key type "null"')
        elif conf['forbid-bool'] and val == "bool":
            yield LintProblem(
                token.start_mark.line + 1,
                token.start_mark.column + 1,
                'Found forbidden key type "bool"')
        elif conf['forbid-int'] and val == "int":
            yield LintProblem(
                token.start_mark.line + 1,
                token.start_mark.column + 1,
                'Found forbidden key type "int"')
        elif conf['forbid-float'] and val == "float":
            yield LintProblem(
                token.start_mark.line + 1,
                token.start_mark.column + 1,
                'Found forbidden key type "float"')
        elif conf['forbid-str'] and val == "str":
            yield LintProblem(
                token.start_mark.line + 1,
                token.start_mark.column + 1,
                'Found forbidden key type "str"')

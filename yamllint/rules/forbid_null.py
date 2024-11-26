"""
Use this rule to ......

"""

import yaml
from yamllint.linter import LintProblem

ID = 'forbid-null'
TYPE = 'token'
CONF = {'forbid-null': bool}
DEFAULT = {'forbid-null': False}


def check(conf, token, prev, next, nextnext, context):
    if not isinstance(token, yaml.tokens.ScalarToken):
        return
    if token.style:
        return
    val = token.value

    if isinstance(token, yaml.tokens.ScalarToken):
        if val == "null":
            yield LintProblem(
                token.start_mark.line + 1,
                token.start_mark.column + 1,
                'Found key with value "null"')

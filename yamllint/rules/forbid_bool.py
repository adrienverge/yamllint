"""
Use this rule to ......

"""

import yaml
from yamllint.linter import LintProblem

ID = 'forbid-bool'
TYPE = 'token'
CONF = {'forbid-bool': bool}
DEFAULT = {'forbid-bool': False}


def check(conf, token, prev, next, nextnext, context):
    if not isinstance(token, yaml.tokens.ScalarToken):
        return
    if token.style:
        return
    val = token.value

    if isinstance(token, yaml.tokens.ScalarToken):
        if val == "bool":
            yield LintProblem(
                token.start_mark.line + 1,
                token.start_mark.column + 1,
                'Found key with value "bool"')

# Copyright (C) 2016 Adrien Vergé
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import json

from yamllint import APP_VERSION
from yamllint.linter import PROBLEM_LEVELS


def format_results(results, no_warn):
    max_level = 0

    sarif = {
        '$schema': 'https://raw.githubusercontent.com/oasis-tcs/sarif-spec'
                   '/master/Schemata/sarif-schema-2.1.0.json',
        'version': '2.1.0',
        'runs': [
            {
                'tool': {
                    'driver': {
                        'name': 'yamllint',
                        'version': APP_VERSION,
                        'informationUri': 'https://yamllint.readthedocs.io',
                        'rules': []
                    },
                },
                'results': []
            }
        ]
    }

    rules = {}
    max_rule_index = 0

    for file in results:
        for problem in results[file]:
            max_level = max(max_level, PROBLEM_LEVELS[problem.level])

            if problem.rule in rules:
                rule_index = rules[problem.rule]
            else:
                rule_index = max_rule_index
                rules[problem.rule] = max_rule_index
                sarif['runs'][0]['tool']['driver']['rules'].append(format_rule(
                    problem))
                max_rule_index += 1

            sarif['runs'][0]['results'].append(format_result(rule_index,
                                                             problem, file))

    print(json.dumps(sarif))

    return max_level


def format_rule(problem):
    uri = 'https://yamllint.readthedocs.io/en/v%s/rules.html#module-yamllint' \
          '.rules.%s' % (APP_VERSION, problem.rule)

    name = ''.join([word.capitalize() for word in problem.rule.split('-')])

    return {
        'id': problem.rule,
        'name': name,
        'defaultConfiguration': {
            'level': problem.level
        },
        'properties': {
            'description': problem.desc,
            'tags': [],
            'queryUri': uri,
        },
        'shortDescription': {
            'text': problem.desc
        },
        'fullDescription': {
            'text': problem.desc
        },
        'helpUri': uri,
        'help': {
            'text': 'More info: {}'.format(uri),
            'markdown': '[More info]({})'.format(uri)
        }
    }


def format_result(rule_index, problem, filename):
    return {
        'ruleId': problem.rule,
        'ruleIndex': rule_index,
        'message': {
            'text': problem.message
        },
        'locations': [
            {
                'physicalLocation': {
                    'artifactLocation': {
                        'uri': filename,
                        'uriBaseId': '%SRCROOT%'
                    },
                    'region': {
                        'startLine': problem.line,
                        'startColumn': problem.column
                    }
                }
            }
        ]
    }

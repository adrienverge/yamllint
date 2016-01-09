# -*- coding: utf-8 -*-
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

import os.path

import yaml

import yamllint.rules
from yamllint.errors import YamlLintConfigError


def get_extended_conf(name):
    # Is it a standard conf shipped with yamllint...
    if '/' not in name:
        std_conf = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                'conf', name + '.yml')

        if os.path.isfile(std_conf):
            return std_conf

    # or a custom conf on filesystem?
    return name


def extend_config(content):
    try:
        conf = yaml.safe_load(content)

        if 'rules' not in conf:
            conf['rules'] = {}

        # Does this conf override another conf that we need to load?
        if 'extends' in conf:
            base = parse_config_from_file(get_extended_conf(conf['extends']))

            base.update(conf['rules'])
            conf['rules'] = base

        return conf
    except Exception as e:
        raise YamlLintConfigError('invalid config: %s' % e)


def parse_config(content):
    conf = extend_config(content)
    rules = {}

    for id in conf['rules']:
        try:
            rule = yamllint.rules.get(id)
        except Exception as e:
            raise YamlLintConfigError('invalid config: %s' % e)

        if conf['rules'][id] == 'disable':
            continue

        rules[id] = {'level': 'error'}
        if type(conf['rules'][id]) == dict:
            if 'level' in conf['rules'][id]:
                if conf['rules'][id]['level'] not in ('error', 'warning'):
                    raise YamlLintConfigError(
                        'invalid config: level should be "error" or "warning"')
                rules[id]['level'] = conf['rules'][id]['level']

            options = getattr(rule, 'CONF', {})
            for optkey in conf['rules'][id]:
                if optkey == 'level':
                    continue
                if optkey not in options:
                    raise YamlLintConfigError(
                        'invalid config: unknown option "%s" for rule "%s"' %
                        (optkey, id))
                if type(conf['rules'][id][optkey]) != options[optkey]:
                    raise YamlLintConfigError(
                        'invalid config: option "%s" of "%s" should be %s' %
                        (optkey, id, options[optkey].__name__))
                rules[id][optkey] = conf['rules'][id][optkey]
        else:
            raise YamlLintConfigError(('invalid config: rule "%s": should be '
                                       'either "disable" or a dict') % id)
    return rules


def parse_config_from_file(path):
    with open(path) as f:
        return parse_config(f.read())


def get_enabled_rules(conf):
    return [yamllint.rules.get(r) for r in conf.keys() if conf[r] is not False]

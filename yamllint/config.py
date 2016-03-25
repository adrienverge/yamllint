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


class YamlLintConfigError(Exception):
    pass


class YamlLintConfig(object):
    def __init__(self, content=None, file=None):
        assert (content is None) ^ (file is None)

        if file is not None:
            with open(file) as f:
                content = f.read()

        self.parse(content)
        self.validate()

    def enabled_rules(self):
        return [yamllint.rules.get(id) for id, val in self.rules.items()
                if val is not False]

    def extend(self, base_config):
        assert isinstance(base_config, YamlLintConfig)

        for rule in self.rules:
            if (type(self.rules[rule]) == dict and
                    rule in base_config.rules and
                    base_config.rules[rule] is not False):
                base_config.rules[rule].update(self.rules[rule])
            else:
                base_config.rules[rule] = self.rules[rule]

        self.rules = base_config.rules

    def parse(self, raw_content):
        try:
            conf = yaml.safe_load(raw_content)
        except Exception as e:
            raise YamlLintConfigError('invalid config: %s' % e)

        if type(conf) != dict:
            raise YamlLintConfigError('invalid config: not a dict')

        self.rules = conf.get('rules', {})

        # Does this conf override another conf that we need to load?
        if 'extends' in conf:
            path = get_extended_config_file(conf['extends'])
            base = YamlLintConfig(file=path)
            try:
                self.extend(base)
            except Exception as e:
                raise YamlLintConfigError('invalid config: %s' % e)

    def validate(self):
        for id in self.rules:
            try:
                rule = yamllint.rules.get(id)
            except Exception as e:
                raise YamlLintConfigError('invalid config: %s' % e)

            self.rules[id] = validate_rule_conf(rule, self.rules[id])


def validate_rule_conf(rule, conf):
    if conf is False or conf == 'disable':
        return False
    elif conf == 'enable':
        conf = {}

    if type(conf) == dict:
        if 'level' not in conf:
            conf['level'] = 'error'
        elif conf['level'] not in ('error', 'warning'):
            raise YamlLintConfigError(
                'invalid config: level should be "error" or "warning"')

        options = getattr(rule, 'CONF', {})
        for optkey in conf:
            if optkey == 'level':
                continue
            if optkey not in options:
                raise YamlLintConfigError(
                    'invalid config: unknown option "%s" for rule "%s"' %
                    (optkey, rule.ID))
            if type(options[optkey]) == tuple:
                if (conf[optkey] not in options[optkey] and
                        type(conf[optkey]) not in options[optkey]):
                    raise YamlLintConfigError(
                        'invalid config: option "%s" of "%s" should be in %s'
                        % (optkey, rule.ID, options[optkey]))
            else:
                if type(conf[optkey]) != options[optkey]:
                    raise YamlLintConfigError(
                        'invalid config: option "%s" of "%s" should be %s'
                        % (optkey, rule.ID, options[optkey].__name__))
        for optkey in options:
            if optkey not in conf:
                raise YamlLintConfigError(
                    'invalid config: missing option "%s" for rule "%s"' %
                    (optkey, rule.ID))
    else:
        raise YamlLintConfigError(('invalid config: rule "%s": should be '
                                   'either "enable", "disable" or a dict')
                                  % rule.ID)

    return conf


def get_extended_config_file(name):
    # Is it a standard conf shipped with yamllint...
    if '/' not in name:
        std_conf = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                'conf', name + '.yaml')

        if os.path.isfile(std_conf):
            return std_conf

    # or a custom conf on filesystem?
    return name

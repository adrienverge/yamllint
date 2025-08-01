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

import pathspec
import yaml

from yamllint import decoder
import yamllint.rules


class YamlLintConfigError(Exception):
    pass


class YamlLintConfig:
    def __init__(self, content=None, file=None):
        assert (content is None) ^ (file is None)

        self.ignore = None

        self.yaml_files = pathspec.PathSpec.from_lines(
            'gitwildmatch', ['*.yaml', '*.yml', '.yamllint'])

        self.locale = None

        if file is not None:
            with open(file, mode='rb') as f:
                content = decoder.auto_decode(f.read())

        self.parse(content)
        self.validate()

    def is_file_ignored(self, filepath):
        return self.ignore and self.ignore.match_file(filepath)

    def is_yaml_file(self, filepath):
        return self.yaml_files.match_file(os.path.basename(filepath))

    def enabled_rules(self, filepath):
        return [yamllint.rules.get(id) for id, val in self.rules.items()
                if val is not False and (
                    filepath is None or 'ignore' not in val or
                    not val['ignore'].match_file(filepath))]

    def extend(self, base_config):
        assert isinstance(base_config, YamlLintConfig)

        for rule in self.rules:
            if (isinstance(self.rules[rule], dict) and
                    rule in base_config.rules and
                    base_config.rules[rule] is not False):
                base_config.rules[rule].update(self.rules[rule])
            else:
                base_config.rules[rule] = self.rules[rule]

        self.rules = base_config.rules

        if base_config.ignore is not None:
            self.ignore = base_config.ignore

    def parse(self, raw_content):
        try:
            conf = yaml.safe_load(raw_content)
        except Exception as e:
            raise YamlLintConfigError(f'invalid config: {e}') from e

        if not isinstance(conf, dict):
            raise YamlLintConfigError('invalid config: not a mapping')

        self.rules = conf.get('rules', {})
        if not isinstance(self.rules, dict):
            raise YamlLintConfigError('invalid config: rules should be a '
                                      'mapping')
        for rule in self.rules:
            if self.rules[rule] == 'enable':
                self.rules[rule] = {}
            elif self.rules[rule] == 'disable':
                self.rules[rule] = False

        # Does this conf override another conf that we need to load?
        if 'extends' in conf:
            path = get_extended_config_file(conf['extends'])
            base = YamlLintConfig(file=path)
            try:
                self.extend(base)
            except Exception as e:
                raise YamlLintConfigError(f'invalid config: {e}') from e

        if 'ignore' in conf and 'ignore-from-file' in conf:
            raise YamlLintConfigError(
                'invalid config: ignore and ignore-from-file keys cannot be '
                'used together')
        elif 'ignore-from-file' in conf:
            if isinstance(conf['ignore-from-file'], str):
                conf['ignore-from-file'] = [conf['ignore-from-file']]
            if not (isinstance(conf['ignore-from-file'], list) and all(
                    isinstance(ln, str) for ln in conf['ignore-from-file'])):
                raise YamlLintConfigError(
                    'invalid config: ignore-from-file should contain '
                    'filename(s), either as a list or string')
            self.ignore = pathspec.PathSpec.from_lines(
                'gitwildmatch',
                decoder.lines_in_files(conf['ignore-from-file'])
            )
        elif 'ignore' in conf:
            if isinstance(conf['ignore'], str):
                self.ignore = pathspec.PathSpec.from_lines(
                    'gitwildmatch', conf['ignore'].splitlines())
            elif (isinstance(conf['ignore'], list) and
                    all(isinstance(line, str) for line in conf['ignore'])):
                self.ignore = pathspec.PathSpec.from_lines(
                    'gitwildmatch', conf['ignore'])
            else:
                raise YamlLintConfigError(
                    'invalid config: ignore should contain file patterns')

        if 'yaml-files' in conf:
            if not (isinstance(conf['yaml-files'], list)
                    and all(isinstance(i, str) for i in conf['yaml-files'])):
                raise YamlLintConfigError(
                    'invalid config: yaml-files '
                    'should be a list of file patterns')
            self.yaml_files = pathspec.PathSpec.from_lines('gitwildmatch',
                                                           conf['yaml-files'])

        if 'locale' in conf:
            if not isinstance(conf['locale'], str):
                raise YamlLintConfigError(
                    'invalid config: locale should be a string')
            self.locale = conf['locale']

    def validate(self):
        for id in self.rules:
            try:
                rule = yamllint.rules.get(id)
            except Exception as e:
                raise YamlLintConfigError(f'invalid config: {e}') from e

            self.rules[id] = validate_rule_conf(rule, self.rules[id])


def validate_rule_conf(rule, conf):
    if conf is False:  # disable
        return False

    if isinstance(conf, dict):
        if ('ignore-from-file' in conf and not isinstance(
                conf['ignore-from-file'], pathspec.pathspec.PathSpec)):
            if isinstance(conf['ignore-from-file'], str):
                conf['ignore-from-file'] = [conf['ignore-from-file']]
            if not (isinstance(conf['ignore-from-file'], list)
                    and all(isinstance(line, str)
                            for line in conf['ignore-from-file'])):
                raise YamlLintConfigError(
                    'invalid config: ignore-from-file should contain '
                    'valid filename(s), either as a list or string')
            conf['ignore'] = pathspec.PathSpec.from_lines(
                'gitwildmatch',
                decoder.lines_in_files(conf['ignore-from-file'])
            )
        elif ('ignore' in conf and not isinstance(
                conf['ignore'], pathspec.pathspec.PathSpec)):
            if isinstance(conf['ignore'], str):
                conf['ignore'] = pathspec.PathSpec.from_lines(
                    'gitwildmatch', conf['ignore'].splitlines())
            elif (isinstance(conf['ignore'], list) and
                    all(isinstance(line, str) for line in conf['ignore'])):
                conf['ignore'] = pathspec.PathSpec.from_lines(
                    'gitwildmatch', conf['ignore'])
            else:
                raise YamlLintConfigError(
                    'invalid config: ignore should contain file patterns')

        if 'level' not in conf:
            conf['level'] = 'error'
        elif conf['level'] not in ('error', 'warning'):
            raise YamlLintConfigError(
                'invalid config: level should be "error" or "warning"')

        options = getattr(rule, 'CONF', {})
        options_default = getattr(rule, 'DEFAULT', {})
        for optkey in conf:
            if optkey in ('ignore', 'ignore-from-file', 'level'):
                continue
            if optkey not in options:
                raise YamlLintConfigError(
                    f'invalid config: unknown option "{optkey}" for rule '
                    f'"{rule.ID}"')
            # Example: CONF = {option: (bool, 'mixed')}
            #          → {option: true}         → {option: mixed}
            if isinstance(options[optkey], tuple):
                if (conf[optkey] not in options[optkey] and
                        type(conf[optkey]) not in options[optkey]):
                    raise YamlLintConfigError(
                        f'invalid config: option "{optkey}" of "{rule.ID}" '
                        f'should be in {options[optkey]}')
            # Example: CONF = {option: ['flag1', 'flag2', int]}
            #          → {option: [flag1]}      → {option: [42, flag1, flag2]}
            elif isinstance(options[optkey], list):
                if (not isinstance(conf[optkey], list) or
                        any(flag not in options[optkey] and
                            type(flag) not in options[optkey]
                            for flag in conf[optkey])):
                    raise YamlLintConfigError(
                        f'invalid config: option "{optkey}" of "{rule.ID}" '
                        f'should only contain values in {options[optkey]}')
            # Example: CONF = {option: int}
            #          → {option: 42}
            else:
                if not isinstance(conf[optkey], options[optkey]):
                    raise YamlLintConfigError(
                        f'invalid config: option "{optkey}" of "{rule.ID}" '
                        f'should be {options[optkey].__name__}')
        for optkey in options:
            if optkey not in conf:
                conf[optkey] = options_default[optkey]

        if hasattr(rule, 'VALIDATE'):
            res = rule.VALIDATE(conf)
            if res:
                raise YamlLintConfigError(f'invalid config: {rule.ID}: {res}')
    else:
        raise YamlLintConfigError(
            f'invalid config: rule "{rule.ID}": should be either "enable", '
            f'"disable" or a mapping')

    return conf


def get_extended_config_file(name):
    # Is it a standard conf shipped with yamllint...
    if '/' not in name:
        std_conf = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                'conf', f'{name}.yaml')

        if os.path.isfile(std_conf):
            return std_conf

    # or a custom conf on filesystem?
    return name

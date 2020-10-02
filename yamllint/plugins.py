# -*- coding: utf-8 -*-
# Copyright (C) 2020 Satoru SATOH
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
"""
Plugin module utilizing setuptools (pkg_resources) to allow users to add their
own custom lint rules.
"""
import warnings

import pkg_resources


PACKAGE_GROUP = "yamllint.plugins.rules"


def validate_rule_module(rule_mod):
    """Test if given rule module is valid.
    """
    return (getattr(rule_mod, "ID", False) and
            getattr(rule_mod, "TYPE", False)
            ) and callable(getattr(rule_mod, "check", False))


def load_plugin_rules_itr(entry_points=None, group=PACKAGE_GROUP):
    """Load custom lint rule plugins."""
    if not entry_points:
        entry_points = pkg_resources.iter_entry_points(group)

    rule_ids = set()
    for entry in entry_points:
        try:
            rules = entry.load()
            for rule_id, rule_mod in rules.RULES_MAP.items():
                if rule_id in rule_ids or not validate_rule_module(rule_mod):
                    continue

                print(rule_id, rule_mod)###
                yield (rule_id, rule_mod)
                rule_ids.add(rule_id)

        # pkg_resources.EntryPoint.resolve may throw ImportError.
        except (AttributeError, ImportError):
            warnings.warn("Could not load the plugin: {}".format(entry),
                          RuntimeWarning)


def get_plugin_rules_map():
    """Get a mappings of plugin rule's IDs and rules."""
    return dict((rule_id, rule_mod)
                for rule_id, rule_mod in load_plugin_rules_itr())

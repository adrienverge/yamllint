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

import yaml

from yamllint.rules.common import max_spaces_after, max_spaces_before


ID = 'colons'
TYPE = 'token'
CONF = {'max-spaces-before': int,
        'max-spaces-after': int}


def check(conf, token, prev, next):
    if isinstance(token, yaml.ValueToken):
        problem = max_spaces_before(conf['max-spaces-before'], token, prev,
                                    next, 'too many spaces before colon')
        if problem is not None:
            yield problem

        problem = max_spaces_after(conf['max-spaces-after'], token, prev, next,
                                   'too many spaces after colon')
        if problem is not None:
            yield problem

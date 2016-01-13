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

from yamllint.rules.common import spaces_after


ID = 'hyphens'
TYPE = 'token'
CONF = {'max-spaces-after': int}


def check(conf, token, prev, next):
    if isinstance(token, yaml.BlockEntryToken):
        problem = spaces_after(token, prev, next,
                               max=conf['max-spaces-after'],
                               max_desc='too many spaces after hyphen')
        if problem is not None:
            yield problem

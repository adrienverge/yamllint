# Copyright (C) 2016 Adrien Vergé
# Copyright (C) 2025 Jason Yundt
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

import locale
import os

locale.setlocale(locale.LC_ALL, 'C')
env_vars_that_could_interfere_with_tests = (
    'YAMLLINT_FILE_ENCODING',
    # yamllint uses these environment variables to find a config file.
    'YAMLLINT_CONFIG_FILE',
    'XDG_CONFIG_HOME',
    # These variables are used to determine where the user’s home
    # directory is. See
    # https://docs.python.org/3/library/os.path.html#os.path.expanduser
    'HOME',
    'USERPROFILE',
    'HOMEPATH',
    'HOMEDRIVE'
)
for name in env_vars_that_could_interfere_with_tests:
    try:
        del os.environ[name]
    except KeyError:
        pass

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

from setuptools import setup

from yamllint import (__author__, __license__,
                      APP_NAME, APP_VERSION, APP_DESCRIPTION)


setup(
    name=APP_NAME,
    version=APP_VERSION,
    author=__author__,
    description=APP_DESCRIPTION.split('\n')[0],
    long_description=APP_DESCRIPTION,
    license=__license__,
)

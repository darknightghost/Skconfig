#! /usr/bin/env python3
# -*- coding: utf-8 -*-
'''
      Copyright 2018,王思远 <darknightghost.cn@gmail.com>
      This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
      You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import re
import pathlib


def scan_file(path, pattern, regexp=None):
    '''
        Search files.
    '''
    if regexp == None:
        #Compile expression
        regexp = re.compile(path)

    #Search files
    begin_dir = pathlib.Path(path).absolute()
    ret = []
    for p in begin_dir.glob("*"):
        if p.name not in (".", ".."):
            if p.is_dir():
                ret += scan_file(str(p.absolute()), "", regexp)

            elif regexp.fullmatch(p.name):
                ret.append((str(p)))
    return ret

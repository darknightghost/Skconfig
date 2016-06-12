#! /usr/bin/env python3
# -*- coding: utf-8 -*-

'''
    Copyright 2016,暗夜幽灵 <darknightghost.cn@gmail.com>
    
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

import xml.dom.minidom
from analyser.target_exceptions import *
from analyser.target import *

class arch:
    def __init__(self, node, path, parent = None):
        self.path = path
        self.root = node
        self.load(parent)
    
    def __str__(self):
        ret = "Architecture \"%s\":"%(self.name)
        ret = ret + "\n%12s: %s"%("name", self.name)
        ret = ret + "\n"
        return ret
    
    def close(self):
        pass

    def regist(self, dict):
        dict[self.name] = self
    
    def load(self, parent):
        #name
        basename = self.root.getAttribute("name").encode('utf-8').decode()
        if basename == "":
            raise MissingAttribute(self.path, "arch", "name")
        if parent != None:
            self.name = parent.name
            self.name = self.name + "." + basename
        else:
            self.name = basename
    
    def restore(self):
        pass

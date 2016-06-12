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
        for k in self.build_dict.keys():
            ret = ret + "\n%12s: %s"%(k, self.build_dict[k][1])
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
        
        #Makeflie variables
        #[node, value]
        self.build_dict = {"PREV" : None,
            "DEP" : None,
            "DEP_COMMAND" : None,
            "CC" : None,
            "CFLAGS" : None,
            "C_COMMAND" : None,
            "AS" : None,
            "ASFLAGS" : None,
            "AS_COMMAND" : None,
            "LD" : None,
            "LDFLAGS" : None,
            "LD_COMMAND" : None,
            "AFTER" : None}
        
        for k in self.build_dict.keys():
            try:
                self.build_dict[k] = [self.root.getElementsByTagName(k)[0]]
            except IndexError:
                raise ArchMissingTag(self.path, k, self.name)
            try:
                self.build_dict[k].append(self.build_dict[k][0].childNodes[0].nodeValue.encode('utf-8').decode())
            except IndexError:
                self.build_dict[k].append("")
                
        #Sub architectures
        

    
    def restore(self):
        pass

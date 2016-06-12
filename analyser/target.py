#! /usr/bin/env python
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
from target_exceptions import *

class target:
    def __init__(self, path):
        self.path = path
        self.file = open(path, "r+")
        self.dom = xml.dom.minidom.parse(self.file)
        self.root = self.dom.documentElement
        self.analyse(None)
        
    def __init__(self,path, actived_arch):
        self.file = open(path, "r+")
        self.dom = xml.dom.minidom.parse(self.file)
        self.root = self.dom.documentElement
        self.analyse(actived_arch)
        
    def __del__(self):
        self.close()
    
    def __str__(self):
        ret = "Target info:\n"
        return ret
        
    def close(self):
        self.file.seek(0,0)
		self.file.truncate(0)
		self.dom.writexml(self.file, addindent='', newl='', encoding='utf-8')
		self.file.close()
		self.file = None
		self.dom = None
		return
    
    def analyse(self,arch):
        #Output file name
        try:
            output_node = root.getElementsByTagName("output")[0]
        except IndexError:
            raise MissingTag(self.path, "output")
        self.output = output_node.getAttribute("name").encode('utf-8')
        if self.output == "":
            raise MissingAttribute(self.path, "output", "name")
        
        #Output dir
        try:
            outdir_node = root.getElementsByTagName("outdir")[0]
        except IndexError:
            raise MissingTag(self.path, "outdir")
        self.outdir = output_dir_node.getAttribute("path").encode('utf-8')
        if self.output == "":
            raise MissingAttribute(self.path, "outdir", "path")

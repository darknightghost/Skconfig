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
from analyser.arch import *
from analyser.options import *

class target:
    target_dict = {}
    def __init__(self,path, actived_arch = None):
        self.path = path
        self.file = open(path, "r+")
        self.dom = xml.dom.minidom.parse(self.file)
        self.root = self.dom.documentElement
        self.load(actived_arch)
        
    def __del__(self):
        self.file.close()
    
    def __str__(self):
        ret = "Target info:"
        ret = ret + "\n%12s: %s"%("id", self.id)
        ret = ret + "\n%12s: %s"%("output", self.output)
        ret = ret + "\n%12s: %s"%("outdir", self.outdir)
        ret = ret + "\n%12s: %s"%("middir", self.middir)
        ret = ret + "\n%12s: %s"%("Actived arch", self.arch_name)
        for k in self.archs:
            ret = ret + "\n" + str(self.archs[k])
        return ret
        
    def close(self):
        target.target_dict.pop(self.id)
        self.restore()
        try:
            self.file.seek(0,0)
            self.file.truncate(0)
            self.dom.writexml(self.file, addindent='', newl='', encoding='utf-8')
            self.file.close()
        except Exception:
            pass
        self.file = None
        self.dom = None
        return
    
    def load(self, actived_arch):
        #id
        try:
            self.id_node = self.root.getElementsByTagName("id")[0]
        except IndexError:
            raise MissingTag(self.path, "id")
        self.id = self.id_node.getAttribute("value").encode('utf-8').decode()
        if self.id == "":
            raise MissingAttribute(self.path, "id", "value")
        
        #Output file name
        try:
            self.output_node = self.root.getElementsByTagName("output")[0]
        except IndexError:
            raise MissingTag(self.path, "output")
        self.output = self.output_node.getAttribute("name").encode('utf-8').decode()
        if self.output == "":
            raise MissingAttribute(self.path, "output", "name")
        
        #Output dir
        try:
            self.outdir_node = self.root.getElementsByTagName("outdir")[0]
        except IndexError:
            raise MissingTag(self.path, "outdir")
        self.outdir = self.outdir_node.getAttribute("path").encode('utf-8').decode()
        if self.output == "":
            raise MissingAttribute(self.path, "outdir", "path")
        
        #Middie dir
        try:
            self.middir_node = self.root.getElementsByTagName("middir")[0]
        except IndexError:
            raise MissingTag(self.path, "middir")
        self.middir = self.middir_node.getAttribute("path").encode('utf-8').decode()
        if self.middir == "":
            raise MissingAttribute(self.path, "middir", "path")
        
        #Architectures
        try:
            self.archs_node = self.root.getElementsByTagName("archs")[0]
            if actived_arch == None:
                self.arch_name = self.archs_node.getAttribute("actived").encode('utf-8').decode()
                if self.arch_name == "":
                    raise MissingAttribute(path, "archs", "actived")
        except IndexError:
            if actived_arch == None:
                raise MissingTag(self.path, "archs")
            
        else:
            #Scan arch list
            self.archs = {}
            for node in self.archs_node.getElementsByTagName("arch"):
                current_arch = arch(node, self.path)
                current_arch.regist(self.archs)
        
        #Get actived arch
        try:
            self.arch = self.archs[self.arch_name]
        except KeyError:
            if actived_arch == None:
                raise MissingArch(self.path, self.arch_name)
            self.arch = actived_arch
        
        #Dependencies
        #Sub targets
        #Options

        target.target_dict[self.id] = target
        
    def restore(self):
        pass

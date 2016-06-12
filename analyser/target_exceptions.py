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

class MissingTag(Exception):
    def __init__(self,path,tag):
        self.path = path
        self.tag = tag
        
    def __str__(self):
        return "Tag \"%s\" was required in file \"\"."%(self.tag,
                                                            self.path)

class MissingAttribute(Exception):
    def __init__(self,path,tag, attr):
        self.path = path
        self.tag = tag
        self.attr = attr
        
    def __str__(self):
        return "Tag \"%s\" requires attribute \"\" in file \"\"."%(self.tag,
                                                            self.attr,
                                                            self.path)

class MissingArch(Exception):
    def __init__(self,path, arch):
        self.path = path
        self.arch = arch
        
    def __str__(self):
        return "Arch \"%s\" was required in file \"\"."%(self.arch,
                                                            self.path)

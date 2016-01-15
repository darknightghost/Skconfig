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

from xml.dom import minidom
from menuobj import *
import os

class target:
	def __init__(self,node):
		self.path = "%s/%s"%(os.getcwd(),node.getAttribute("src"))
		old_path = os.getcwd()
		os.chdir(self.path)
		self.name = node.getAttribute("node")
		self.file = open("target.xml","rw")
		self.dom = minidom.parse(self.file)
		root = self.dom.documentElement
		
		#Analyse architectures
		#{"archname" : [archname,obj],"archname" : [archobj],...}
		build_node = root.getElementsByTagName("build")[0]
		arch_nodes = build_node.getElementsByTagName("arch")
		self.archs = {}
		for t in arch_nodes:
			info = arch(t)
			if info[0] in self.archs.keys():
				raise ConflictedArchName(info[0])
			else:
				self.archs[info[0]] = info
				
		#Analyse menu
		#[menu-object,menu-object,...]
		self.menu_info = []
		menu_node = root.getElementsByTagName("menu")[0]
		for t in menu_node.childNodes:
			if isinstance(t,minidom.Element):
				info = get_menu_obj(t)
				menu_info.append(info)

		os.chdir(old_path)
		return
		
	def __del__(self):
		self.dom.writexml(self.file,addindent='\t', newl='',encoding='utf-8')
		return
		
	def open_menu(self):
		pass
		
	def close_menu(self):
		pass

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
from target import *
from cfg_excpt import *
from menuobj import *
from arch import *

class cfg:
	def __init__(self,path):
		self.file = open(path,"rw")
		self.dom = minidom.parse(self.file)
		root = self.dom.documentElement
		
		#Analyse architectures
		#{"archname" : [archname,obj],"archname" : [archobj],...}
		self.build_node = root.getElementsByTagName("build")[0]
		arch_nodes = self.build_node.getElementsByTagName("arch")
		self.archs = {}
		for t in arch_nodes:
			info = [t.getAttribute("name"),arch(t)]
			if info[0] in self.archs.keys():
				raise ConflictedArchName(info[0])
			else:
				self.archs[info[0]] = info

		#Load targets
		targets_node = root.getElementsByTagName("targets")[0]
		#[[menu-obj,[menu-obj],...]
		self.targets = []
		for t in targets_node.getElementsByTagName("target"):
			target = get_menu_obj(t)
			self.targets.append(target)	
		return

	def __del__(self):
		self.dom.writexml(self.file,addindent='\t', newl='',encoding='utf-8')
		return

	def open_menu(self):
		pass
		
	def close_menu(self):
		pass

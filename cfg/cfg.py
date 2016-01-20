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
from cfg_excpt import *
import os

#target_list : [[path,options,[children]],[path,options,[children]],...]

class cfg:
	def __init__(self,path):
		self.file = open(path,"rw")
		self.dom = minidom.parse(self.file)
		root = self.dom.documentElement
		self.title = root.getAttribute("name")
		
		#Analyse architectures
		#{"archname" : [archname,obj],"archname" : [archobj],...}
		self.build_node = root.getElementsByTagName("build")[0]
		self.build_arch = self.build_node.getAttribute("actived")
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
		self.file.close()
		return
		
	def get_title(self):
		return self.title

	def open_menu(self):
		self.arch_list = ["listcontrol","Archtecture",[[],0]]
		self.menu = []
		self.arch_menu = []
		for t in self.archs.keys():
			self.arch_list[2][0].append(t)
			self.arch_menu.append(self.archs[t][1].open_menu())
			if t == self.build_arch:
				self.arch_list[2][1] = len(self.arch_list[2][0])
				
		self.menu = [["lable","Architectures",None],
			self.arch_list,
			["submenu","Architecture Settings",self.arch_menu],
			["lable","Targets",None]]
		
		for t in self.targets:
			self.menu.append(t.open_menu())
			
		return self.menu
		
	def close_menu(self):
		self.build_arch = self.arch_list[2][0][self.arch_list[2][1]]
		self.build_node.setAttribute("actived",self.build_arch)
		for t in self.archs.keys():
			self.archs[t][1].close_menu()
		
		for t in self.targets:
			t.close_menu()
			
		self.dom.writexml(self.file,addindent='\t', newl='',encoding='utf-8')
		
	def get_build_options(self,target_list):
		arch = self.archs[self.build_arch]
		for t in self.targets:
			t.get_build_options(target_list,arch)
		return

################################Target#########################################			
class target:
	def __init__(self,node):
		self.node = node
		self.path = "%s/%s"%(os.getcwd(),node.getAttribute("src"))
		old_path = os.getcwd()
		os.chdir(self.path)
		self.name = node.getAttribute("name")
		self.enable_build = node.getAttribute("build") == "true"
		self.file = open("target.xml","rw")
		self.dom = minidom.parse(self.file)
		root = self.dom.documentElement
		
		#Analyse architectures
		#{"archname" : [archname,obj],"archname" : [archobj],...}
		build_node = root.getElementsByTagName("build")[0]
		self.objdir = build_node.getAttribute("objdir")
		self.output = build_node.getAttribute("output")
		arch_nodes = build_node.getElementsByTagName("arch")
		self.archs = {}
		for t in arch_nodes:
			info = arch(t)
			if info.name in self.archs.keys():
				raise ConflictedArchName(info[0])
			else:
				self.archs[info.name] = info
				
		#Analyse menu
		#[menu-object,menu-object,...]
		self.menu_objs = []
		menu_node = root.getElementsByTagName("menu")[0]
		for t in menu_node.childNodes:
			if isinstance(t,minidom.Element):
				info = get_menu_obj(t)
				self.menu_objs.append(info)

		os.chdir(old_path)
		return
		
	def __del__(self):
		self.dom.writexml(self.file,addindent='\t', newl='',encoding='utf-8')
		self.file.close()
		return
		
	def open_menu(self):
		self.build_menu = ["checkbox","Build this target.",self.enable_build]
		self.submenu = [self.build_menu]
		self.submenu.append(["lable","Architectures:",None])
		for t in self.archs.keys():
			self.submenu.append(self.archs[t].open_menu())
		self.submenu.append(["lable","Build Options:",None])
		for t in self.menu_objs:
			self.submenu.append(t.open_menu())
		self.menu = ["submenu","Target : %s"%(self.name),self.submenu]
		return self.menu
		
	def close_menu(self):
		self.enable_build = self.build_menu[2]
		self.node.setAttribute("build",str(self.enable_build).lower())
		for t in self.archs.keys():
			self.archs[t].close_menu()
		for t in self.menu_objs:
			t.close_menu()
		self.dom.writexml(self.file,addindent='\t', newl='',encoding='utf-8')
		
	def get_build_options(self,target_list,arch):
		children = []
		for t in self.menu_objs:
			option = t.get_build_options(children,arch)
			if t != "":
				macros = "%s %s"%(macros,option)
		try:
			options = self.archs[arch.name].get_build_options(macros)
		except KeyError:
			options = arch.get_build_options(macros)
		options = "%s\nARCH = %s\n"%(options,arch.name)
		options = "%sOBJDIR = %s\nOUTPUT = %s\nTARGET = %s\n"%(options,self.objdir,self.output,self.name)
		target_list.append([self.path,options,children])
		return ""


##################################Arch#######################################	
class arch:
	option_names = ["AS","ASFLAGS","ASRULE","CC","CFLAGS","CCRULE","LD",
			"LDFLAGS","LDRULE","DEP","DEPRULE","AFTER"]
	def __init__(self,node):
		self.node = node
		self.name = node.getAttribute("name")
		#{name : obj,name : obj,...}
		self.options_dict = {}

		for t in self.option_names:
			try:
				info_node = node.getElementsByTagName(t)[0]
			except IndexError:
				raise ElementNotFound(t)
				
				
			info_obj = get_menu_obj(info_node)
			self.options_dict[t] = info_obj


	def open_menu(self):
		self.submenu = []
		for t in self.option_names:
			self.submenu.append(self.options_dict[t].open_menu())
		self.menu = ["submenu",self.name,self.submenu]
		return self.menu
		
	def close_menu(self):
		for t in self.option_names:
			self.options_dict[t].close_menu()
			
	def get_build_options(self,options):
		ret = ""
		for t in self.option_names:
			ret = ret + self.options_dict[t].get_build_options(None,self.name)
			if t in ["ASFLAGS","CFLAGS"]:
				if options != "":
					ret = "%s %s"%(ret,options)
			ret = ret + "\n"
		return ret

##############################Menu Objects#####################################

class menuobj:
	def __init__(self,node):
		pass

	def open_menu(self):
		pass
		
	def close_menu(self):
		pass
		
	def get_build_options(self,target_list,arch):
		pass
		
class submenu(menuobj):
	def __init__(self,node):
		self.node = node
		self.text = node.getAttribute("text")
		self.menu_objs = []
		for t in node.childNodes:
			if isinstance(t,minidom.Element):
				info = get_menu_obj(t)
				self.menu_objs.append(info)

	def open_menu(self):
		self.sub_menu = []
		for t in self.menu_objs:
			self.sub_menu.append(t.open_menu())
		self.menu = ["submenu",self.text,self.sub_menu]
		return self.menu
		
	def close_menu(self):
		for t in self.menu_objs:
			t.close_menu()
		
	def get_build_options(self,target_list,arch):
		ret = ""
		for t in self.menu_objs:
			option = t.get_build_options(target_list,arch)
			if option != "":
				if ret != "":
					ret = ret + " "
				ret = ret + option
		return ret
	
class lable(menuobj):
	def __init__(self,node):
		self.text = node.getAttribute("text")

	def open_menu(self):
		return ["lable",self.text,None]
		
	def get_build_options(self,target_list,arch):
		return ""
	
class textbox(menuobj):
	def __init__(self,node):
		self.node = node
		self.text = node.nodeName
		try:
			self.value = node.childNodes[0].nodeValue.strip()
		except IndexError:
			self.value = ""

	def open_menu(self):
		self.menu = ["textbox",self.text,self.value]
		return self.menu
		
	def close_menu(self):
		self.value = self.menu[2]
		try:
			self.node.childNodes[0].nodeValue = self.value
		except IndexError:
			t = minidom.Text()
			self.node.childNodes.append(t)
			t.nodeValue = self.value
		
	def get_build_options(self,target_list,arch):
		return "%s = %s"%(self.text,self.value)
	
class listctrl(menuobj):
	def __init__(self,node):
		self.node = node
		self.text = node.getAttribute("text")
		self.value = int(node.getAttribute("value"))
		self.macro = node.getAttribute("macro")
		self.options = node.childNodes[0].nodeValue.split()

	def open_menu(self):
		self.menu = ["listcontrol",self.text,[self.options,self.value]]
		return self.menu
		
	def close_menu(self):
		self.value = self.menu[2][1]
		self.node.setAttribute("value",str(self.value))
		
	def get_build_options(self,target_list,arch):
		return "%s%d"%(self.macro,self.value)
	
class checkbox(menuobj):
	def __init__(self,node):
		self.node = node
		self.text = node.getAttribute("text")
		self.value = node.getAttribute("value") == "true"
		self.macro = node.getAttribute("macro")

	def open_menu(self):
		self.menu = ["checkbox",self.text,self.value]
		return self.menu
		
	def close_menu(self):
		self.value = self.menu[2]
		self.node.setAttribute("value",str(self.value).lower())
		
	def get_build_options(self,target_list,arch):
		if self.value:
			return self.macro
		else:
			return ""
			
type_dict = {"textbox" : textbox,
		"lable" : lable,
		"listcontrol" : listctrl,
		"checkbox" : checkbox}

def get_menu_obj(node):
	global type_dict
	if node.nodeName == "options" and not node.hasAttribute("type"):
		return submenu(node)
	elif node.nodeName == "target" and not node.hasAttribute("type"):
		return target(node)
	else:
		try:
			return type_dict[node.getAttribute("type")](node)
		except KeyError:
			raise UnknownNode(node.nodeName,node.getAttribute("type"))

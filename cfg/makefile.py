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

from cfg import *
import os

def configure(path):
	configure = cfg(path)
	target_list = []
	configure.get_build_options(target_list)
	print("Creating Makefile...")
	try:
		make_file = open("Makefile","x")
	except FileExistsError:
		make_file = open("Makefile","w")
		
	#all
	make_file.wrtie("all :\n")
	for t in target_list:
		create_target_makefile(t)
		make_file.wrtie("\tmake -f \"%s\" all\n")
	
	#clean
	make_file.wrtie("clean :\n")
	for t in target_list:
		make_file.wrtie("\tmake -f \"%s\" clean\n")
		
	#delete
	make_file.wrtie("delete :\n")
	for t in target_list:
		make_file.wrtie("\tmake -f \"%s\" delete\n")
		
	#rebuild
	make_file.wrtie("rebuild :\n")
	for t in target_list:
		make_file.wrtie("\tmake -f \"%s\" rebuild\n")
	return

def create_target_makefile(target):
	#Get config
	path = target[0]
	options = target[1]
	old_path = os.getcwd()
	os.chdir(path)
	print("Creating Makefile...")
	try:
		make_file = open("Makefile","x")
	except FileExistsError:
		make_file = open("Makefile","w")
	sources = get_sources(arch)
	
	#Create makefile
	make_file.wrtie(options)
	make_file.wrtie("all : $(TARGET)\n")
	
	#Children
	subtargets = target[2]
	make_file.wrtie("$(TARGET) : $(OUTPUT)\n")
	for t in subtargets:
		make_file.wrtie("\tmake -f \"%s/Makefile\" all\n"%(t[0]))
		create_target_makefile(t)
	make_file.wrtie("\t$(AFTER)\n")
	
	#clean
	make_file.wrtie("clean :")
	for t in subtargets:
		make_file.wrtie("\tmake -f \"%s/Makefile\" clean\n"%(t[0]))
	make_file.wrtie("\trm -r $(OBJDIR)/$(ARCH)\n")
	
	#delete
	make_file.wrtie("delete :")
	for t in subtargets:
		make_file.wrtie("\tmake -f \"%s/Makefile\" delete\n"%(t[0]))
	make_file.wrtie("\trm -r $(OBJDIR)/$(ARCH)\n")
	make_file.wrtie("\trm -r $(OUTPUT)\n")
	
	#rebuild
	make_file.wrtie("rebuild :")
	make_file.wrtie("\tmake delete\n")
	make_file.wrtie("\tmake all\n")
	
	#Target
	objs = ""
	#Sources
	for s in sources:
		base_name = os.path.splitext(s)[0]
		ext_name = os.path.splitext(s)[1]
		make_file.wrtie("sinclude $(OBJDIR)/$(ARCH)/%s.dep\n"%(base_name))
		objs = "%s$(OBJDIR)/$(ARCH)/%s.o "%(objs,base_name)
		make_file.wrtie("$(OBJDIR)/$(ARCH)/%s.o : %s\n"%(base_name,s))
		if ext_name in [".c"]:
			#.c
			make_file.wrtie("\t$(CCRULE)\n")
		elif ext_name in [".s",".S"]:
			#.s,.S
			make_file.wrtie("\t$(ASRULE)\n")
		#.dep
		make_file.wrtie("$(OBJDIR)/$(ARCH)/%s.dep : %s\n"%(base_name,s))
		make_file.wrtie("\tmkdir -p $(dir $@)\n\t$(DEPRULE)\n")
	
	#Link
	make_file.wrtie("$(OUTPUT) : %s\n"%(objs))
	make_file.wrtie("\tmkdir -p $(dir $(OUTPUT))\n")
	make_file.wrtie("\t$(LDRULE)\n")
	
	make_file.close()
	os.chdir(old_path)
	return
	
def get_sources(arch):
	f = open("sources","r")
	ret = r.readlines()
	f.close()
	f = open("sources.%s"%(arch),"r")
	ret = ret + r.readlines()
	f.close()
	for i in range(0,len(ret)):
		ret[i] = ret[i].split()
		print("Checking source file \"%s\"..."%(ret[i]))
		if not os.access(ret[i],os.F_OK):
			raise FileNotFoundError("Source file \"%s\" missing."%(ret[i]))
	return ret

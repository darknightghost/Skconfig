#! /usr/bin/env python3
# -*- coding: utf-8 -*-
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
import os
from analyser.target_exceptions import *
from analyser.arch import *
from analyser.options import *

def get_child_tags_by_name(parent, name):
    ret = []
    for node in parent.getElementsByTagName(name):
        if node.parentNode == parent:
            ret.append(node)
    return ret

class target:
    target_dict = {}
    def __init__(self,path, actived_arch = None):
        self.path = os.path.abspath(path)
        self.file = open(path, "r+")
        self.dom = xml.dom.minidom.parse(self.file)
        self.root = self.dom.documentElement
        if actived_arch == None:
            self.is_root = True
        else:
            self.is_root = False
        self.__load(actived_arch)

    def __del__(self):
        try:
            self.file.close()
        except Exception:
            pass

    def __str__(self):
        ret = "Target info:"
        ret = ret + "\n%12s: %s"%("name", self.name)
        ret = ret + "\n%12s: %s"%("path", self.path)
        ret = ret + "\n%12s: %s"%("output", self.output)
        ret = ret + "\n%12s: %s"%("outdir", self.outdir)
        ret = ret + "\n%12s: %s"%("middir", self.middir)
        ret = ret + "\n%12s: %s"%("Introduction", self.introduction)
        ret = ret + "\n%12s: %s"%("Actived arch", self.arch_name)
        ret = ret + "\n%12s:"%("Architectures")
        for i in self.base_archs:
            ret = ret + "\n" + str(i)

        ret = ret + "\n%12s:"%("Dependencies")
        for d in self.dependencies:
            ret = ret + "\n%12s = \"%s\""%("path", d)

        ret = ret + "\n%12s:"%("Options")
        for o in self.options:
            ret = ret + "\n\t" + str(o)

        ret = ret + "\n%12s:"%("Sub targets")
        for t in self.sub_targets:
            ret = ret + "\n" + str(t)

        return ret

    def close(self):
        #Architectures
        for t in self.base_archs:
            t.close()
        
        #Sub targets
        for t in self.sub_targets:
            t.close()
        
        #Options
        for t in self.options:
            t.close()
        
        target.target_dict.pop(self.path)
        self.__restore()
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

    def __load(self, actived_arch):
        #Name
        self.name = self.root.getAttribute("name").encode('utf-8').decode()
        
        #Output file name
        try:
            self.output_node = get_child_tags_by_name(self.root, "output")[0]
        except IndexError:
            raise MissingTag(self.path, "output")
        self.output = self.output_node.getAttribute("name").encode('utf-8').decode()
        if self.output == "":
            raise MissingAttribute(self.path, "output", "name")

        #Output dir
        try:
            self.outdir_node = get_child_tags_by_name(self.root, "outdir")[0]
        except IndexError:
            raise MissingTag(self.path, "outdir")
        self.outdir = self.outdir_node.getAttribute("path").encode('utf-8').decode()
        if self.output == "":
            raise MissingAttribute(self.path, "outdir", "path")

        #Middie dir
        try:
            self.middir_node = get_child_tags_by_name(self.root, "middir")[0]
        except IndexError:
            raise MissingTag(self.path, "middir")
        self.middir = self.middir_node.getAttribute("path").encode('utf-8').decode()
        if self.middir == "":
            raise MissingAttribute(self.path, "middir", "path")

        #Introduction
        try:
            self.introduction_node = get_child_tags_by_name(self.root, "introduction")[0]
        except IndexError:
            raise MissingTag(self.path, "introduction")
        try:
            self.introduction = self.introduction_node.childNodes[0].nodeValue.encode('utf-8').decode()
        except IndexError:
            self.introduction = ""

        #Architectures
        self.archs = {}
        self.base_archs = []
        try:
            self.archs_node = get_child_tags_by_name(self.root, "archs")[0]
            if actived_arch == None:
                self.arch_name = self.archs_node.getAttribute("actived").encode('utf-8').decode()
                if self.arch_name == "":
                    raise MissingAttribute(path, "archs", "actived")
        except IndexError:
            if actived_arch == None:
                raise MissingTag(self.path, "archs")

        else:
            #Scan arch list
            for node in get_child_tags_by_name(self.archs_node, "arch"):
                current_arch = arch(node, self.dom, self.path)
                current_arch.regist(self.archs)
                self.base_archs.append(current_arch)

        #Get actived arch
        try:
            self.actived_arch = self.archs[self.arch_name]
        except KeyError:
            if actived_arch == None:
                raise MissingArch(self.path, self.arch_name)

        #Dependencies
        self.dependencies = []
        try:
            dep_node = get_child_tags_by_name(self.root, "dependencies")[0]
        except IndexError:
            raise MissingTag(self.path, "dependencies")
        for dep in get_child_tags_by_name(dep_node, "dep"):
            try:
                self.dependencies.append(os.path.abspath(os.path.abspath(dep_node.getAttribute("path").encode('utf-8').decode())))
            except IndexError:
                raise MissingAttribute(path, "dep", "path")

        #Sub targets
        #[node, target, enabled, checkbox]
        self.sub_targets = []
        try:
            subtarget_node = get_child_tags_by_name(self.root, "sub-targets")[0]
        except IndexError:
            raise MissingTag(self.path, "sub-targets")
        for subtarget in get_child_tags_by_name(subtarget_node, "target"):
            self.sub_targets.append([subtarget,
                target(subtarget.getAttribute("path"), actived_arch),
                subtarget.getAttribute("enable").encode('utf-8').decode().lower() == "true", None])

        #Options
        self.options = []
        try:
            options_node = get_child_tags_by_name(self.root, "options")[0]
        except IndexError:
            raise MissingTag(self.path, "options")
        for o in get_child_tags_by_name(options_node, "option"):
            self.options.append(get_option(o, self.path))

        target.target_dict[self.path] = target

        return

    def __restore(self):
        #Actived arch
        if self.is_root:
            self.archs_node.setAttribute("actived", self.arch_name)
        
        #Sub targets
        for t in self.sub_targets:
            t[0].setAttribute("enable", str(t[2]).lower())
        return

    def open_menu(self):
        #Intruduction
        self.menu = [["label", self.introduction, None]]
        
        #Dependencies
        dep_str = "Required targets:"
        for d in self.dependencies:
            dep_str = "\n    " + target.target_dict[d].name
        self.menu.append(["label", dep_str, None])

        #Actived arch
        if self.is_root:
            arch_list = []
            i = 0
            selected = 0
            for a in self.base_archs:
                arch_list.append(a.name)
                if a.name == self.arch_name:
                    selected = i
                i = i + 1
            self.active_arch_menu = ["listcontrol", "Actived architecture", [arch_list, selected]]
            self.menu.append(self.active_arch_menu)
        
        #Architecuture settings
        arch_setting_menu = []
        for a in self.base_archs:
            arch_setting_menu.append(a.open_menu())
        self.menu.append(["submenu", "Architecture settings" , arch_setting_menu])

        #Build options
        option_menu = []
        for opt in self.options:
            option_menu.append(opt.open_menu())
        self.menu.append(["submenu", "Build options" , option_menu])
        
        #Sub targets
        sub_targets_menu = []
        for t in sub_targets:
            sub_targets_menu.append(["label", t[1].name, None])
            c = ["checkbox", "Build this target", t[2]]
            sub_targets_menu.append(c)
            t[3] = c
            sub_targets_menu.append(["submenu", "Target options", t[1].open_menu()])
        self.menu.append(["submenu", "Sub targets" , sub_targets_menu])
                         
        return self.menu

    def close_menu(self):
        #Actived arch
        if self.is_root:
            self.arch_name = self.base_archs[self.active_arch_menu[2][1]].name
            self.active_arch_menu = None
        
        #Architecuture settings
        for a in self.base_archs:
            a.close_menu()
        
        #Options
        for opt in self.options:
            opt.close_menu()
            
        #sub targets
        for t in sub_targets:
            t[2] = t[3][2]
            t[3] = None
            t[1].close_menu()
        
        self.menu = None
            
        return

    def configure(self):
        pass

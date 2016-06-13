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

class options:
    def __init__(self, node, path):
        self.root = node
        self.path = path
        self.__load()

    def close(self):
        self.__restore()

    def __load(self):
        pass

    def __restore(self):
        pass

    def open_menu(self):
        pass

    def close_menu(self):
        pass

    def configure(self):
        pass

class opt_checkbox(options):
    def __load(self):
        #name
        try:
            self.name = self.root.getAttribute("name").encode('utf-8').decode()
        except IndexError:
            raise MissingAttribute(self.path, "option", "name")

        #value
        try:
            self.value = self.root.getAttribute("value").encode('utf-8').decode()
        except IndexError:
            raise MissingAttribute(self.path, "option", "value")

        #enable
        try:
            self.enable = (self.root.getAttribute("enable").encode('utf-8').decode().lower() == "true")
        except IndexError:
            raise MissingAttribute(self.path, "option", "enable")

        #target
        try:
            target_str = self.root.getAttribute("target").encode('utf-8').decode()
        except IndexError:
            raise MissingAttribute(self.path, "option", "target")
        self.targets = []
        for k in target_str.split("|"):
            self.targets.append(k.split())
        
        return

    def __restore(self):
        self.root.setAttribute("enable", str(self.enable).lower())
        return

    def open_menu(self):
        pass

    def close_menu(self):
        pass

    def configure(self):
        pass

class opt_list(options):
    def __load(self):
        #name
        try:
            self.name = self.root.getAttribute("name").encode('utf-8').decode()
        except IndexError:
            raise MissingAttribute(self.path, "option", "name")

        #index
        try:
            self.selected = int(self.root.getAttribute("selected").encode('utf-8').decode())
        except IndexError:
            raise MissingAttribute(self.path, "option", "selected")

        #target
        try:
            target_str = self.root.getAttribute("target").encode('utf-8').decode()
        except IndexError:
            raise MissingAttribute(self.path, "option", "target")
        self.targets = []
        for k in target_str.split("|"):
            self.targets.append(k.split())

        #item
        #[name, value]
        self.items = []
        for item in self.root.getElementsByTagName("item"):
            self.name.append([item.getAttribute("name").encode('utf-8').decode(),
                item.getAttribute("value").encode('utf-8').decode()])
        return

    def __restore(self):
        self.root.setAttribute("selected", str(self.selected))
        return

    def open_menu(self):
        pass

    def close_menu(self):
        pass

    def configure(self):
        pass

class opt_input(options):
    def __load(self):
        #name
        try:
            self.name = self.root.getAttribute("name").encode('utf-8').decode()
        except IndexError:
            raise MissingAttribute(self.path, "option", "name")

        #macro
        try:
            self.macro = self.root.getAttribute("macro").encode('utf-8').decode()
        except IndexError:
            raise MissingAttribute(self.path, "option", "macro")

        #value
        try:
            self.value = self.root.getAttribute("value").encode('utf-8').decode()
        except IndexError:
            raise MissingAttribute(self.path, "option", "value")

        #target
        try:
            target_str = self.root.getAttribute("target").encode('utf-8').decode()
        except IndexError:
            raise MissingAttribute(self.path, "option", "target")
        self.targets = []
        for k in target_str.split("|"):
            self.targets.append(k.split())

        return

    def __restore(self):
        self.root.setAttribute("value", self.value)
        return

    def open_menu(self):
        pass

    def close_menu(self):
        pass

    def configure(self):
        pass

class opt_menu(options):
    def __load(self):
        #name
        try:
            self.name = self.root.getAttribute("name").encode('utf-8').decode()
        except IndexError:
            raise MissingAttribute(self.path, "option", "name")

        #options
        self.options = []
        for opt_node in self.root.getElementsByTagName("option"):
            self.options.append(get_option(opt_node, self.path))
        return

    def close(self):
        for opt in self.options:
            opt.close()
        return

    def open_menu(self):
        pass

    def close_menu(self):
        pass

    def configure(self):
        pass

OPTION_DICT = {"checkbox" : opt_checkbox,
    "list" : opt_list,
    "input" : opt_input,
    "menu" : opt_menu}
def get_option(node, path):
    global OPTION_DICT
    return OPTION_DICT[node.getAttribute("type")](node, path)

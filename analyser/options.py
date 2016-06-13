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

class options:
    def __init__(self, node):
        self.root = node
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
    def close(self):
        self.__restore()

    def __load(self):
        #name
        #value
        #enable
        #taget
        pass

    def __restore(self):
        pass

    def open_menu(self):
        pass

    def close_menu(self):
        pass

    def configure(self):
        pass

class opt_list(options):
    def close(self):
        self.__restore()

    def __load(self):
        #name
        #index
        #target
        #item
            #name
            #value
        pass

    def __restore(self):
        pass

    def open_menu(self):
        pass

    def close_menu(self):
        pass

    def configure(self):
        pass

class opt_input(options):
    def close(self):
        self.__restore()

    def __load(self):
        #name
        #macro
        #value
        #target
        pass

    def __restore(self):
        pass

    def open_menu(self):
        pass

    def close_menu(self):
        pass

    def configure(self):
        pass

class opt_menu(options):
    def close(self):
        self.__restore()

    def __load(self):
        #name
        #options
        pass

    def __restore(self):
        pass

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
def get_option(node):
    global OPTION_DICT
    return OPTION_DICT[node.getAttribute("type")](node)

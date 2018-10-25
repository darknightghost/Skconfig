#! /usr/bin/env python3
# -*- coding: utf-8 -*-
'''
      Copyright 2018,王思远 <darknightghost.cn@gmail.com>
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

import skconfig
from skconfig import TypeChecker as TypeChecker


class Option:
    @TypeChecker(object, dict)
    def __init__(self, cfg):
        pass

    def __new__(cls, cfg):
        return OPTION_TYPES[cfg["type"]](cfg)

    def gen_ui(self):
        pass


class OptionVariables:
    '''
        Variable list influlenctd by the option.

        Json format:
        {
            "variable1" : "value1",
            "variable2" : "value2",
            "variable3" : "value3",
            ...
        }
    '''

    @TypeChecker(object, dict)
    def __init__(self, cfg):
        pass


class Menu(Option):
    '''
        Menu.

        Json format:
        {
            "type" : "menu",
            "title" : "menu-name",
            "options" : [
                Option,
                Option,
                Option,
                ...
            ]
        }
    '''

    @TypeChecker(object, dict)
    def __init__(self, cfg):
        super().__init__(cfg)


class Text(Option):
    '''
        Edit box.

        Use ${VALUE} to get the value of the option in OptionVariables.
        Json format:
        {
            "type" : "text",
            "title" : "option-name",
            "value" : "value-of-option",
            "variables" : OptionVariables,
        }
    '''

    @TypeChecker(object, dict)
    def __init__(self, cfg):
        super().__init__(cfg)


class List(Option):
    '''
        List.

        Json format:
        {
            "type" : "list",
            "title" : "option-name",
            "selected" : 0,                 #Index
            "choices" : [
                {"name" : "name1", "variables" : OptionVariables},
                {"name" : "name2", "variables" : OptionVariables},
                {"name" : "name3", "variables" : OptionVariables},
                ...
            ]
        }
    '''

    @TypeChecker(object, dict)
    def __init__(self, cfg):
        super().__init__(cfg)


class Checkbox(Option):
    '''
        Checkbox.

        Json format:
        {
            "type" : "checkbox",
            "title" : "option-name",
            "value" : true,                 #True if checked.
            "variables" : OptionVariables
        }
    '''

    @TypeChecker(object, dict)
    def __init__(self, cfg):
        super().__init__(cfg)


OPTION_TYPES = {"menu": Menu, "text": Text, "list": List, "checkbox": Checkbox}


def test():
    pass

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
import logging


class Option:
    @TypeChecker(object, dict)
    def __init__(self, desc):
        self._type = desc["type"]
        self._title = desc["title"]
        logging.debug("Loading option, type=\"%s\", title=\"%s\"", self._type,
                      self._title)

    def __new__(cls, desc):
        return OPTION_TYPES[desc["type"]](desc)

    def gen_ui(self):
        '''
            Generate ui info.
        '''
        raise NotImplementedError()

    @TypeChecker(object, dict)
    def gen_var(self, values={}):
        '''
            Generate makefile variables.
        '''
        raise NotImplementedError()

    def gen_cfg(self):
        '''
            Generate config.
        '''
        raise NotImplementedError()

    @TypeChecker(object, dict)
    def load_cfg(self, cfg):
        '''
            Load config.
        '''
        raise NotImplementedError()


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
    def __init__(self, desc):
        self.__values = dict(desc)

    @TypeChecker(object, dict, str)
    def gen_var(self, plat, value=""):
        '''
            Generate makefile variables.
        '''
        ret = dict(plat)
        for name in self.__values.keys():
            val = self.__values[name]

            #Replace variables
            while True:
                svalue = skconfig.get_value(val)
                if svalue == None:
                    break

                name, begin, end = svalue
                var_value = ""
                if name == "VALUE":
                    var_value = value

                else:
                    try:
                        var_value = ret[name]

                    except KeyError:
                        raise AttributeError(
                            "Missing attribute \"%s\"." % (name))

                val = val[:begin] + var_value + val[end:]

            val.replace("$$", "$")
            ret[val_name] = val

        return ret

    def __getiten__(self, key):
        return self.__values[key]

    def __setitem__(self, key, value):
        if key not in self.__values.keys():
            raise KeyError("Unknow variable \"%s\"." % (key))

        self.__values[key] = value


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
    def __init__(self, desc):
        super().__init__(desc)

        self._options = []

        #Load options
        for o in dict["options"]:
            self._options.append(Option(o))

    def gen_ui(self):
        '''
            Genetate ui info.
        '''
        ret = {"type": "menu", "title": self._title, "objects": []}

        #Append options
        for o in self._options:
            ret["objects"].append(o.gen_ui)

        return ret

    @TypeChecker(object, dict)
    def gen_var(self, values={}):
        '''
            Generate makefile variables.
        '''
        ret = dict(values)
        for o in self._options:
            ret = o.gen_var(ret)

        return ret

    def gen_cfg(self):
        '''
            Generate config.
        '''
        ret = {"options": []}
        for o in self._options:
            ret["options"].append(o.gen_cfg())

        return ret

    @TypeChecker(object, dict)
    def load_cfg(self, cfg):
        '''
            Load config.
        '''
        for i in range(0, len(self.options)):
            self._options[i].load_cfg(cfg["options"][i])


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
    def __init__(self, desc):
        super().__init__(desc)
        self._value = desc["value"]
        self._variables = OptionVariables(desc["variables"])

    def gen_ui(self):
        '''
            Generate ui info.
        '''

        def on_value_change(val):
            self._value = val

        return {
            "type": "text",
            "title": self._title,
            "text": self._value,
            "onChange": on_value_change
        }

    @TypeChecker(object, dict)
    def gen_var(self, values={}):
        '''
            Generate makefile variables.
        '''
        ret = self._variables.gen_var(values, self._value)
        return ret

    def gen_cfg(self):
        '''
            Generate config.
        '''
        return {"value": self._value}

    @TypeChecker(object, dict)
    def load_cfg(self, cfg):
        '''
            Load config.
        '''
        self._value = cfg["value"]


class List(Option):
    '''
        List.

        Json format:
        {
            "type" : "list",
            "title" : "option-name",
            "selected" : 0,                 #Index
            "choices" : [
                {"name" : "name1", "variables" : OptionVariables, "menu" : Menu},
                {"name" : "name2", "variables" : OptionVariables, "menu" : Menu},
                {"name" : "name3", "variables" : OptionVariables, "menu" : Menu},
                ...
            ]
        }
    '''

    @TypeChecker(object, dict)
    def __init__(self, desc):
        super().__init__(desc)


class Checkbox(Option):
    '''
        Checkbox.

        Json format:
        {
            "type" : "checkbox",
            "title" : "option-name",
            "value" : true,                 #True if checked.
            "variables" : OptionVariables,
            "menu" " Menu
        }
    '''

    @TypeChecker(object, dict)
    def __init__(self, desc):
        super().__init__(desc)


OPTION_TYPES = {"menu": Menu, "text": Text, "list": List, "checkbox": Checkbox}


def test():
    pass

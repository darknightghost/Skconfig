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
            ui = o.gen_ui()

            if "keys" in dir(ui):
                ret["objects"].append(ui)

            else:
                ret["objects"] += ui

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

        @TypeChecker(str)
        def on_change(val):
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
                {"name" : "name1",
                    "variables" : OptionVariables, 
                    "menu" : Menu},                     #Menu is optional
                {"name" : "name2", "variables" : OptionVariables, "menu" : Menu},
                {"name" : "name3", "variables" : OptionVariables, "menu" : Menu},
                ...
            ]
        }
    '''

    @TypeChecker(object, dict)
    def __init__(self, desc):
        super().__init__(desc)
        self._setected = desc["selected"]

        #Load choices
        self._choices = []
        for c in desc.choices:
            choice = {
                "name": c["name"],
                "variables": OptionVariables(c["variables"])
            }
            try:
                choice["menu"] = Menu(c["menu"])

            except KeyError:
                pass

            self._choices.append(choice)

    def gen_ui(self):
        '''
            Generate ui info.
        '''
        #List
        @TypeChecker(int)
        def on_change(val):
            self._setected = val

        ret = [{
            "type": "list",
            "title": self._title,
            "options": [],
            "index": self._setected,
            "onChange": on_change
        }]

        for c in self._choices:
            ret[0]["options"].append(c["name"])

        #Menu
        try:
            ret.append(self._choices[self._setected]["menu"])

        except KeyError:
            pass

        return ret

    @TypeChecker(object, dict)
    def gen_var(self, values={}):
        '''
            Generate makefile variables.
        '''
        choosed = self._choices[self._setected]
        ret = choosed["variables"].gen_var(values)
        try:
            ret = choosed["menu"].gen_var(values)

        except KeyError:
            pass

        return ret

    def gen_cfg(self):
        '''
            Generate config.
        '''
        ret = {"selected": self._setected, "choices": []}
        for c in self._choices:
            try:
                ret["choices"].append(c["menu"].gen_cfg())

            except KeyError:
                ret["choices"].append(None)

        return ret

    @TypeChecker(object, dict)
    def load_cfg(self, cfg):
        '''
            Load config.
        '''
        self._setected = cfg["selected"]
        for i in range(0, len(self._choices)):
            try:
                self._choices[i]["menu"].load_cfg(cfg["choices"][i])

            except KeyError:
                pass


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
        self._value = desc["value"]
        self._variables = OptionVariables(desc["variables"])
        try:
            self._menu = Menu(desc["menu"])

        except KeyError:
            pass

    def gen_ui(self):
        '''
            Generate ui info.
        '''

        @TypeChecker(bool)
        #Checkbox
        def on_change(val):
            self._value = val

        ret = [{
            "type": "checkbox",
            "title": self._title,
            "value": self._value,
            "onChange": on_change
        }]

        #Menu
        if self._value:
            try:
                ret.append(self._menu.gen_ui())

            except AttributeError:
                pass

        return ret

    @TypeChecker(object, dict)
    def gen_var(self, values={}):
        '''
            Generate makefile variables.
        '''
        if self._value:
            return self._variables.gen_var(values)

        else:
            return dict(values)

    def gen_cfg(self):
        '''
            Generate config.
        '''
        ret = {"value": self._value}

        try:
            ret["menu"] = self._menu.gen_cfg()

        except AttributeError:
            pass

        return ret

    @TypeChecker(object, dict)
    def load_cfg(self, cfg):
        '''
            Load config.
        '''
        self._value = cfg["value"]
        try:
            self._menu.load_cfg(cfg["menu"])

        except AttributeError:
            pass


OPTION_TYPES = {"menu": Menu, "text": Text, "list": List, "checkbox": Checkbox}


def test():
    pass

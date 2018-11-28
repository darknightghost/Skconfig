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

import logging
import skconfig
from skconfig import TypeChecker as TypeChecker


class Platform:
    '''
        Compile platform.

        Json format:
        {
                "enabled": "i686",
                "AS": "${AS}",
                "ASFLAGS": "${ASFLAGS}",
                "ASRULE": "${ASRULE}",
                "CC": "${CC}",
                "CFLAGS": "${CFLAGS}",
                "CRULE": "${CRULE}",
                "CPP": "${CPP}",
                "CPPFLAGS": "${CPPFLAGS}",
                "CPPRULE": "${CPPRULE}",
                "DEPRULE": "${CC} -m",
                "AR": "${AR}",
                "ARFLAGS": "${ARFLAGS}",
                "ARRULE": "${ARRULE}",
                "LD": "${LD}",
                "LDFLAGS": "${LDFLAGS}",
                "LDRULE": "${LDRULE}",
                "PREBUILD": "${PREBUILD}",
                "POSTBUILD": "${POSTBUILD}",
                "platforms": [{
                        "name": "i686",
                        "enabled": null,
                        "PREFIX": "",
                        "AS": "${AS}",
                        "ASFLAGS": "${ASFLAGS}",
                        "ASRULE": "${ASRULE}",
                        "CC": "${CC}",
                        "CFLAGS": "${CFLAGS}",
                        "CRULE": "${CRULE}",
                        "CPP": "${CPP}",
                        "CPPFLAGS": "${CPPFLAGS}",
                        "CPPRULE": "${CPPRULE}",
                        "DEPRULE": "${CC} -m",
                        "AR": "${AR}",
                        "ARFLAGS": "${ARFLAGS}",
                        "ARRULE": "${ARRULE}",
                        "LD": "${LD}",
                        "LDFLAGS": "${LDFLAGS}",
                        "LDRULE": "${LDRULE}",
                        "PREBUILD": "${PREBUILD}",
                        "POSTBUILD": "${POSTBUILD}",
                        "platforms": []
                }]
    }

        Config format :
        {
            "name1" : "value1",
            "name2" : "value2",
            "name3" : "value3",
            ...
            "nameN" : "valueN",
            "enabledChild" : "name of enabled child",
            "children" : [child1, child2, child3, ...]
        }
    '''

    @TypeChecker(object, dict, object)
    def __init__(self, desc, parent=None):
        #Load values
        if "_var_list" not in dir(self):
            self._var_list = []

        self._var_list += [
            "AS", "ASFLAGS", "ASRULE", "CC", "CFLAGS", "CRULE", "CPP",
            "CPPFLAGS", "CPPRULE", "DEPRULE", "AR", "ARFLAGS", "ARRULE", "LD",
            "LDFLAGS", "LDRULE", "PREBUILD", "POSTBUILD"
        ]
        self._parent = parent

        if "_values" not in dir(self):
            self._values = {}

        if "_name" not in dir(self):
            self._name = "global"

        logging.info("Loading platform \"%s\"." % (self.name()))
        logging.debug("----------------------------------------------")
        self.__load_values(desc)
        self.__load_children(desc)

    def __load_values(self, desc):
        '''
            Load values from json file.
        '''
        for name in self._var_list:
            try:
                val = desc[name]
                self._values[name] = val
                logging.debug("%s = %s" % (name, val))

            except KeyError:
                raise KeyError("Missing attribute \"%s\"." % (name))

    def __load_children(self, desc):
        '''
            Load child platforms from json file.
        '''
        self._children = {}
        self._enabled_child = desc["enabled"]
        try:
            plat_list = desc["platforms"]

        except KeyError:
            self._enabled_child = None
            return

        for c in plat_list:
            child = SubPlatform(c, self)
            self._children[child.name()] = child

        if len(self._children) == 0:
            self._enabled_child = None

        elif self._enabled_child not in self._children.keys():
            self._enabled_child = list(self._children.keys())[0]

        if self._enabled_child != None:
            logging.info("Platform \"%s\" enabled." %
                         (self._children[self._enabled_child].name()))

    def name(self):
        '''
            Get name opf the platform.
        '''
        parent_name = ""
        if self._parent != None:
            parent_name = self._parent.name()
            return "%s.%s" % (parent_name, self._name)

        else:
            return self._name

    def gen_desc(self):
        '''
            Generate json dictionary.
        '''
        ret = {}

        #Add variables
        if self._parent != None:
            ret["name"] = self._name

        ret["enabled"] = self._enabled_child

        for var in self._var_list:
            ret[var] = self._values[var]

        #Add children
        if len(self._children) > 0:
            platforms = []
            for c in self._children.keys():
                platforms.append(self._children[c].gen_desc())

            ret["platforms"] = platforms

        return ret

    @TypeChecker(object, dict)
    def gen_var(self, values={}):
        '''
            Generate makefile variables.
        '''
        cur_values = dict(values)

        #Generate values
        for val_name in self._var_list:
            #Get value
            val = ""
            try:
                val = self._values[val_name]

            except KeyError:
                continue

            #Replace variables
            while True:
                svalue = skconfig.get_value(val)
                if svalue == None:
                    break

                name, begin, end = svalue
                var_value = ""
                try:
                    var_value = cur_values[name]

                except KeyError:
                    try:
                        var_value = values[name]

                    except KeyError:
                        raise AttributeError(
                            "Missing attribute \"%s\"." % (name))

                val = val[:begin] + var_value + val[end:]

            val.replace("$$", "$")
            cur_values[val_name] = val

        if self._enabled_child == None:
            #Generate variables
            return cur_values

        else:
            #Generate child platform
            return self._children[self._enabled_child].gen_var(cur_values)

    def __getiten__(self, key):
        return self._values[key]

    def __setitem__(self, key, value):
        if key not in self._values.keys():
            raise KeyError("Unknow variable \"%s\"." % (key))

        self._values[key] = value

    def gen_ui(self):
        '''
            Generate ui.
        '''

        class UIVarCallback:
            '''
                Text callback function.
            '''

            @TypeChecker(object, str, object)
            def __init__(self, key_name, plat):
                self.__key_name = key_name
                self.__plat = plat

            @TypeChecker(self, str)
            def __call__(self, val):
                self.__plat[self.__key_name] = val

        class UIChildCallback:
            '''
                List callback function.
            '''

            @TypeChecker(object, object, list)
            def __init__(self, plat, names):
                self.__plat = plat
                self.__names = names.copy()

            @TypeChecker(self, int)
            def __call__(self, val):
                self.__plat._enabled_child = self.__names[val]

            #Variables
            options = []
            for var in self._var_list:
                options.append({
                    "type": "text",
                    "title": var,
                    "text": self[var],
                    "onChange": UIVarCallback(var, self)
                })

            #Children
            if self._enabled_child != None:
                #Enabled child
                child_names = list(self._children.keys()).copy()
                options.append({
                    "type":
                    "list",
                    "title":
                    "Enabled child",
                    "options":
                    child_names,
                    "index":
                    child_names.index(self._enabled_child),
                    "onChange":
                    UIChildCallback(self, child_names)
                })

                #Children
                child_menus = []
                for c in self._children.keys():
                    child_menus.append(self._children[c].gen_ui())

                options.append({
                    "type": "menu",
                    "title": "Child platform options",
                    "objects": child_menus
                })

            return {
                "type": "menu",
                "title": "Platform \"%s\" options" % (self.name()),
                "objects": options
            }

    def gen_cfg(self):
        '''
            Generate config.
        '''
        ret = {}
        for name in self._var_list:
            ret[name] = self._values[name]

        if self._enabled_child != None:
            ret["enabledChild"] = self._enabled_child

            children = {}
            for name in self._children.keys():
                children[name] = self._children[name].gen_cfg()
            ret["children"] = children

        return ret

    @TypeChecker(object, dict)
    def load_cfg(self, cfg):
        '''
            Load config.
        '''
        for name in cfg.keys():
            if name == "enabledChild":
                self._enabled_child = cfg[name]

            elif name == "children":
                for child in cfg[name].keys():
                    self._children[child].load_cfg(cfg[name][child])

            else:
                if name not in self._var_list:
                    raise AttributeError("Unknow variable \"%s\"." % (name))

                self._values[name] = cfg[name]


class SubPlatform(Platform):
    @TypeChecker(object, dict, object)
    def __init__(self, desc, parent):
        if "_var_list" not in dir(self):
            self._var_list = []

        self._name = desc["name"]
        self._var_list += ["PREFIX"]

        super().__init__(desc, parent=parent)


def test():
    import json

    test_desc = "{" \
            "   \"enabled\": \"i686\"," \
            "   \"AS\": \"gcc\"," \
            "   \"ASFLAGS\": \"-S\"," \
            "   \"ASRULE\": \"${AS} ${ASFLAGS} -o\"," \
            "   \"CC\": \"gcc\"," \
            "   \"CFLAGS\": \"-c\"," \
            "   \"CRULE\": \"${CC} ${CFLAGS} -o\"," \
            "   \"CPP\": \"g++\"," \
            "   \"CPPFLAGS\": \"-c\"," \
            "   \"CPPRULE\": \"${CPP} ${CPPFLAGS} -o\"," \
            "   \"DEPRULE\": \"${CC} -m\"," \
            "   \"AR\": \"ar\"," \
            "   \"ARFLAGS\": \" rcs\"," \
            "   \"ARRULE\": \"${AR} ${ARFLAGS} aaa\"," \
            "   \"LD\": \"ld\"," \
            "   \"LDFLAGS\": \"-a\"," \
            "   \"LDRULE\": \"${LD} ${LDFLAGS}\"," \
            "   \"PREBUILD\": \"ls\"," \
            "   \"POSTBUILD\": \"aaa\"," \
            "   \"platforms\": [{" \
            "       \"name\": \"i686\"," \
            "       \"enabled\": null," \
            "       \"PREFIX\": \"i686-\"," \
            "       \"AS\": \"${PREFIX}${AS}\"," \
            "       \"ASFLAGS\": \"${ASFLAGS}\"," \
            "       \"ASRULE\": \"${ASRULE}\"," \
            "       \"CC\": \"${PREFIX}${CC}\"," \
            "       \"CFLAGS\": \"${CFLAGS}\"," \
            "       \"CRULE\": \"${CRULE}\"," \
            "       \"CPP\": \"${PREFIX}${CPP}\"," \
            "       \"CPPFLAGS\": \"${CPPFLAGS}\"," \
            "       \"CPPRULE\": \"${CPPRULE}\"," \
            "       \"DEPRULE\": \"${CC} -m\"," \
            "       \"AR\": \"${PREFIX}${AR}\"," \
            "       \"ARFLAGS\": \"${ARFLAGS}\"," \
            "       \"ARRULE\": \"${ARRULE}\"," \
            "       \"LD\": \"${PREFIX}${LD}\"," \
            "       \"LDFLAGS\": \"${LDFLAGS}\"," \
            "       \"LDRULE\": \"${LDRULE}\"," \
            "       \"PREBUILD\": \"${PREBUILD}\"," \
            "       \"POSTBUILD\": \"${POSTBUILD}\"" \
            "   }]" \
            "}"
    logging.debug("Testing platforms...")
    archs = Platform(json.loads(test_desc))
    logging.debug("Generating description...")
    logging.debug(archs.gen_desc())
    logging.debug("Generating config...")
    cfg = archs.gen_cfg()
    logging.debug(cfg)
    archs.load_cfg(cfg)
    logging.debug("Generating makefile variables...")
    logging.debug(str(archs.gen_var()))

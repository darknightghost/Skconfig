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
'''
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
'''

import logging
import skconfig
from skconfig import TypeChecker as TypeChecker


class Platform:
    @TypeChecker(object, dict, object)
    def __init__(self, cfg, parent=None):
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
        self.__load_values(cfg)
        self.__load_children(cfg)

    def __load_values(self, cfg):
        '''
            Load values from json file.
        '''
        for name in self._var_list:
            try:
                val = cfg[name]
                self._values[name] = val
                logging.debug("%s = %s" % (name, val))

            except KeyError:
                raise KeyError("Missing attribute \"%s\"." % (name))

    def __load_children(self, cfg):
        '''
            Load child platforms from json file.
        '''
        self._children = {}
        self._enabled_child = cfg["enabled"]
        try:
            plat_list = cfg["platforms"]

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

    def gen_config(self):
        '''
            Generate json dictiony.
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
                platforms.append(self._children[c].gen_config())

            ret["platforms"] = platforms

        return ret

    @TypeChecker(object, dict)
    def gen_var(self, values={}):
        '''
            Generate makefile variables.
        '''
        cur_values = {}

        #Generate values
        for val_name in self._var_list:
            #Get value
            val = ""
            try:
                val = self._values[val_name]

            except KeyError:
                pass

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


class SubPlatform(Platform):
    @TypeChecker(object, dict, object)
    def __init__(self, cfg, parent):
        if "_var_list" not in dir(self):
            self._var_list = []

        self._name = cfg["name"]
        self._var_list += ["PREFIX"]

        super().__init__(cfg, parent=parent)


def test():
    import json

    test_cfg = "{" \
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
    archs = Platform(json.loads(test_cfg))
    logging.debug("Generating config...")
    logging.debug(archs.gen_config())
    logging.debug("Generating makefile variables...")
    logging.debug(str(archs.gen_var()))

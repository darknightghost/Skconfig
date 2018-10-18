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
            "CC": "${CC}",
            "CFLAGS": "${CFLAGS}",
            "CRULE": "${CRULLE}",
            "CPP": "${CPP}",
            "CPPFLAGS": "${CPPFLAGS}",
            "CPPRULE": "${CPPRULE}",
            "DEPRULE": "${CC} -m",
            "AR`": "${AR}",
            "ARFLAGS": "${ARFLAGS}",
            "ARRULE": "${ARRULE}",
            "LD": "${LD}",
            "LDFLAGS": "${LDFLAGS}",
            "LDRULE": "${LDRULE}",
            "PREBUILD": "${PREBUILD}",
            "POSTBUILD": "${POSTBUILD}",
            "archs": [{
                    "name": "i686",
                    "enabled": null,
                    "PREFIX": "",
                    "AS": "${AS}",
                    "ASFLAGS": "${ASFLAGS}",
                    "CC": "${CC}",
                    "CFLAGS": "${CFLAGS}",
                    "CRULE": "${CRULLE}",
                    "CPP": "${CPP}",
                    "CPPFLAGS": "${CPPFLAGS}",
                    "CPPRULE": "${CPPRULE}",
                    "DEPRULE": "${CC} -m",
                    "AR`": "${AR}",
                    "ARFLAGS": "${ARFLAGS}",
                    "ARRULE": "${ARRULE}",
                    "LD": "${LD}",
                    "LDFLAGS": "${LDFLAGS}",
                    "LDRULE": "${LDRULE}",
                    "PREBUILD": "${PREBUILD}",
                    "POSTBUILD": "${POSTBUILD}",
                    "archs": []
            }]
}
'''

import logging

class Architecture:
    def __init__(self, cfg, logger):
        self.__logger = logger

        #Load values
        if "_var_list" not in dir(self):
            self._var_list = []

        self._var_list += [
            "AS", "ASFLAGS", "ASRULE",
            "CC", "CFLAGS", "CRULE",
            "CPP", "CPPFLAGS", "CPPRULE",
            "DEPRULE",
            "AR", "ARFLAGS", "ARRULE",
            "LD", "LDFLAGS" , "LDRULE",
            "PREBUILD", "POSTBUILD"
            ]

        self._load_values(cfg)

    def _load_values(self, cfg):
        for name in self._var_list:
            print(name)
        pass

    def _load_children(self, cfg):
        pass

    def _info(self, msg, *args, **kwargs):
        '''
            Logs a message with level INFO on the logger.
        '''
        self.__logger.info(msg, *args, **kwargs)

    def _warning(self, msg, *args, **kwargs):
        '''
            Logs a message with level WARNING on the logger.
        '''
        self.__logger.warning(msg, *args, **kwargs)

    def _error(self, msg, *args, **kwargs):
        '''
            Logs a message with level ERROR on the logger.
        '''
        self.__logger.errno(msg, *args, **kwargs)

    def _critical(self, msg, *args, **kwargs):
        '''
            Logs a message with level CRITICAL on the logger.
        '''
        self.__logger.critical(msg, *args, **kwargs)

    def __str__(self):
        return ""


class SubArchitecture(Architecture):
    def __init__(self, cfg, logger):
        self._parent = parent
        if "_var_list" not in dir(self):
            self._var_list = []

        self._var_list += ["PREFIX"]

        super().__init__(cfg, logger)

if __name__ == "__main__":
    import json

    test_cfg = "{"
            "   \"enabled\": \"i686\","
            "   \"AS\": \"${AS}\","
            "   \"ASFLAGS\": \"${ASFLAGS}\","
            "   \"CC\": \"${CC}\","
            "   \"CFLAGS\": \"${CFLAGS}\","
            "   \"CRULE\": \"${CRULLE}\","
            "   \"CPP\": \"${CPP}\","
            "   \"CPPFLAGS\": \"${CPPFLAGS}\","
            "   \"CPPRULE\": \"${CPPRULE}\","
            "   \"DEPRULE\": \"${CC} -m\","
            "   \"AR`\": \"${AR}\","
            "   \"ARFLAGS\": \"${ARFLAGS}\","
            "   \"ARRULE\": \"${ARRULE}\","
            "   \"LD\": \"${LD}\","
            "   \"LDFLAGS\": \"${LDFLAGS}\","
            "   \"LDRULE\": \"${LDRULE}\","
            "   \"PREBUILD\": \"${PREBUILD}\","
            "   \"POSTBUILD\": \"${POSTBUILD}\","
            "   \"archs\": [{"
            "       \"name\": \"i686\","
            "       \"enabled\": null,"
            "       \"PREFIX\": \"\","
            "       \"AS\": \"${AS}\","
            "       \"ASFLAGS\": \"${ASFLAGS}\","
            "       \"CC\": \"${CC}\","
            "       \"CFLAGS\": \"${CFLAGS}\","
            "       \"CRULE\": \"${CRULLE}\","
            "       \"CPP\": \"${CPP}\","
            "       \"CPPFLAGS\": \"${CPPFLAGS}\","
            "       \"CPPRULE\": \"${CPPRULE}\","
            "       \"DEPRULE\": \"${CC} -m\","
            "       \"AR`\": \"${AR}\","
            "       \"ARFLAGS\": \"${ARFLAGS}\","
            "       \"ARRULE\": \"${ARRULE}\","
            "       \"LD\": \"${LD}\","
            "       \"LDFLAGS\": \"${LDFLAGS}\","
            "       \"LDRULE\": \"${LDRULE}\","
            "       \"PREBUILD\": \"${PREBUILD}\","
            "       \"POSTBUILD\": \"${POSTBUILD}\","
            "       \"archs\": []"
            "   }]"
            "}"
    archs = Architecture(cfg, verbose=True)

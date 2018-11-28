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


class Target:
    '''
        Buildable target.

        Json format:
        {
            "name" : "target name",
            "dependencies" : [
                "path of target file 1",
                "path of target file 2",
                "path of target file 3",
                ... ,
                "path of target file n"
            ],
            "platform" : Platform,
            "options" : [
                option1,
                option2,
                option3,
                ...,
                optionN
            ]
        }

        Config file format:
        {
            "platform" : platform-config,
            "options" : options-config
        }
    '''

    @TypeChecker(object, dict)
    def __init__(self, desc):
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

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
import analyser
import analyser.platform
from analyser.platform import Platform as Platform
import analyser.option
from analyser.option import Option as Option
import logging
import pathlib
import json


class Target:
    '''
        Buildable target.

        .target Json format:
        {
            "name" : "target name",
            "platform" : platform,
            "midDir": "objects directory.",
            "output": "output file.",
            "dependencies" : [
                "path of target file 1",
                "path of target file 2",
                "path of target file 3",
                ... ,
                "path of target file n"
            ],
            "options" : [
                option1,
                option2,
                option3,
                ...,
                optionN
            ]
        }

        .module json format:
        {
            "options" : [
            option1,
            option2,
            option3,
            ...,
            optionN
            ]
        }

        Target config file format:
        {
            "midDir": "objects directory.",
            "output": "output file.",
            "platform" : platform-config,
            "options" : options-config
        }
        
        Module config file format:
        {
            "options" : options-confg
        }
    '''

    @TypeChecker(object, str)
    def __init__(self, path):
        logging.debug("Loading target, path=\"%s\"", path)
        self.__path = path
        self.__load_target(path)

    def __load_target(self, path):
        '''
            Load target.
        '''
        #Load target
        with open(path) as f:
            desc = json.load(f)
            self.__name = desc["name"]
            logging.debug("name=\"%s\"" % (self.__name))
            self.__platform = Platform(desc["platform"])
            self.__mid_dir = desc["midDir"]
            logging.debug("midDir=\"%s\"" % (self.__mid_dir))
            self.__output = desc["output"]
            logging.debug("output=\"%s\"" % (self.__output))
            self.__dependencies = []
            for d in desc["dependencies"]:
                logging.debug("Dependency : \"%s\"" % (d))
                self.__dependencies.append(str(pathlib.Path(d).absolute()))

            self.__options = []
            logging.debug("Loading options...")
            for o in desc["options"]:
                self.__options.append(Option(o))

        #Load config file
        cfg_path = pathlib.Path(path).absolute().parent / ".config"
        if cfg_path.exists() \
            and pathlib.Path.lstat().st_mtime < cfg_path.lstat().st_mtime:
            logging.debug("Loading config file \"%s\"..." % (str(cfg_path)))
            with open(str(cfg_path)) as f:
                cfg = json.load(f)
                self.__platform.load_cfg(cfg["platform"])
                self.__mid_dir = cfg["midDir"]
                logging.debug("midDir=\"%s\"" % (self.__mid_dir))
                self.__output = cfg["output"]
                logging.debug("output=\"%s\"" % (self.__output))
                for i in range(0, len(self.__options)):
                    self.__options[i].load_cfg(cfg["options"][i])

        #Search modules
        module_paths = analyser.scan_file(path, "\\.module")
        logging.debug("Loading modules...")

    def __load_module(self, path):
        pass

    def __load_sources(self, dirname):
        pass

    def name(self):
        '''
            Get name of target.
        '''
        return self.__name

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

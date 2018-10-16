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

import json

'''
    Module file / config file format:
    {
        "arch" : {
            "enabled" : "i686",
            "AS" : "${AS}",                 //Assembler
            "ASFLAGS" : "${ASFLAGS}",       //Assembler flags
            "CC" : ${CC},                   //Name of c compiler
            "CFLAGS" : "${CFLAGS}",         //C compile flags
            "CRULE" : "${CRULLE}",          //Command to compile c
            "CPP" : "${CPP}",               //Name of c++ compiler
            "CPPFLAGS" : "${CPPFLAGS}",     //C++ compile flags
            "CPPRULE" : "${CPPRULE}",       //Command to compile c++
            "DEPRULE" : "${CC} -m",         //Depdence rule
            "AR`" : "${AR}",                 //Name of ar
            "ARFLAGS" : "${ARFLAGS}",       //AR flags
            "ARRULE" : "${ARRULE}",         //AR rule
            "LD" : "${LD}",                 //Linker
            "LDFLAGS" : "${LDFLAGS}",       //LD flags
            "PREBUILD" : "${PREBUILD}",     //Prebuild commands
            "POSTBUILD" : "${POSTBUILD}",   //Post build commands
            "archs" : [
                {
                    "name" : "i686",                //Name
                    "enabled" : "default",
                    "PREFIX" : "",                  //Cross-compile prefix
                    "AS" : "${AS}",                 //Assembler
                    "ASFLAGS" : "${ASFLAGS}",       //Assembler flags
                    "CC" : ${CC},                   //Name of c compiler
                    "CFLAGS" : "${CFLAGS}",         //C compile flags
                    "CRULE" : "${CRULLE}",          //Command to compile c
                    "CPP" : "${CPP}",               //Name of c++ compiler
                    "CPPFLAGS" : "${CPPFLAGS}",     //C++ compile flags
                    "CPPRULE" : "${CPPRULE}",       //Command to compile c++
                    "DEPRULE" : "${CC} -m",         //Depdence rule
                    "AR`" : "${AR}",                 //Name of ar
                    "ARFLAGS" : "${ARFLAGS}",       //AR flags
                    "ARRULE" : "${ARRULE}",         //AR rule
                    "LD" : "${LD}",                 //Linker
                    "LDFLAGS" : "${LDFLAGS}",       //LD flags
                    "PREBUILD" : "${PREBUILD}",     //Prebuild commands
                    "POSTBUILD" : "${POSTBUILD}",   //Post build commands
                    "archs" : [],
                }
            ]
        },
        "options" : []                      //Options
    }
'''

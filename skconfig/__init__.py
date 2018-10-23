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

import inspect
import functools
import logging

LOG_FORMAT_STR = "%(message)s"

#Replace logging functions

REAL_DEBUG = logging.debug


@functools.wraps(REAL_DEBUG)
def _debug(msg, *args, **kwargs):
    msg = "\x1B[1;34mDEBUG : %s\x1B[0m" % (str(msg))
    REAL_DEBUG(msg, *args, **kwargs)


logging.debug = _debug

REAL_INFO = logging.info


@functools.wraps(REAL_INFO)
def _info(msg, *args, **kwargs):
    msg = "\x1B[1;37mINFO : %s\x1B[0m" % (str(msg))
    REAL_INFO(msg, *args, **kwargs)


logging.info = _info

REAL_WARNING = logging.warning


@functools.wraps(REAL_WARNING)
def _warning(msg, *args, **kwargs):
    msg = "\x1B[1;33mWARNING : %s\x1B[0m" % (str(msg))
    REAL_WARNING(msg, *args, **kwargs)


logging.warning = _warning

REAL_ERROR = logging.error


@functools.wraps(REAL_ERROR)
def _error(msg, *args, **kwargs):
    msg = "\x1B[1;31mERROR : %s\x1B[0m" % (str(msg))
    REAL_ERROR(msg, *args, **kwargs)


logging.error = _error

REAL_CRITICAL = logging.critical


@functools.wraps(REAL_CRITICAL)
def _critical(msg, *args, **kwargs):
    msg = "\x1B[1;31;47mCRITICAL : %s\x1B[0m" % (str(msg))
    REAL_CRITICAL(msg, *args, **kwargs)


logging.critical = _critical


def TypeChecker(*type_args, **type_kwargs):
    '''
        Check types of arguments.

        @TypeChecker(type_of_arg0, type_of_arg1, ...)
        def func(arg0, arg1):
            ...
    '''

    def decorator(func):
        sig = inspect.signature(func)

        #Get arguments types
        types = sig.bind_partial(*type_args, **type_kwargs).arguments

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            #Get arguments values
            values = sig.bind(*args, **kwargs)

            #Check types
            for name, value in values.arguments.items():
                if name in types:
                    if not isinstance(value, types[name]):
                        raise TypeError('Argument {} must be {}'.format(
                            name, types[name]))

            return func(*args, **kwargs)

        return wrapper

    return decorator


def get_value(s):
    '''
        Get variable string, return None if failed.

        get_value(str) -> name, begin, end
    '''
    i = 0
    begin, end = 0, 0
    name = ""
    #Search for variable
    while i < len(s):
        if s[i] == '$':
            begin = i
            i += 1
            if s[i] == '{':
                #Get value name and end
                i += 1
                try:
                    while s[i] != '}':
                        name += s[i]
                        i += 1

                    end = i
                    return name, begin, end + 1
                except IndexError:
                    return None

        i += 1
    return None


def test():
    logging.debug("debug")
    logging.info("info")
    logging.warning("warning")
    logging.error("error")
    logging.critical("critical")

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

        @wraps(func)
        def wrapper(*args, **kwargs):
            #Get arguments values
            values = sig.bind(*args, **kwargs)

            #Check types
            for name, value in bound_values.arguments.items():
                if name in bound_types:
                    if not isinstance(value, bound_types[name]):
                        raise TypeError('Argument {} must be {}'.format(name, bound_types[name]))

            return func(*args, **kwargs)

        return wrapper

    return decorator

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
    Defination of ui object:
    +==========+================================================+=============+
    | Type     | Format                                         | Description |
    +==========+================================================+=============+
    | lable    | {"type" : "lable",                             | Static text.|
    |          |    "title" : "title"}                          |             |
    +----------+------------------------------------------------+-------------+
    | menu     | {"type" : "menu",                              | Menu.       |
    |          |    "title" : "title",                          |             |
    |          |    "objects" : [obj1, obj2, obj3, ...]}        |             |
    +----------+------------------------------------------------+-------------|
    | text     | {"type" : "text",                              | Input box.  |
    |          |    "title" : "title",                          |             |
    |          |    "text" : "value",                           |             |
    |          |    "onChange" : callback}                      |             |
    +----------+------------------------------------------------+-------------+
    | list     | {"type" : "list",                              | List to     |
    |          |    "title" : "title",                          | select one  |
    |          |    "options" : [                               | item.       |
    |          |        "option1", "option2", "option3", ...],  |             |
    |          |    "index" : 0,                                |             |
    |          |    "onChange" : callback}                      |             |
    +----------+------------------------------------------------+-------------+
    | checkbox | {"type" : "checkbox",                          | Checkbox.   |
    |          |    "title" : "title",                          |             |
    |          |    "value" : True,                             |             |
    |          |    "onChange" : callback}                      |             |
    +----------+------------------------------------------------+-------------+
    * Defination of Callback: def onChange(value):

'''

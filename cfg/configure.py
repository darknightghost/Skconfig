#! /usr/bin/env python3
# -*- coding: utf-8 -*-

'''
      Copyright 2016,暗夜幽灵 <darknightghost.cn@gmail.com>
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

from analyser.target import *
from analyser.arch import *
from analyser.target_exceptions import *
from cfg.err import *
import os

'''
    Data structure of build tree:
        [target, [sub-targets]]
'''
def configure(root_target):
    ret = []

    #Get build tree
    print("\nScaning targets...")
    missing_deps = root_target.get_dependencies()
    if len(missing_deps) != 0:
        raise MissingDepecncency(missing_deps)
    ret = get_build_tree(root_target)
    
    #Sort build tree
    print("\nComputing build order...")
    sort_build_tree(ret)

    return ret

def create_makefile(build_tree):
    cur_target = build_tree[0]
    print("\n" + ("*" * 80))
    print("Configuring target : \"%s\"...\npath = \"%s\""%(cur_target.name, cur_target.path))
    
    #Change working directory
    old_dir = os.path.abspath(".")
    cur_dir = os.path.dirname(cur_target.path)
    os.chdir(cur_dir)
    
    #Get build options
    if cur_target.build_type == "build":
        #build
        print("Target type : build")
        
        #Scan source files
        sources = scan_sources(cur_target.arch_name)
        #Create Makefile
        
    else:
        #virtual
        print("Target type : virtual")

        #Create Makefile
    
    #Change working directory
    os.chdir(old_dir)
    
    for s in build_tree[1]:
        create_makefile(s)
    return

def get_build_tree(root):
    print("Target found : \"%s\".\npath = \"%s\"."%(root.name, root.path))
    sub_targets = []
    for t in root.get_sub_targets():
        sub_targets.append(get_build_tree(t))
    return [root, sub_targets]

def sort_build_tree(build_tree):
    sub_targets = build_tree[1]
    for t in sub_targets:
        sort_build_tree(t)
    while True:
        flag = False
        for i in range(0, len(sub_targets) - 1):
            order = target.check_order(sub_targets[i][0], sub_targets[i + 1][0])
            if order == target.RESERVE:
                sub_targets[i], sub_targets[i + 1] = sub_targets[i + 1], sub_targets[i]
                flag = True
            elif order == target.CONFLICT:
                raise ConfilctDepecncency(sub_targets[i][0].name, sub_targets[i + 1][0].name)
        if flag == False:
            break
    return

def scan_sources(arch_name):
    pass

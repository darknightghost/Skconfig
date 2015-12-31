#! /usr/bin/env python
# -*- coding: utf-8 -*-

import curses
from ui.ui import *

class control:
	def __init__(self,frame,wnd,data):
		pass
	
	def draw(self,pos,begin,max):
		return 0
	
	def get_size(self):
		return rect_t(0,0)
	
	def on_get_focus(self):
		pass
	
	def on_lost_focus(self):
		pass
	
	def on_key_press(self,key):
		pass
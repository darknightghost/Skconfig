#! /usr/bin/env python
# -*- coding: utf-8 -*-

import curses
import control
from ui.ui import *

class lable(control.control):
	def __init__(self,frame,wnd,data):
		e = encoder()
		self.wnd = wnd
		self.text = e.convert(data[1])
		c = color_t()
		self.color = c.get_color(color_t.BLACK,color_t.WHITE) | curses.A_BOLD
	
	def draw(self,pos,begin,max):
		self.pos = pos
		self.wnd.addstr(self.pos.top, self.pos.left,self.text,self.color)
		return 1
	
	def get_size(self):
		return rect_t(len(self.text) + 2,1)
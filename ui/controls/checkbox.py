#! /usr/bin/env python
# -*- coding: utf-8 -*-

import curses
import control
from ui.ui import *

class checkbox(control.control):
	def __init__(self,frame,wnd,data):
		self.wnd = wnd
		self.data = data
		c = color_t()
		self.focus = False
		self.color = c.get_color(color_t.BLACK,color_t.WHITE) | curses.A_BOLD
	
	def draw(self,pos,begin,max):
		self.pos = pos
		self.refresh()
		return 1
		
	def refresh(self):
		if self.focus:
			color = self.color | curses.A_REVERSE
		else:
			color = self.color
		if self.data[2] == True:
			self.wnd.addstr(self.pos.top, self.pos.left,"[\xFB] %s"%(self.data[1]),color)
		else:
			self.wnd.addstr(self.pos.top, self.pos.left,"[ ] %s"%(self.data[1]),color)
		self.wnd.refresh()
		return
		
	def get_size(self):
		return rect_t(len(self.data[1]) + 4,1)
	
	def on_get_focus(self):
		self.focus = True;
		self.refresh()
		return
		
	
	def on_lost_focus(self):
		self.focus = False;
		self.refresh()
		return
	
	def on_key_press(self,key):
		if key == curses.KEY_ENTER:
			self.data[2] = not self.data[2]
			self.refresh()
		return
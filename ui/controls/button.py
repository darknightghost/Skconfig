#! /usr/bin/env python
# -*- coding: utf-8 -*-

import curses
import control
from ui.ui import *

class button(control.control):
	def __init__(self,wnd,data):
		e = encoder()
		self.wnd = wnd
		self.text = e.convert(data[0])
		self.on_click = data[1]
		c = color_t()
		self.color = c.get_color(color_t.WHITE,color_t.RED) | curses.A_BOLD
	
	def draw(self,pos,begin,max):
		self.pos = pos
		e = encoder()
		self.wnd.addstr(self.pos.top, self.pos.left,e.convert("<%s>"%(self.text)),self.color)
		return 1
	
	def get_size(self):
		return rect_t(len(self.text) + 2,1)
	
	def on_get_focus(self):
		e = encoder()
		self.wnd.addstr(self.pos.top, self.pos.left,e.convert("<%s>"%(self.text)),self.color | curses.A_REVERSE)
		self.wnd.refresh()
		return
	
	def on_lost_focus(self):
		e = encoder()
		self.wnd.addstr(self.pos.top, self.pos.left,e.convert("<%s>"%(self.text)),self.color)
		self.wnd.refresh()
		return
	
	def on_key_press(self,key):
		if key == ord('\n'):
			self.on_click()
		return
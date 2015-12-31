#! /usr/bin/env python
# -*- coding: utf-8 -*-

import curses

class color_t:
	BLACK = curses.COLOR_BLACK
	BLUE = curses.COLOR_BLUE
	GREEN = curses.COLOR_GREEN
	CYAN = curses.COLOR_CYAN
	RED = curses.COLOR_RED
	MAGENTA = curses.COLOR_MAGENTA
	YELLOW = curses.COLOR_YELLOW
	WHITE = curses.COLOR_WHITE
	
	def init_color(self):
		curses.start_color()
		for i in range(7 + 1):
			for j in range(7 + 1):
				if (7 - i) * 8 + j != 0:
					curses.init_pair((7 - i) * 8 + j,i,j)
		return
		
	def get_color(self,fg,bg):
		return curses.color_pair((7 - fg) * 8 + bg)
	
class pos_t:
	def __init__(self):
		self.top = 0
		self.left = 0
		
	def __init__(self,top,left):
		self.top = top
		self.left = left
	
class rect_t:
	def __init__(self):
		self.width = 0
		self.height = 0
		
	def __init__(self,width,height):
		self.width = width
		self.height = height
	
class region_t:
	def __init__(self):
		self.pos = pos_t()
		self.rect = rect_t()
	
	def __init__(self,top,left,width,height):
		self.pos = pos_t(top,left)
		self.rect = rect_t(width,height)

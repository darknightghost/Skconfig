#! /usr/bin/env python
# -*- coding: utf-8 -*-

from data import *
from controls.control import *
from controls.button import *
from controls.lable import *
from controls.checkbox import *

class ControlTypeError(Exception):
	def __init__(self,ctrl_type):
		self.ctrl_type = ctrl_type
		self.msg = ""
		return
		
	def __init__(self,ctrl_type,msg):
		self.ctrl_type = ctrl_type
		self.msg = msg
		return
		
	def __str__(self):
		return "Unknow type of control: %s.%s"%(self.ctrl_type,self.msg)

class menu:
	#{control-name:(class,indent,able-get-focus)}
	control_dict = {"lable" : (lable,0,False),
		"checkbox" : (checkbox,4,True)}
	def __init__(self,scr,title):
		self.scr = scr
		self.back = False
		self.title = title

	def show_menu(self,menu):
		#Draw window
		self.draw_wnd()
		
		#Draw menu
		page = self.analyse_menu(menu)
		self.index = 0
		while not self.back:
			#Clear menu
			self.client.erase()
			self.client.box()

			#Draw buttons
			btn_back = button(self,self.wnd,("Back",self.on_back))
			btn_prev = button(self,self.wnd,("Prev",self.on_prev))
			btn_next = button(self,self.wnd,("Next",self.on_next))
			
			btn_back.draw(pos_t(self.rect.height - 2,self.rect.width / 4 - 2),0,1)
			
			if self.index > 0:
				btn_prev.draw(pos_t(self.rect.height - 2,self.rect.width / 4 * 2 - 2),0,1)
			
			if self.index + 1 < len(page):
				btn_next.draw(pos_t(self.rect.height - 2,self.rect.width / 4 * 3 - 2),0,1)

			#Draw menu
			if len(page) > 0:
				current_page = page[self.index]
				for l in current_page:
					l[0].draw(l[1],l[2],l[3])
			
			self.wnd.refresh()
			self.client.refresh()
			
			self.refresh = False

			#Key input
			while not self.refresh:
				pass


	def draw_wnd(self):
		#Compute window size
		parent_rect = self.scr.get_size()
		self.rect = rect_t(parent_rect.width * 80 / 100,
			parent_rect.height * 80 / 100)
		self.pos = pos_t((parent_rect.height - self.rect.height) / 2,
			(parent_rect.width - self.rect.width) / 2)

		color = color_t()

		#Draw shadow
		shadow_color = color.get_color(color_t.BLACK,color_t.BLUE)
		for top in range(self.pos.top + 1,
			self.pos.top + self.rect.height + 1):
			self.scr.stdscr.addch(top,self.pos.left + self.rect.width,
				'\xDB',shadow_color)
		for left in range(self.pos.left + 1,
			self.pos.left + self.rect.width):
			self.scr.stdscr.addch(self.pos.top + self.rect.height,left,
				'\xDB',shadow_color)
		self.scr.stdscr.refresh()
		
		#Draw window
		self.wnd = self.scr.stdscr.subwin(self.rect.height,self.rect.width,
			self.pos.top,self.pos.left)
		self.wnd.bkgd(' ',color.get_color(0,color_t.WHITE))
		self.wnd.addstr(0, self.rect.width / 2 - len(self.title) / 2,self.title,color.get_color(0,color_t.WHITE) | curses.A_BOLD)
		self.wnd.refresh()
		
		#Draw client region
		self.client_region = region_t(1,1,self.rect.width - 2,self.rect.height - 1 - 3)
		self.client = self.wnd.derwin(self.client_region.rect.height,self.client_region.rect.width,
			self.client_region.pos.top,self.client_region.pos.left)
		self.client.box()
		self.client.refresh()
		
		return

	def get_input(self):
		pass
	
	def analyse_menu(self,menu):
		#[[(control,pos,begin,max),...],...]
		ret = []
		max_height = self.client.getmaxyx()[0] - 2
		
		#Create controls
		ctrl_index = 0
		line = 1
		page = []
		while ctrl_index < len(menu):
			if line >= max_height:
				line = 1
				ret.append(page)
				page = []

			#Create control
			try:
				ctrl = self.control_dict[menu[ctrl_index][0]][0](self,self.client,menu[ctrl_index])
				indent = self.control_dict[menu[ctrl_index][0]][1]
			except KeyError:
				raise ControlTypeError(menu[ctrl_index][0])
				
			#Get control height
			ctrl_height = ctrl.get_size().height
			
			#Add control
			begin = 0
			while ctrl_height > max_height - line:
				page.append((ctrl,pos_t(line,1 + indent),begin,max_height - line))
				begin = begin + (max_height - line)
				ctrl_height = ctrl_height - (max_height - line)
				line = 1
				ret.append(page)
				page = []
				
			page.append((ctrl,pos_t(line,1 + indent),begin,ctrl_height))
			line = line + ctrl_height

			ctrl_index = ctrl_index + 1
		if page != []:
			ret.append(page)
			
		return ret
	
	def on_back(self):
		self.back = True
		self.refresh = True
		
	def on_prev(self):
		self.index = self.index - 1
		self.refresh = True

		
	def on_next(self):
		self.index = self.index + 1
		self.refresh = True
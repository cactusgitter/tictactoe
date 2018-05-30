import kivy
import numpy
kivy.require("1.10.0")
from kivy.app import App
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.core.image import Image
from kivy.uix.image import Image
from kivy.properties import ObjectProperty
from kivy.config import Config
from kivy.graphics import Color
from kivy.graphics import Rectangle
from kivy.uix.behaviors import ButtonBehavior
import time
import random

global toe_box
global toe_box_ids

def startup():
	Config.set('graphics', 'resizable', False)
	#Config.set('graphics', 'borderless', 1)
	Config.set('graphics', 'width', 800)
	Config.set('graphics', 'height', 800)
	Config.set('graphics', 'top', 50)

# Main
# Builds the kv file instead of having it separate
class Main(App):
	def build(self):
		startup()
		Builder.load_string(
"""
Container:

#Container holds all the other layouts
<Container>:
	id: contain
	orientation: "vertical"
	#pos_hint: {'center_y': 0.5, 'center_x': 0.5}
	#size_hint_y: None
	#height: 0.5625 * root.width
	StartMenu
	
#Custom Image class to prevent blurring on all images
<CustomImage>:
	Image:
		id: img
        source: root.source
        pos: root.pos
        size: root.size
		allow_stretch: True
		
#Custom class for buttons that have images
<ImageButton>:
	id: imgbtn
    source: None
    on_press: root.change_color()
    #on_press: root.click_box()
    on_release: root.reset_color()
    always_release: True
    allow_stretch: True
    
    #Helps the button on_press
    tint: 0,0,0,0
	canvas.after:
		Color:
			rgba: self.tint
		Rectangle:
			size: self.size
			pos: self.pos
    
    CustomImage:
		id: img
        source: root.source
        pos: root.pos
        size: root.size
		allow_stretch: True
	
<StartMenu>:
	orientation: "vertical"
	Button:
		text: "Tic Tac Toe, CPU = Impossible"
		on_press: root.goto_impossible()
	Button:
		text: "Tic Tac Toe, CPU = Random"
	Button:
		text: "Tic Tac Toe, CPU = Trying To Lose"
	Button:
		text: "Exit"
		on_press: root.quit_game()
		
<TicTacToe>:
	orientation: "vertical"
	BoxLayout:
		orientation: "horizontal"
		ImageButton:
			id: A1
			source: "blank.gif"	
			on_press: root.clicked([0,0], "A1")
		ImageButton:
			id: A2
			source: "blank.gif"	
			on_press: root.clicked([0,1], "A2")
		ImageButton:
			id: A3
			source: "blank.gif"
			on_press: root.clicked([0,2], "A3")
				
	BoxLayout:
		orientation: "horizontal"
		ImageButton:
			id: B1
			source: "blank.gif"
			on_press: root.clicked([1,0], "B1")	
		ImageButton:
			id: B2
			source: "blank.gif"
			on_press: root.clicked([1,1], "B2")
		ImageButton:
			id: B3
			source: "blank.gif"
			on_press: root.clicked([1,2], "B3")
				
	BoxLayout:
		orientation: "horizontal"
		ImageButton:
			id: C1
			source: "blank.gif"
			on_press: root.clicked([2,0], "C1")		
		ImageButton:
			id: C2
			source: "blank.gif"
			on_press: root.clicked([2,1], "C2")
		ImageButton:
			id: C3
			source: "blank.gif"	
			on_press: root.clicked([2,2], "C3")
""")
		global root
		root = Container()
		return root

class CustomImage(Image):
	def __init__(self, *args, **kwargs):
		Image.__init__(self, *args, **kwargs)
		self.bind(texture=self._update_texture_filters)

	def _update_texture_filters(self, image, texture):
		texture.mag_filter = 'nearest'
	
class ImageButton(ButtonBehavior, Image):	
	#def __init__(self, *args, **kwargs):
	#	super(ImageButton, self).__init__(**kwargs)

	def change_color(self):
		self.tint = 0,0,0,0.2
		
	def reset_color(self):
		self.tint = 0,0,0,0
		
	def click_box(self):
		pass#self.source = "x.gif"

# The primary gui container that holds all the other gui pieces
class Container(BoxLayout):
	pass
	
class CPU():
	global toe_box
	global toe_box_ids
	toe_box = [[0,0,0],[0,0,0],[0,0,0]] # The array of the tic tac toe box
	toe_box_ids = [["A1","A2","A3"],["B1","B2","B3"],["C1","C2","C3"]]
	

# The first menu the user sees
class StartMenu(BoxLayout):
	def goto_impossible(self):
		root.clear_widgets()
		root.add_widget(TicTacToe())
	def quit_game(self):
		App.get_running_app().stop()
		
# The first menu the user sees
class TicTacToe(BoxLayout):
	global toe_box
	global toe_box_ids
	turn = 1
	
	#Turn 1 possibilities
	xmiddle = [[0,0,0],[0,1,0],[0,0,0]]
	
	#Turn 3 possibilities
	xblock = [[2,0,0],[0,1,0],[0,0,1]]
	
	def clicked(self, loc, imgid): #loc = location, imgid = image id
		a = loc[0]
		b = loc[1]
		if toe_box[a][b] == 0:
			toe_box[a][b] = 1
			self.ids[imgid].source = "x.gif"
			self.run_cpu_turn()
		else:
			print("Box already taken")
	
	def play(self, loc): #loc = location, imgid = image id
		a = loc[0]
		b = loc[1]
		img_id = toe_box_ids[a][b]
		toe_box[a][b] = 2
		self.ids[img_id].source = "o.gif"
	
	def find_wins(self):
		i = 0
		j = 0
		# check rows
		while i < 3:
			print("i = " + str(i))
			if sum(toe_box[i]) == 3:
				if toe_box[i][j] == 0:
					self.play([i][j])
					break
				elif toe_box[i][j+1] == 0:
					self.play([i,j+1])
					break
				else:
					self.play([i,j+2])
					break
			i += 1

	#TO DO
	def block_x(self):
		i = 0
		j = 0
		
		# check rows
		while i < 3:
			while j < 3:
				if toe_box[i][j] == 2:
					j = 3
				elif sum(toe_box[i]) == 2:
					if toe_box[i][j] == 0:
						play([i,j])
				j += 1
			i += 1
		
		#TODO TO DO
		#check columns
		col_totals = numpy.sum(toe_box, axis=0)
		while j < 3:
			while i < 3:
				if toe_box[i][j] == 2:
					j = 3
				elif col_totals[0] == 2:
					if toe_box[i][j] == 0:
						play([i,j])
				i += 1
			j += 1
	
	def run_cpu_turn(self):
		if self.turn == 1:
			self.turn += 2
			if toe_box == self.xmiddle:
				self.play([0,0])
			else:
				self.ids["B2"].source = "o.gif"
				toe_box[1][1] = 2
				
		elif self.turn == 3:
			self.turn += 2
			print(toe_box)
			if toe_box == [[2,0,0],[0,1,0],[0,0,1]]: #x blocks themselves
				self.play([0,2])
		
		elif self.turn == 5:
			self.find_wins()

# Runs the program	
if __name__ == '__main__':
	Main().run()

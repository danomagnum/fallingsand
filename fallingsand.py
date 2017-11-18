import platform



try:
	import pygame_cffi as python
except:
	import pygame
from pygame.locals import *
import renderers
import pygame.font


if platform.python_implementation() == "CPython":
	import renderers
elif platform.python_implementation() == "PyPy":
	import renderers_pypy as renderers

from elements import *
import time
from settings import *
from pgu import gui
import inspect
from sandbox import Sandbox, Debug
import easygui
import os
import sys

from wireworld import Wire, Generator, Electron
from conway import Conway
#from apocalypse import Zombie, Human, Wall, Barricade


import os


# These two functions are used for determining the current working directory.
# They are needed instead of simply using __file__ because of py2exe compatibility.
# They break python 3 compatibility.  Remove them and edit current dir to restore
def we_are_frozen():
	"""Returns whether we are frozen via py2exe.
	This will affect how we find out where we are located."""
	return hasattr(sys, "frozen")

def module_path():
	if we_are_frozen():
			return os.path.dirname(unicode(sys.executable, sys.getfilesystemencoding( )))
	return os.path.dirname(unicode(__file__, sys.getfilesystemencoding( )))

CURRENT_DIR = module_path()
OUTSIDE_DIR = CURRENT_DIR.split('library.zip')[0]
mytheme = os.path.join(OUTSIDE_DIR, THEME) # generated a usable path to the theme files pgu uses

#these are the elements that show up in the selection box.  Add your elements to this in order to use them
ELEMENTLIST = [Water,Oil,Steam,Stone,Wall,Fire,Lava,Plant,Faucet,Boom,KaBoom,TnT,Conway,SteadyTemp,Insulator, Wire, Electron, Generator, Debug]
#ELEMENTLIST = [Zombie, Human, Wall, Barricade, Water,Oil,Steam,Stone,Wall,Fire,Lava,Plant,Faucet,Boom,KaBoom,TnT,Conway,SteadyTemp,Insulator, Wire, Electron, Generator, Debug]

#This is a debug toggle.  When true, it creates a bunch of water faucets to test lag.
SPEEDCHECK = False

screensize = (BORDER[1]+BORDER[3] + PIXELSIZE*WIDTH,BORDER[0]+BORDER[2] + PIXELSIZE*HEIGHT) # set the total screen size
screen = pygame.display.set_mode(screensize, pygame.DOUBLEBUF)
clock = pygame.time.Clock()  # start the clock

sandbox = Sandbox(WIDTH, HEIGHT)  # Initialize the sandbox.  This is where the magic happens


#This is used for doing framerate tests  flag is up above in this file
if SPEEDCHECK:
	barlength = 40
	for x in range(barlength):
		Faucet(x, 0, sandbox)


paintelement = Water  # Initialize the paintbrush

# The gui does weird things when the value of the selected item is None, so this function
# sorts that out and sets the paintbrush correctly
def updatebrush():
	global paintelement
	val = mm.selbox.value
	if inspect.isclass(val):
		paintelement = val
	else:
		paintelement = None

def updategrid():
	sandbox.full_regen()
	renderer.show_grid = mm.gridbutton.value

def updatecursor():
	renderer.show_cursor = mm.cursorbutton.value

#Set up the gui
class MainMenu(gui.Table):

	def speed(self):
		if self.pausebutton.value:  # When we are paused, don't destroy the framerate
			return 60
		else:
			return self.speedslider.value

	def update_total(self, val1, val2):  # updates the gui display of active element counts
		self.totalcelldisplay.value = str(val2)
		self.activecelldisplay.value = str(val1)

	def update_mouse_pos(self, x, y):  # updates the gui display of active element counts
		self.positiondisplay.value = '(' + str(x) + ',' + str(y) + ')'

	def __init__(self,**params):
		gui.Table.__init__(self,**params)
		fg = (255,255,255)

		#set up the list of elements
		self.tr()
		self.selbox = gui.List(width=BORDER[3],height=200)
		self.selbox.add("None", value=None)
		for elem in ELEMENTLIST:
			#self.selbox.add(elem.name, elem)
			self.selbox.add(elem.name, value=elem)
		self.selbox.connect(gui.CHANGE,updatebrush)
		self.td(self.selbox, colspan=3)

		#set up the brush size selection
		self.tr()
		self.td(gui.Label("Size:", color=fg), align=-1)
		self.sizedisplay = gui.Input("1", width=80)
		self.sizedisplay.disabled = True
		#self.sizedisplay = gui.Label("1",color=fg)
		self.td(self.sizedisplay)
		#self.sld = gui.HSlider(1,1,16,20,width=BORDER[3])
		self.sld = gui.HSlider(1,1,16,20,width=BORDER[3],height=16,name='brushsize')

		def updatesize():
			self.sizedisplay.value = str(self.sld.value)
			#self.sizedisplay.set_text(str(self.sld.value))
			renderer.change_cursor_size(self.sld.value)

		self.sld.connect(gui.CHANGE,updatesize)
		self.tr()
		self.td(self.sld,colspan=3)

		#Set up the temperature display and slider
		self.tr()
		self.td(gui.Label("Temp:",color=fg), align=-1)
		#self.tempdisplay = gui.Label("300",color=fg)
		self.tempdisplay = gui.Input('300', width=60)
		self.tempdisplay.disabled = True
		self.td(self.tempdisplay, align=-1)
		#self.sld = gui.HSlider(1,1,16,20,width=BORDER[3])
		self.tempslider = gui.HSlider(300,1,2000,20,width=BORDER[3],height=16,name='tempslide')

		def updatetemp():
			#This function smoothly transitions the color of the temperature display from bluish to redish
			#a very similar thing is used for the stone/lava elements
			clr_cold = (192, 192, 250)
			clr_hot = (255, 85, 96)
			clr_delta = (clr_hot[0] - clr_cold[0], clr_hot[1] - clr_cold[1], clr_hot[2] - clr_cold[2])

			v1 = self.tempslider.min
			val = self.tempslider.value
			v2 = self.tempslider.max
			percent = float(val - v1) / float(v2 - v1)

			clr_now = (int(clr_cold[0] + percent*clr_delta[0]), int(clr_cold[1] + percent*clr_delta[1]), int(clr_cold[2] + percent*clr_delta[2]))

			self.tempdisplay.style.color = clr_now
			self.tempdisplay.value = (str(val))

		self.tempslider.connect(gui.CHANGE,updatetemp)
		self.tr()
		self.td(self.tempslider,colspan=3)

		updatetemp()

		#Set up the pause button - this one is just a boolean, so no need to attach functions
		self.tr()
		self.pausebutton = gui.Switch(False)
		self.td(gui.Label('Pause:',color=fg), align=-1)
		self.td(self.pausebutton)

		#Set up the grid toggle button - this one is just a boolean, so no need to attach functions
		self.tr()
		self.gridbutton = gui.Switch(False)
		self.td(gui.Label('Grid:',color=fg), align=-1)
		self.td(self.gridbutton)
		self.gridbutton.connect(gui.CHANGE, updategrid)

		#Set up the grid toggle button - this one is just a boolean, so no need to attach functions
		self.tr()
		self.cursorbutton = gui.Switch(False)
		self.td(gui.Label('Cursor:',color=fg), align=-1)
		self.td(self.cursorbutton)
		self.cursorbutton.connect(gui.CHANGE, updatecursor)


		#set up the framerate slider
		self.tr()
		self.td(gui.Label("Max Speed:",color=fg), align=-1)
		self.speeddisplay = gui.Input('60', width=60)
		self.speeddisplay.disabled = True
		self.td(self.speeddisplay, alig=-1)
		self.speedslider = gui.HSlider(60,1,200,20,width=BORDER[3],height=16,name='speedslide')

		def updatespeed():
			self.speeddisplay.value = str(self.speedslider.value)

		self.speedslider.connect(gui.CHANGE,updatespeed)
		self.tr()
		self.td(self.speedslider,colspan=3)

		#Set up the display of total and active cells
		self.tr()
		self.td(gui.Label("Total Cells:",color=fg), align=-1)
		self.totalcelldisplay = gui.Input("0", width=60)
		self.totalcelldisplay.disabled = True
		self.td(self.totalcelldisplay, align=-1)
		self.tr()
		self.td(gui.Label("Active Cells:",color=fg), align=-1)
		self.activecelldisplay = gui.Input("0", width=60)
		self.activecelldisplay.disabled = True
		self.td(self.activecelldisplay, align=-1)
		self.tr()
		self.td(gui.Label("Mouse Pos",color=fg), align=-1)
		self.positiondisplay = gui.Input("(0, 0)", width=90)
		self.positiondisplay.disabled = True
		self.td(self.positiondisplay, align=-1)

		#add some save and load buttons
		self.tr()
		svbtn = gui.Button('Save')
		svbtn.connect(gui.CLICK, savedialog)
		self.td(svbtn)
		ldbtn = gui.Button('Load')
		ldbtn.connect(gui.CLICK, loaddialog)
		self.td(ldbtn)

		#self.tr()
		clrbtn = gui.Button('Clear')
		clrbtn.connect(gui.CLICK, sandbox.clear_all)
		self.td(clrbtn)


#shows a save file dialog and attempts to save the current sandbox
def savedialog():
	filename = easygui.filesavebox('SaveFileName', 'Save FallingSand File', '.sbx', FILETYPES)
	result = False
	if filename is not None:
		result = sandbox.save(filename)
	if not result:
		easygui.msgbox("Save Failed")

#shows an open file dialog and attemps to load it
def loaddialog():
	filename = easygui.fileopenbox('SaveFileName', 'Save FallingSand File', '', FILETYPES)
	result = False
	if filename is not None:
		result = sandbox.load(filename)
	if not result:
		easygui.msgbox("Load Failed")


#set up explicit theme selection - needed for py2exe compatibility
theme = gui.Theme(mytheme)
app = gui.App(theme=theme)

#Initialize the gui
mm = MainMenu()
c = gui.Container(align=-1,valign=-1)
c.add(mm,0,0)
app.init(c)

#This is the function that does the painting
def draw(element):
	x0,y0 = pygame.mouse.get_pos() # first steps are to back out the grid position from the screen pos
	if x0 > BORDER[3]+PIXELSIZE:
		x0 = int((x0-BORDER[3])/PIXELSIZE)
		y0 = int((y0-BORDER[0])/PIXELSIZE)
		for xs in range(mm.sld.value):
			for ys in range(mm.sld.value):
				x = x0 + xs
				y = y0 + ys
				if 0 > x or x >= WIDTH:
					continue  # skip any grid positions outside the grid
				if 0 > y or y >= HEIGHT:
					continue  # skip any grid positions outside the grid
				if element is None:
					item = sandbox.grid[x][y]
					if item is not None:
						item.remove_now()  # remove if we are painting with None
				else:
					if sandbox.grid[x][y] is None:
						element(x, y, sandbox, mm.tempslider.value)  # Create the new element

# draw the gui for the first time.  This draws the entire gui.
# Later i use the update function which only updates things that have changed
app.paint()

# generate a surface for use with some renderers.  This ends up being persistant
rendermethod = 1  # select a render method.  This can be changed on the fly.

renderer = renderers.RenderWithGrid2xScale(sandbox, screen)


#Main LOOOOP
running = True # toggled to false when it's time to exit
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 4:  # scroll wheel up
				x0,y0 = pygame.mouse.get_pos()  # check if the mouse is over the sandbox -- The GUI takes care of itself
				if x0 > BORDER[3]+PIXELSIZE:
					if pygame.key.get_mods() & KMOD_LCTRL: # if ctrl is pressed, change temp. Otherwise change brushsize
						mm.tempslider.value += (mm.tempslider.max - mm.tempslider.min)/10
					else:
						mm.sld.value += 1
			app.event(event)
		elif event.type == pygame.MOUSEBUTTONUP:
			if event.button == 5:
				x0,y0 = pygame.mouse.get_pos()
				if x0 > BORDER[3]+PIXELSIZE:
					if pygame.key.get_mods() & KMOD_LCTRL:
						mm.tempslider.value -= (mm.tempslider.max - mm.tempslider.min)/10
					else:
						mm.sld.value -= 1
			app.event(event)
		elif event.type == pygame.KEYDOWN:  # Old keybindings from before there was a GUI.  Quickly change element!
			if event.key == K_0:
				paintelement = None
			elif event.key == K_1:
				paintelement = Water
			elif event.key == K_2:
				paintelement = Wall
			elif event.key == K_3:
				paintelement = Fire
			elif event.key == K_4:
				paintelement = Oil
			elif event.key == K_5:
				paintelement = Lava
			elif event.key == K_6:
				paintelement = Plant
			elif event.key == K_7:
				paintelement = Faucet
			elif event.key == K_8:
				paintelement = Stone
			elif event.key == K_KP_PLUS:  # or brush size!
				mm.sld.value += 1
			elif event.key == K_KP_MINUS:
				mm.sld.value -= 1
			elif event.key == K_p:
				mm.pausebutton.click()  # the P button pauses/unpauses the game
			elif event.key == K_s:  # the s button brings up the save dialog
				savedialog()
			elif event.key == K_l:  # The L button brings up the load dialog
				loaddialog()
			elif event.key == K_F5:  # The F5 button quicksaves
				sandbox.save('QuickSave.sbx')
				print("QuickSave")
			elif event.key == K_F9:  # The F9 button quickloads
				sandbox.load('QuickSave.sbx')
				print("QuickLoad")
			elif event.key == K_a:  # a and b change the render method
				print("changing rendermethod 1")
				rendermethod = 1
				sandbox.full_regen()
			elif event.key == K_b:
				print("changing rendermethod 2")
				rendermethod = 2
				sandbox.full_regen()
			elif event.key == K_g:
				print("Toggling Grid")
				mm.gridbutton.value = not mm.gridbutton.value
			elif event.key == K_c:
				print("Toggling Cursor")
				mm.cursorbutton.value = not mm.cursorbutton.value
			app.event(event)  # make sure the gui gets all events
		else:
			app.event(event)  # make sure the gui gets all events

	sandbox.paused = mm.pausebutton.value # update the sandbox pause state
	sandbox.tick()  # this makes the sandbox go one step.

	if pygame.mouse.get_pressed()[0]:  # left click paints according to the current selected element
		draw(paintelement)
	if pygame.mouse.get_pressed()[2]:  # right click paints None / erases
		draw(None)

	if 0:
		if rendermethod == 1:
			renderers.render_pixarray(sandbox, screen)
		else:
			renderers.render_pixarray_scale(sandbox, srf, screen)
	else:
		renderer.render()

	sandbox.clear_changed() # make sure the sandbox is ready for the next loop

	clock.tick(mm.speed())  # this sets the framerate to selected value (unless we're all bogged down of course)

	app.update(screen)  # update only the changed parts of the GUI
	pygame.display.flip()  # update the display

	pygame.display.set_caption("fallingsand (%.2f fps)" % (clock.get_fps()))  # show the FPS in the title bar

	mm.update_total(len(sandbox.active_elements),len(sandbox.all_elements))  # update the cell count


	x2,y2 = pygame.mouse.get_pos() # first steps are to back out the grid position from the screen pos
	if x2 > BORDER[3]+PIXELSIZE:
		x2 = min(max(0, int((x2-BORDER[3])/PIXELSIZE)), sandbox.width)
		y2 = min(max(0, int((y2-BORDER[0])/PIXELSIZE)), sandbox.height)
		mm.update_mouse_pos(x2, y2)

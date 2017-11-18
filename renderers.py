import pygame
from settings import *
import math


class RenderWithGrid(object):
	def __init__(self, sandbox, screen):
		self.sandbox = sandbox
		self.screen = screen
		self.surface = pygame.Surface((sandbox.width, sandbox.height)) # the most recent screen.  Keep this so we only have to update changed pixels
		self.gridcolor = GRID
		self.cursorcolor = CURSOR
		self.show_grid = False
		self.show_cursor = False
		self.cursorsize = 1
		self.cursor = None
		self.change_cursor_size()

	def change_cursor_size(self, size=1):
		self.cursorsize = size
		self.cursor = pygame.Surface((self.cursorsize * PIXELSIZE, self.cursorsize * PIXELSIZE))
		self.cursor.fill(self.cursorcolor)
		self.cursor.set_alpha(CURSORALPHA)

	def add_cursor(self, srf):
		x0, y0 = pygame.mouse.get_pos() # first steps are to back out the grid position from the screen pos
		x1 = min(max(0, int((x0-BORDER[3])/PIXELSIZE)), self.sandbox.width)
		y1 = min(max(0, int((y0-BORDER[0])/PIXELSIZE)), self.sandbox.height)
		srf.blit(self.cursor, (x1 * PIXELSIZE, y1 * PIXELSIZE))


	def add_grid(self, srf):
		for x in range(self.sandbox.width):
				pygame.draw.line(srf, self.gridcolor, (PIXELSIZE * (x + 1), 0), (PIXELSIZE * (x + 1), self.sandbox.height*PIXELSIZE), 1)
		for y in range(self.sandbox.height):
			pygame.draw.line(srf, self.gridcolor, (PIXELSIZE, PIXELSIZE * y), (self.sandbox.width*PIXELSIZE, PIXELSIZE * y), 1)

	def render(self):
		#srf.fill(BACKGROUND)

		pixarray = pygame.PixelArray(self.surface)
		#pixarray = pygame.surfarray.pixels2d(srf)

		for pos in set(self.sandbox.changedempty):  # update anywhere where elements moved
			#for pos in self.changedempty:  # update anywhere where elements moved
			x0 = pos[0]
			y0 = pos[1]
			pixarray[x0,y0] = BACKGROUND

		#for pos in set(self.changed):  # update anywhere where elements moved
		for pos in self.sandbox.changed:  # update anywhere where elements moved
			x0 = pos[0]
			y0 = pos[1]
			if self.sandbox.grid[pos[0]][pos[1]] is not None:
				clr = self.sandbox.grid[pos[0]][pos[1]].color()
			else:
				clr = BACKGROUND
			pixarray[x0, y0] = clr
		del(pixarray) # have to delete the pixelarray to get it to release the lock on the screen so that we can draw the gui.
		srf2 = pygame.transform.scale(self.surface, (PIXELSIZE*self.sandbox.width, PIXELSIZE*self.sandbox.height))
		if self.show_cursor:
			self.add_cursor(srf2)
		if self.show_grid:
			self.add_grid(srf2)
		self.screen.blit(srf2, (BORDER[3],BORDER[0]))




class RenderWithGrid2xScale(object):
	''' Like regular RenderWithGrid, but it uses the special 2x image scaler.
	If the PIXELSIZE isn't a multiple of 2, this will be weird.
	'''
	def __init__(self, sandbox, screen):
		self.sandbox = sandbox
		self.screen = screen
		self.surface = pygame.Surface((sandbox.width, sandbox.height)) # the most recent screen.  Keep this so we only have to update changed pixels
		self.gridcolor = GRID
		self.cursorcolor = CURSOR
		self.show_grid = False
		self.show_cursor = False
		self.cursorsize = 1
		self.cursor = None
		self.change_cursor_size()

	def change_cursor_size(self, size=1):
		self.cursorsize = size
		self.cursor = pygame.Surface((self.cursorsize * PIXELSIZE, self.cursorsize * PIXELSIZE))
		self.cursor.fill(self.cursorcolor)
		self.cursor.set_alpha(CURSORALPHA)

	def add_cursor(self, srf):
		x0, y0 = pygame.mouse.get_pos() # first steps are to back out the grid position from the screen pos
		x1 = min(max(0, int((x0-BORDER[3])/PIXELSIZE)), self.sandbox.width)
		y1 = min(max(0, int((y0-BORDER[0])/PIXELSIZE)), self.sandbox.height)
		srf.blit(self.cursor, (x1 * PIXELSIZE, y1 * PIXELSIZE))


	def add_grid(self, srf):
		for x in range(self.sandbox.width):
			pygame.draw.line(srf, self.gridcolor, (PIXELSIZE * (x + 1), 0), (PIXELSIZE * (x + 1), self.sandbox.height*PIXELSIZE), 1)
		for y in range(self.sandbox.height):
			pygame.draw.line(srf, self.gridcolor, (PIXELSIZE, PIXELSIZE * y), (self.sandbox.width*PIXELSIZE, PIXELSIZE * y), 1)

	def render(self):
		#srf.fill(BACKGROUND)

		pixarray = pygame.PixelArray(self.surface)
		#pixarray = pygame.surfarray.pixels2d(srf)

		for pos in set(self.sandbox.changedempty):  # update anywhere where elements moved
			#for pos in self.changedempty:  # update anywhere where elements moved
			x0 = pos[0]
			y0 = pos[1]
			pixarray[x0,y0] = BACKGROUND

		#for pos in set(self.changed):  # update anywhere where elements moved
		for pos in self.sandbox.changed:  # update anywhere where elements moved
			x0 = pos[0]
			y0 = pos[1]
			if self.sandbox.grid[pos[0]][pos[1]] is not None:
				clr = self.sandbox.grid[pos[0]][pos[1]].color()
			else:
				clr = BACKGROUND
			pixarray[x0, y0] = clr
		del(pixarray) # have to delete the pixelarray to get it to release the lock on the screen so that we can draw the gui.
		srf2 = pygame.transform.scale2x(self.surface)
		for t in range(int(math.log(PIXELSIZE, 2)) - 1):
			srf2 = pygame.transform.scale2x(srf2)
		#srf2 = pygame.transform.scale(self.surface, (PIXELSIZE*self.sandbox.width, PIXELSIZE*self.sandbox.height))
		if self.show_cursor:
			self.add_cursor(srf2)
		if self.show_grid:
			self.add_grid(srf2)

		for se in tuple(self.sandbox.special_effects):
			se.render(srf2)
		self.screen.blit(srf2, (BORDER[3],BORDER[0]))


class SpecialEffectLine(object):
	def __init__(self, x0, y0, x1, y1, sandbox, color=None, lifetime=1, width=1):
		self.x0, self.y0, self.x1, self.y1 = x0, y0, x1, y1
		self.sandbox = sandbox
		if color is None:
			self.color = (255, 255, 255, 100)
		else:
			self.color = color
		self.lifetime = lifetime
		self.width = 1
		self.sandbox.special_effects.add(self)

	def render(self, srf):
		pygame.draw.line(srf, self.color, (self.x0*PIXELSIZE + PIXELSIZE/2, self.y0*PIXELSIZE + PIXELSIZE/2), (self.x1*PIXELSIZE + PIXELSIZE/2, self.y1*PIXELSIZE + PIXELSIZE/2), self.width)
		self.lifetime -= 1
		if self.lifetime <= 0:
			self.sandbox.special_effects.discard(self)



import math
import pickle as pickle
from settings import *
import sys
import time


class Sandbox(object):
	def __init__(self, width, height):
		self.height, self.width = height, width
		self.grid = self.generate_empty_grid()

		# using sets seems to work just as fast as lists here.  The big benefit is that you can check if
		# an item is in them already without looping over them because they act a lot like dicts
		# they also have a built in function for removal only if the item is in the set (dispose)
		self.active_elements = set()
		self.all_elements = set()
		self.toremove = []
		self.changed = set()
		self.changedempty = []
		self.post_spawn = []
		self.post_transform = []
		self.after_functions = []
		self.paused = False
		self.special_effects = set()
	
	def generate_empty_grid(self):
		return [[None for y in range(self.height)] for x in range(self.width)]

	def tick(self):
		if not self.paused:
			[z.act() for z in tuple(self.active_elements)]

			# some things need to make sure they are there the whole frame so that their neighbors don't get
			# confused.  They get to change here.
			if self.post_spawn:
				for fn, x, y in self.post_spawn:
					if self.grid[x][y] is None:
						fn(x, y, self)
				self.post_spawn[:] = []

			if self.post_transform:
				for cls, x in self.post_transform:
					cls.transform(x)
				self.post_transform[:] = []

			if self.toremove:
				self.remove_delayed()

	def clear_changed(self):
		# this should get called after rendering is done
		self.changedempty[:] = []
		self.changed.clear()

	def remove_delayed(self):
		for x in self.toremove:
			x.remove_now()
		self.toremove[:] = []

	def full_regen(self):
		#This will force a redraw of the whole screen on the next render
		for x in range(len(self.grid)):
			for y in range(len(self.grid[x])):
				self.changed.add((x, y))
	
	def clear_all(self):
		self.grid = self.generate_empty_grid()
		self.active_elements.clear()
		self.all_elements.clear()
		self.toremove[:] = []
		self.clear_changed()
		self.post_spawn[:] = []
		self.post_transform[:] = []
		self.full_regen()

	def save(self, filename):
		try:
			self.special_effects = []
			rl = sys.getrecursionlimit()
			sys.setrecursionlimit(self.width*self.height*100)
			f = open(filename, 'wb')
			pickle.dump(self.__dict__, f, 2)
			f.close()
			sys.setrecursionlimit(rl)
		except:
			return False
		return True

	def load(self, filename):
		try:
			f = open(filename, 'rb')
			tmp = pickle.load(f)
			f.close()
		except:
			return False
		self.__dict__.update(tmp)
		for i in self.all_elements:
			i.sandbox = self
		self.full_regen()
		return True



class Automata(object):
	#This is the base cell class.  All others should inherit from this or one of its derivatives
	name = "Base Automata"
	basecolor = (100, 100, 100)

	def __init__(self, x, y, sandbox, *args, **kwargs):
		self.x, self.y = x, y
		self.sandbox = sandbox
		self.frozen = False
		self.nearlistfull = []
		self.nearlistpartial = []
		self.acted = False
		self.lastupdate = 0
		self.abort = False
		self.stage = 1
		self.stages = 3
		self.regen_near_full()
		self.regen_near_partial()
		self.touch_neighbors()
		self.register()
		self.removed = False
		self.on_create()

	def on_create(self):
		pass

	def regen_near_full(self, x=None, y=None):
		"""this looks up the cell's neighbors from the grid and
		returns the list as shown here.  It also puts it in the
		self.nearlistfull so it doesn't need generated again
		the list is a tuple containing a clockwise list of
		elements next to this one starting at the top left
		0	1	2
		7	x	3
		6	5	4

		"""
		if x is None:  # this can work on a passed point, or by default, the cell's position
			x = self.x
		if y is None:
			y = self.y
		grid = self.sandbox.grid

		#lots of bounds checking and such here
		if x > 0:
			if y > 0:
				n0 = grid[x-1][y-1]
			else:
				n0 = None
			if y < HEIGHT - 1:
				n6 = grid[x-1][y+1]
			else:
				n6 = None
			n7 = grid[x-1][y]
		else:
			n0,n6,n7 = None, None, None
		if x < WIDTH - 2:
			if y > 0:
				n2 = grid[x+1][y-1]
			else:
				n2 = None
			n3 = grid[x+1][y]
			if y < HEIGHT - 2:
				n4 = grid[x+1][y+1]
			else:
				n4 = None
		else:
			n2,n3,n4 = None, None, None
		if y > 0:
			n1 = grid[x][y-1]
		else:
			n1 = None
		if y < HEIGHT - 2:
			n5 = grid[x][y+1]
		else:
			n5 = None
		self.nearlistfull = (n0, n1, n2, n3, n4, n5, n6, n7)
		return self.nearlistfull

	def near_all(self):
		x0 = self.x
		y0 = self.y
		positions = []
		for x in (x0-1, x0, x0+1):
			for y in (y0-1, y0, y0+1):
				if self.position() != (x, y) and 0 < x < WIDTH and 0 < y < HEIGHT:
					positions.append((x, y))
		return positions

	def near_empty(self):
		return [n for n in self.near_all() if self.sandbox.grid[n[0]][n[1]] is None]

	def near_nonempty(self):
		return [n for n in self.nearlistfull if n is not None]

	def regen_near_partial(self):
		#this removes all None's from nearlistfull
		self.nearlistpartial = [n for n in self.nearlistfull if n is not None]
		return self.nearlistpartial

	def touch_neighbors(self):
		# After somethign happens to a cell that should cause it's neighbors to unfreeze, this takes care of that
		[z.thaw() for z in self.nearlistpartial]

	def register(self):
		# sets up this element into all the needed sandbox lists/sets/whatever
		self.sandbox.grid[self.x][self.y] = self
		self.sandbox.changed.add((self.x, self.y))
		self.sandbox.active_elements.add(self)
		self.sandbox.all_elements.add(self)

	def act(self):
		pass

	def color(self):
		return self.basecolor

	def remove_delayed(self):
		#sets this element up to be removed on the removal pass after the acting pass of the sandbox
		#needed for cells where other cells actions depends heavily on whether this one exists
		self.acted = True
		self.removed = True
		self.abort = True
		self.sandbox.toremove.append(self)

	def remove_now(self):
		#immediately removes this element from the sandbox.
		self.acted = True
		self.sandbox.changedempty += [(self.x, self.y)]
		self.sandbox.grid[self.x][self.y] = None
		self.removed = True
		self.sandbox.active_elements.discard(self)
		self.sandbox.all_elements.discard(self)
		self.abort = True
		self.regen_near_full() # Make sure we update the list of neighbors before touching, otherwise
		self.regen_near_partial() # we run the risk of thawing elements that are removed but not
		self.touch_neighbors() # deleted yet which is bad. (particularly for elements that spawn others)

	def changed(self):
		#call this when your element has changed and needs to be redrawn
		self.acted = True
		self.frozen = False
		self.sandbox.changed.add((self.x, self.y))
		self.lastupdate = 0

	def freeze(self):
		#takes the element out of the active list without deleting it
		#so static items can be skipped during the act loop
		self.frozen = True
		self.sandbox.active_elements.discard(self)

	def thaw(self):
		#puts the element back into the active list
		if not self.removed:
			self.frozen = False
			self.acted = False
			self.lastupdate = 0
			self.sandbox.active_elements.add(self)

	def nearbypos(self,radius=1):
		#this returns x, y pairs of points within a certain radius.
		#useful for explosions and such
		x, y = self.x, self.y
		l = []
		for xt in range(max(0,x-radius),min(WIDTH,x+radius+1)):
			for yt in range(max(0,y-radius),min(HEIGHT,y+radius+1)):
				if math.sqrt( (x-xt)**2 + (y-yt)**2) <= radius:
					if (xt, yt) != (x, y):
						l.append((xt, yt))
		return l

	def neighbors(self,radius=1):
		#this returns x, y pairs of points within a cartesian distance
		x, y = self.x, self.y
		l = []
		for xt in range(max(0,x-radius),min(WIDTH,x+radius+1)):
			for yt in range(max(0,y-radius),min(HEIGHT,y+radius+1)):
				if (xt, yt) != (x, y):
					l.append((xt, yt))
		return l
	
	def transform(self, final):
		#for when a cell needs to turn into another one.
		#This is instant, so use the sandbox.post_transform list to do it after act phase is over
		self.acted = True
		self.remove_now()
		final(self.x, self.y, self.sandbox)

	def on_create(self):
		pass

	def position(self):
		return self.x, self.y

	def move(self, direction=None, gravity=True):
		"""sets a new x&y position based on a direction tuple"""
		#actually moves the cell, as opposed to deleting and creating a new one
		if direction is None:
			direction = (0, 1)
		oldx = self.x
		oldy = self.y
		self.x += direction[0]
		self.y += direction[1]
		if self.x <= 0 or self.x >= WIDTH:
			self.x -= direction[0]
			self.y -= direction[1]
			self.remove_now()
			return

		if self.y <= 0 or self.y >= HEIGHT:
			self.x -= direction[0]
			self.y -= direction[1]
			self.remove_now()
			return
		self.changed()

		self.sandbox.grid[oldx][oldy] = None
		self.sandbox.grid[self.x][self.y] = self

		self.changed()

		#changed.append((self.x, self.y))
		self.sandbox.changedempty.append((oldx, oldy))
		#changedempty += [(oldx, oldy)]
		self.touch_neighbors()

	def color(self):
		return self.basecolor

	def dist_to_point(self, x, y):
		xt = self.x
		yt = self.y
		return math.sqrt((x1-xt)**2 + (y-yt)**2)

	def ray_to_points(self, x1, y1):
		''' Returns all the points between this object and x, y'''
		saw = []
		x0 = self.x
		y0 = self.y
		xdir = 1
		if x0 > x1:
			xdir = -1

		ydir = 1
		if y0 > y1:
			ydir = -1

		dx = float(x0 - x1)
		dy = float(y0 - y1)
		y = self.y
		x = self.x
		err = 0.0
		if abs(dx) > abs(dy):
			if dx != 0:
				derr = abs(dy / dx)
				for x in range(x0, x1+xdir, xdir):
					if (x0, y0) != (x, y):
						saw.append((x, y))
					err = err + derr
					if err > 0.5:
						y += ydir
						err -= 1
			else:
				for x in range(x0, x1+xdir, xdir):
					if (x0, y0) != (x, y):
						saw.append((x, y))
		else:
			if dy != 0:
				derr = abs(dx / dy)
				for y in range(y0, y1+ydir, ydir):
					if (x0, y0) != (x, y):
						saw.append((x, y))
					err = err + derr
					if err > 0.5:
						x += xdir
						err -= 1
			else:
				for y in range(y0, y1+ydir, ydir):
					if (x0, y0) != (x, y):
						saw.append((x, y))

		return saw


class Debug(Automata):
	name = "Debug"
	def __init__(self, x, y, sandbox, *args, **kwargs):
		print (x, y)

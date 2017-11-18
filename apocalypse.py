from sandbox import Automata
from renderers import SpecialEffectLine
from settings import *
import random
import math
import time

class Apocalypse(Automata):
	name = 'Apocalypse Actor'
	basecolor = (255, 255, 255)
	vision = 4
	attack_strength = 3.0
	defense_strength = 3.0
	weapon_strength = 1.0
	health = 10.0
	maxhealth = 10.0
	target = None
	basespeed = .75

	def attack(self, victim):
		dmg = 1.0 + (self.attack_strength / victim.defense_strength) * self.weapon_strength
		victim.damage(dmg)

	def damage(self, amount):
		self.health -= amount
		if self.health <= 0:
			self.remove_delayed()

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

	def FloodFill2(self,x,y):
		changetile = self.tile(x,y)
		que = []
		que.append((x,y))
		maxy = len(self.mapdata)
		maxx = len(self.mapdata[0])
		while que:
			x,y = que.pop()
			if self.tile(x,y) == self.selectedtile:
				return
			while (y >= 0) and (self.tile(x,y) == changetile):
				y = y - 1
			y += 1
			sl = False
			sr = False
			while (y < maxy) and (self.tile(x,y) == changetile):
				self.paint(x,y)
				if (not sl) and (x > 0) and (self.tile(x-1,y) == changetile):
					sl = True
					que.append((x-1,y))
				elif (sl) and (x > 0) and (self.tile(x-1,y) != changetile):
					sl = False

				if (not sr) and (x < maxx-1) and (self.tile(x+1,y) == changetile):
					sr = True
					que.append((x+1,y))
				elif (sr) and (x < maxx-1) and (self.tile(x+1,y) != changetile):
					sr = False
				y += 1

	def near_circle(self, radius):
		pts = []
		x = radius
		y = 0
		err = 1 - radius
		x0 = self.x
		y0 = self.y
		while x >= y:
			pts.append((x + x0, y + y0))
			pts.append((y + x0, x + y0))
			pts.append((-x + x0, y + y0))
			pts.append((-y + x0, x + y0))
			pts.append((-x + x0, -y + y0))
			pts.append((-y + x0, -x + y0))
			pts.append((x + x0, -y + y0))
			pts.append((y + x0, -x + y0))
			y += 1
			if err < 0:
				err += 2.0 * y + 1.0
			else:
				x -= 1
				err += 2.0 * (y - x + 1.0)
		return pts

	def line_of_sight(self):
		ti = []
		visible = []
		ti.append(time.time())
		nc = self.near_circle(self.vision)
		ti.append(time.time())
		checked = set()
		for pt in nc:
			t = self.ray_to_points(pt[0], pt[1])
			for z in t:
				if z in checked:  # t = .001 - .004 vs .002 - .007 without set
					break
				checked.add(z)
				if 0 < z[0] < WIDTH and 0 < z[1] < HEIGHT:
					i = self.sandbox.grid[z[0]][z[1]]
					if not isinstance(i, Wall):
						if i is not None:
							visible.append(i)
					else:
						break
				else:
					break

		ti.append(time.time())
		print ti, [ti[0] - n for n in ti]
		return visible




	def pathfind(self, x, y):
		ray = self.ray_to_points(x, y)
		if ray:
			return ray[0]
		else:
			return None

	def speed(self):
		if self.health > 0:
			return self.basespeed * self.maxhealth / self.health
		else:
			return 0


class Zombie(Apocalypse):
	name = 'Zombie'
	basecolor = (119, 227, 52)
	ragecolor = (242, 175, 51)
	vision = 20
	basespeed = .5

	def act(self):
		#make sure we are not dead
		if self.removed:
			return
		if self.health <= 0:
			self.remove_delayed()
			return
		self.regen_near_full()

		# if we are next to humans, attack.
		hmn = self.near_human()
		if hmn:
			self.attack(hmn)
			SpecialEffectLine(self.x, self.y, hmn.x, hmn.y, self.sandbox)
			return

		if self.target:
			SpecialEffectLine(self.x, self.y, self.target[-1][0], self.target[-1][1], self.sandbox)

		if random.random() < self.speed():
			newpos = None
			#look around for some food (brains)
			if self.target:  # If we already have a goal destination
				newpos = self.target.pop(0)
				if newpos == self.position():
					self.target = None
					return
			else:
				#food = self.look_for_food()
				food = self.look_for_food2()
				if food is not None:
					self.target = self.ray_to_points(food.x, food.y)
					return
			if newpos is None:
				newpos = random.choice(self.near_all())

			if self.sandbox.grid[newpos[0]][newpos[1]] is None:
				self.move((newpos[0] - self.x, newpos[1] - self.y))
				self.changed()
			else:
				self.target = None

	def color(self):
		if self.target:
			return self.ragecolor
		else:
			return self.basecolor

	def look_for_food(self):
		targets = self.line_of_sight()
		for t in targets:
			if isinstance(t, Human):
				return t
		return None

	def near_human(self):
		for n in self.nearlistfull:
			if isinstance(n, Human):
				return n
		return None

	def look_for_food2(self):
		nc = self.nearbypos(self.vision)
		#nc = self.near_circle(self.vision)
		for pt in nc:
			i = self.sandbox.grid[pt[0]][pt[1]]
			if isinstance(i, Human):
				rti = self.ray_to_points(i.x, i.y)
				through = False
				for z in rti:
					c = self.sandbox.grid[z[0]][z[1]]
					if isinstance(c, Wall):
						break
					if c == i:
						return i
		return None


class Human(Apocalypse):
	name = 'Human'
	basecolor = (52, 113, 227)

	def act(self):
		pass



class Barricade(Apocalypse):
	name = 'Barricade'
	basecolor = (143, 72, 14)

	def act(self):
		self.freeze()


class Wall(Apocalypse):
	name = 'Wall'
	basecolor = (77, 37, 4)

	def act(self):
		self.freeze()



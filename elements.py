import random
from sandbox import Automata
from settings import *
import math


class Element(Automata):
	moverate = 0.5
	conductivity = 1
	basecolor = (255, 255, 255)
	name = "Base Element"
	gravity = 0
	density = 100
	liquid = False
	removed = False

	def __init__(self, x, y, sandbox, temperature=None):
		self.x, self.y = x, y
		self.sandbox = sandbox
		if sandbox.grid[x][y] is not None:
			self.remove_delayed()
			return

		self.temperature = temperature
		self.on_create()
		if temperature is None:
			if self.temperature is None:
				self.temperature = DEFAULTTEMP
		else:
			self.temperature = temperature
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

	def decidemove(self):
		""" This decides where the cell should move, if anywhere based on density, etc  """
		if self.gravity > 0:
			if self.nearlistfull[5] is None:
				return ((0,1))
			elif self.nearlistfull[6] is None:
				return ((-1,1))
			elif self.nearlistfull[4] is None:
				return ((1,1))
			elif self.liquid:
				if self.nearlistfull[7] is None:
					return((-1,0))
				elif self.nearlistfull[3] is None:
					return ((1,0))
				elif self.name != self.nearlistfull[5].name:
					self.densitycheck(self.nearlistfull[5])
					return None
		elif self.gravity < 0:
			if self.nearlistfull[1] is None:
				return((0,-1))
			elif self.nearlistfull[0] is None:
				return((-1,-1))
			elif self.nearlistfull[2] is None:
				return((1,-1))
			else:
				if self.liquid:
					if self.nearlistfull[7] is None:
						return((-1,0))
					elif self.nearlistfull[3] is None:
						return((1,0))

	def act(self):
		if self.removed:
			return
		if self.acted:
			self.lastupdate = 0
			self.acted = False
		self.regen_near_full()
		self.regen_near_partial()

		self.temp_action() #even frozen points need to check whether their temperature change effected them
		if self.frozen or self.abort:
			return
		self.stage = (self.stage +1) % self.stages
		self.abort = False
		randout = False

		if self.stage == 0:
			[self.temperate(z) for z in self.nearlistpartial]
			#map(lambda x: self.temperate(x), self.nearlistpartial)
		elif self.stage == 1:
			[self.reaction(z) for z in self.nearlistpartial]
			#map(lambda x: self.reaction(x), self.nearlistpartial)
		if self.abort:
			return
		elif self.stage == 2:
			if random.random() < self.moverate:
				v = self.decidemove()
				if v:
					self.move(v)
			else:
				randout = True
		if not self.acted:
			if not randout:
				if self.lastupdate > MAXUPDATE:
					self.freeze()
				else:
					self.lastupdate += 1
		else:
			self.touch_neighbors()
		#self.last_thing()

	def TransferHeat(self, degrees):
		""" This function accepts heat from another element """
		self.temperature += degrees
		if degrees > self.temperature / 10:
			self.changed() # only a change of 10% or greater wakes this element up

		if self.temperature < 1:
			self.temperature = 1
		elif self.temperature > 2000:
			self.temperature = 2000

	def temperate(self, touching):
		""" This function checks nearby cells and sends them heat """
		if self.temperature == touching.temperature:
			return
		r = random.random()
		if r > GLOBAL_TEMP_RATE:
			kc = min(self.conductivity, touching.conductivity)

			dt = (self.temperature-touching.temperature)*kc*GLOBAL_TEMP_FACTOR
			if math.isnan(dt):
				raise Exception("Temperature was a nan.  That's not a good thing.  Probably a conductivity too high")
			if -1 < dt < 1:
				return
			self.temperature -= dt
			if self.temperature < 1:
				self.temperature = 1
			elif self.temperature > 2000:
				self.temperature = 2000
			touching.TransferHeat(dt)
			if dt > self.temperature / 10:
				self.changed()

	def densitycheck(self, item, below=True):
		"""checks density of what's below to see if it can take its place"""
		proceed = False
		if below:
			if item.density < self.density:
				proceed = True
		else:
			if item.density > self.density:
				proceed = True

		if proceed:
			x0 = self.x
			y0 = self.y
			x1 = item.x
			y1 = item.y
			self.x = x1
			self.y = y1
			item.x = x0
			item.y = y0
			self.sandbox.grid[self.x][self.y] = self
			self.sandbox.grid[item.x][item.y] = item
			self.acted = True
			item.acted = True
			self.sandbox.changed.add((self.x, self.y))
			self.sandbox.changed.add((item.x, item.y))

	def temp_action(self):
		pass


	def reaction(self, touching):
		pass

	def transform(self, final):
		self.acted = True
		self.remove_now()
		final(self.x, self.y, self.sandbox, self.temperature)

class Water(Element):
	name = "Water"
	basecolor = (50, 50, 255)
	conductivity = 1.0
	moverate = .8
	gravity = 1
	density = 20
	liquid = True

	def temp_action(self):
		if self.temperature > 378:
			if random.random() < .5:
				self.transform(Steam)


class Oil(Element):
	name = 'Oil'
	basecolor = (180, 180, 180)
	moverate = .4
	gravity = 1
	density = 10
	conductivity = .50
	liquid = True

	def temp_action(self):
		if self.temperature > 500:
			if random.random() < .2:
				self.transform(Fire)


class Steam(Element):
	name = "Steam"
	basecolor = (50, 50, 150)
	moverate = .8
	gravity = -1
	density = 1
	conductivity = 1
	liquid = True

	def temp_action(self):
		if self.temperature < 370:
			if random.random() < .5:
				self.transform(Water)


class Stone(Element):
	name = "Stone"
	basecolor = (90, 90, 90)
	moverate = .5
	gravity = 0
	liquid = False
	density = 100
	conductivity = .30
	c1 = (90, 90, 90)
	c2 = (200, 90, 90)
	ctv = c2[0] - c1[0], c2[1] - c1[1], c2[2] - c1[2]
	transition = 1050.0

	def on_create(self):
		self.freeze()

	def color(self):
		if self.temperature < 0:
			return self.c1
		percent = self.temperature / self.transition
		deltac = [percent*z for z in self.ctv]
		newc = (self.c1[0] + deltac[0], self.c1[1] + deltac[1], self.c1[2] + deltac[2])
		color = tuple(int(min(abs(a),abs(b))) for a, b in zip(newc,self.c2))
		return color

	def temp_action(self):
		if self.temperature > self.transition:
			self.transform(Lava)


class Wall(Element):
	name = "Wall"
	basecolor = (100, 100, 100)
	moverate = .5
	gravity = 0
	liquid = False
	density = 100
	conductivity = .30

	def on_create(self):
		self.freeze()





class Fire(Element):
	name = 'Fire'
	basecolor = (200, 50, 50)
	moverate = .5
	gravity = -1
	density = 1
	liquid = True
	conductivity = 10.0

	def on_create(self):
		self.temperature = 1000.0

	def temp_action(self):
		if random.random() > .96:
			self.remove_now()


class Lava(Element):
	name = 'Lava'
	basecolor = (200, 90, 90)
	moverate = .2
	gravity = 1
	density = 80
	liquid = True
	conductivity = 1.
	transition = 900.0

	def on_create(self):
		self.temperature = 2000.0

	def temp_action(self):
		if self.temperature < self.transition:
			self.transform(Stone)


class Plant(Element):
	name = 'Plant'
	basecolor = (40, 240, 30)
	moverate = .5
	gravity = 0
	density = 80
	liquid = False
	conductivity = .40
	water_rate = 0.02
	fire_rate = 0.1

	def temp_action(self):
		if self.temperature > 700:
			if random.random() < .2:
				self.transform(Fire)

	def reaction(self, touching):
		rv = random.random()
		if touching.name == 'Water':
			if rv < self.water_rate:
				touching.transform(Plant)
		if touching.name == 'Fire':
			if rv < self.fire_rate:
				self.transform(Fire)


class Faucet(Element):
	name = "Faucet"
	basecolor = (110, 110, 255)
	conductivity = 1.0
	moverate = .7
	gravity = 0
	density = 20

	def act(self):
		if self.y < self.sandbox.height:
			if self.sandbox.grid[self.x][self.y+1] is None:
				Water(self.x, self.y+1, self.sandbox, self.temperature)


class Boom(Element):
	name = 'Boom'
	basecolor = (250, 100, 0)
	moverate = .5
	gravity = 0
	density = 100
	liquid = False
	conductivity = 10.0
	reproduce = 0.80
	fire = 0.75
	obliterate = 0.6

	def on_create(self):
		self.temperature = 1000.0

	def temp_action(self):
		for z in self.nearbypos():
			i = self.sandbox.grid[z[0]][z[1]]
			r = random.random()
			if i is None:
				if r > self.reproduce:
					#new = Water(self.x, self.y+1, self.grid, self.active, self.temperature)
					Boom(z[0], z[1], self.sandbox, 1000)
				elif r > self.fire:
					Fire(z[0], z[1], self.sandbox, 1000)
					#z.transform(Boom)
			else:
				if r > self.reproduce:
					i.transform(Boom)
				elif r > self.fire:
					i.transform(Fire)
				elif r > self.obliterate:
					i.remove_now()
		self.remove_now()


class KaBoom(Element):
	name = 'KaBoom'
	basecolor = (250, 100, 0)
	moverate = .5
	gravity = 0
	density = 100
	liquid = False
	conductivity = 10.0
	radius = 8
	firerate = 0.8
	boomrate = 0.9

	def on_create(self):
		self.temperature = 1000.0


	def temp_action(self):
		for z in self.nearbypos(self.radius):
			i = self.sandbox.grid[z[0]][z[1]]
			r = random.random()
			if i is None:
				if r > self.boomrate:
					Boom(z[0], z[1], self.sandbox, 1000)
				elif r > self.firerate:
					Fire(z[0], z[1], self.sandbox, 1000)
			else:
				if r > self.boomrate:
					Boom(z[0], z[1], self.sandbox, 1000)
				elif r > self.firerate:
					Fire(z[0], z[1], self.sandbox, 1000)
				else:
					i.remove_now()
		self.remove_now()
	

class TnT(Element):
	name = 'TnT'
	basecolor = (200, 150, 150)
	moverate = .5
	gravity = 0
	density = 100
	liquid = False
	conductivity = 0.4
	volatility = .6

	def temp_action(self):
		if self.temperature > 500:
			self.transform(KaBoom)

	def reaction(self, touching):
		rv = random.random()
		if touching.name in ('Fire','KaBoom','Boom'):
			if rv > self.volatility:
				self.transform(KaBoom)


class SteadyTemp(Element):
	""" This element can be used as a cooler or a heater depending on the temp it is created at """
	name = "SteadyTemp"
	basecolor = (255, 100, 100)
	gravity = 0
	liquid = False
	density = 100
	conductivity = .30

	c1 = (192, 192, 250)
	c2 = (255, 85, 96)
	ctv = c2[0] - c1[0], c2[1] - c1[1], c2[2] - c1[2]
	transition = 2000.0

	def on_create(self):
		self.freeze()
		clr_cold = (192, 192, 250)
		clr_hot = (255, 85, 96)
		clr_delta = (clr_hot[0] - clr_cold[0], clr_hot[1] - clr_cold[1], clr_hot[2] - clr_cold[2])
		v1 = 1
		val = self.temperature
		v2 = 2000
		percent = float(val - v1) / float(v2 - v1)
		clr_now = (int(clr_cold[0] + percent*clr_delta[0]), int(clr_cold[1] + percent*clr_delta[1]), int(clr_cold[2] + percent*clr_delta[2]))
		self.mycolor = clr_now

	def color(self):
		return self.mycolor

	def act(self):
		if self.removed:
			return
		self.regen_near_full()
		self.regen_near_partial()

		self.temp_action() #even frozen points need to check whether their temperature change effected them

		self.stage = (self.stage +1) % self.stages

		if self.stage == 0:
			[self.temperate(z) for z in self.nearlistpartial]

	def freeze(self):
		pass
	
	def temperate(self, touching):
		if self.temperature == touching.temperature:
			return
		r = random.random()
		if r > GLOBAL_TEMP_RATE:
			kc = min(self.conductivity, touching.conductivity)

			dt = (self.temperature-touching.temperature)*kc*GLOBAL_TEMP_FACTOR
			touching.TransferHeat(dt)
			if dt > self.temperature / 10:
				self.changed()
	def TransferHeat(self, dt):
		pass


class Insulator(Element):
	""" This element does not transfer heat """
	name = "Insulator"
	basecolor = (255, 255, 100)
	gravity = 0
	liquid = False
	density = 100
	conductivity = 0

	def temperate(self, touching):
		pass
	def TransferHeat(self, dt):
		pass
	def act(self):
		self.freeze()







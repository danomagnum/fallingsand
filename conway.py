from sandbox import Automata
from elements import Element
import math


class Conway(Element):
	name = "Conway"
	basecolor = (255, 255, 255)

	def act(self):
		self.regen_near_full()
		self.regen_near_partial()
		neighbors = len(self.nearlistpartial)
		if neighbors < 2:
			self.remove_delayed()
		elif neighbors > 3:
			self.remove_delayed()
		#for pos in self.nearbypos():
		for pos in self.neighbors():
			if self.sandbox.grid[pos[0]][pos[1]] is None:
				self.multiply(pos[0],pos[1])

	def multiply(self, x, y):
		nearlist = self.regen_near_full(x, y)
		if len([z for z in nearlist if z is not None]) == 3:
		#if len([z for z in nearlist if isinstance(z, Conway)]) == 3:
			self.sandbox.post_spawn.append((Conway, x, y))

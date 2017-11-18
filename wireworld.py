from sandbox import Automata
from elements import Element, KaBoom
import random


class Wire(Element):
	name = "Wire"
	basecolor = (227, 173, 234)

	def act(self):
		self.regen_near_full()
		self.regen_near_partial()

		count = 0
		for i in self.nearlistpartial:
			if isinstance(i,Power):
				count += 1

		if 1 <= count <= 2:
			self.sandbox.post_transform.append((self, Power))
		self.freeze()

class Power(Element):
	name = "Electron"
	basecolor = (173, 234, 201)

	def act(self):
		self.regen_near_full()
		self.regen_near_partial()
		self.sandbox.post_transform.append((self, Tail))
		for z in self.nearlistpartial:
			if z.name in ('TnT',):
				self.sandbox.post_transform.append((z, KaBoom))


class Tail(Element):
	name = "ElectronTail"
	basecolor = (234, 234, 173)

	def act(self):
		self.regen_near_full()
		self.regen_near_partial()
		#self.transform(Wire)
		#self.changeto = Wire
		self.sandbox.post_transform.append((self, Wire))


class Generator(Element):
	name = "Generator"
	basecolor = (173, 234, 201)

	def act(self):
		self.regen_near_full()
		self.regen_near_partial()
		if random.random() > 0.8:
			for i in self.nearlistpartial:
					if isinstance(i, Wire):
						self.sandbox.post_transform.append((i, Power))


class Electron(Element):
	""" This class is like the Power class, but user placeable"""
	name = "Electron"
	basecolor = (173, 234, 201)

	def act(self):
		self.regen_near_full()
		self.regen_near_partial()
		for i in self.nearlistpartial:
				if isinstance(i, Wire):
					self.sandbox.post_transform.append((i, Power))
		self.remove_now()

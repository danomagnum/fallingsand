# fallingsand
Python Cellular Automata

Newer info can be found [here](http://danomagnum.com/wiki/fallingsand2)

Here is the old readme:

Python FallingSand -- danomagnum.com 2014

Update 2014-05-07 -- ZOMBIES!!
	This is not complete yet, so don't let zombies or humans (or walls actually since they are the apocalypse walls instead of fallingsand walls) come into contact with other cells.  This breaks the game.

This is a falling sand game implemented in python (2.7 is the target).  It also allows for various cellular atomata to be impletmented fairly easily.

It currently has conways game of life and wireworld implemented in it along with the falling sand elements.

Some of the falling sand element could be improved upon such as oil which should turn into fire upon touching fire.  It should also increase its temperature a nominal amount to simulate heat of combustion.o

However, it is still pretty complete and works well.

python3 worked at one point, but was abandoned for py2exe compatability.  it could be added back through a quick edit of fallingsand.py -- see the comments there.  HOWEVER, python 3 runs slower than python 2.7 and isn't recommended.

Compatibility with pypy and python3 is there for the simulation portion of the code, but not for the interface.  A new interface would be fairly simple; a renderer for the actual game screen could be created (see renderers.py) and then a new gui to replace the one in fallingsand.py.  Until then, it's not possible; the pgu gui I'm using depends on pygame.  Porting the actual simulation engine woudl be simpler than porting the gui; looking at renderers.py should give an idea of how to do this.



from distutils.core import setup
import py2exe
import os

origIsSystemDLL = py2exe.build_exe.isSystemDLL

def IsSystemDLL(pathname):
	if os.path.basename(pathname).lower() in ["sdl_ttf.dll"]:
		return 0
	return origIsSystemDLL(pathname)
py2exe.build_exe.isSystemDLL = IsSystemDLL
setup(console=['fallingsand.py'])
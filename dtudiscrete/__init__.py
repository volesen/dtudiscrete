import os, sys
from os.path import abspath, basename, dirname, isfile

import glob
import importlib



# Dynamically import all modules in the package.
__all__ = []

sys.path.insert(0, dirname(abspath(__file__))) # Path hack.

for modname in map(
	lambda p: basename(p).replace(".py", ""),
	filter(
		lambda p: isfile(p) and '__' not in p,
		glob.glob( dirname(__file__) + os.sep + "*.py" )
	)
) :
	
	# Import the Module into global scope.
	globals()[modname] = importlib.import_module(modname) # Deeply illegal hackery
	
	# Make sure it's added to __all__.
	__all__ += [modname]

del sys.path[0] # Cleanup our path hack.


# Do No Evil... Evil has been Done.

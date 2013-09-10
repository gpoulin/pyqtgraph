#!/usr/bin/env python

import sys
import os
import subprocess
import inspect

try:
    from PyQt4 import QtCore
except ImportError:
    from PySide import QtCore



pyqtgraph_path=os.path.abspath(os.path.join(os.path.dirname(inspect.getfile(
    inspect.currentframe())),'..'))

env = os.environ.copy()
env['PYQTDESIGNERPATH'] = os.path.join(pyqtgraph_path,'designer/plugins/')
env['PYTHONPATH'] = pyqtgraph_path

designer_bin = QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.BinariesPath)

if sys.platform == 'darwin':
    designer_bin += '/Designer.app/Contents/MacOS/Designer'
else:
    designer_bin += '/designer'

subprocess.Popen([str(designer_bin)],env=env)

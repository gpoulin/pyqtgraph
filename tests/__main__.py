import sys, os

if __name__ == "__main__" and (__package__ is None or __package__==''):
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, parent_dir)
    import tests
    __package__ = "tests"

from . import test
from .functions import siEval, siFormat, siScale
from .svg import SVGTest

if __name__ == "__main__":
    test.unittest.main()

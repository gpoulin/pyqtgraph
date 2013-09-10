#!/usr/bin/env python

from pyqtgraph.Qt import QtGui
from pyqtgraph import ValueLabel
from pyqtgraph.Qt import USE_PYSIDE

if USE_PYSIDE:
    from PySide import QtDesigner
else:
    from PyQt4 import QtDesigner


class PyValueLabelPlugin(QtDesigner.QPyDesignerCustomWidgetPlugin):

    """PyValueLabelPlugin(QtDesigner.QPyDesignerCustomWidgetPlugin)

    Provides a Python custom plugin for Qt Designer by implementing the
    QDesignerCustomWidgetPlugin via a PyQt-specific custom plugin class.
    """

    # The __init__() method is only used to set up the plugin and define its
    # initialized variable.
    def __init__(self, parent=None):

        super(PyValueLabelPlugin, self).__init__(parent)

        self.initialized = False

    # The initialize() and isInitialized() methods allow the plugin to set up
    # any required resources, ensuring that this can only happen once for each
    # plugin.
    def initialize(self, core):

        if self.initialized:
            return

        self.initialized = True

    def isInitialized(self):

        return self.initialized

    # This factory method creates new instances of our custom widget with the
    # appropriate parent.
    def createWidget(self, parent):
        return ValueLabel(parent)

    # This method returns the name of the custom widget class that is provided
    # by this plugin.
    def name(self):
        return "ValueLabel"

    # Returns the name of the group in Qt Designer's widget box that this
    # widget belongs to.
    def group(self):
        return "pyqtgraph"

    # Returns the icon used to represent the custom widget in Qt Designer's
    # widget box.
    def icon(self):
        return QtGui.QIcon(_logo_pixmap)

    # Returns a short description of the custom widget for use in a tool tip.
    def toolTip(self):
        return ""

    # Returns a short description of the custom widget for use in a "What's
    # This?" help message for the widget.
    def whatsThis(self):
        return ""

    # Returns True if the custom widget acts as a container for other widgets;
    # otherwise returns False. Note that plugins for custom containers also
    # need to provide an implementation of the QDesignerContainerExtension
    # interface if they need to add custom editing support to Qt Designer.
    def isContainer(self):
        return False

    # Returns an XML description of a custom widget instance that describes
    # default values for its properties. Each custom widget created by this
    # plugin will be configured using this description.
    def domXml(self):
        return '<widget class="ValueLabel" name="ValueLabel">\n' \
               ' <property name="toolTip">\n' \
               '  <string>pyqtgraph ValueLabel</string>\n' \
               ' </property>\n' \
               ' <property name="whatsThis">\n' \
               '  <string> QLabel specifically for displaying numerical values' \
               '</string>\n' \
               ' </property>\n' \
               '</widget>\n'

    # Returns the module containing the custom widget class. It may include
    # a module path.
    def includeFile(self):
        return "pyqtgraph"


# Define the image used for the icon.
_logo_32x32_xpm = [
"22 22 117 2 ",
"   c black",
".  c gray3",
"X  c #181818",
"o  c #252525",
"O  c gray20",
"+  c gray21",
"@  c gray22",
"#  c #3A3A3A",
"$  c gray24",
"%  c #3F3F3F",
"&  c #414141",
"*  c #434343",
"=  c #464646",
"-  c gray28",
";  c #484848",
":  c gray29",
">  c #4B4B4B",
",  c #4C4C4C",
"<  c gray30",
"1  c #4E4E4E",
"2  c gray31",
"3  c #515151",
"4  c #535353",
"5  c #565656",
"6  c gray34",
"7  c #585858",
"8  c gray35",
"9  c #5A5A5A",
"0  c #5D5D5D",
"q  c gray37",
"w  c #5F5F5F",
"e  c #606060",
"r  c gray38",
"t  c gray39",
"y  c #646464",
"u  c gray40",
"i  c #686868",
"p  c #6A6A6A",
"a  c #6D6D6D",
"s  c #6F6F6F",
"d  c #717171",
"f  c #727272",
"g  c gray45",
"h  c #767676",
"j  c gray47",
"k  c gray48",
"l  c #7C7C7C",
"z  c gray50",
"x  c #818181",
"c  c #838383",
"v  c #848484",
"b  c #868686",
"n  c gray55",
"m  c gray57",
"M  c gray60",
"N  c #B6B6B6",
"B  c #B7B7B7",
"V  c #B9B9B9",
"C  c gray73",
"Z  c #BBBBBB",
"A  c gray74",
"S  c gray",
"D  c gray75",
"F  c #C1C1C1",
"G  c gray76",
"H  c #C3C3C3",
"J  c gray77",
"K  c #C6C6C6",
"L  c gray78",
"P  c #C8C8C8",
"I  c gray79",
"U  c #CACACA",
"Y  c #CBCBCB",
"T  c #CDCDCD",
"R  c #CECECE",
"E  c gray81",
"W  c #D0D0D0",
"Q  c gray82",
"!  c #D2D2D2",
"~  c LightGray",
"^  c gray83",
"/  c #D5D5D5",
"(  c gray84",
")  c #D7D7D7",
"_  c #D8D8D8",
"`  c gray85",
"'  c #DADADA",
"]  c gray86",
"[  c #DDDDDD",
"{  c gray87",
"}  c #DFDFDF",
"|  c gray88",
" . c #E1E1E1",
".. c #E2E2E2",
"X. c #E4E4E4",
"o. c gray90",
"O. c #E6E6E6",
"+. c #E7E7E7",
"@. c gray91",
"#. c #E9E9E9",
"$. c #EAEAEA",
"%. c #ECECEC",
"&. c gray93",
"*. c #EEEEEE",
"=. c #EFEFEF",
"-. c #F1F1F1",
";. c gray95",
":. c #F3F3F3",
">. c #F4F4F4",
",. c gray96",
"<. c #F6F6F6",
"1. c gray97",
"2. c #F8F8F8",
"3. c gray98",
"4. c #FDFDFD",
"5. c gray100",
"6. c None",
"6.6.6.6.6.6.6.6.6.6.6.6.6.6.6.6.6.6.6.6.6.6.",
"6.6.b c c z z k k h d s s s i i y t t 0 6.6.",
"6.b T 1.1.1.2.2.1.1.1.1.1.1.1.1.1.1.1.A 9 6.",
"6.c 1.5.5.5.5.2.1.1.:.:.&.&.$.+.+...+.:.9 6.",
"6.c 1.5.5.2.2.2.1.:.:.&.&.$.+.( t ! [ &.5 6.",
"6.z 1.5.5.2.1.1.:.:.&.$.$.+...< X < ` $.4 6.",
"6.z 1.5.2.2.1.:.:.&.$.$.+.+.t . . . t +.4 6.",
"6.k 1.2.2.2.:.:.&.$.$.+.......[ ` ` ( ..< 6.",
"6.k 1.1.` b :.&.&.$.c s F [ [ [ ` ( ( [ < 6.",
"6.h 1.1.n > &.$.$.+.( ! < [ ` ` ( ! ! ` > 6.",
"6.d 1.:.:.5 $.$.+.+.....< ` ` ( ( ! ! ( - 6.",
"6.d 1.:.&.9 $.+.....[ M m ` ( ( ! T T ! - 6.",
"6.s 1.&.&.5 +.+...[ V d ` ( ! ! ! T U T * 6.",
"6.s 1.&.d o y ..  [ o 0 0 ( ! T T U U U * 6.",
"6.i 1.$.+.......[ [ ` ( ! ! T T U K K U $ 6.",
"6.y 1.+.+.....[ ` ` ( ( ! ! 9 . . . 5 F $ 6.",
"6.i 1.+.....[ ` ` ( ( ! T T K - X - A A # 6.",
"6.y 1...[ [ [ ` ( ! ! T T U U V 5 N F V # 6.",
"6.t :...[ [ ` ` ( ! ! T U U K K F F A V + 6.",
"6.t A :.&.+.+...[ ` ( ! T U K F A V N b O 6.",
"6.6.9 9 5 4 4 < < > - - * * $ $ # # + O 6.6.",
"6.6.6.6.6.6.6.6.6.6.6.6.6.6.6.6.6.6.6.6.6.6."
]

_logo_pixmap = QtGui.QPixmap(_logo_32x32_xpm)

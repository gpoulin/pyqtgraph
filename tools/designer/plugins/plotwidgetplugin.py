#!/usr/bin/env python

from pyqtgraph.Qt import QtGui
from pyqtgraph import PlotWidget
from pyqtgraph.Qt import USE_PYSIDE

if USE_PYSIDE:
    from PySide import QtDesigner
else:
    from PyQt4 import QtDesigner



class PyPlotWidgetPlugin(QtDesigner.QPyDesignerCustomWidgetPlugin):

    """PyPlotWidgetPlugin(QtDesigner.QPyDesignerCustomWidgetPlugin)

    Provides a Python custom plugin for Qt Designer by implementing the
    QDesignerCustomWidgetPlugin via a PyQt-specific custom plugin class.
    """

    # The __init__() method is only used to set up the plugin and define its
    # initialized variable.
    def __init__(self, parent=None):
        super(PyPlotWidgetPlugin, self).__init__(parent)
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
        return PlotWidget(parent)

    # This method returns the name of the custom widget class that is provided
    # by this plugin.
    def name(self):
        return "PlotWidget"

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
        return '<widget class="PlotWidget" name="PlotWidget">\n' \
               ' <property name="toolTip">\n' \
               '  <string>pyqtgraph PlotWidget</string>\n' \
               ' </property>\n' \
               ' <property name="whatsThis">\n' \
               '  <string> GraphicsView widget with a single PlotItem inside.' \
               '</string>\n' \
               ' </property>\n' \
               '</widget>\n'

    # Returns the module containing the custom widget class. It may include
    # a module path.
    def includeFile(self):
        return "pyqtgraph"


# Define the image used for the icon.
_logo_32x32_xpm = [
"22 22 111 2 ",
"   c #9C516E",
".  c #864E71",
"X  c #925474",
"o  c #985B7A",
"O  c #A75D78",
"+  c #AB5F79",
"@  c #AD627C",
"#  c #625E8B",
"$  c #7B5B81",
"%  c #536A9B",
"&  c #6F628C",
"*  c #6F6B95",
"=  c #466EA2",
"-  c #496FA3",
";  c #4D73A6",
":  c #567BAC",
">  c #5A7DAD",
",  c #647BA9",
"<  c #825E82",
"1  c #9D6280",
"2  c #9E6E8D",
"3  c #9C708E",
"4  c #857398",
"5  c #82789E",
"6  c #987291",
"7  c #A56783",
"8  c #AD6983",
"9  c #A66D89",
"0  c #AE6E88",
"q  c #B96B80",
"w  c #A5718E",
"e  c #A77996",
"r  c #6385B3",
"t  c #6689B6",
"y  c #698AB6",
"u  c #638BB9",
"i  c #6B8EBA",
"p  c #728FB8",
"a  c #6E91BD",
"s  c #7393BC",
"d  c #7996BE",
"f  c #6F94C0",
"g  c #7296C0",
"h  c #7699C3",
"j  c #7B9CC4",
"k  c #7BA0C9",
"l  c #8689AE",
"z  c #9982A2",
"x  c #9486A8",
"c  c #9A8CAB",
"v  c #8F8CB0",
"b  c #8C90B4",
"n  c #8797BA",
"m  c #A089A7",
"M  c #839DC4",
"N  c #85A1C5",
"B  c #8BA4C6",
"V  c #83A4CB",
"C  c #89A5C8",
"Z  c #85A8CF",
"A  c #8CABCF",
"S  c #9CADC2",
"D  c #94ACCB",
"F  c #99AFCD",
"G  c #96B0CF",
"H  c #9BB1CE",
"J  c #87A9D0",
"K  c #8BADD2",
"L  c #91AFD3",
"P  c #94B2D5",
"I  c #9BB4D2",
"U  c #98B6D8",
"Y  c #9CB9DA",
"T  c #A0B1C7",
"R  c #A0B4CF",
"E  c #AABACE",
"W  c #A2B6D1",
"Q  c #A4BAD5",
"!  c #ABBDD5",
"~  c #A0BEDD",
"^  c #BDC4CD",
"/  c #ADC1DA",
"(  c #B1C1D5",
")  c #B4C5DB",
"_  c #B8C7DA",
"`  c #B3C8DF",
"'  c #B9C9DE",
"]  c #B5C9E1",
"[  c #BCCDE1",
"{  c #BDD0E6",
"}  c #C5C9CF",
"|  c #C9CED5",
" . c #D7D9DA",
".. c #E9D5DC",
"X. c #C0CEE0",
"o. c #C2D1E3",
"O. c #CBD8E7",
"+. c #CFDAE9",
"@. c #D4DEEA",
"#. c #DBE1EC",
"$. c #DAE5F1",
"%. c #DFE8F3",
"&. c #E3E2EB",
"*. c #EBEBEB",
"=. c #E2EAF3",
"-. c #E8EEF4",
";. c #ECF1F6",
":. c #EFF3F8",
">. c #F4F4F4",
",. c #F3F6FA",
"<. c #FEFEFE",
"<.<.<.<.,.;.;.;.;.;.;.;.;.;.;.;.>.;.:.<.<.<.",
"<.<.:.[ ' [ ' [ [ [ X.' ' X.[ [ ' ' [ o.,.<.",
"<.<.] o.E H R R R R W W Q E W R W I ) X.o.<.",
"<.;.' W - d ; = r r > r ; ; ; r - = - ( ] ,.",
"<.=.' B p =.d > ) N D d : : : D s % # W [ ;.",
"<.=.' D E <.! C X.a W t B ! D d G & . E [ ;.",
"<.=.' F y @.p C F i E i D ' j p I < $ Q [ ;.",
"<.=.[ F r @.a W N i / j ) ] C M P X * ! [ ;.",
"<.=.[ H y @.F ' g a R D g g a Q n   , ! [ ;.",
"<.=.[ I i @.j h a f h V g g f k 5 o r / [ ;.",
"<.=.[ R a #.j f s 6 + 3 d h h f 1 4 u / { ;.",
"<.=.[ Q f #.j d 7 9 b w 8 M k l O p u ) X.;.",
"<.=.[ Q g #.V 2 w V Z Z e 8 x @ x f i ) [ ;.",
"<.=.X.Q j $.c @ M Z J K A m 0 z j h a ` [ ;.",
"<.=.[ ! M #.q v Z K L P P K J V k h s ` X.;.",
"<.=.{ Q M ..e A L U Y ~ ~ Y P U { I j ` X.;.",
"<.=.X.! h #.&.%.%.%.=.=.=.=.%.=.<.=.G ` X.;.",
"<.-.] ) a j Z A L P Y Y Y Y P P { P j { ' ;.",
"<.>.! +.) / ) ` [ { { { { { [ ] ` / ' O.E *.",
"<.>.| T ( ) ) ) _ _ _ _ ` ` _ _ _ _ ( S } *.",
"<.<.*. .} } ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ } }  .*.>.",
"<.<.<.,.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.<.<."
        ]

_logo_pixmap = QtGui.QPixmap(_logo_32x32_xpm)

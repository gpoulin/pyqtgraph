# -*- coding: utf-8 -*-
"""
PlotWidget.py -  Convenience class--GraphicsView widget displaying a single PlotItem
Copyright 2010  Luke Campagnola
Distributed under MIT/X11 license. See license.txt for more infomation.
"""

from pyqtgraph.Qt import QtCore, QtGui
from .GraphicsView import *
from pyqtgraph.graphicsItems.PlotItem import *
import pyqtgraph as pg

__all__ = ['PlotWidget']
class PlotWidget(GraphicsView):
    
    sigRangeChangedRectF = QtCore.Signal("QRectF")
    sigYRangeChangedFloat = QtCore.Signal(float, float)
    sigXRangeChangedFloat = QtCore.Signal(float, float)
    
    """
    :class:`GraphicsView <pyqtgraph.GraphicsView>` widget with a single 
    :class:`PlotItem <pyqtgraph.PlotItem>` inside.
    
    The following methods are wrapped directly from PlotItem: 
    :func:`addItem <pyqtgraph.PlotItem.addItem>`, 
    :func:`removeItem <pyqtgraph.PlotItem.removeItem>`, 
    :func:`clear <pyqtgraph.PlotItem.clear>`, 
    :func:`setXRange <pyqtgraph.ViewBox.setXRange>`,
    :func:`setYRange <pyqtgraph.ViewBox.setYRange>`,
    :func:`setRange <pyqtgraph.ViewBox.setRange>`,
    :func:`autoRange <pyqtgraph.ViewBox.autoRange>`,
    :func:`setXLink <pyqtgraph.ViewBox.setXLink>`,
    :func:`setYLink <pyqtgraph.ViewBox.setYLink>`,
    :func:`viewRect <pyqtgraph.ViewBox.viewRect>`,
    :func:`setMouseEnabled <pyqtgraph.ViewBox.setMouseEnabled>`,
    :func:`enableAutoRange <pyqtgraph.ViewBox.enableAutoRange>`,
    :func:`disableAutoRange <pyqtgraph.ViewBox.disableAutoRange>`,
    :func:`setAspectLocked <pyqtgraph.ViewBox.setAspectLocked>`,
    :func:`register <pyqtgraph.ViewBox.register>`,
    :func:`unregister <pyqtgraph.ViewBox.unregister>`
    :func:`setTitle <pyqtgraph.PlotItem.setTitle>`
    
    
    For all 
    other methods, use :func:`getPlotItem <pyqtgraph.PlotWidget.getPlotItem>`.
    """
    def __init__(self, parent=None, background='default', **kargs):
        """When initializing PlotWidget, *parent* and *background* are passed to 
        :func:`GraphicsWidget.__init__() <pyqtgraph.GraphicsWidget.__init__>`
        and all others are passed
        to :func:`PlotItem.__init__() <pyqtgraph.PlotItem.__init__>`."""
        GraphicsView.__init__(self, parent, background=background)
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.enableMouse(False)
        self.plotItem = PlotItem(**kargs)
        self.setCentralItem(self.plotItem)
        self._title = None
        ## Explicitly wrap methods from plotItem
        ## NOTE: If you change this list, update the documentation above as well.
        for m in ['addItem', 'removeItem', 'setAspectLocked', 'setXLink', 'setYLink', 'disableAutoRange', 'register', 'unregister', 'viewRect']:
            setattr(self, m, getattr(self.plotItem, m))
        #QtCore.QObject.connect(self.plotItem, QtCore.SIGNAL('viewChanged'), self.viewChanged)
        self.plotItem.sigRangeChanged.connect(self.viewRangeChanged)
        self.plotItem.sigXRangeChanged.connect(self.viewXRangeChanged)
        self.plotItem.sigYRangeChanged.connect(self.viewYRangeChanged)
    
    def close(self):
        self.plotItem.close()
        self.plotItem = None
        #self.scene().clear()
        #self.mPlotItem.close()
        self.setParent(None)
        GraphicsView.close(self)

    def __getattr__(self, attr):  ## implicitly wrap methods from plotItem
        if hasattr(self.plotItem, attr):
            m = getattr(self.plotItem, attr)
            if hasattr(m, '__call__'):
                return m
        raise NameError(attr)
    
    def viewRangeChanged(self, view, range):
        self.sigRangeChangedRectF.emit(self.viewRange)

    def viewXRangeChanged(self, view, range):
        self.sigXRangeChangedFloat.emit(range[0],range[1])

    def viewYRangeChanged(self, view, range):
        self.sigYRangeChangedFloat.emit(range[0],range[1])

    def widgetGroupInterface(self):
        return (None, PlotWidget.saveState, PlotWidget.restoreState)

    def saveState(self):
        return self.plotItem.saveState()
        
    def restoreState(self, state):
        return self.plotItem.restoreState(state)
        
    def getPlotItem(self):
        """Return the PlotItem contained within."""
        return self.plotItem

    @QtCore.Property("QRectF")
    def viewRange(self):
        return self.viewRect()

    @viewRange.setter
    def viewRange(self, value):
        self.setRange(value, padding = 0)

    @QtCore.Property(str)
    def title(self):
        return self.plotItem.titleLabel.text

    @title.setter
    def title(self, value):
        if value == '' :
            self.plotItem.titleLabel.text = ''
            value = None
        self.setTitle(value)

    @QtCore.Property("QColor")
    def titleColor(self):
        color = self.plotItem.titleLabel.opts['color']
        if color == None:
            return pg.mkColor(pg.getConfigOption('foreground'))
        return color

    @titleColor.setter
    def titleColor(self, value):
        self.setTitle(self.title, color=pg.mkColor(value))

    @QtCore.Property(bool)
    def autoRangeX(self):
        return bool(self.getViewBox().autoRangeEnabled()[0])

    @autoRangeX.setter
    def autoRangeX(self,value):
        self.enableAutoRange('x', value)

    @QtCore.Property(bool)
    def autoRangeY(self):
        return bool(self.getViewBox().autoRangeEnabled()[1])

    @autoRangeY.setter
    def autoRangeY(self,value):
        self.enableAutoRange('y', value)
                
    @QtCore.Property(bool)
    def mouseXEnabled(self):
        x, y = self.getViewBox().mouseEnabled()
        return x

    @QtCore.Property(bool)
    def mouseYEnabled(self):
        x, y = self.getViewBox().mouseEnabled()
        return y

    @mouseXEnabled.setter
    def mouseXEnabled(self, value):
        self.plotItem.setMouseEnabled(x=value)

    @mouseYEnabled.setter
    def mouseYEnabled(self, value):
        self.plotItem.setMouseEnabled(y=value)

    @QtCore.Slot(bool,bool)
    @QtCore.Slot(bool)
    def setMouseEnabled(self, x=True, y=None):
        if y == None:
            y = x
        self.plotItem.setMouseEnabled(x, y)

    @QtCore.Slot(bool)
    @QtCore.Slot(str, bool)
    @QtCore.Slot(int, bool)
    @QtCore.Slot(str, float)
    @QtCore.Slot(int, float)
    def enableAutoRange(self, ax=None, enable=True):
        if isinstance(ax, bool):
            enable = ax
            ax = None
        self.plotItem.enableAutoRange(ax, enable)

    @QtCore.Slot("QRectF")
    @QtCore.Slot("QRect")
    def setRange(self, *args, **kargs):
        self.plotItem.setRange(*args, **kargs)
    
    @QtCore.Slot(float,float)
    @QtCore.Slot(float, float, float)
    @QtCore.Slot(float, float, float, bool)
    def setXRange(self, *args, **kargs):
        self.plotItem.setXRange(*args, **kargs)

    @QtCore.Slot(float,float)
    @QtCore.Slot(float, float, float)
    @QtCore.Slot(float, float, float, bool)
    def setYRange(self, *args, **kargs):
        self.plotItem.setYRange(*args, **kargs)

    @QtCore.Slot()
    def clear(self):
        self.plotItem.clear()

    @QtCore.Slot()
    @QtCore.Slot(float)
    def autoRange(self, *args, **kargs):
        self.plotItem.autoRange(*args, **kargs)

    @QtCore.Slot(str)
    def setTitle(self, text, **kargs):
        self._title = text
        self.plotItem.setTitle(text, **kargs)

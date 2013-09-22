from collections import deque

import numpy as np

from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph.functions as fn
from .GraphicsObject import GraphicsObject
import pyqtgraph.debug as debug
from pyqtgraph.graphicsItems.ScatterPlotItem import renderSymbol

__all__ = ['FastScatterPlotItem']

class Symbol(object):

    def __init__(self, pen='l', brush='s', symbol='o', size=7):
        self.size = size
        self.symbol = symbol
        
        if isinstance(pen,QtGui.QPen):
            self.pen = pen
        else:
            self.pen = fn.mkPen(pen)

        if isinstance(brush,QtGui.QBrush):
            self.brush = brush
        else:
            self.brush = fn.mkBrush(brush)
        
        self.width = size + self.pen.widthF()
        self.img = None

    def render(self):
        if self.img == None
            self.img = fn.imageToArray(renderSymbol(self.symbol, self.size, 
                self.pen, self.brush), copy=False, transpose=False)
        return self.img

    def __eq__(self, other):
        attribute = ['pen', 'brush', 'symbol', 'size']
        for att in attribute:
            if self.__getattr__(att) != other.__getattr__(att):
                return False
        return True


class FastScatterPlotItem(GraphicsObject):
    def __init__(self, *args, **kargs):
        GraphicsObject.__init__(self)
        self.data = np.empty(0, dtype=[('x', float), ('y', float), ('symbol', np.int16)]) 
        self._QPoints = []
        self._symbolList = []
        self._unusedSymbol = [] ## index of unused Symbol
        self._sprite = None ## Cache the symbol Pixmap
        self._spriteValid = False
        self._symbolRectF = []
        self.pointMode = False ## Draw only point instead of symbol
        self._maxWidth = 0
        self.fragments = None
        self.bounds = [None, None]  ## caches data bounds
        self.setData(*args, **kargs)
        
    def setData(self, x, y, pen='l', brush='s', symbol='o', size=7):
        self.clear()
        self.bounds = [None, None]
        self.addPoints(*args, **kargs)
        self.cleanSymbol()

    def addPoints(self, x, y, pen='l', brush='s', symbol='o', size=7):
        symbol = Symbol(pen, brush, symbol, size)
        i = self._addSymbol(symbol)

        numPts = len(x)
        oldData = self.data
        self.data = np.empty(len(oldData)+numPts, dtype=self.data.dtype)
        self.data[:len(oldData)] = oldData
        newData = self.data[len(oldData):]
        newData['x'] = x
        newData['y'] = y
        newData['symbol'] = i
        for j in len(x):
            self._QPoints.append(QtCore.QPointF(x[i], y[j]))
        self.bounds = [None, None]
        self.prepareGeometryChange()
        self.update()

    def _addSymbol(self, symbol):
        """
        Add a symbol to the list of symbol and return the index of the symbol
        """
        try: ## check if the symbol is already there
            i = self.symbolList.index(symbol)
            self._unusedSymbol[i] = False
            return i
        except ValueError:
            self.valideSprite=False
            self._maxWidth = max(self._maxWidth, symbol.width)
            for i in xrange(len(self._unusedSymbol)):
                if self._unusedSymbol[i]:
                    self._unusedSymbol[i] = False
                    self._symbolList[i] = symbol
                    return i
        self._symbolList.append(symbol)
        i=len(self.symbolList) - 1
        self._symbolList[i] = symbol
        return i


    def implements(self, interface=None):
        ints = ['plotData']
        if interface is None:
            return ints
        return interface in ints
    
    def clear(self):
        """Remove all spots from the scatter plot"""
        self.data = np.empty(0, dtype=self.data.dtype)
        self._QPoints = []
        self.bounds = [None, None]

    def cleanSymbol(self):
        """Remove unused symbol from the cache"""
        self._unusedSymbol = deque()
        symbol = []
        data = []
        self._maxWidth = 0
        used = np.unique(self.data['symbol']).sort() ## to make sure to keep good symbol
        i = 0
        for x in used:
            symbol.append(self._symbolList[x])
            self.data['symbol'][self.data['symbol'] == x] = i
            i += 1
        self._symbolList = symbol
        self._spriteValid = False

    def dataBounds(self, ax, frac=1.0, orthoRange=None):
        if frac >= 1.0 and orthoRange is None and self.bounds[ax] is not None:
            return self.bounds[ax]
        
        #self.prepareGeometryChange()
        if self.data is None or len(self.data) == 0:
            return (None, None)
        
        if ax == 0:
            d = self.data['x']
            d2 = self.data['y']
        elif ax == 1:
            d = self.data['y']
            d2 = self.data['x']
        
        if orthoRange is not None:
            mask = (d2 >= orthoRange[0]) * (d2 <= orthoRange[1])
            d = d[mask]
            d2 = d2[mask]
            
        if frac >= 1.0:
            self.bounds[ax] = (np.nanmin(d), np.nanmax(d))
            return self.bounds[ax]
        elif frac <= 0.0:
            raise Exception("Value for parameter 'frac' must be > 0. (got %s)" % str(frac))
        else:
            mask = np.isfinite(d)
            d = d[mask]
            return (np.percentile(d, 50 - (frac * 50)), np.percentile(d, 50 + (frac * 50)))
            
    def pixelPadding(self):
        return self.maxWidth*0.7072

    def boundingRect(self):
        (xmn, xmx) = self.dataBounds(ax=0)
        (ymn, ymx) = self.dataBounds(ax=1)
        if xmn is None or xmx is None:
            xmn = 0
            xmx = 0
        if ymn is None or ymx is None:
            ymn = 0
            ymx = 0
        
        px = py = 0.0
        pxPad = self.pixelPadding()
        if pxPad > 0:
            # determine length of pixel in local x, y directions    
            px, py = self.pixelVectors()
            px = 0 if px is None else px.length() 
            py = 0 if py is None else py.length()
            
            # return bounds expanded by pixel size
            px *= pxPad
            py *= pxPad
        return QtCore.QRectF(xmn-px, ymn-py, (2*px)+xmx-xmn, (2*py)+ymx-ymn)

    def viewTransformChanged(self):
        self.prepareGeometryChange()
        GraphicsObject.viewTransformChanged(self)
        self.bounds = [None, None]
        self.fragments = None


    def _generateSprite(self):
        # get rendered array for all symbols, keep track of avg/max width
        rendered = {}
        avgWidth = 0.0
        maxWidth = 0
        images = []
        for key, coords in self.symbolMap.items():
            if len(coords) == 0:
                pen = self.symbolPen[key]
                brush = self.symbolBrush[key]
                img = renderSymbol(key[0], key[1], pen, brush)
                images.append(img)  ## we only need this to prevent the images being garbage collected immediately
                arr = fn.imageToArray(img, copy=False, transpose=False)
            else:
                (x,y,w,h) = self.symbolMap[key]
                arr = self.atlasData[x:x+w, y:y+w]
            rendered[key] = arr
            w = arr.shape[0]
            avgWidth += w
            maxWidth = max(maxWidth, w)
            
        nSymbols = len(rendered)
        if nSymbols > 0:
            avgWidth /= nSymbols
            width = max(maxWidth, avgWidth * (nSymbols**0.5))
        else:
            avgWidth = 0
            width = 0
        
        # sort symbols by height
        symbols = sorted(rendered.keys(), key=lambda x: rendered[x].shape[1], reverse=True)
        
        self.atlasRows = []

        x = width
        y = 0
        rowheight = 0
        for key in symbols:
            arr = rendered[key]
            w,h = arr.shape[:2]
            if x+w > width:
                y += rowheight
                x = 0
                rowheight = h
                self.atlasRows.append([y, rowheight, 0])
            self.symbolMap[key][:] = x, y, w, h
            x += w
            self.atlasRows[-1][2] = x
        height = y + rowheight

        self.atlasData = np.zeros((width, height, 4), dtype=np.ubyte)
        for key in symbols:
            x, y, w, h = self.symbolMap[key]
            self.atlasData[x:x+w, y:y+h] = rendered[key]
        self.atlas = None
        self.atlasValid = True
        self.max_width=maxWidth


    def _generateFragments(self):
        tr = self.deviceTransform()
        if tr is None:
            return
        self.fragments = []
        for i in xrange(len(self.data)):
            pos = tr.map(self._QPoints[i])
            rect = self._symbolRectF[self.data['symbol'][i]
            self.fragments.append(QtGui.QPainter.PixmapFragment.create(pos, rect))
            
    def setExportMode(self, *args, **kwds):
        GraphicsObject.setExportMode(self, *args, **kwds)
        self.invalidate()
        
    @debug.warnOnException  ## raising an exception here causes crash
    def paint(self, p, *args):
        
        if self._exportOpts is not False:
            aa = self._exportOpts.get('antialias', True)
            scale = self._exportOpts.get('resolutionScale', 1.0)  ## exporting to image; pixel resolution may have changed
        else:
            aa = True #self.opts['antialias']
            scale = 1.0
        
        p.setRenderHint(p.Antialiasing, aa)            
        p.resetTransform()

        if not self._spriteValid:
            self._generateSprite()
        
        if self._fragments == None:
            self._generateFragments()
        
        p.drawPixmapFragments(self._fragments, self._sprite)

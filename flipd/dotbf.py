import math
import numpy as np

try:
    from fnt import XU
except:
    from flipd.fnt import XU

class Dotbf:

    def __init__(self, wdth=28, hght=7, txt=None, txtmx=0, fnt=XU):

        if txt is not None:
            a = self._txtarray(txt, fnt)

            if txtmx > 0:
                self.wdth = min(txtmx, len(a))
            else:
                self.wdth = len(a)

            self.hght = 7
            self._b = np.zeros((self.hght, self.wdth), dtype=np.bool)
            for x in range(self.wdth):
                for y in range(self.hght):
                    self._b[y, x] = a[x] & (0x1 << y)

        else:
            self.wdth = wdth
            self.hght = hght
            self._b = np.zeros((self.hght, self.wdth), dtype=np.bool)

    def __str__(self):
        s = ""
        for x in range(self.wdth):
            c = ""
            for y in range(self.hght):
                if self._b[y, x]:
                    c = "o" + c
                else:
                    c = "." + c
            s += c + "\n"
        return s

    def __setitem__(self, dex, on):
        x, y = dex
        x %= self.wdth
        y %= self.hght
        self._b[y, x] = on

    def __getitem__(self, dex):
        x, y = dex
        x %= self.wdth
        y %= self.hght
        return self._b[y, x]

    def writebf(self, obf, ox=0, oy=0, x=0, y=0, wdth=-1, hght=-1):
        if wdth < 0:
            wdth = self.wdth
        if hght < 0:
            hght = self.hght
        obf._b[oy:oy+hght, ox:ox+wdth] = self._b[y:y+hght, x:x+wdth]

    def writefrm(self, frm, x, y):
        for i, nx in enumerate(range(x, x + frm.WDTH)):
            clmn = 0
            for j, ny in enumerate(range(y, y + frm.HGHT)):
                if self[nx, ny]:
                    clmn |= 0x1 << j
            frm[i] = clmn

    def flipmask(self, obf, ox, oy, x=0, y=0, wdth=-1, hght=-1):
        if wdth < 0:
            wdth = self.wdth
        if hght < 0:
            hght = self.hght
        for u in range(x, x+wdth):
            for v in range(y, y+hght):
                if self[u, v]:
                    obf[ox+u, oy+v] = ~obf[ox+u, oy+v]

    def wipe(self):    
        self._b = np.zeros((self.hght, self.wdth), dtype=np.bool)

    def _txtarray(self, txt, fnt):
        
        a = bytearray([0])
        for c in txt.upper():
            if c in fnt:
                a.extend(fnt[c])
                a.append(0)
            else:
                print("dotbf ignoring:", c)
        return a

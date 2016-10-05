# library for flipdot display buffer
import math

try:
    from frm import Frm
except:
    from flipd.frm import Frm

class Dsply:

    @staticmethod
    def WIPE(srl, white):
        """wipe all displays"""
        f = Frm(white=white)
        if srl is not None:
            srl.write(f.b)
        else:
            print(f)

    def __init__(self, adrss):
        self.adrss = [int(a) for a in adrss]
        self.wdth = Frm.WDTH * len(self.adrss)
        self.hght = Frm.HGHT # panel height
    
    def render(self, srl, bf, x=0, y=0): # render from given buffer at given origin

        for i, adrs in enumerate(self.adrss):
            f = Frm(adrs)
            bf.writefrm(f, x + (i * Frm.WDTH), y)
            if srl is not None:
                srl.write(f.b)
            else:
                print(f)





from __future__ import division

from flipd.dsply import Dsply
from flipd.dotbf import Dotbf

class Qst: # question state
    qscroll = 1
    postqpause = 2
    vscroll = 3
    vpause = 4
    nvscroll = 5
    preqpause = 6
    noq = 7

class Qdsply:

    def __init__(self):

        # left & right displays
        self.lftd = Dsply([1, 2, 3, 4])
        self.rtd = Dsply([5, 6, 7, 8])

        # buffers
        self.qbf = None # question buffer
        self.lftbf = Dotbf(self.lftd.wdth, self.lftd.hght)
        self.rtbf = Dotbf(self.rtd.wdth, self.rtd.hght)
        self.abf = None
        self.bbf = None
        self.lftbgbf = Dotbf(self.lftd.wdth, self.lftd.hght * 2)
        self.rtbgbf = Dotbf(self.rtd.wdth, self.rtd.hght * 2)
        self.lftrtiobf = Dotbf(self.lftd.wdth, self.lftd.hght)
        self.rtrtiobf = Dotbf(self.rtd.wdth, self.rtd.hght)

        ### states
        self.qst = Qst.noq # question state
        self.vst = False # vote buzzer state

        self.adpth = 0 # depth of a vote buzzer
        self.bdpth = 0 # depth of b vote buzzer
        self.rtio = 0.5

        self.qscroll = 0
        self.mxqscroll = 0
        self.vscroll = 0
        self.mxvscroll = 7

    def step(self, srl):
        """step animation forwards"""

        if self.qst == Qst.noq:
            print("noq")
            self.wipe(srl, False)
            return

        if self.vst:
            print("vst",)
            if self.adpth > 0 or self.bdpth > 0:
                self._render_ratio()
            else:
                self.vst = False
                return
            
            if self.adpth > 0:
                self.adpth -= 1
                if self.adpth % 2:
                    self._buzza()

            if self.bdpth > 0:
                self.bdpth -= 1
                if self.bdpth % 2:
                    self._buzzb()

            self.lftd.render(srl, self.lftrtiobf)
            self.rtd.render(srl, self.rtrtiobf)
            return

        if self.qst == Qst.qscroll:
            print("qscroll", self.qscroll, )
            if self.qscroll == 0:
                self.qst = Qst.vscroll
            else:
                self.qscroll -= 1
                self.qbf.writebf(self.lftbgbf, self.qscroll, 0)
                self.qbf.writebf(self.rtbgbf, self.qscroll, 0)

            self.lftd.render(srl, self.lftbgbf, 0, 0)
            self.rtd.render(srl, self.rtbgbf, 0, 0)
            return

        if self.qst == Qst.vscroll:
            print("vscroll", self.vscroll,)
            if self.vscroll == self.mxvscroll:
                self.qscroll = self.mxqscroll
                self.qst = Qst.nvscroll
                return

            self.vscroll += 1
            self.lftd.render(srl, self.lftbgbf, 0, self.vscroll)
            self.rtd.render(srl, self.rtbgbf, 0, self.vscroll)
            return
        
        if self.qst == Qst.nvscroll:
            print("nvscroll", self.vscroll,)
            if self.vscroll == 0:
                self.qst = Qst.qscroll
                return

            self.vscroll -= 1
            self.lftd.render(srl, self.lftbgbf, 0, self.vscroll)
            self.rtd.render(srl, self.rtbgbf, 0, self.vscroll)
            return                      


    def _buzza(self):
        aw = self.abf.wdth
        hlw = self.lftd.wdth // 2
        lap = (hlw - aw) // 2
        self.abf.flipmask(self.lftrtiobf, lap, 0)

        hrw = self.rtd.wdth // 2
        rap = hrw + ((hrw - aw) // 2)
        self.abf.flipmask(self.rtrtiobf, rap, 0)
        #print("lap:", lap, "rap:", rap)

    def _buzzb(self):
        bw = self.bbf.wdth
        hlw = self.lftd.wdth // 2
        lbp = hlw + ((hlw - bw) // 2)
        self.bbf.flipmask(self.lftrtiobf, lbp, 0)

        hrw = self.rtd.wdth // 2
        rbp = (hrw - bw) // 2
        self.bbf.flipmask(self.rtrtiobf, rbp, 0)


    def _render_ratio(self):
        llst = int(self.lftd.wdth * self.rtio)
        print("render ratio:", llst, ":", self.lftd.wdth)
        for x in range(self.lftd.wdth):
            on = (x < llst)
            for y in range(self.lftd.hght):
                self.lftrtiobf[x, y] = on

        rlst = int(self.rtd.wdth * self.rtio)
        for x in range(self.rtd.wdth):
            on = (x >= rlst)
            for y in range(self.rtd.hght):
                self.rtrtiobf[x, y] = on


    def ask(self, q, a, b):
        """ask new question"""
        qbf = Dotbf(txt=q)
        if qbf.wdth < self.lftd.wdth:
            self.qbf = Dotbf(self.lftd.wdth)
            dlta = (self.qbf.wdth - qbf.wdth) // 2
            qbf.writebf(self.qbf, dlta, 0)
            self.mxqscroll = 0
        else:
            self.qbf = qbf
            self.mxqscroll = self.qbf.wdth - self.lftd.wdth

        self.qscroll = self.mxqscroll
        self.qbf.writebf(self.lftbgbf, self.qscroll, 0)
        self.qbf.writebf(self.rtbgbf, self.qscroll, 0)

        self.abf = Dotbf(txt=a)
        self.bbf = Dotbf(txt=b)

        hld = self.lftd.wdth // 2
        lap = (hld - self.abf.wdth) // 2
        self.abf.writebf(self.lftbgbf, lap, self.lftd.hght)
        lbp = hld + ((hld - self.bbf.wdth) // 2)
        self.bbf.writebf(self.lftbgbf, lbp, self.lftd.hght)

        hrd = self.rtd.wdth // 2
        rap = hrd + ((hrd - self.abf.wdth) // 2)
        self.abf.writebf(self.rtbgbf, rap, self.rtd.hght)
        rbp = (hrd - self.bbf.wdth) // 2
        self.bbf.writebf(self.rtbgbf, rbp, self.rtd.hght)
        
        self.qst = Qst.qscroll # start scrolling!

    def vote(self, a, ratio, dpth=10): # a -> bool, true if vote is for a
        """add depth to a or b vote buzzer"""
        self.rtio = ratio
        self.vst = True
        if a:
            self.adpth += dpth
        else:
            self.bdpth += dpth

    def wipe(self, srl, white=True):
        Dsply.WIPE(srl, white)

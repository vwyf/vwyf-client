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
        self.pause = 8
        self.mxpause = 8

    def step(self, srl):
        """step animation forwards"""

        if self.qst == Qst.noq:
            self.wipe(srl, False)
            return

        if self.vst:
            if self.adpth > 0 or self.bdpth > 0:
                self._render_ratio()
            else:
                self.vst = False
                self.qst = Qst.nvscroll
                self.qscroll = 0
                self.vscroll = self.mxvscroll
                return
            
            if self.adpth > 0:
                self.adpth -= 1
                self._buzza()

            if self.bdpth > 0:
                self.bdpth -= 1
                self._buzzb()

            self.lftd.render(srl, self.lftrtiobf)
            self.rtd.render(srl, self.rtrtiobf)
            return

        if self.qst == Qst.preqpause:
            if self.pause > 0:
                self.pause -= 1
            else:
                self.qst = Qst.qscroll
                self.pause = self.mxpause

        if self.qst == Qst.qscroll:
            if self.qscroll >= self.mxqscroll:
                self.qst = Qst.postqpause
            else:
                self.qscroll += 1
                self.qbf.writebf(
                    self.lftbgbf, 0, 0, 
                    self.qscroll, 0, self.lftbgbf.wdth, self.qbf.hght)
                self.qbf.writebf(
                    self.rtbgbf, 0, 0, 
                    self.qscroll, 0, self.rtbgbf.wdth, self.qbf.hght)
            self.lftd.render(srl, self.lftbgbf, 0, 0)
            self.rtd.render(srl, self.rtbgbf, 0, 0)
            return

        if self.qst == Qst.postqpause:
            if self.pause > 0:
                self.pause -= 1
            else:
                self.qst = Qst.vscroll
                self.pause = self.mxpause

        if self.qst == Qst.vscroll:
            if self.vscroll == self.mxvscroll:
                self.qscroll = 0
                self.qst = Qst.vpause
                return

            self.vscroll += 1
            self.lftd.render(srl, self.lftbgbf, 0, self.vscroll)
            self.rtd.render(srl, self.rtbgbf, 0, self.vscroll)
            return

        if self.qst == Qst.vpause:
            if self.pause > 0:
                self.pause -= 1
            else:
                self.qst = Qst.nvscroll
                self.pause = self.mxpause
        
        if self.qst == Qst.nvscroll:
            if self.vscroll == 0:
                self.qst = Qst.preqpause
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
        for x in range(self.lftd.wdth):
            on = x < llst
            for y in range(self.lftd.hght):
                self.lftrtiobf[x, y] = on

        rlst = self.rtd.wdth - int(self.rtd.wdth * self.rtio)
        for x in range(self.rtd.wdth):
            on = x >= rlst
            for y in range(self.rtd.hght):
                self.rtrtiobf[x, y] = on


    def ask(self, q, a, b):
        """ask new question"""

        # wipe old question
        self.lftbgbf.wipe()
        self.rtbgbf.wipe()

        qbf = Dotbf(txt=q)
        if qbf.wdth < self.lftd.wdth:
            self.qbf = Dotbf(self.lftd.wdth)
            dlta = (self.qbf.wdth - qbf.wdth) // 2
            qbf.writebf(self.qbf, dlta, 0)
            self.mxqscroll = 0
        else:
            self.qbf = qbf
            self.mxqscroll = self.qbf.wdth - self.lftd.wdth
            print("mxqscroll:", self.mxqscroll)

        self.qscroll = 0
        self.qbf.writebf(
            self.lftbgbf, 0, 0, 
            self.qscroll, 0, self.lftbgbf.wdth, self.qbf.hght)
        self.qbf.writebf(
            self.rtbgbf, 0, 0, 
            self.qscroll, 0, self.rtbgbf.wdth, self.qbf.hght)

        hld = self.lftd.wdth // 2
        self.abf = Dotbf(txt=a, txtmx=hld)
        self.bbf = Dotbf(txt=b, txtmx=hld)

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

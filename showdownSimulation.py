import random 
import sys

""" Run in terminal command:
python -c 'import showdownSimulation; hitter = showdownSimulation.showdownHitter(); pitcher = showdownSimulation.showdownPitcher(); numTrials = 10000000; showdownSimulation.showdownSimulation(numTrials, hitter, pitcher)'
"""

class showdownPlayer(object):
    def __init__(self, points):
        self.points = points
    def getPoints(self):
        return self.points
    #def __str__(self):
        # need this at all? not attaching names or anything 

class showdownHitter(showdownPlayer):
    def __init__(self, ob = 11, out=6, bb=2, single=7, singleplus=2, double=3, triple=0, hr=0):
        self.ob = ob
        self.out = out
        self.bb = bb
        self.single = single
        self.singleplus = singleplus
        self.double = double
        self.triple = triple
        self.hr = hr
        self.chart = {}
    # one get method for whole chart or get methods for each piece?
    def buildChart(self):
        # use loops to add entries to dict(chart) for num of results
        # ie for i in range(single): chart[i] = single
        lB = 1
        uB = self.out + 1
        for i in range(lB,uB):
            self.chart[i] = 'out'
        lB+=self.out
        uB+=self.bb
        for i in range(lB, uB):
            self.chart[i] = 'bb'
        lB+=self.bb
        uB+=self.single
        for i in range(lB, uB):
            self.chart[i] = 'single'  
        lB+=self.single
        uB+=self.singleplus
        for i in range(lB, uB):
            self.chart[i] = 'singleplus' 
        lB+=self.singleplus
        uB+=self.double
        for i in range(lB, uB):
            self.chart[i] = 'double'
        lB+=self.double
        uB+=self.triple
        for i in range(lB,uB):
            self.chart[i] = 'triple' 
        lB+=self.triple
        uB+=self.hr
        for i in range(lB,uB):
            self.chart[i] = 'hr'
    def getChart(self):
        return self.chart
    def getOB(self):
        return self.ob
    #def __str__(self):
        # want to print it out so there is number of results 
        # (or chart values) for each on their own line
        
class showdownPitcher(showdownPlayer):
    def __init__(self, control=5, out=16, bb=1, single=2, double=4, hr=3):
        ### TO DO
        self.control = control
        self.out = out
        self.bb = bb
        self.single = single
        self.double = double
        self.hr = hr
        self.chart = {}
   
    def buildChart(self):
        # possible to buildChart while initializing? 
        lB = 1
        uB = self.out + 1
        for i in range(lB,uB):
            self.chart[i] = 'out'
        lB+=self.out
        uB+=self.bb
        for i in range(lB, uB):
            self.chart[i] = 'bb'
        lB+=self.bb
        uB+=self.single
        for i in range(lB, uB):
            self.chart[i] = 'single'  
        lB+=self.single
        uB+=self.double
        for i in range(lB, uB):
            self.chart[i] = 'double' 
        lB+=self.double
        uB+=self.hr
        for i in range(lB, uB):
            self.chart[i] = 'hr'
    
    def getChart(self):
        return self.chart   
    def getControl(self):
        return self.control 

def showdownSimulation(numTrials, hitter, pitcher):
    #numTrials = sys.argv[1]
    hitter.buildChart()
    pitcher.buildChart()
    bbs, hits, singles = 0, 0, 0
    # singlepluses = 0 
    doubles, triples, hr = 0, 0, 0
    for i in xrange(numTrials):
        # roll for advantage
        pitcherRoll = random.randint(1,20)
        hitterRoll = random.randint(1,20)
        #print str(pitcherRoll) + ', ' + str(hitterRoll)
        if ((pitcherRoll + pitcher.getControl()) > hitter.getOB()):
            # use pitcher's chart
            res = pitcher.chart[hitterRoll]
            # use if statement for each res? or better way to do it?
            if res == 'single':
                hits += 1
                singles += 1
            elif res == 'double':
                hits += 1
                doubles += 1
            elif res == 'hr':
                hits += 1
                hr += 1
            elif res == 'bb':
                bbs += 1
        else:
            # use hitter's chart
            res = hitter.chart[hitterRoll]
            if res == 'single':
                hits += 1
                singles += 1
            elif res == 'singleplus':
                hits += 1
                if random.random() < .4:
                    doubles += 1
                else: 
                    singles += 1
                #singlepluses += 1
            elif res == 'double':
                hits += 1
                doubles += 1
            elif res == 'triple':
                hits += 1
                triples += 1
            elif res == 'hr':
                hits += 1
                hr += 1
            elif res == 'bb':
                bbs += 1
    # compute BA, SLG, OBP outside the for loop
    print hits, bbs, doubles, triples, hr
    battingAvg = round(hits/float(numTrials - bbs), 4)
    totalBases = singles + 2*doubles + 3*triples + 4*hr 
    SLG = round(totalBases/float(numTrials - bbs), 4)
    OBP = round((hits+bbs)/float(numTrials), 4)
    wOBA = round((.69*bbs + .89*singles + 1.27*doubles + 1.62*triples + 2.1*hr)/float(numTrials), 4)
    print battingAvg, OBP, SLG, wOBA
    
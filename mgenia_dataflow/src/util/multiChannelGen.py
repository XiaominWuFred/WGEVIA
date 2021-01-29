import os
import sys
from g2vpre import findRange


class multiChannelGen():
    def __init__(self,threshold,posT):
        #inputs
        self.reader = None
        self.posT = posT
        self.Threshold = threshold
        #variables
        self.top = None
        self.bot = None
        #output
        self.step = None
        self.Ts = []

    def load(self,reader):
        self.reader = reader


    def run(self):
        self.top, self.bot = findRange(self.reader.X)
        print("got top " + str(self.top))
        print("got bot " + str(self.bot))

        if self.posT == 'posT':
            print("posT")
            posT = True
        else:
            print("negT")
            posT = False

        if posT != True:
            self.step = (float(self.top) - float(self.bot)) / (int(self.Threshold))  # negT
        else:
            self.step = float(self.top) / (int(self.Threshold))  # posT

        for i in range(int(self.Threshold)):
            if posT != True:
                self.Ts.append(float(self.bot) + i * self.step)  # negT
            else:
                self.Ts.append(i * self.step)  # posT

        # clean previous g2vi.csv files and json folder of previous run
        os.system("cd ../../channels\nrm -rf [a-zA-Z]*[0-9]")
        os.system("cd ../../channels/g2vFeatures\nrm g* c*")









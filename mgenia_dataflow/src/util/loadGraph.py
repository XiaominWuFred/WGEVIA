import os
import sys
from readData import ReadMCData


class loadGraph():
    def __init__(self, isTrain = True):
        self.isTrain = isTrain
        self.reader = None
        self.path = None
        #self.load()

    def load(self,path):
        self.path = path

    def run(self):
        #count number of files, should be equal or larger than files existed
        filenum = len(os.listdir(self.path))#'../../weightedGraphs/'
        print("num of files: "+str(int(filenum)))
        if filenum <= 2:
            print("ERROR: not enough input files")
        else:
            if self.isTrain:
                #remove previous saved model from train mode
                os.system("cd ../../trainedModel\nrm d2v*")

            self.reader = ReadMCData('04', int(filenum), '../../weightedGraphs/')
            self.reader.readX()
            print("done read X")
            #not necessary if user provided labelAll.csv
            #reader.readY()
            #print("done read Y")
            #not necessary if user provided labelAll.csv
            #reader.writeY()

            numOfGraph = len(self.reader.X)
            print("amount of input graphs: "+str(numOfGraph))

if __name__ == "__main__":
    loader = loadGraph()

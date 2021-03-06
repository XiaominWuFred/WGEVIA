import numpy as np
import numpy as np
import matplotlib.pyplot as plt

class ConvertBinaryGraph:
    """
    convert weighted graph to binary graph
    @author Xiaomin Wu
    @date 09162019
    """

    def __init__(self, threshold):
        self.threshold = threshold
        self.X = None
        self.Y = None
        self.Xb = None
        self.abs = None
        self.edgeWeightSumPerNode = None
        self.nonZeros = []

        self.allTop = None
        self.bottom = None
        self.top = None

    def tonparyfloat(self, X,Y):
        self.X = np.array(X)
        self.X = self.X.astype(np.float)
        self.Y = np.array(Y)
        self.Y = self.Y.astype(np.int)


    def findTopRange(self):
        #maxEachPic = []
        #for pic in self.X:
        #    if(np.max(pic) != 0):
        #        maxEachPic.append(np.max(pic))

        self.bottom = np.min(self.X)
        #self.top = np.min(maxEachPic)
        self.allTop = np.max(self.X)
        print(str(self.allTop)+ '  bottom: '+str(self.bottom)+"\n")

    def storeNonZeros(self):
        for pic in self.X:
            for row in pic:
                for value in row:
                    if value != 0:
                        self.nonZeros.append(value);

    def plotValueHistogram(self):
        self.nonZeros = np.array(self.nonZeros)
        max = self.nonZeros.max()
        min = self.nonZeros.min()
        for bins in [10,15,20,25,30]:
            plt.figure(figsize=(20,10))
            plt.hist(self.nonZeros, bins=bins)
            plt.title("Histogram of edge weights with "+str(bins)+" bins")
            #plt.show()
            plt.savefig("/Users/xiaomin/Desktop/GCNWork/dataHistogram/histogram"+str(bins)+"bins")



    def gatherEdgeInfo(self):
        self.edgeWeightSumPerNode = np.sum(self.X, axis=1)
        print('edges weigts sumed\n')

    def gatherEdgeInfoAbs(self):
        self.edgeWeightSumPerNode = np.sum(np.abs(self.X), axis=1)
        #print('abs edges weigts sumed\n')

    def convert(self):
        self.Xb = self.X
        self.Xb = (self.Xb > self.threshold).astype(int)

    def convertRangeT(self,T, step,abs):
        self.threshold = T
        if abs == True:
            self.abs = np.abs(self.X)
        else:
            self.abs = self.X
        print("before convert\n")
        print(self.X)
        
        bindex1 = (self.abs > self.threshold)
        bindex2 = (self.abs < self.threshold + step)
        bindex3 = bindex1 & bindex2
        self.Xb = bindex3.astype(int)
        print("after convert\n")
        print(self.Xb)

    def convertLessT(self,T, step,abs):
        self.threshold = T
        if abs == True:
            #abs edge cut
            self.abs = np.abs(self.X)
        else:
            self.abs = self.X
                ######
        print("before convert\n")
        print(self.X)
        #nonabs edge cut
        self.Xb = (self.abs > (self.threshold+step/2)).astype(int)
        ######
        print("after convert\n")
        print(self.Xb)

    def originalMatrixplot(self, path):

        for i in range(len(self.X)):
            plt.imshow(self.X[i])
            if(i == 0):
                plt.colorbar()
            plt.title('label: '+str(self.Y[i]))
            plt.savefig(path+str(i)+".png")

    def emptyGraph(self):
        count = 0
        for pic in self.X:
            if np.max(pic)==0:
                print(str(count) + "th graph has no positive edges\n")
            count = count + 1

    def Yratio(self):
        count0 = 0
        count1 = 0
        for eachY in self.Y:
            if eachY == 1:
                count1 = count1 + 1
            else:
                count0 = count0 + 1

        print("Dataset has "+str(count1)+" 1 label; "+str(count0)+" 0 label\n")

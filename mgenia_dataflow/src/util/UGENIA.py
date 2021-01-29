import numpy as np
import networkx as nx
import multiprocessing
import time
from multiprocessing import Pool
from swg2v.docGen import docGen
from swg2v.graphFeatureGen import graphFeatureGen
from swg2v.represent import represent
from swg2v.doDoc2Vec import doDoc2Vec


class UGENIA():
    def __init__(self,parallel,MODE,workerAmount,downSampleRate,learnRate,dim,wlIter,isTrain,abs,lessCut):
        self.reader = None
        self.Ts = None
        self.step = None
        self.numOfGraph  = None
        self.Dim = dim
        self.downSampleRate = downSampleRate
        self.learnRate = learnRate
        self.wlIter = wlIter
        self.g2vout = "../../channels/g2vFeatures"
        self.parallel = parallel
        self.MODE = MODE
        self.workerAmount = workerAmount
        self.isTrain = isTrain
        self.isAbs = abs
        self.isLessCut = lessCut

    def load(self,reader,numofgraph,Ts,step):
        self.reader = reader
        self.numOfGraph = numofgraph
        self.Ts = Ts
        self.step = step

    def run(self):
        self.parrallelPool()


    def channelSG2V(self,T ,docGener): #T is different for each call
        """
        thresholding input weighted sparse graphs with one threshold
        and generate features

        Inputs:
        reader : reader object contain loaded data sets
        T : current base threshod
        step : threshold step, threshold = T + step/2
        docGener : object to generate doc for Doc2Vec
        numOfGraph : number of graphs
        """
        for i in range(self.numOfGraph):
            if self.isAbs == 'abs':
                # Abs
                absx = np.abs(self.reader.X[i])
            else:
                # NonAbs
                absx = self.reader.X[i]

            if self.isLessCut == 'lessCut':
                # LessCut
                x = (absx > (T + self.step / 2)).astype(int)
            else:
                # RangeCut
                bindex1 = (absx > T)
                bindex2 = (absx < T + self.step)
                bindex3 = bindex1 & bindex2
                x = bindex3.astype(int)


            G = nx.from_numpy_matrix(x)

            # UGENIA
            features = []
            De = G.degree()
            if len(G.edges) == 0:
                G = nx.from_edgelist([])
            else:
                for v ,d in De:
                    if d != 0:
                        features.append(str(v))
                    else:
                        features.append('Z' +str(v))

            graphDoc = graphFeatureGen(G, features, self.wlIter)
            docGener.addDoc(graphDoc.wlIterations(), i)


    def oneChannelDocGen(self,i):
        """
        generate features for single channel of unweighted sparse graphs

        inputs:
        i : channel index
        """

        print("current ThresholdS: " + str(self.Ts[i]) +" in channel " + str(i))

        docGener = docGen()
        g2vfile = "g2v" + str(i) + ".csv"
        featureOut = self.g2vout + '/' + g2vfile
        # get Doc for current channel
        self.channelSG2V(float(self.Ts[i]), docGener)
        Doc2vec = doDoc2Vec(i, docGener.getDoc(), self.numOfGraph, self.Dim, self.downSampleRate, self.learnRate)
        del docGener
        # generate features using Doc by call Doc2Vec

        if self.isTrain == 'train':
            Doc2vec.run()
        elif self.isTrain == 'inference':
            Doc2vec.runWithTrainedModel()
        else:
            print("Error,please specify train or inference")

        outwriter = represent(Doc2vec.getRepresent(), self.numOfGraph, featureOut)
        del Doc2vec
        outwriter.output()
        del outwriter
        print("Doc2Vec done, SG2V done " + str(i))


    def parrallelPool(self):
        start = time.time()

        if self.parallel == True:
            #adjust mode when no enough memory for big data set
            if self.MODE == 'corenum':
                p = Pool(multiprocessing.cpu_count())
            elif self.MODE == 'channelnum':
                p = Pool(len(self.Ts))
            elif self.MODE == '4worker':
                p = Pool(int(self.workerAmount))
            else:
                p = Pool(multiprocessing.cpu_count())
            p.map(self.oneChannelDocGen, range(len(self.Ts)))
        else:
            for i in range(len(self.Ts)):
                self.oneChannelDocGen(i)

        end = time.time()
        elapsedT = (end-start)
        print("MCSWE finished in "+str(elapsedT)+" s")
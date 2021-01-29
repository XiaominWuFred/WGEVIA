from readData import ReadMCData
import sys
import numpy as np
import networkx as nx

"""
Python script used for converting graphs into formatted input to powergnn package
"""

def getedgeCount(X,index):
    count = 0;
    for each in X[index]:
        if each > 0:
            count = count+1

    return count

def ToGNNinputNumOfGraph(file,numOfGraphs):
    file.write(str(numOfGraphs)+"\n")

def ToGNNinput100(file,labelfile,wrc,X, T): 

    G = nx.from_numpy_matrix(X)


    numOfNodesHavingEdge = len(G.nodes)

    labelOfThisG = labelfile.readline()
    if len(G.edges) != 0:
        file.write(str(numOfNodesHavingEdge)+' '+labelOfThisG)
        wrc = wrc+1
        for i in range(numOfNodesHavingEdge):
            edgeCount = getedgeCount(X,i)
            tmpAry = X[i]
            connectedTo = np.where( tmpAry == 1)[0]
            file.write("0 "+str(edgeCount)+' ')#write node tag, edgecount
            wrc = wrc + 1
            for j in range(edgeCount):
                file.write(str(connectedTo[j]) + ' ')

            file.write('\n')
            #print(wrc)

    return wrc


T = 0 #pre calculated

reader = ReadMCData('04', 18200, '../mcDataset/csvsReal2/')  # name , MC count, path
reader.readX()

# reader.writeXcsv()
print("current Threshold: " + str(T) + "\n")


# write each graph to json, create a dataset for graph2vec
#labelFile = open('../dataset/csvs/labelAll.csv', "r")
labelFile = open('../mcDataset/csvsReal2/labelAll.csv','r')
gnnInFile = open('./gnnIn.txt', "w+")


numOfEmptyG=0
for i in range(len(reader.X)):
    reader.X[i] = np.array(reader.X[i])
    reader.X[i] = reader.X[i].astype(np.float)
    reader.X[i] = (reader.X[i] > T).astype(int)
    top = np.max(reader.X[i])
    if top == 0:
        numOfEmptyG = numOfEmptyG + 1

writerowcount = 1
for i in range(len(reader.X)):
    if i == 0:
        ToGNNinputNumOfGraph(gnnInFile, len(reader.X)-numOfEmptyG)

    writerowcount = ToGNNinput100(gnnInFile, labelFile,writerowcount, reader.X[i],T)
    print("finished graph :"+str(i))
print("wote rows: "+str(writerowcount))
labelFile.close()
gnnInFile.close()


print("done")
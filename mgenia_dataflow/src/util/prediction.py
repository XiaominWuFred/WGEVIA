import sys
import os

class prediction():
    def __init__(self,dim):
        self.dim = str(dim)

    def load(self):
        pass

    def run(self):
        # classification using generated features
        of = "../../exp/runtimeRecord/modelSave.csv"
        lof = "../../exp/runtimeRecord/lastLoss.csv"
        modelNum = '2'
        os.system("pwd")
        os.system(
            "cd ../util/\npython3 ./rc_datamining_dl_1d_cv.py ../../channels/g2vFeatures/combinedFeature.csv " + of + " " + self.dim + " " + modelNum + " " + lof)
        os.system("echo classfication finished")
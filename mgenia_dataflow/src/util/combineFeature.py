import os


class combineFeature():
    def __init__(self,threshold):
        self.threshold = int(threshold)

    def load(self):
        pass

    def run(self):
        # combine channel features
        for i in range(self.threshold):
            if i > 0:
                os.system("cd ../../channels/g2vFeatures\nsed -i 's/^[^,]*[0-9a-z]//' g2v" + str(i) + ".csv")
            os.system("cd ../../channels/g2vFeatures\nsed -i 's/\r//g' g2v" + str(i) + ".csv\nsed -i 's/\t//g' g2v" + str(
                i) + ".csv")
        os.system("cd ../../channels/g2vFeatures\npaste g* > combinedFeature.csv")

import sys
sys.path.append("../util/")
sys.path.append("../../wrapped/welter/exp/lang/python/src/gems/actors/common/")
sys.path.append("../../wrapped/welter/exp/lang/python/src/gems//edges/")
from welt_py_actor import Actor
from prediction import prediction
from welt_py_fifo_basic import welt_py_fifo_basic_new

class mgenia_prediction(Actor):
    def __init__(self,signalqin,dim):
        super().__init__(index=0, mode="COMMON")
        self.signalqin = signalqin
        self.predict = prediction(dim)

    def enable(self):
        if self.signalqin.welt_py_fifo_basic_population() > 0:
            return True
        else:
            return False

    def invoke(self):
        #check
        _ = self.signalqin.welt_py_fifo_basic_read_direct()
        print("prediction actor invokes")
        self.predict.load()
        self.predict.run()

    def terminate(self):
        pass
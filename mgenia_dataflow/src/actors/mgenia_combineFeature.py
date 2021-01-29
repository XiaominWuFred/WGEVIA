import sys
sys.path.append("../util/")
sys.path.append("../../wrapped/welter/exp/lang/python/src/gems/actors/common/")
sys.path.append("../../wrapped/welter/exp/lang/python/src/gems//edges/")
from welt_py_actor import Actor
from combineFeature import combineFeature
from welt_py_fifo_basic import welt_py_fifo_basic_new

class mgenia_combineFeature(Actor):
    def __init__(self,signalqin,signalqout,threshold):
        super().__init__(index=0, mode="COMMON")
        self.signalqin = signalqin
        self.signalqout = signalqout

        self.cf = combineFeature(threshold)

    def enable(self):
        if self.signalqin.welt_py_fifo_basic_population() > 0:
            if self.signalqout.welt_py_fifo_basic_population() == 0:
                return True
            else:
                return False
        else:
            return False

    def invoke(self):
        #check
        print("combineFeature actor invokes")
        _ = self.signalqin.welt_py_fifo_basic_read_direct()
        self.cf.load()
        self.cf.run()

        signal = True
        self.signalqout.welt_py_fifo_basic_write(signal)



    def terminate(self):
        pass
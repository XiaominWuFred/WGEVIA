import sys
sys.path.append("../util/")
sys.path.append("../../wrapped/welter/exp/lang/python/src/gems/actors/common/")
sys.path.append("../../wrapped/welter/exp/lang/python/src/gems//edges/")
from welt_py_actor import Actor
from multiChannelGen import multiChannelGen
from welt_py_fifo_basic import welt_py_fifo_basic_new

class mgenia_multiChannelGen(Actor):
    def __init__(self,threshold,posT,readerqin,readerqout,stepqout,Tsqout):
        super().__init__(index=0, mode="COMMON")
        #input
        self.readerqin = readerqin
        #variables
        self.multiCG = multiChannelGen(threshold,posT)
        #output
        self.readerqout = readerqout
        self.stepqout = stepqout
        self.Tsqout = Tsqout

    def enable(self):
        if self.readerqin.welt_py_fifo_basic_population() > 0:
            if self.readerqout.welt_py_fifo_basic_population() == 0:
                return True
            else:
                return False
        else:
            return False

    def invoke(self):
        #check
        print("loadGraph actor invokes")
        reader = self.readerqin.welt_py_fifo_basic_read_direct()
        self.multiCG.load(reader)
        self.multiCG.run()

        self.readerqout.welt_py_fifo_basic_write_ref(reader)
        self.stepqout.welt_py_fifo_basic_write(self.multiCG.step)
        self.Tsqout.welt_py_fifo_basic_write(self.multiCG.Ts)



    def terminate(self):
        pass




#readerqin,readerqout,stepqout,Tsqout
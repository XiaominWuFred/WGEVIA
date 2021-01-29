import sys
sys.path.append("../util/")
sys.path.append("../../wrapped/welter/exp/lang/python/src/gems/actors/common/")
sys.path.append("../../wrapped/welter/exp/lang/python/src/gems//edges/")
from welt_py_actor import Actor
from UGENIA import UGENIA
from welt_py_fifo_basic import welt_py_fifo_basic_new

class mgenia_UGENIA(Actor):
    def __init__(self,readerqin,stepqin,Tsqin,signalqout,
                 parallel,MODE,workerAmount,downSampleRate,learnRate,dim,wlIter,isTrain,isAbs,isLessCut):
        super().__init__(index=0, mode="COMMON")
        self.readerqin = readerqin
        self.stepqin = stepqin
        self.Tsqin = Tsqin
        self.signalqout = signalqout

        self.ugenia = UGENIA(parallel,MODE,workerAmount,downSampleRate,learnRate,dim,wlIter,isTrain,isAbs,isLessCut)

    def enable(self):
        if self.readerqin.welt_py_fifo_basic_population() > 0:
            if self.signalqout.welt_py_fifo_basic_population() == 0:
                return True
            else:
                return False
        else:
            return False

    def invoke(self):
        #check
        print("UGENIA actor invokes")
        reader = self.readerqin.welt_py_fifo_basic_read_direct()
        Ts = self.Tsqin.welt_py_fifo_basic_read_direct()
        step = self.stepqin.welt_py_fifo_basic_read_direct()
        numofgraph = len(reader.X)
        self.ugenia.load(reader,numofgraph,Ts,step)
        self.ugenia.run()
        signal = True
        self.signalqout.welt_py_fifo_basic_write(signal)


    def terminate(self):
        pass
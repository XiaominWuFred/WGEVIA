import sys
sys.path.append("../util/")
sys.path.append("../../wrapped/welter/exp/lang/python/src/gems/actors/common/")
sys.path.append("../../wrapped/welter/exp/lang/python/src/gems//edges/")
from welt_py_actor import Actor
from loadGraph import loadGraph
from welt_py_fifo_basic import welt_py_fifo_basic_new

class mgenia_loadGraph(Actor):
    def __init__(self,pathqin,readerqout,isTrain = True):
        super().__init__(index=0, mode="COMMON")
        self.pathqin = pathqin
        self.readerqout = readerqout
        self.loader = loadGraph(isTrain)

    def enable(self):
        if self.pathqin.welt_py_fifo_basic_population() > 0:
            if self.readerqout.welt_py_fifo_basic_population() == 0:
                return True
            else:
                return False
        else:
            return False

    def invoke(self):
        #check
        print("loadGraph actor invokes")
        path = self.pathqin.welt_py_fifo_basic_read_direct()
        self.loader.load(path)
        self.loader.run()

        self.readerqout.welt_py_fifo_basic_write_ref(self.loader.reader)


    def terminate(self):
        pass

#unit test

if __name__ == "__main__":
    fifo_test = welt_py_fifo_basic_new(1, 0)
    actor_lg = mgenia_loadGraph(fifo_test,isTrain=True)
    if actor_lg.enable():
        actor_lg.invoke()
    print(fifo_test)
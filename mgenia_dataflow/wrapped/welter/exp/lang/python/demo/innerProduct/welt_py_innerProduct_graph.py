import sys
sys.path.append("../../src/gems/actors/basic")
sys.path.append("../../src/gems/actors/common")
sys.path.append("../../src/gems/edges")
sys.path.append("../../src/tools/graph")
sys.path.append("../../src/tools/runtime")

from welt_py_file_sink import welt_py_file_sink
from welt_py_file_source import welt_py_file_source
from welt_py_inner_product import welt_py_inner_product
from welt_py_graph import *
from welt_py_util import *
from welt_py_fifo_basic import *

class welt_py_innerProduct_graph(Graph):
    def __init__(self,file_x,file_y,file_m,file_out):
        actorReadX = 0
        actorReadY = 1
        actorReadM = 2
        actorInnerProduct = 3
        actorWriteOut = 4

        actorCount = 5

        self.descriptor = [None]*5

        fifoX2IP = 0
        fifoY2IP = 1
        fifoM2IP = 2
        fifoIP2Out = 3

        fifoCount = 4

        super().__init__(actorCount,fifoCount)

        fifo_x2ip = welt_py_fifo_basic_new(capacity=3, index=0)
        fifo_y2ip = welt_py_fifo_basic_new(capacity=3, index=1)
        fifo_m2ip = welt_py_fifo_basic_new(capacity=1, index=2)
        fifo_ip2out = welt_py_fifo_basic_new(capacity=1, index=3)

        self.welt_py_graph_set_fifo(fifoX2IP, fifo_x2ip)
        self.welt_py_graph_set_fifo(fifoY2IP, fifo_y2ip)
        self.welt_py_graph_set_fifo(fifoM2IP, fifo_m2ip)
        self.welt_py_graph_set_fifo(fifoIP2Out, fifo_ip2out)

        actor_readX = welt_py_file_source(index=0,file=file_x,fifo_out=fifo_x2ip)
        actor_readY = welt_py_file_source(index=1,file=file_y,fifo_out=fifo_y2ip)
        actor_readM = welt_py_file_source(index=3,file=file_m,fifo_out=fifo_m2ip)
        actor_innerProduct = welt_py_inner_product(index=4,fifo_m = fifo_m2ip,fifo_x=fifo_x2ip,
                                                   fifo_y = fifo_y2ip,fifo_out=fifo_ip2out)
        actor_writeOut = welt_py_file_sink(index=5,file=file_out,fifo_in=fifo_ip2out)

        self.welt_py_graph_set_actor(actorReadX, actor_readX)
        self.descriptor[actorReadX] = 'actorReadX'
        self.welt_py_graph_set_actor(actorReadY, actor_readY)
        self.descriptor[actorReadY] = 'actorReadY'
        self.welt_py_graph_set_actor(actorReadM, actor_readM)
        self.descriptor[actorReadM] = 'actorReadM'
        self.welt_py_graph_set_actor(actorInnerProduct, actor_innerProduct)
        self.descriptor[actorInnerProduct] = 'actorInnerProduct'
        self.welt_py_graph_set_actor(actorWriteOut, actor_writeOut)
        self.descriptor[actorWriteOut] = 'actorWriteOut'

        #print(self.actors)

if __name__ == "__main__":
    #simulate driver
    file_x = open('./x.txt', 'r')
    file_y = open('./y.txt', 'r')
    file_m = open('./m.txt', 'r')
    file_out = open('./out.txt', 'w')
    graph = welt_py_innerProduct_graph(file_x,file_y,file_m,file_out)

    welt_py_util_simple_scheduler(graph.actors, graph.actorCount, graph.descriptor)

    print('all done')
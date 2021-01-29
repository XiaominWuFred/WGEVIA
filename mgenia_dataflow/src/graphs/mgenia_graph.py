################################################################################
# @ddblock_begin copyright
# -------------------------------------------------------------------------
# Copyright (c) 2017-2020
# UMB-UMD Neuromodulation Research Group,
# University of Maryland at Baltimore, and
# University of Maryland at College Park.
#
# All rights reserved.
#
# IN NO EVENT SHALL THE UNIVERSITY OF MARYLAND BALTIMORE
# OR UNIVERSITY OF MARYLAND COLLEGE PARK BE LIABLE TO ANY PARTY
# FOR DIRECT, INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES
# ARISING OUT OF THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF
# THE UNIVERSITY OF MARYLAND HAS BEEN ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
#
# THE UNIVERSITY OF MARYLAND SPECIFICALLY DISCLAIMS ANY WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. THE SOFTWARE
# PROVIDED HEREUNDER IS ON AN "AS IS" BASIS, AND THE UNIVERSITY OF
# MARYLAND HAS NO OBLIGATION TO PROVIDE MAINTENANCE, SUPPORT, UPDATES,
# ENHANCEMENTS, OR MODIFICATIONS.DE MAINTENANCE, SUPPORT, UPDATES,
# ENHANCEMENTS, OR MODIFICATIONS.
# -------------------------------------------------------------------------

# @ddblock_end copyright
################################################################################
import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

import sys
sys.path.append("../actors")
sys.path.append("../util/")
sys.path.append("../../wrapped/welter/exp/lang/python/src/gems/edges/")
sys.path.append("../../wrapped/welter/exp/lang/python/src/tools/graph")
sys.path.append("../../wrapped/welter/exp/lang/python/src/tools/runtime")

from welt_py_graph import Graph
from welt_py_util import welt_py_util_simple_scheduler
from welt_py_fifo_basic import welt_py_fifo_basic_new

from mgenia_loadGraph import mgenia_loadGraph
from mgenia_multiChannelGen import mgenia_multiChannelGen
from mgenia_UGENIA import mgenia_UGENIA
from mgenia_combineFeature import mgenia_combineFeature
from mgenia_prediction import mgenia_prediction

class mgenia_graph(Graph):
    def __init__(self):
        super().__init__(actorCount=5, fifoCount=1,scheduler=self.scheduler)
        self.descriptor = [None] * self.actorCount

    def construct(self,isTrain,posT,MODE,workerAmount,isAbs,isLessCut,threshold,dim,wlIter):
        #actor_loadGRaph
        #input FIFO

        pathqin_lg = welt_py_fifo_basic_new(capacity=3, index=0)
        readerqout_lg = welt_py_fifo_basic_new(capacity=1, index=0)

        pathqin_lg.welt_py_fifo_basic_write('../../weightedGraphs/')

        lg = mgenia_loadGraph(pathqin_lg,readerqout_lg,isTrain)

        #actor_multiChannelGen
        readerqin_mcg = readerqout_lg
        readerqout_mcg = welt_py_fifo_basic_new(capacity=1, index=0)
        stepqout_mcg = welt_py_fifo_basic_new(capacity=1, index=0)
        Tsqout_mcg = welt_py_fifo_basic_new(capacity=1, index=0)

        mcg = mgenia_multiChannelGen(threshold,posT,readerqin_mcg,readerqout_mcg,stepqout_mcg,Tsqout_mcg)

        #actor_UGENIA
        readerqin_ugenia = readerqout_mcg
        stepqin_ugenia = stepqout_mcg
        Tsqin_ugenia = Tsqout_mcg
        signalqout_ugenia = welt_py_fifo_basic_new(capacity=1, index=0)

        ugenia = mgenia_UGENIA(readerqin_ugenia,stepqin_ugenia,Tsqin_ugenia,signalqout_ugenia,
                 True,MODE,workerAmount,0.0001,0.025 ,dim,wlIter,isTrain,isAbs,isLessCut)
        #actor_combineFeature
        signalqin_cf = signalqout_ugenia
        signalqout_cf = welt_py_fifo_basic_new(capacity=1, index=0)
        cf = mgenia_combineFeature(signalqin_cf,signalqout_cf,threshold)
        #actor_prediction
        signalqin_predict = signalqout_cf
        predict = mgenia_prediction(signalqin_predict,dim)

        #schedule actors
        actor_loadGraph = 0
        actor_multiChannelGen = 1
        actor_UGENIA = 2
        actor_combineFeature = 3
        actor_prediction = 4

        #add actors, construct graph
        self.welt_py_graph_set_actor(actor_loadGraph, lg)
        self.descriptor[actor_loadGraph] = 'actor_loadGraph'

        self.welt_py_graph_set_actor(actor_multiChannelGen, mcg)
        self.descriptor[actor_multiChannelGen] = 'actor_multiChannelGen'

        self.welt_py_graph_set_actor(actor_UGENIA, ugenia)
        self.descriptor[actor_UGENIA] = 'actor_UGENIA'

        self.welt_py_graph_set_actor(actor_combineFeature, cf)
        self.descriptor[actor_combineFeature] = 'actor_combineFeature'

        self.welt_py_graph_set_actor(actor_prediction, predict)
        self.descriptor[actor_prediction] = 'actor_prediction'

    def scheduler(self):
        welt_py_util_simple_scheduler(self.actors, self.actorCount, self.descriptor)


if __name__ == "__main__":
    threshold = sys.argv[1]
    dim = int(sys.argv[2])
    wlIter = int(sys.argv[3])

    isTrain = sys.argv[4]
    posT = sys.argv[5]
    isLessCut = sys.argv[6]
    isAbs = sys.argv[7]
    MODE = sys.argv[8]

    try:
        workerAmount = sys.argv[9]
    except:
        workerAmount = None

    pathes = []
    graph = mgenia_graph()
    graph.construct(isTrain,posT,MODE,workerAmount,isAbs,isLessCut,threshold,dim,wlIter)
    graph.scheduler()

    print("ALL done")
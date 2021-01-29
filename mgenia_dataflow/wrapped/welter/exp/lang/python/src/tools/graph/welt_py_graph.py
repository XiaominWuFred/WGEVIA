from abc import ABC


class Graph(ABC):
    def __init__(self, actorCount,fifoCount,scheduler=None):
        self.actors = [None]*actorCount
        self.actorCount = actorCount
        self.fifos = [None]*fifoCount
        self.fifoCount = fifoCount
        self.scheduler = scheduler
        super().__init__()


    def welt_py_graph_set_actor(self, index, actor):
        self.actors[index] = actor

    def welt_py_graph_get_actor(self, index):
        return self.actors[index]

    def welt_py_graph_add_fifo(self):
        self.fifoCount += 1

    def welt_py_graph_set_fifo(self, index, fifo):
        self.fifos[index] = fifo

    def welt_py_graph_get_fifo(self, index):
        return self.fifos[index]

    def welt_py_graph_actor_count(self):
        return self.actorCount

    def welt_py_graph_fifo_count(self):
        return self.fifoCount

    def welt_py_graph_set_scheduler(self, scheduler):
        self.scheduler = scheduler

    def welt_py_graph_get_scheduler(self):
        return self.scheduler
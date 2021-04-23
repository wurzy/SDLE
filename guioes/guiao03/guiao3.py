class Node:
    def __init__(self, node_num):
        self.id = node_num

    # handle 'msg' by process 'src' at time 't'
    def handle(self, src, msg, to):
        pass


class Simulator:
    # - nodes: {0: Node, 1: Node, 2:Node ... }
    # - distances: {(0,1): 103, (0,2): 40, ...}
    def __init__(self, nodes, distances):
        self.nodes = nodes
        self.distances = distances
        self.current_time = 0
        self.pending = []  # [(delay, (src, dst, msg))]

    def start(self, initial_msg):
        # schedule first event
        for i in self.nodes:
            event = (0, (None, i, initial_msg))
            self.pending.append(event)

        # run the simulation loop
        self.run_loop()

    def run_loop(self):
        while len(self.pending) > 0:
            print()
            # to do
            # - find in 'self.pending' the nex message that should be delivered
            # - handle such message in its destination
            # - schedule new messages (if any)
            #   > set the delay according to 'self.distances'


s = Simulator({}, {})
s.start('ola')
class FlowEdge:
    def __init__(self, v, u, cap=0):
        self.v = v
        self.u = u
        self.flow = 0
        self.cap = cap
        self.residual = None

    def augment(self, flow):
        if flow <= 0:
            raise Exception('flow must be positive')
        if self.remaining_cap() < flow:
            raise Exception("overflow on edge")
        self.flow += flow
        self.residual.flow -= flow

    def remaining_cap(self):
        assert((self.cap - self.flow) >= 0) # must be positive
        return self.cap - self.flow

    def is_replica(self):
        return self.cap == 0

    def get_flow(self):
        return -1 * self.flow if self.is_replica() else self.flow

    def get_cap(self):
        return -1 * self.flow if self.is_replica() else self.cap

    def src(self):
        return self.v

    def dst(self):
        return self.u


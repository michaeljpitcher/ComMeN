from LungComMeN.LungNetwork import *


def get_nodes(compartments):
    a = LungPatch(0, compartments, 1.1, 0.9)
    b = LungPatch(1, compartments, 1.2, 0.8)
    c = LymphPatch(2, compartments)
    d = LymphPatch(3, compartments)
    e1 = LungEdge(a, b, False, 1.3)
    e2 = LymphEdge(a, c, False, 1.4)
    e3 = LymphEdge(b, d, False, 1.5)
    return [a, b, c, d]

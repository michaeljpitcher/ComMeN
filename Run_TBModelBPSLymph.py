from PulmonaryTBComMeN import *

# a = BacteriaReplicate(0.1, [], 'a')

model = TBModelBPSLymph('TBModel.cfg')

seeding = {ANTERIOR_LEFT: {MACROPHAGE_REGULAR: 2}}

import cProfile as cp
c = cp.Profile()
c.enable()
model.run(10000, seeding)
c.disable()
c.print_stats("cumtime")
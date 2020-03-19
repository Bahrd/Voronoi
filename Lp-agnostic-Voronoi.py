## The Lp agnostic 1-NN algorithm illustration
# 1. Generate N random sites inside a square
# 2. Create the Voronoi's diagram for Lp, 0 < p ≤ 2 (p = 2.0 is somehow distingushed)
# 3. Create a lattice of N(N - 1) sites for the generated N random ones
# 4. Associate the new N(N - 1) sites to the classes accordingly to the diagram for the selected Lp
# 5. Generate o Voronoi diagram for these NxN sites
# 6. Repeat the steps #2-#5 for other Lq, 0 < q ≤ 2 (q = 0.25 is weird enough)

from winsound import Beep as beep
from random import randrange as RA, seed
from sys import argv
## Local stuff...
from VoronoiUtilities import *

## Show time off!
rsd = int(RA(0x12345678))
c, sd = (int(argv[1]), int(argv[2])) if len(argv) == 3 else \
	    (int(argv[1]), rsd) if len(argv) == 2 else (0x10, rsd)

# Lp, with p as a reference and q as an illustration
p, q, w = 2.0, 0.25, 0x100

# The reference diagram for p and just an illustration for q...
NXY, _ = lp_Voronoi_diagram(w, p, c, sd), lp_Voronoi_diagram(w, q, c, sd)

# ... the diagram's Lp-agnostic counterparts w.r.t. p and q
for pq in ((p, q), (q, p)):	lp_agnostic_Voronoi_diagram(*NXY, w, *pq, c, sd)

# ... a summary and fanfares!
for pl in ((0x1b8, 0x7d), (0x1b8, 0x7d), (0x19f, 0x7d), (0x1b8, 0xfa)): beep(*pl)
print('seed =', rsd)
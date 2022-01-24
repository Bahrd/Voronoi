## The Lp agnostic (invariant!) 1-NN algorithm illustration
# 1. Generate N random sites inside a square
# 2. Create the Voronoi diagram for Lp, 0 < p ≤ 2 (p = 2.0 is somehow distingushed)
# 3. Create a lattice of N(N - 1) sites for the generated N random ones
# 4. Associate the new N(N - 1) sites to the classes accordingly to the diagram for the selected Lp
# 5. Generate o Voronoi diagram for these NxN sites
# 6. Repeat the steps #2-#5 for other Lq, 0 < q ≤ 2 (q = 0.25 is weird enough)

## &"C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python37_64\pyton.exe"

from winsound import Beep as beep
from random import randrange as RA, seed
from sys import argv
## Local stuff...
from VoronoiUtilities import *

## Show time off!
rsd = int(RA(0x12345678))
c, sd = (int(argv[1]), int(argv[2])) if len(argv) == 3 else (int(argv[1]), rsd) if len(argv) == 2 else (0x10, rsd)

patterns = [[0x60, 0x60, 0xb0, 0xb0, 0xb0], [0x60, 0xb0, 0x64, 0x60, 0xb0], 
            [0xff, 0xff, 0, 0x80, 0], [0, 0xff, 0, 0x80, 0], [0, 0xff, 0, 0x80, 0]]


# Lp, for both p and q
w = 0x100
qs, ps = [.25] , [.25, 0.5, 1.0, 2.0, 4.0] # (2.0, 0.25, 1.0, 2.0, 4.0, 8.0) ## extensions = ('PNG', 'PDF')
for p in ps:
   for q in qs: 
        # The reference diagrams for p and q...
        _ = lp_planted_Voronoi_diagram(patterns, w, p)

        #NXY, _ = lp_Voronoi_diagram(w, p, c, sd), lp_Voronoi_diagram(w, q, c, sd)
        # ... together with the diagram's Lp-agnostic counterparts w.r.t. p and q
        #lp_agnostic_Voronoi_diagram(*NXY, w, p, q, c, sd)

# ... a summary and fanfares!
for pl in ((0x1b8, 0x7d), (0x1b8, 0x7d), (0x19f, 0x7d), (0x1b8, 0xfa)): beep(*pl)
print('seed =', sd)
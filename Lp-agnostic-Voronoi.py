## The Lp agnostic 1-NN algorithm illustration [Project «⅄⅃LY»]
# 1. Generate N random patterns inside a square
# 2. Create the Voronoi's diagram for Lp, 0 < p ≤ 2 (p = 2.0 is somehow distingushed)
# 3. Complement N patterns with a lattice of N × (N - 1) patterns to get a Hanan grid
# 4. Associate the new N × (N - 1) patterns to the classes w.r.t. the selected Lp
# 5. Generate o Voronoi diagram for these N × N patterns (effectively, for the N × N Hanan grid)
# 6. Repeat the steps #2-#5 for other Lq, 0 < q ≤ 2 (q = 0.25 seems arbitrary enough)

## &"C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python37_64\python.exe" - YPMV (Your Python May Vary)
## .\Lp-agnostic-Voronoi.py 8 98828880 - used in the IEEE article

from winsound import Beep as beep
from random import randrange as RA, seed
from sys import argv
## Local stuff...
from VoronoiUtilities import *

## Show time off!
rsd = int(RA(0x12345678))
c, sd = (int(argv[1]), int(argv[2])) if len(argv) >= 3 else (int(argv[1]), rsd) if len(argv) == 2 else (0x10, rsd)

# Lp, for both p and q
w, Hanan = 0x100, eval(argv[3]) if len(argv) == 4 else False
qs, ps = [2.0], [.25, 0.5, 1.0, 2.0, 4.0]
for p in ps:
   for q in qs: 
        ## The diagrams for fixed (planted) patterns... 
        #  ♫♪ This thorn in my side is from the tree I've planted ♪♫ [so]
        #  ♫♪ I'm diggin' my way to somethin' better ♪♫ 
        _ = lp_planted_Voronoi_diagram(sd, w, p, Hanan = Hanan, sites = True)

        # The reference diagrams for p and q...
        NXY, _ = lp_Voronoi_diagram(w, p, c, sd, sites = False), lp_Voronoi_diagram(w, q, c, sd, sites = False)
        # ... together with the diagram's Lp-agnostic counterparts w.r.t. p and q
        _ = lp_agnostic_Voronoi_diagram(*NXY, p, q, c, sd)
        # ... and the sets of patterns with different decisions
        _ = lp_agnostic_Voronoi_ps(p, sd)

# ... a summary (in a nutshell) and fanfares! 
print('seed =', sd)
for pl in ((0x1b8, 0x7d), (0x1b8, 0x7d), (0x19f, 0x7d), (0x1b8, 0xfa)): beep(*pl) #♫♪ ¡⅄⅃LY! ♪♫
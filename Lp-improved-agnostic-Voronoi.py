## The Lp agnostic 1-NN algorithm illustration [Project «⅄⅃LY»]
# 1. Generate N random patterns inside a square
# 2. Create the Voronoi's diagram for Lp, 0 < p ≤ 2 (p = 2.0 is somehow distingushed)
# 3. Complement N patterns with a lattice of N × (N - 1) patterns to get a Hanan grid
# 4. Associate the new N × (N - 1) patterns to the classes w.r.t. the selected Lp
# 5. Generate o Voronoi diagram for these N × N patterns (effectively, for the N × N Hanan grid)
# 6. Repeat the steps #2-#5 for other Lq, 0 < q ≤ 2 (q = 0.25 seems intriguing enough)
# 7. In order to improve approximation quality one can add a new (set of) 
#    pattern(s) in the arbitrary position(s), together with the accompanying lattice points.

## &"C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python37_64\python.exe" .\Lp-improved-agnostic-Voronoi.py
#    YPMV (Your Path May Vary)

from winsound import Beep as beep
from random import randrange as RA, seed
from sys import argv
## Local stuff...
from VoronoiUtilities import *

## Voronoi diagrams and their agnostic versions...
rsd = int(RA(0x12345678))	
c, sd = (int(argv[1]), int(argv[2])) if len(argv) == 3 else (int(argv[1]), rsd) if len(argv) == 2 else (0x10, rsd)

# Lp, for p and q 
p, q, w = 2.0, 1.0, 0x100
## The reference diagrams for p and q...
NXY, _ = lp_Voronoi_diagram(w, p, c, sd, sites = True), lp_Voronoi_diagram(w, q, c, sd, sites = False)
# ... together with the diagram's Lp-agnostic counterparts w.r.t. p and q
for pq in ((p, q), (q, p)):	lp_agnostic_Voronoi_diagram(*NXY, w, *pq, c, sd)

## ... and (supposedly) their more accurate versions
# Make a difference
lp_agnostic_Voronoi_ps(p, sd); lp_agnostic_Voronoi_ps(q, sd)
# Compute the improved version for Lp
lp_improved_agnostic_Voronoi_diagram(*NXY, w, 0x1, c, p, q, sd, sites = True, lattice = True)

# ... a (nutshell) summary and fanfares!
print('seed =', sd)
for pl in ((0x1b8, 0x7d), (0x1b8, 0x7d), (0x19f, 0x7d), (0x1b8, 0xfa)): beep(*pl)
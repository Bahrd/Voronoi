## The Lp agnostic 1-NN algorithm illustration
# 1. Generate N random sites inside a square
# 2. Create the Voronoi's diagram for lp, 0 < p ≤ 2 (p = 2.0 is set by default)
# 3. Create a lattice of N(N - 1) sites for the generated N random ones
# 4. Associate the new N(N - 1) sites to the classes accordingly to the diagram for the selected lp
# 5. Generate o Voronoi diagram (for arbitrary p <= 2) for these NxN sites
# 6. In order to (supposedly) improve approximation quality one can add a new (set of) 
#    site(s) in the arbitrary position(s), together with the accompanying lattice points.

from winsound import Beep as beep
from random import randrange as RA, seed
from sys import argv
## Local stuff...
from VoronoiUtilities import *

## Voronoi diagrams and their agnostic versions...
rsd = int(RA(0x12345678))
c, sd = (int(argv[1]), int(argv[2])) if len(argv) == 3 else (int(argv[1]), rsd) if len(argv) == 2 else (0x10, rsd)

# Lp, for p and q 
p, q, w = 2.0, 0.25, 0x100
# The reference diagrams for p and q...
NXY, _ = lp_Voronoi_diagram(w, p, c, sd), lp_Voronoi_diagram(w, q, c, sd)
# ... together with the diagram's Lp-agnostic counterparts w.r.t. p and q
for pq in ((p, q), (q, p)):	lp_agnostic_Voronoi_diagram(*NXY, w, *pq, c, sd)

## ... and (supposedly) their more accurate versions
if(0b1):
	# Make a difference
	lp_agnostic_Voronoi_ps(p, sd); lp_agnostic_Voronoi_ps(q, sd)
	# Compute the improved version for Lp
	lp_improved_agnostic_Voronoi_diagram(*NXY, w, 0x1, c, p, q, sd)
	lp_improved_agnostic_Voronoi_diagram(*NXY, w, 0x1, c, q, p, sd)

if(0b0): ... # TODO: Make it nicer with sites
	#lp_improved_agnostic_Voronoi_diagram(*NXY, w, 0x1, c, p, q, sd, sites = True)
	#lp_improved_agnostic_Voronoi_diagram(*NXY, w, 0x1, c, q, p, sd, sites = True)
	#lp_agnostic_Voronoi_ps(p = p, sd = sd, improved = True)
	#lp_agnostic_Voronoi_ps(p = p, sd = sd, improved = True, sites = True, opr = '(a + 3*b)/4')

# ... a summary and fanfares!
for pl in ((0x1b8, 0x7d), (0x1b8, 0x7d), (0x19f, 0x7d), (0x1b8, 0xfa)): beep(*pl)
print('seed =', rsd)
## The Lp agnostic (invariant!) 1-NN algorithm illustration
# 1. Generate N random sites inside a square
# 2. Create the Voronoi diagram for Lp, 0 < p ≤ 2 (p = 2.0 is somehow distingushed)
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
c, sd = (int(argv[1]), int(argv[2])) if len(argv) == 3 else (int(argv[1]), rsd) if len(argv) == 2 else (0x4, rsd)

# Resolution... (length of a side of the square test-bed (in pixels))
w = 0x100
# Lp, for both p and q
#for p in (2.0, 0.25, 1.0, 2.0, 4.0, 8.0):
#   for q in (2.0, 0.25, 1.0, 2.0, 4.0, 8.0): 
for p in [.25, 2.0]:
   for q in [.25, 2.0]:         # The reference diagrams for p and q... (extensions = ('PNG', 'PDF'))
        NXY, _ = lp_Voronoi_diagram(w, p, c, sd), lp_Voronoi_diagram(w, q, c, sd)
        # ... together with the diagram's Lp-agnostic counterparts w.r.t. p and q
        #for pq in ((p, q)):	
        lp_agnostic_Voronoi_diagram(*NXY, w, p, q, c, sd, True)

# ... a summary and fanfares! See: https://www.alt-codes.net/music_note_alt_codes.php 
#                                  https://realpython.com/python-encodings-guide/#enter-unicode 
# ♪ a.k.a. print(b'\xe2\x99\xaa'.decode('utf-8'), 'or \U0001D160, or \N{EIGHTH NOTE}') 
# ♩        print(b'\xe2\x99\xa9'.decode('utf-8'), 'or \U0001D15F, or \N{Quarter note}')
for pl in ((0x1b8, 0x7d), (0x1b8, 0x7d), (0x19f, 0x7d), (0x1b8, 0xfa)): beep(*pl)
print('seed =', sd)
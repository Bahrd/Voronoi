## The Lp agnostic 1-NN algorithm illustration
# 1. Generate N random sites inside a square
# 2. Create the Voronoi's diagram for lp, 0 < p ≤ 2 (p = 2.0 is set by default)
# 3. Create a lattice of N(N - 1) sites for the generated N random ones
# 4. Associate the new N(N - 1) sites to the classes accordingly to the diagram for the selected lp
# 5. Generate o Voronoi diagram (for arbitrary p <= 2) for these NxN sites

# REMARK: In order to (supposedly) improve approximation quality one can add a new (set of) 
#         site(s) in the arbitrary position(s), together with the accompanying lattice points.

from winsound import Beep as beep
from time import time as TT
from PIL import Image, ImageMath
from random import randrange as RA, seed
from sys import argv
import os.path
from numpy import arange

## A decorative fun... See: https://www.geeksforgeeks.org/decorators-in-python/
def ITT(f):
	def time_warper_wrapper(*args, **kwargs): 
		begin = TT() # from time import time as TT
		r = f(*args, **kwargs) 
		end = TT()
		print('{0} evaluated in {1}s'.format(f.__name__, round(end - begin)))
		return r
	return time_warper_wrapper
## Random random utilities...
def RRGB(l = 0x0, u = 0xff, s = 0x20): return [RA(l, u, s) for _ in range(0x3)]
def RBW(l = 0x32, u = 0xd0, s = 0x20): return [RA(l, u, s)] * 0x3 if RA(0x10) > 1 else (0xff, 0x0, 0x0) # s = 0x96 for binary B&W diagrams
RRC = RBW if(0x1) else RRGB
def RR(l):  return RA(int(l/0x20), int(0x1f * l/0x20))
def RXY(l): return [RR(l) for _ in range(2)]
## A pivotal yet elementary function...
def distanceLp(x, y, p):
	return pow(pow(abs(x), p) + pow(abs(y), p), 1.0/p) if p > 0.0 else max(abs(x), abs(y))

## Actual stuff... 
@ITT
def lp_Voronoi_diagram(w = 0x100, p = 2.0, c = 0x10, sd = 0x303):
	seed(sd) # Controlled randomness to get the same points for various p
	image = Image.new("RGB", (w, w))
	
	# Just a standard random case... # Black & white...

	nxy, nrgb = zip(*[(RXY(w), RRC(0x0, 0x100)) for _ in range(c)])
	nx, ny = zip(*nxy); nr, ng, nb = zip(*nrgb)
	##Drawing...
	img = image.load()
	# ... cells
	for y in range(w):
		for x in range(w):
			dmin = distanceLp(w - 1, w - 1, p); j = -1
			for i in range(c):
				d = distanceLp(nx[i] - x, ny[i] - y, p)
				if d < dmin:
					dmin = d; j = i
			img[x, y] = nr[j], ng[j], nb[j]

	f = './images/Voronoi-L{0}@{1}.png'.format(p, sd)
	image.save(f, 'PNG')
	return nx, ny
@ITT
def lp_agnostic_Voronoi_diagram(NX, NY, w = 0x100, p = 2.0, q = 0.25, c = 0x10):
	# Generate N(N-1) additional sites to form an NxN lattice
	# ... and extra sites as well
	c = len(NX); nx, ny = [], c*NY
	for n in range(c):
		nx += c*[NX[n]]		
	c *= len(NY);

	# Set sites' classes from the image
	f = './images/Voronoi-L{0}@{1}.png'.format(p, sd)
	image = Image.open(f); img = image.load()
	w = image.size[0]
	nr, ng, nb = zip(*[img[nx[j], ny[j]] for j in range(c)])
	image.close()
	
	## Drawing...
	image = Image.new("RGB", (w, w))
	img = image.load()
	# ... cells
	for y in range(w):
		for x in range(w):
			dmin = distanceLp(w - 1, w - 1, q); j = -1
			for i in range(c):
				d = distanceLp(nx[i] - x, ny[i] - y, q)
				if d < dmin:
					dmin = d; j = i
			img[x, y] = nr[j], ng[j], nb[j]

	f = './images/Lp-agnostic-Voronoi-L{0}@{1}.png'.format(q, sd)
	image.save(f, 'PNG')
	image.save(f, 'PNG')

## Show time off!
rsd = int(RA(0x12345678))
c, sd = (int(argv[1]), int(argv[2])) if len(argv) == 3 else \
	    (int(argv[1]), rsd) if len(argv) == 2 else (0x10, rsd)
# Lp, with p as a reference and q as an illustration
p, q, w = 2.0, 0.25, 0x100
# The reference diagram for p and just an illustration for q...
NXY, _ = lp_Voronoi_diagram(w, p, c, sd), lp_Voronoi_diagram(w, q, c, sd)
# ... the diagram's Lp-agnostic counterparts w.r.t. p and q
for pq in ((p, q), (q, p)):	lp_agnostic_Voronoi_diagram(*NXY, w, *pq)
# ... a summary and fanfares!
for pl in ((0x1b8, 0x7d), (0x1b8, 0x7d), (0x19f, 0x7d), (0x1b8, 0xfa)): beep(*pl)
print('seed =', rsd)
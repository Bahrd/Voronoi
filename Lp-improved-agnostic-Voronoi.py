## The Lp agnostic 1-NN algorithm illustration
# 1. Generate N random sites inside a square
# 2. Create the Voronoi's diagram for lp, 0 < p ≤ 2 (p = 2.0 is set by default)
# 3. Create a lattice of N(N - 1) sites for the generated N random ones
# 4. Associate the new N(N - 1) sites to the classes accordingly to the diagram for the selected lp
# 5. Generate o Voronoi diagram (for arbitrary p <= 2) for these NxN sites
# 6. In order to (supposedly) improve approximation quality one can add a new (set of) 
#    site(s) in the arbitrary position(s), together with the accompanying lattice points.

from winsound import Beep as beep
from PIL import Image, ImageMath; from random import randrange as RA, seed
from sys import argv; from numpy import arange
import os.path
## Local stuff...
from VoronoiUtilities import *

@ITT
def lp_improved_agnostic_Voronoi_diagram(NX, NY, w = 0x100, m = 0x1, c = 0x10, p = 2.0, q = 0.25, sites = False):
	## Generate extra sites for extra precision (in locations
	# where the classifications differ for Lp and for agnostic-Lp).
	f = './images/Lp-agnostic-Voronoi-math-L{0}@{1}.png'.format(p, sd)
	image = Image.open(f); img = image.load()
	w = image.size[0]
	#seed(TT())
	ax, ay = [], []
	while(len(ax) < m * c):
		x, y = RXY(w)
		if(img[x, y] != (0x0, 0x0, 0x0)):
			ax += [x]; ay += [y]
	image.close()
	NX += tuple(ax); NY += tuple(ay)
	
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

	f = './images/Lp-improved-agnostic-Voronoi-L{0}@{1}.png'.format(p, sd)
	image.save(f, 'PNG'); #image.show()
	## ... sites
	if(sites):
		px = [-1, 0, 1]
		for dx in px:
			for dy in px:
				for i in range(len(NX)):
					img[NX[i] + dx, NY[i] + dy] = (0xff, 0x0, 0x0)
				for i in range(len(ax)):
					img[ax[i] + dx, ay[i] + dy] = (0xff, 0xff, 0xff)
		## ... and the lattice
		#px = [0]
		#for dx in px:
		#	for dy in px:
		#		for i in range(c):
		#			img[nx[i] + dx, ny[i] + dy] = (0xff, 0xff, 0xff)
		f = './images/Lp-improved-agnostic-Voronoi-sites@{0}.png'.format(sd)
		image.save(f, 'PNG')
def lp_agnostic_Voronoi_ps(p = 2, sd = 0x303, improved = False, sites = False, opr = 'abs(a - b)'):
	imp, sts = 'improved-' if improved else '', '-sites' if sites else ''
	
	fa = './images/Lp-{0}agnostic-Voronoi{1}-L{2}@{3}.png'.format(imp, sts, p, sd)
	if(os.path.isfile(fa)):
		fp = './images/Voronoi-L{0}@{1}.png'.format(p, sd)
		fav, fpv = Image.open(fa), Image.open(fp); fdv = Image.new('RGB', fpv.size)
		#ImageMath doesn't process RGB images (yet)...
		fdv = Image.merge('RGB', [ImageMath.eval('convert({0}, "L")'.format(opr), a = ipb, b = iqb) \
								  for (ipb, iqb) in zip(fpv.split(), fav.split())])
		f = './images/Lp-{0}agnostic-Voronoi-math{1}-L{2}@{3}.png'.format(imp, sts, p, sd)
		fdv.save(f, 'PNG')
		fpv.close(); fdv.close()


## Voronoi diagrams and their agnostic versions...
rsd = int(RA(0x12345678))
c, sd = (int(argv[1]), int(argv[2])) if len(argv) == 3 else \
	    (int(argv[1]), rsd) if len(argv) == 2 else (0x10, rsd)
# Lp, with p as a reference and q as an illustration
p, q, w = 2.0, 0.25, 0x100
# The reference diagram for p and just an illustration for q...
NXY, _ = lp_Voronoi_diagram(w, p, c, sd), lp_Voronoi_diagram(w, q, c, sd)
# ... the diagram's Lp-agnostic counterparts w.r.t. p and q
for pq in ((p, q), (q, p)):	lp_agnostic_Voronoi_diagram(*NXY, w, *pq, c, sd)

## ... and (supposedly) their more accurate versions
if(0b1):
	# Make a difference
	lp_agnostic_Voronoi_ps(p, sd); lp_agnostic_Voronoi_ps(q, sd)
	# Compute the improved version for Lp
	lp_improved_agnostic_Voronoi_diagram(*NXY, w, 0x1, c, p, q)
	lp_improved_agnostic_Voronoi_diagram(*NXY, w, 0x1, c, q, p)
	#lp_agnostic_Voronoi_ps(p = p, sd = sd, improved = True)
	#lp_agnostic_Voronoi_ps(p = p, sd = sd, improved = True, sites = True, opr = '(a + 3*b)/4')




## ... a summary and fanfares!
for (p, l) in ((0x1b8, 0x7d), (0x1b8, 0x7d), (0x19f, 0x7d), (0x1b8, 0xfa)): 
	beep(p, l)
print('seed =', rsd)
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

## Random random utilities...
def RRGB(l = 0x0, u = 0xff, s = 0x20): return [RA(l, u, s) for _ in range(3)]
def RBW(l = 0x32, u = 0xd0, s = 0x20): return [RA(l, u, s)] * 0x3 if RA(0x10) else (0xff, 0x0, 0x0) # s = 0x96 for binary B&W diagrams
RRC = RBW if(0x1) else RRGB
def RR(l):  return RA(int(l/0x20), int(0x1f * l/0x20))
def RXY(l): return [RR(l) for _ in range(2)]

## A pivotal yet elementary function...
def distanceLp(x, y, p):
	return pow(pow(abs(x), p) + pow(abs(y), p), 1.0/p)

## Actual stuff...
def lp_Voronoi_diagram(w = 0x100, c = 0x10, p = 2.0, sd = 0x303, show = False):
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
	print('Lp Voronoi diagram: {0}'.format(f))
	return nx, ny
def lp_agnostic_Voronoi_diagram(NX, NY, w = 0x100, c = 0x10, p = 2.0):
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
			dmin = distanceLp(w - 1, w - 1, p); j = -1
			for i in range(c):
				d = distanceLp(nx[i] - x, ny[i] - y, p)
				if d < dmin:
					dmin = d; j = i
			img[x, y] = nr[j], ng[j], nb[j]

	f = './images/Lp-agnostic-Voronoi@{0}.png'.format(sd)
	image.save(f, 'PNG'); #image.show()
	print('Lp agnostic Voronoi diagram: {0}'.format(f))
def lp_improved_agnostic_Voronoi_diagram(NX, NY, w = 0x100, m = 0x1, c = 0x10, p = 2.0, sites = False):
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
			dmin = distanceLp(w - 1, w - 1, p); j = -1
			for i in range(c):
				d = distanceLp(nx[i] - x, ny[i] - y, p)
				if d < dmin:
					dmin = d; j = i
			img[x, y] = nr[j], ng[j], nb[j]

	f = './images/Lp-improved-agnostic-Voronoi@{0}.png'.format(sd)
	image.save(f, 'PNG'); #image.show()
	print('Lp improved agnostic Voronoi diagram: {0}'.format(f))
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
		image.save(f, 'PNG'); #image.show()
		print('Lp improved agnostic Voronoi diagram with sites: {0}'.format(f))
def lp_agnostic_Voronoi_ps(p = 2, sd = 0x303, improved = False, sites = False, opr = 'abs(a - b)'):
	imp, sts = 'improved-' if improved else '', '-sites' if sites else ''
	
	fa = './images/Lp-{0}agnostic-Voronoi{1}@{2}.png'.format(imp, sts, sd)
	if(os.path.isfile(fa)):
		fp = './images/Voronoi-L{0}@{1}.png'.format(p, sd)
		fav, fpv = Image.open(fa), Image.open(fp); fdv = Image.new('RGB', fpv.size)
		#ImageMath doesn't process RGB images (yet)...
		fdv = Image.merge('RGB', [ImageMath.eval('convert({0}, "L")'.format(opr), a = ipb, b = iqb) \
								  for (ipb, iqb) in zip(fpv.split(), fav.split())])
		f = './images/Lp-{0}agnostic-Voronoi-math{1}-L{2}@{3}.png'.format(imp, sts, p, sd)
		fdv.save(f, 'PNG')
		fpv.close(); fdv.close()
		print('Lp agnostic Voronoi math: {0}'.format(f))

## Show time off!
start, rsd = TT(), int(RA(0x12345678))
c, sd = (int(argv[1]), int(argv[2])) if len(argv) == 3 else \
	    (int(argv[1]), rsd) if len(argv) == 2 else (0x10, rsd)
## Lp, with p as a reference and q as an illustration
p, q, w = 2.0, 0.5, 0x100

## The reference diagram for p and just an illustration for q...
NXY, _ = lp_Voronoi_diagram(w = w, c = c, sd = sd, p = p), lp_Voronoi_diagram(w = w, c = c, sd = sd, p = q)
if(0x1): # ... the diagram's Lp-agnostic counterparts
	lp_agnostic_Voronoi_diagram(*NXY, w = w, p = p); lp_agnostic_Voronoi_ps(p = p, sd = sd)
if(0x0): # ... and (supposedly) their more accurate versions
	lp_improved_agnostic_Voronoi_diagram(*NXY, w = w, c = c, p = p, m = 0x1, sites = False)
	lp_agnostic_Voronoi_ps(p = p, sd = sd, improved = True)
	lp_agnostic_Voronoi_ps(p = p, sd = sd, improved = True, sites = True, opr = '(a + 3*b)/4')
## ... a summary and fanfares!
print('Elapsed time = {0}s'.format(round(TT() - start))); 
for (p, l) in ((0x1b8, 0x7d), (0x1b8, 0x7d), (0x19f, 0x7d), (0x1b8, 0xfa)): 
	beep(p, l)
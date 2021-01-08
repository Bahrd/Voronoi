﻿## The Lp agnostic 1-NN algorithm illustration
# 1. Generate N random sites inside a square
# 2. Create the Voronoi's diagram for Lp, 0 < p ≤ 2 (p = 2.0 is somehow distingushed)
# 3. Create a lattice of N(N - 1) sites for the generated N random ones
# 4. Associate the new N(N - 1) sites to the classes accordingly to the diagram for the selected Lp
# 5. Generate o Voronoi diagram for these NxN sites
# 6. Repeat the steps #2-#5 for other Lq, 0 < q ≤ 2 (q = 0.25 is weird enough)

from time import time as TT
from random import randrange as RA, seed
from numpy import arange
from PIL import Image, ImageMath
import os.path

## Random random utilities... [l:u:s]
RRGB = lambda l = 0x0, u = 0x100, s = 0x10: [RA(l, u, s) for _ in range(0x3)]
RBW = lambda l = 0x0, u = 0x100, s = 0x10: [RA(l, u, s)] * 0x3 if RA(0x10) > 1 else (0xff, 0x0, 0x0) # s = 0x96 for binary B&W diagrams
RRC = RBW if(0x1) else RRGB
RR, RXY = lambda l:  RA(int(l/0x20), int(0x1f * l/0x20)), lambda l: [RR(l) for _ in range(2)]

## A pivotal yet elementary function...
distanceLp = lambda x, y, p, w = 1.0: pow(pow(abs(x), p) + w * pow(abs(y), p), 1.0/p) if p > 0.0 else max(abs(x), abs(y))

## A decorative fun... See: https://www.geeksforgeeks.org/decorators-in-python/
def ITT(f):
	def time_warper_wrapper(*args, **kwargs): 
		begin = TT() # from time import time as TT
		r = f(*args, **kwargs) 
		end = TT()
		print('{} evaluated in {}s'.format(f.__name__, round(end - begin)))
		return r
	return time_warper_wrapper
## Actual stuff... 
@ITT
def lp_Voronoi_diagram(w = 0x100, p = 2.0, c = 0x10, sd = 0x303, extensions = ['PNG']):
	seed(sd) # Controlled randomness to get the same points for various p
	image = Image.new("RGB", (w, w))
	
	# Just a standard random case... # Black (, red) & white...

	nxy, nrgb = zip(*[(RXY(w), RRC(0x0, 0x100)) for _ in range(c)])
	nx, ny = zip(*nxy); nr, ng, nb = zip(*nrgb)
	##Drawing...
	img = image.load()
	# ... cells
	for y in range(w):
		for x in range(w):
			s = 2.0 if p == 2.0 else 1.0
			dmin, j = distanceLp(w - 1, w - 1, p, s), -1
			for i in range(c):
				d = distanceLp(nx[i] - x, ny[i] - y, p, s)
				if d < dmin:
					dmin, j = d, i 
			img[x, y] = nr[j], ng[j], nb[j]

	for ext in extensions:
		f = './images/Voronoi-L{}@{}.{}'.format(p, sd, ext)
		image.save(f, ext, dpi = (600, 600))	

	return nx, ny
@ITT
def lp_agnostic_Voronoi_diagram(NX, NY, w = 0x100, p = 2.0, q = 0.25, c = 0x10, sd = 0x303, sites = False, extensions = ['PNG']):
	# Generate N(N-1) additional sites to form an NxN lattice
	# ... and extra sites as well
	c = len(NX); nx, ny = [], c*NY
	for n in range(c):
		nx += c*[NX[n]]		
	c *= len(NY)
	## add at point at random (off-grid x & y and off-grif y):
	#nx, ny = list(nx) + [RA(w)],			list(ny) + [RA(w)]; c += 1			 
	#nx, ny = list(nx) + [NX[RA(len(NX))]], list(ny) + [RA(w)]; c += 1  
	# Set sites' classes from the image
	f = './images/Voronoi-L{}@{}.png'.format(p, sd)
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
			s = 2.0 if q == 2.0 else 1.0
			dmin, j = distanceLp(w - 1, w - 1, q, s), -1
			for i in range(c):
				d = distanceLp(nx[i] - x, ny[i] - y, s, q)
				if d < dmin:
					dmin, j = d, i
			img[x, y] = nr[j], ng[j], nb[j]

	if(sites):
		px = [-1, 0, 1]
		for dx in px:
			for dy in px:
				for i in range(len(NX)):
					img[NX[i] + dx, NY[i] + dy] = (0xff, 0xff, 0x0)
		for i in range(len(nx)):
			img[nx[i], ny[i]] = (0x00, 0xff, 0x00)
	
	for ext in extensions:
		f = './images/Lp-agnostic-Voronoi-L{}L{}@{}.{}'.format(p, q, sd, ext)
		image.save(f, ext, dpi = (72, 72))	

@ITT
def lp_improved_agnostic_Voronoi_diagram(NX, NY, w = 0x100, m = 0x1, c = 0x10, p = 2.0, q = 0.25, sd = 0x303, sites = False):
	## Generate extra sites for extra precision (in locations
	# where the classifications differ for Lp and for agnostic-Lp).
	f = './images/Lp-agnostic-Voronoi-math-L{}@{}.png'.format(p, sd)
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
	f = './images/Voronoi-L{}@{}.png'.format(p, sd)
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
			dmin, j = distanceLp(w - 1, w - 1, q), -1
			for i in range(c):
				d = distanceLp(nx[i] - x, ny[i] - y, q)
				if d < dmin:
					dmin, j = d, i
			img[x, y] = nr[j], ng[j], nb[j]

	f = './images/Lp-improved-agnostic-Voronoi-L{}@{}.png'.format(p, sd)
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
		f = './images/Lp-improved-agnostic-Voronoi-sites@{}.png'.format(sd)
		image.save(f, 'PNG')
def lp_agnostic_Voronoi_ps(p = 2, sd = 0x303, improved = False, sites = False, opr = 'abs(a - b)'):
	imp, sts = 'improved-' if improved else '', '-sites' if sites else ''
	
	fa = './images/Lp-{}agnostic-Voronoi{}-L{}@{}.png'.format(imp, sts, p, sd)
	if(os.path.isfile(fa)):
		fp = './images/Voronoi-L{}@{}.png'.format(p, sd)
		fav, fpv = Image.open(fa), Image.open(fp); fdv = Image.new('RGB', fpv.size)
		#ImageMath doesn't process RGB images (yet)...
		fdv = Image.merge('RGB', [ImageMath.eval('convert({}, "L")'.format(opr), a = ipb, b = iqb) \
								  for (ipb, iqb) in zip(fpv.split(), fav.split())])
		f = './images/Lp-{}agnostic-Voronoi-math{}-L{}@{}.png'.format(imp, sts, p, sd)
		fdv.save(f, 'PNG')
		fpv.close(); fdv.close()

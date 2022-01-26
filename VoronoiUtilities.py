## The Lp agnostic 1-NN algorithm illustration [Project «⅄⅃LY»]
# 1. Generate N random sites inside a square
# 2. Create the Voronoi's diagram for Lp, 0 < p ≤ 2 (p = 2.0 is somehow distingushed)
# 3. Create a lattice of N(N - 1) sites for the generated N random ones
# 4. Associate the new N(N - 1) sites to the classes accordingly to the diagram for the selected Lp
# 5. Generate o Voronoi diagram for these NxN sites (effectively, an NxN Hanan grid)
# 6. Repeat the steps #2-#5 for other Lq, 0 < q ≤ 2 (q = 0.25 seems counterintuitive enough)

from time import time as TT
from random import randrange as RA, seed
from numpy import arange
from PIL import Image, ImageMath
from os.path import isfile

## Random random utilities...
RRGB = lambda l = 0x0, u = 0xff, s = 0x20: [RA(l, u, s) for _ in range(0x3)]
RBW = lambda l = 0x32, u = 0xd0, s = 0x20: [RA(l, u, s)] * 0x3 if RA(0x10) > 1 else (0xff, 0x0, 0x0) # s = 0x96 for binary B&W diagrams and s = 0x20 for others 
#RBW = lambda l = 0x32, u = 0xd0, s = 0x96: [RA(l, u, s)] * 0x3 #if RA(0x10) > 1 else (0xff, 0x0, 0x0) # s = 0x96 for binary B&W diagrams and s = 0x20 for others 
RRC = RBW if(0x1) else RRGB                                    # ^red patches^
RR, RXY = lambda l:  RA(int(l/0x20), int(0x1f * l/0x20)), lambda l: [RR(l) for _ in range(2)]

## A pivotal yet elementary function...
distanceLp = lambda x, y, p: pow(pow(abs(x), p) + pow(abs(y), p), 1.0/p) if p > 0.0 else max(abs(x), abs(y))

## A decorative fun... See: https://www.geeksforgeeks.org/decorators-in-python/
def ITT(f):
	def time_warper_wrapper(*args, **kwargs): 
		begin = TT() # from time import time as TT
		r = f(*args, **kwargs) 
		end = TT()
		print('{0} evaluated in {1}s'.format(f.__name__, round(end - begin)))
		return r
	return time_warper_wrapper

## A diagram with planted on a Hanan grid pattern seeds
## ...
@ITT
def lp_planted_Voronoi_diagram(sd, w = 0x100, p = 2.0, Hanan = False, sites = True):
	seed(sd) # Controlled randomness to get a better picture of the phenomenon
	         # ♫ Choking on the bad, bad, bad, bad, bad, bad seed ♫
	image = Image.new("RGB", (w, w))
	# Fixed (action?) patterns
	#patterns = [[0x60, 0x60, 0xb0, 0xb0, 0xb0], [0x60, 0xb0, 0x64, 0x60, 0xb0], 
	#            [0xff, 0xff, 0, 0x80, 0], [0, 0xff, 0, 0x80, 0], [0, 0xff, 0, 0x80, 0]]
	# Random Hanan grid with a new non-grid pattern
	stp = [RA(0x10, w - 0x10), RA(0x10, w - 0x10)]
	patterns = [[stp[0], stp[0], stp[1], stp[1], stp[1] if Hanan else RA(w)], [stp[1], stp[0], stp[1], stp[0], stp[1]], 
				[0xff, 0xf0, 0, 0x80, 0], [0, 0xf0, 0, 0x80, 0], [0, 0xf0, 0, 0x80, 0]]
	nx, ny, nr, ng, nb = patterns
	c = len(patterns[0])
	##Drawing...
	img = image.load()
	# ... cells
	for y in range(w):
		for x in range(w):
			dmin, j = distanceLp(w - 1, w - 1, p), -1
			for i in range(c):
				d = distanceLp(nx[i] - x, ny[i] - y, p)
				if d < dmin:
					dmin, j = d, i 
			img[x, y] = nr[j], ng[j], nb[j]
	if(not sites):
		f = './images/Voronoi-planted-L{0}@{1}.png'.format(p, sd)
		image.save(f, 'PNG')

	## ... sites
	if(sites):
		px = [-2, -1, 0, 1, 2]
		for dx in px:
			for dy in px:
				for i in range(len(nx)):
					img[nx[i] + dx, ny[i] + dy] = (0xff, 0xff, 0x0)
		f = './images/Voronoi-planted-sites-L{0}@{1}.png'.format(p, sd)
		image.save(f, 'PNG')
	return nx, ny

## Actual stuff... 
@ITT
def lp_Voronoi_diagram(w = 0x100, p = 2.0, c = 0x10, sd = 0x303, sites = False):
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
			dmin, j = distanceLp(w - 1, w - 1, p), -1
			for i in range(c):
				d = distanceLp(nx[i] - x, ny[i] - y, p)
				if d < dmin:
					dmin, j = d, i 
			img[x, y] = nr[j], ng[j], nb[j]

	f = './images/Voronoi-L{0}@{1}'.format(p, sd)
	image.save(f + '.png', 'PNG')
	image.save(f + '.pdf', 'PDF')

	## ... sites
	if(sites):
		px = [-2, -1, 0, 1, 2]
		for dx in px:
			for dy in px:
				for i in range(len(nx)):
					img[nx[i] + dx, ny[i] + dy] = (0xff, 0xff, 0x0)
		f = './images/Voronoi-sites-L{0}@{1}'.format(p, sd)
		image.save(f + '.png', 'PNG')
		image.save(f + '.pdf', 'PDF')
	return nx, ny
@ITT
def lp_agnostic_Voronoi_diagram(NX, NY, w = 0x100, p = 2.0, q = 0.25, c = 0x10, sd = 0x303):
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
			dmin, j = distanceLp(w - 1, w - 1, q), -1
			for i in range(c):
				d = distanceLp(nx[i] - x, ny[i] - y, q)
				if d < dmin:
					dmin, j = d, i
			img[x, y] = nr[j], ng[j], nb[j]

	f = './images/Lp-agnostic-Voronoi-L{0}@{1}'.format(p, sd)
	image.save(f + '.png', 'PNG')
	image.save(f + '.pdf', 'PDF')
	if(1):
		if(1):
			px = [-1, 0, 1]
			for dx in px:
				for dy in px:
					for i in range(c):
						img[nx[i] + dx, ny[i] + dy] = (0xff, 0xff, 0xff)
		px = [-2, -1, 0, 1, 2]
		for dx in px:
			for dy in px:
				for i in range(len(NX)):
					img[NX[i] + dx, NY[i] + dy] = (0xff, 0xff, 0x0)
				#for i in range(len(ax)):
				#	img[ax[i] + dx, ay[i] + dy] = (0xff, 0x00, 0x00) ## ALLY (0xff, 0xff, 0x00)
	f = './images/Lp-agnostic-Voronoi-sites-L{0}@{1}.pdf'.format(p, sd)
	image.save(f, 'pdf')

@ITT
def lp_improved_agnostic_Voronoi_diagram(NX, NY, w = 0x100, m = 0x1, c = 0x10, p = 2.0, q = 0.25, sd = 0x303, sites = False, lattice = False):

	## Generate extra sites for extra precision (in locations
	# where the classifications differ for Lp and for agnostic-Lp).
##ALLY
	f = './images/Agnostic-Voronoi-math-L{}@{}.png'.format(p, sd)
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
##ALLY
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
			dmin, j = distanceLp(w - 1, w - 1, q), -1
			for i in range(c):
				d = distanceLp(nx[i] - x, ny[i] - y, q)
				if d < dmin:
					dmin, j = d, i
			img[x, y] = nr[j], ng[j], nb[j]

	f = './images/Lp-improved-agnostic-Voronoi-L{0}@{1}'.format(p, sd)
	image.save(f + '.png', 'PNG')
	image.save(f + '.pdf', 'PDF')
	## ... sites
	if(sites):
		if(lattice):
			px = [-1, 0, 1]
			for dx in px:
				for dy in px:
					for i in range(c):
						img[nx[i] + dx, ny[i] + dy] = (0xff, 0xff, 0xff)
		px = [-2, -1, 0, 1, 2]
		for dx in px:
			for dy in px:
				for i in range(len(NX)):
					img[NX[i] + dx, NY[i] + dy] = (0xff, 0xff, 0x0)
		px = [-3, -2, -1, 0, 1, 2, 3]
		for dx in px:
			for dy in px:
				for i in range(len(ax)):
					img[ax[i] + dx, ay[i] + dy] = (0xff, 0x00, 0x00) 
		## ... and the lattice
		f = './images/Lp-improved-agnostic-Voronoi-sites@{0}.{1}'.format(sd, 'png')
		image.save(f, 'PNG')
		f = './images/Lp-improved-agnostic-Voronoi-sites@{0}.{1}'.format(sd, 'pdf')
		image.save(f, 'PDF')


## Pre-release version
def lp_agnostic_Voronoi_ps(p = 2, sd = 0x303, improved = False, sites = False, opr = 'abs(a - b)'):
	fa = './images/Lp-{}agnostic-Voronoi-L{}@{}.png'.format('improved-' if improved else '', p, sd)
	if(isfile(fa)):
		fp = './images/Voronoi-L{}@{}.png'.format(p, sd)
		fav, fpv = Image.open(fa), Image.open(fp); fdv = Image.new('RGB', fpv.size)
		#ImageMath doesn't process RGB images (yet)...
		fdv = Image.merge('RGB', [ImageMath.eval('convert({0}, "L")'.format(opr), a = ipb, b = iqb) \
								  for (ipb, iqb) in zip(fpv.split(), fav.split())])
		f = './images/Agnostic-{}Voronoi-math-L{}@{}.png'.format('improved-' if improved else '', p, sd)
		fdv.save(f, 'PNG')
		f = './images/Agnostic-{}Voronoi-math-L{}@{}.pdf'.format('improved-' if improved else '', p, sd)
		fdv.save(f, 'PDF')
		fpv.close(); fdv.close()
	else:
		print('File: [{}] not found!'.format(fa))

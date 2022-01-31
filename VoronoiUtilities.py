## The Lp agnostic 1-NN algorithm illustration [Project «⅄⅃LY»]
# 1. Generate N random patterns inside a square
# 2. Create the Voronoi's diagram for Lp, 0 < p ≤ 2 (p = 2.0 is somehow distingushed)
# 3. Complement N patterns with a lattice of N × (N - 1) patterns to get a Hanan grid
# 4. Associate the new N × (N - 1) patterns to the classes w.r.t. the selected Lp
# 5. Generate o Voronoi diagram for these N × N patterns (effectively, for the N × N Hanan grid)
# 6. Repeat the steps #2-#5 for other Lq, 0 < q ≤ 2 (q = 0.25 seems unpredictable enough)

from time import time as TT
from random import randrange as RA, seed
from numpy import arange
from math import sqrt, inf
from PIL import Image, ImageMath
from os.path import isfile

## Colors...
c_red, c_green, c_blue, c_yellow, c_black, c_gray, c_white = ((0xff, 0, 0), (0, 0xff, 0), (0, 0, 0xff), (0xff, 0xff, 0),
															  (0, 0, 0), (0x80, 0x80, 0x80), (0xff, 0xff, 0xff))

## Random random utilities... (s = 0x96 for binary B&W diagrams and s = 0x20 for others)
RRGB = lambda l = 0x0, u = 0xff, s = 0x20: [RA(l, u, s) for _ in range(0x3)]
RBW = lambda l = 0x32, u = 0xd0, s = 0x20: [RA(l, u, s)] * 0x3 if RA(0x10) > 1 else c_red 
RRC = RBW if(0x1) else RRGB                                    # ^red patches^
RR, RXY = lambda l:  RA(int(l/0x20), int(0x1f * l/0x20)), lambda l: [RR(l) for _ in range(2)]

## ... and an lp-distance function implementation... See: https://www.geeksforgeeks.org/python-infinity/
dictum_acerbum = {	0.0: lambda x, y: int(x != 0.0) + int(y != 0.0),		# p == 0.0, the Hamming distance
					0.5: lambda x, y: (sqrt(abs(x)) + sqrt(abs(y)))**2.0,	# p == 0.5, hand-crafted optimization
					1.0: lambda x, y: abs(x) + abs(y),						# p == 1.0, the taxi-cab metric (Manhattan distance) 
					2.0: lambda x, y: sqrt(x**2.0 + y**2.0),				# p == 2.0, the good ol' Euclid
					inf: lambda x, y: max(abs(x), abs(y))}					# p ==  ∞,  the max metric
def lp_length(x, y, p): 
	try:				return dictum_acerbum[p](x, y)						# kinda branch-less programming ;)
	except KeyError:	return pow(pow(abs(x), p) + pow(abs(y), p), 1.0/p)	

## ... with a decorative fun... See: https://www.geeksforgeeks.org/decorators-in-python/
def ITT(f):
	def time_warper_wrapper(*args, **kwargs): 
		begin = TT() # from time import time as TT
		r = f(*args, **kwargs) 
		end = TT()
		print('{0} evaluated in {1}s'.format(f.__name__, round(end - begin)))
		return r
	return time_warper_wrapper

### 2D diagram generators (based on https://rosettacode.org/wiki/Voronoi_diagram#Python)
##  A diagram of seeds (patterns) planted on a Hanan grid
@ITT
def lp_planted_Voronoi_diagram(sd, w = 0x100, p = 2.0, Hanan = False, sites = True):
	seed(sd) # Controlled randomness to get a better picture of the phenomenon
	         # ♫ Choking on the bad, bad, bad, bad, bad, bad seed! ♫
	image = Image.new("RGB", (w, w))
	pp = [RA(0x10, w - 0x10), RA(0x10, w - 0x10)]
	# ♫ We're gonna have to reap from some seed that's been sowed... ♫
	planted_pattern =  [[pp[0], pp[0]], [pp[0], pp[1]], [pp[1], pp[0]], [pp[1], pp[1]]] # on-grid patterns
	planted_pattern += [[pp[1], pp[0] if Hanan else RA(w)]]								# a random pattern
	colors = [c_black, c_white, c_gray, c_red, c_red]

	(nx, ny), (nr, ng, nb) = zip(*planted_pattern), zip(*colors)
	##Drawing...
	img = image.load()
	# ... cells
	c = len(colors)
	for y in range(w):
		for x in range(w):
			dmin, j = lp_length(w - 1, w - 1, p), -1
			for i in range(c):
				d = lp_length(nx[i] - x, ny[i] - y, p)
				if d < dmin:
					dmin, j = d, i 
			img[x, y] = nr[j], ng[j], nb[j]
	if(not sites):
		f = './images/Voronoi-planted-L{0}@{1}'.format(p, sd)
		image.save(f + '.png', 'PNG'); image.save(f + '.pdf', 'PDF')

	## ... sites
	if(sites):
		px = [-2, -1, 0, 1, 2]
		for dx in px:
			for dy in px:
				for i in range(len(nx)):
					img[nx[i] + dx, ny[i] + dy] = c_yellow
		f = './images/Voronoi-planted-sites-L{0}@{1}'.format(p, sd)
		image.save(f + '.png', 'PNG'); image.save(f + '.pdf', 'PDF')
	return nx, ny

## Working stuff... 
@ITT
def lp_Voronoi_diagram(w = 0x100, p = 2.0, c = 0x10, sd = 0x303, sites = False):
	seed(sd) # Controlled randomness to get the same points for various p
	image = Image.new("RGB", (w, w))
	
	# Just a standard random case... # Black (, red) & white...

	nxy, nrgb = zip(*[(RXY(w), RRC(0x0, 0x100)) for _ in range(c)])
	(nx, ny), (nr, ng, nb) = zip(*nxy), zip(*nrgb)
	##Drawing...
	img = image.load()
	# ... cells
	for y in range(w):
		for x in range(w):
			dmin, j = lp_length(w - 1, w - 1, p), -1
			for i in range(c):
				d = lp_length(nx[i] - x, ny[i] - y, p)
				if d < dmin:
					dmin, j = d, i 
			img[x, y] = nr[j], ng[j], nb[j]

	f = './images/Voronoi-L{0}@{1}'.format(p, sd)
	image.save(f + '.png', 'PNG'); image.save(f + '.pdf', 'PDF')

	## ... sites
	if(sites):
		px = [-2, -1, 0, 1, 2]
		for dx in px:
			for dy in px:
				for i in range(len(nx)):
					img[nx[i] + dx, ny[i] + dy] = c_yellow
		f = './images/Voronoi-sites-L{0}@{1}'.format(p, sd)
		image.save(f + '.png', 'PNG'); image.save(f + '.pdf', 'PDF')
	return nx, ny

@ITT
def lp_agnostic_Voronoi_diagram(NX, NY, w = 0x100, p = 2.0, q = 0.25, c = 0x10, sd = 0x303):
	# Generate N × (N-1) additional patterns to form an N × N lattice (Hanan grid)
	# ... and extra patterns as well
	c = len(NX); nx, ny = [], c*NY
	for n in range(c):
		nx += c*[NX[n]]		
	c *= len(NY);

	# Set pattern's classes from the image
	f = './images/Voronoi-L{0}@{1}'.format(p, sd)
	image = Image.open(f + '.png'); img = image.load()
	w = image.size[0]
	nr, ng, nb = zip(*[img[nx[j], ny[j]] for j in range(c)])
	image.close()
	
	## Drawing...
	image = Image.new("RGB", (w, w))
	img = image.load()
	# ... cells
	for y in range(w):
		for x in range(w):
			dmin, j = lp_length(w - 1, w - 1, q), -1
			for i in range(c):
				d = lp_length(nx[i] - x, ny[i] - y, q)
				if d < dmin:
					dmin, j = d, i
			img[x, y] = nr[j], ng[j], nb[j]

	f = './images/Lp-agnostic-Voronoi-L{0}@{1}'.format(p, sd)
	image.save(f + '.png', 'PNG'); image.save(f + '.pdf', 'PDF')
	if(1):
		if(1):
			px = [-1, 0, 1]
			for dx in px:
				for dy in px:
					for i in range(c):
						img[nx[i] + dx, ny[i] + dy] = c_white
		px = [-2, -1, 0, 1, 2]
		for dx in px:
			for dy in px:
				for i in range(len(NX)):
					img[NX[i] + dx, NY[i] + dy] = c_yellow
	f = './images/Lp-agnostic-Voronoi-sites-L{0}@{1}'.format(p, sd)
	image.save(f + '.png', 'png'); image.save(f + '.pdf', 'pdf')

@ITT
def lp_improved_agnostic_Voronoi_diagram(NX, NY, w = 0x100, m = 0x1, c = 0x10, p = 2.0, q = 0.25, sd = 0x303, sites = False, lattice = False):

	## Generate extra patterns for extra precision (in locations
	#   where the classifications differ for Lp and for agnostic-Lp).
##ALLY
	f = './images/agnostic-Voronoi-math-L{}@{}'.format(p, sd)
	image = Image.open(f + '.png'); img = image.load()
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
	# Generate N × (N-1) additional patterns to form an N × N lattice (Hanan grid)
	# ... and some extra patterns as well
	c = len(NX); nx, ny = [], c*NY
	for n in range(c):
		nx += c*[NX[n]]		
	c *= len(NY);

	# Set pattern's classes from the image
	f = './images/Voronoi-L{0}@{1}'.format(p, sd)
	image = Image.open(f + '.png'); img = image.load()
	w = image.size[0]
	nr, ng, nb = zip(*[img[nx[j], ny[j]] for j in range(c)])
	image.close()
	
	## Drawing...
	image = Image.new("RGB", (w, w))
	img = image.load()
	# ... cells
	for y in range(w):
		for x in range(w):
			dmin, j = lp_length(w - 1, w - 1, q), -1
			for i in range(c):
				d = lp_length(nx[i] - x, ny[i] - y, q)
				if d < dmin:
					dmin, j = d, i
			img[x, y] = nr[j], ng[j], nb[j]

	f = './images/Lp-improved-agnostic-Voronoi-L{0}@{1}'.format(p, sd)
	image.save(f + '.png', 'PNG'); image.save(f + '.pdf', 'PDF')
	## ... sites
	if(sites):
		if(lattice):
			px = [-1, 0, 1]
			for dx in px:
				for dy in px:
					for i in range(c):
						img[nx[i] + dx, ny[i] + dy] = c_white
		px = [-2, -1, 0, 1, 2]
		for dx in px:
			for dy in px:
				for i in range(len(NX)):
					img[NX[i] + dx, NY[i] + dy] = c_yellow
		px = [-3, -2, -1, 0, 1, 2, 3]
		for dx in px:
			for dy in px:
				for i in range(len(ax)):
					img[ax[i] + dx, ay[i] + dy] = c_red
		## ... and the lattice
		f = './images/Lp-improved-agnostic-Voronoi-sites@{}'.format(sd)
		image.save(f + '.png', 'PNG'); image.save(f + '.pdf', 'PDF')

## Perform an 'opr' on diagrams (a difference in particular, when opr = 'abs(a - b)'
def lp_agnostic_Voronoi_ps(p = 2, sd = 0x303, improved = False, sites = False, opr = 'abs(a - b)'):
	fa = './images/Lp-{}agnostic-Voronoi-L{}@{}.png'.format('improved-' if improved else '', p, sd)
	if(isfile(fa)):
		fp = './images/Voronoi-L{}@{}.png'.format(p, sd)
		fav, fpv = Image.open(fa), Image.open(fp); fdv = Image.new('RGB', fpv.size)
		#ImageMath doesn't process RGB images (at the time of writing this code)...
		fdv = Image.merge('RGB', [ImageMath.eval('convert({0}, "L")'.format(opr), a = ipb, b = iqb) \
								  for (ipb, iqb) in zip(fpv.split(), fav.split())])
		f = './images/agnostic-{}Voronoi-math-L{}@{}'.format('improved-' if improved else '', p, sd)
		fdv.save(f + '.png', 'PNG'); fdv.save(f + '.pdf', 'PDF')
	else:
		print('File: [{}] not found!'.format(fa))
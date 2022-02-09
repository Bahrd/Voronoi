## The Lp agnostic 1-NN algorithm illustration [Project «⅄⅃LY»]
# 1. Generate N random patterns inside a square
# 2. Create the Voronoi's diagram for Lp, 0 < p ≤ 2 (p = 2.0 is somehow distingushed)
# 3. Compute an N × N Cartesian product of pattern's coordinates to get a Hanan grid
# 4. Associate the new N × (N - 1) patterns to the classes w.r.t. the selected Lp
# 5. Generate o Voronoi diagram for these N × N patterns (effectively, for the N × N Hanan grid)
# 6. Repeat the steps #2-#5 for other Lq, 0 < q ≤ 2 (q = 0.25 seems unpredictable enough)

from time import time as TT
from random import randrange as RA, seed
from numpy import arange
from itertools import product
from math import sqrt, inf
from PIL import Image, ImageMath
from os.path import isfile

## Colors united...
c_red, c_green, c_blue, c_yellow, c_black, c_gray, c_whitish, c_white = ((0xff, 0, 0), (0, 0xff, 0), 
																		 (0, 0, 0xff), (0xff, 0xff, 0),
																		 (0, 0, 0), (0x80, 0x80, 0x80), 
																		 (0xdd, 0xdd, 0xdd), (0xff, 0xff, 0xff))
## Random random utilities... (s = 0x96 for binary B&W diagrams and s = 0x20 for others)
RRGB = lambda l = 0x0, u = 0xff, s = 0x20: [RA(l, u, s) for _ in range(0x3)]
RBW = lambda l = 0x32, u = 0xd0, s = 0x20: [RA(l, u, s)] * 0x3 if RA(0x10) > 1 else c_red 
RRC = RBW if(0x1) else RRGB                                    # ^red patches^
RR, RXY = lambda l:  RA(int(l/0x20), int(0x1f * l/0x20)), lambda l: [RR(l) for _ in range(2)]

## ... and an lp-distance function implementation... See: https://www.geeksforgeeks.org/python-infinity/
#  (waiting for pattern matching in Python...)
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
		print('{} created [in {}s]'.format(f.__name__, round(end - begin)))
		return r
	return time_warper_wrapper

## Let's Cartesian'em all!
def paint_patterns(img, nxy, px, color):
	for nx, ny in nxy:
		for dx, dy in product(px, px):
			img[nx + dx, ny + dy] = color

def classify_NN(w, p, img, nxy, colors):
	for x, y in product(range(w), range(w)):
		dmin, j = lp_length(w - 1, w - 1, p), -1
		for i, (nx, ny) in enumerate(nxy):
			d = lp_length(nx - x, ny - y, p)
			if d < dmin: 
				dmin, j = d, i
		img[x, y] = tuple(colors[j])

### 2D Voronoi diagram generators (based on https://rosettacode.org/wiki/Voronoi_diagram#Python)
##  A diagram of seeds (patterns) planted on a Hanan grid
@ITT
def lp_planted_Voronoi_diagram(sd, w = 0x100, p = 2.0, Hanan = False, sites = True):
	seed(sd) # Controlled randomness to get a better picture of the phenomenon
	         # ♫♪ Choking on the bad, bad, bad, bad, bad, bad seed! ♪♫
	image = Image.new("RGB", (w, w))
	pp = [RA(0x10, w - 0x10), RA(0x10, w - 0x10)]
	# ♫♪ We're gonna have to reap from some seed that's been sowed... ♪♫
	planted =  list(product(pp, pp))				# on-grid patterns
	planted += [[pp[1], pp[0] if Hanan else RA(w)]]	# a random pattern
	colors = [c_red, c_whitish, c_gray, c_black, c_black]

	img = image.load()
	## Filling cells (i.e. performing classification)
	classify_NN(w, p, img, planted, colors)
	## ... and sites
	if(sites):
		paint_patterns(img, planted, [-2, -1, 0, 1, 2], c_yellow)
		f = './images/Voronoi-planted-sites-L{}@{}'.format(p, sd)
		image.save(f + '.png', 'PNG'); image.save(f + '.pdf', 'PDF')
	# ... or no sites...
	else:
		f = './images/Voronoi-planted-L{}@{}'.format(p, sd)
		image.save(f + '.png', 'PNG'); image.save(f + '.pdf', 'PDF')
	return planted

## Actual working stuff... 
@ITT
def lp_Voronoi_diagram(w = 0x100, p = 2.0, c = 0x10, sd = 0x303, sites = False):
	seed(sd) # Controlled randomness that yields the same pseudo-random patterns for various p
			 # Just a standard random case... # Black (, red) & white(-ish)...
	nxy, nrgb = zip(*((RXY(w), RRC(0x0, 0x100)) for _ in range(c)))
	
	## Drawing... (i.e. classifying w.r.t. the set Sn)
	image = Image.new("RGB", (w, w)); img = image.load()
	# ... cells
	classify_NN(w, p, img, nxy, nrgb)

	f = './images/Voronoi-L{}@{}'.format(p, sd)
	image.save(f + '.png', 'PNG'); image.save(f + '.pdf', 'PDF')

	## ... sites
	if(sites):
		paint_patterns(img, nxy, [-2, -1, 0, 1, 2], c_yellow)
		f = './images/Voronoi-sites-L{}@{}'.format(p, sd)
		image.save(f + '.png', 'PNG'); image.save(f + '.pdf', 'PDF')
	return zip(*nxy)
@ITT
def lp_agnostic_Voronoi_diagram(NX, NY, p = 2.0, q = 0.25, c = 0x10, sd = 0x303):
	## Essentially, given N points, we 'yield' a Cartesian product of two vectors 
	# of N elements being their first and second coordinates, respectively
	f = './images/Voronoi-L{}@{}'.format(p, sd)
	image = Image.open(f + '.png')
	img, (w, _) = image.load(), image.size
	nrgb = [img[nx, ny] for nx, ny in product(NX, NY)]
	image.close()

	## Drawing... (i.e. classifying w.r.t. the set An)
	image = Image.new("RGB", (w, w))
	img = image.load()
	# ... cells
	classify_NN(w, p, img, list(product(NX, NY)), nrgb)

	f = './images/Lp-agnostic-Voronoi-L{}@{}'.format(p, sd)
	image.save(f + '.png', 'PNG'); image.save(f + '.pdf', 'PDF')

	paint_patterns(img, product(NX, NY), [-1, 0, 1], c_white)
	paint_patterns(img, zip(NX, NY), [-2, -1, 0, 1, 2], c_yellow)
	f = './images/Lp-agnostic-Voronoi-sites-L{}@{}'.format(p, sd)
	image.save(f + '.png', 'png'); image.save(f + '.pdf', 'pdf')
@ITT
def lp_improved_agnostic_Voronoi_diagram(NX, NY, m = 0x1, c = 0x10, p = 2.0, q = 0.25, sd = 0x303, sites = False, lattice = False):
	## Generate extra patterns for extra precision (in locations
	#   where the classifiers differ for Lp and for agnostic-Lp).
	## ⅄⅃LY 
	f = './images/agnostic-Voronoi-math-L{}@{}'.format(p, sd)
	image = Image.open(f + '.png'); img = image.load()
	w, _  = image.size
	ax, ay = [], []
	while(len(ax) < m * c):
		x, y = RXY(w)
		if(img[x, y] != (0x0, 0x0, 0x0)): ax += [x]; ay += [y]
	image.close()
	NX += tuple(ax); NY += tuple(ay)

	# Set pattern's classes from the image
	f = './images/Voronoi-L{}@{}'.format(p, sd)
	image = Image.open(f + '.png'); img = image.load()
	nrgb = [img[nx, ny] for nx, ny in product(NX, NY)]
	image.close()
	
	## Filling... (i.e. classifying w.r.t. the set An+l)
	image = Image.new("RGB", (w, w))
	img = image.load()
	# ... cells
	classify_NN(w, p, img, list(product(NX, NY)), nrgb)

	f = './images/Lp-improved-agnostic-Voronoi-L{}@{}'.format(p, sd)
	image.save(f + '.png', 'PNG'); image.save(f + '.pdf', 'PDF')
	## ... sites
	if(sites):
		if(lattice): paint_patterns(img, product(NX, NY), [-1, 0, 1], c_white)
		paint_patterns(img, zip(NX, NY), [-2, -1, 0, 1, 2], c_yellow)
		paint_patterns(img, zip(ax, ay), [-3, -2, -1, 0, 1, 2, 3], c_red)
		
		f = './images/Lp-improved-agnostic-Voronoi-sites@{}'.format(sd)
		image.save(f + '.png', 'PNG'); image.save(f + '.pdf', 'PDF')

## Perform an 'opr' on diagrams (a difference in particular, when opr = 'abs(a - b)'
def lp_agnostic_Voronoi_ps(p = 2, sd = 0x303, improved = False, sites = False, opr = 'abs(a - b)'):
	fa = './images/Lp-{}agnostic-Voronoi-L{}@{}.png'.format('improved-' if improved else '', p, sd)
	if(isfile(fa)):
		fp = './images/Voronoi-L{}@{}.png'.format(p, sd)
		fav, fpv = Image.open(fa), Image.open(fp); fdv = Image.new('RGB', fpv.size)
		#ImageMath doesn't process RGB images (at the time of writing this code)...
		fdv = Image.merge('RGB', [ImageMath.eval('convert({}, "L")'.format(opr), a = ipb, b = iqb) \
								  for (ipb, iqb) in zip(fpv.split(), fav.split())])
		f = './images/agnostic-{}Voronoi-math-L{}@{}'.format('improved-' if improved else '', p, sd)
		fdv.save(f + '.png', 'PNG'); fdv.save(f + '.pdf', 'PDF')
	else:
		print('File: [{}] not found!'.format(fa))
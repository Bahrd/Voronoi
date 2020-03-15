## https://rosettacode.org/wiki/Voronoi_diagram#Python

from PIL import Image
from random import randrange as RR, seed
from sys import argv
from numpy import arange

weird = True#False#

def RA(l = 50, u = 201, s = 150): return 3 * [RR(l, u, s)]

def distance(x, y, p):
	return pow(pow(abs(x), p) + pow(abs(y), p), 1.0/p) if (p > 0.0) else max(abs(x), abs(y)) # special case 'lmax'

def generate_voronoi_diagram(w = 0x100, h = 0x100, c = 0x8, p = 2.0, sd = 0x29):
	seed(sd) # Controlled randomness to get the same points for various p
	image = Image.new("RGB", (w, h))
	
	# Just a standard random case...
	if(weird):
		nx, ny = zip(*[[RR(6*w/8) + w/8, RR(6*h/8) + h/8] for _ in range(c)])
	else:
		# ... and N random points and N(N-1) additional ones that form a grid
		NX, NY = zip(*[[RR(6*w/8) + w/8, RR(6*h/8) + h/8] for _ in range(c)])
		nx, ny = [], c*NY
		for n in range(c):
			nx += c*[NX[n]]		
		c *= c;

	# Black & white...
	nr, ng, nb = zip(*[RA(0, 255) for _ in range(c)])	

	# A standard, colorful 
	#random_field = [[RB(w/2) + w/4, RB(h/2) + h/4, *RA(0,255)] for _ in range(c)]
	#nx, ny, nr, ng, nb = zip(*random_field) # transposition
	
	##Drawing...
	img = image.load()
	# ... cells
	for y in range(h):
		for x in range(w):
			dmin = distance(w - 1, h - 1, p); j = -1
			for i in range(c):
				d = distance(nx[i] - x, ny[i] - y, p)
				if d < dmin:
					dmin = d; j = i
			img[x, y] = nr[j], ng[j], nb[j]
	# ... and sites
	px = (-3, -2, -1, 1, 2, 3)
	for dx in px:
		for dy in px:
			for i in range(c):
				img[nx[i] + dx, ny[i] + dy] = 0xff, 0, 0

	f = "./images/Voronoi-L{0}.png".format(p if p > 0.0 else 'max')
	image.save(f, 'PNG'); image.show()
	print("Voronoi's diagram saved to: {0}".format(f))

## Start the show off!
# Lp distances (from the command line arguments if they exist)
# Any value p <= 0.0 yields an 'lmax' metric-based diagram
# For example 'python ./Voronoi.py 2 0 -.5' draws diagrams for l2, l1.5, l1.0, l0.5 and lmax

sd = RR(0x1000) #947 #505
print(sd)
[start, stop, step], c = ([float(p) for p in (argv[1:4])], int(argv[4])) if (len(argv) == 5) \
						 else [0.5, 2.0, 1.5], 8

for p in arange(start, stop, step if step != 0.0 else 1.0):
	generate_voronoi_diagram(p = round(p, 2), sd = sd, c = c)
generate_voronoi_diagram(p = round(stop, 2), sd = sd, c = c) # Diagrams for a stop value
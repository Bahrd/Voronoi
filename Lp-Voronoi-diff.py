from PIL import Image, ImageMath
from random import randrange as RR, seed
from sys import argv
from numpy import arange

# 0..255 - a default RGB range # 0..1 - for B&W

def RA(l = 50, u = 201, s = 150): 
	rr = RR(l, u, s) 
	return 3*[rr]

p, q = (float(argv[1]), float(argv[2])) if len(argv) < 3 else (2.0, 0.5)
f = './images/Voronoi-L{0}.png'
ip, iq = (Image.open(f.format(l)) for l in (p, q))
i = Image.new('RGB', ip.size)
#ImageMath doesn't process RGB images (yet)...
i = Image.merge('RGB', [ImageMath.eval('convert(abs(a - b), "L")', a = ipb, b = iqb) \
                        for (ipb, iqb) in zip(ip.split(), iq.split())])

#restoring sites 
if len(argv) == 5:
	c = int(argv[3]); seed(int(argv[4]))
	w, h = i.size
	nx, ny = zip(*[[RR(6*w/8) + w/8, RR(6*h/8) + h/8] for _ in range(c)])
	img = i.load()
	px = [-1, 0, 1]
	for dx in px:
		for dy in px:
			for ic in range(c):
				img[nx[ic] + dx, ny[ic] + dy] = 0xff, 0, 0

i.show(); i.save('./images/Voronoi-L{0}-{1}.png'.format(p, q), 'PNG')
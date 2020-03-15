from PIL import Image, ImageMath
from sys import argv

fp = argv[1]
fa = argv[2]
opr = 'convert({0}, "L")'.format(argv[3])
fpv = Image.open(fp)
fav = Image.open(fa)

fdv = Image.new('RGB', fpv.size)
fdv = Image.merge('RGB', [ImageMath.eval(opr, a = ipb, b = iqb) \
		                    for (ipb, iqb) in zip(fpv.split(), fav.split())])
fdv.show(); fdv.save('./images/diff.png', 'PNG')
fpv.close(); fav.close(); fdv.close()

#PS C:\Users\Przem\source\repos\Bahrd\AppliedPythonology> 
#   python .\img-diff.py .\images\Lp-improved-agnostic-Voronoi-math-L2.0@36351.png .\images\Lp-agnostic-Voronoi-math-L2.0@36351.png "(a + 3*b)/4"
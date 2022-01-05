'''
https://pypi.org/project/fastDamerauLevenshtein/
SYNTAX:
python .\Damerau-Levenshtein-distance.py ALLY ⅄⅃LY 
> d(ALLY, ⅄⅃LY) = 2.0
'''
from fastDamerauLevenshtein import damerauLevenshtein as ddl
from sys import argv

(α, β), λ = (argv[1], argv[2]), lambda α, β: ddl(α, β, similarity = False)
print(f'd({α}, {β}) = {λ(α, β)}') 

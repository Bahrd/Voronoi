# [Ain't] be so square... Voronoi

Our goal is to make the NN algorithms with various distance functions equivalent (in some sense)).
The following questions have already got their answer 
(because it looks like the **[Hanan grid](https://en.wikipedia.org/wiki/Hanan_grid)** is the **(unique!)** answer to these questions!):
- Can a pair of **1-NN** algorithms with distance functions *L<sub>p</sub>* and *L<sub>q</sub>*, 0 < *p,q* < ∞, classify in the same way? [YES]
- How to learn an **1-NN**, *L<sub>q*</sub>-based classifier to behave like an *L<sub>p*</sub>-based one? [YES]

See exemplary Voronoi diagrams for *p = 1/4* and *p = 2* and the same set *S<sub>N</sub>, N = 8*, of random patterns

![Lp, p = .25](./samples/0.25.png) ![Lp, p = 2](./samples/2.png) 

and the *L<sub>p</sub>*-agnostic Hanan-grid approximations for *p = 2*

![Lq-agnostic](./samples/2A.png) ![Lq-agnostic&improved](./samples/2AI.png)
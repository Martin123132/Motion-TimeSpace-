> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# What a momentum difference measures

Use the two frozen TT shear/two-current projectors of the previous matter calculation (not bundled here). With Euclidean \(W=-\log Z\), define \(t=(\epsilon/m)^2\); divide the projected vertex by \(\epsilon^4 e^2/[(4\pi)^2m^2]\). At zero momentum both choices return the same local Weyl coefficient. At finite momentum they are different linear combinations of a tensor at different photon virtualities, not universal functions of the graviton momentum. A nonzero difference by itself is not evidence for a running local Weyl coupling.

## Off-shell experiment: independently deriving the signed measure

For spatial harmonic \(n\), \(P=p^2/\epsilon^2=k^2/\epsilon^2=1+n^2,\ q^2/\epsilon^2=4,\ d=p\cdot k/\epsilon^2=1-n^2\). Write \(B=P x(1-x)\), \(v=x+y,\ w=x-y,\ D=P v+(1-P)v^2-w^2=A-w^2\) on the triangle \(0\le v\le1, -v\le w\le v\), measure \(dv\,dw/2\). The other triangle contraction in the Dirac loop obeys \(b\cdot c-D=(v-1)d-2D\).

The saved scalar integral contains \(H(z)=(1+z)\log(1+z)-z\); Taylor's integral remainder gives \(H(tB)/t^2=\int_0^B(B-u)/(1+tu)\,du\). In the Dirac integral use \(\log(1+tD)/t=\int_0^Ddu/(1+tu)\). Interchanging these compact integrations gives an independent one-dimensional spectral representation \(F(t)=c+\int_0^{U}\rho(u)\,du/(1+tu)\). Here \(c\) is a possible additional local term, absent in the free determinants. For one harmonic let \(b=\sqrt{\max(0,1-4u/P)}\), \(a(v)=\min(v,\sqrt{\max(0,A-u)})\). Then

\[
\begin{aligned}
 \rho_s(u)&=4Pb^3/6-4\int_0^1[(A-u)a-a^3/3]\,dv,\\
 \rho_f(u)&=8(Pb^3/6+ub)+4\int_0^1[(v-1)da-2(Aa-a^3/3)]\,dv .
\end{aligned}
\]

For \(P\le2\), \(U=1\); otherwise \(U=P^2/[4(P-1)]\), from maximizing \(A\). The weights of the saved projector combine the individual densities. The integration splits where a triangle or bubble boundary changes, rather than integrating a discontinuous indicator on a rectangular grid. Here \(u\) is an inverse-cut variable for a simultaneous rescaling of all three Euclidean invariants; it is **not** the invariant mass in a measured two-photon channel.

For \(t_2>t_1\),
\[
 F(t_2)-F(t_1)=-(t_2-t_1)\int_0^U\frac{u\rho(u)}{(1+t_2u)(1+t_1u)}\,du .
\]
The cancellation is exact for any constant \(c\), irrespective of sign. The 22 available exact rational moments and all 20 two-scale comparisons (both fields and both projectors) were checked against the earlier simplex/logarithmic determinants. Several spectral combinations have both signs: e.g. the second scalar density is positive at \(u=0.4\) and negative at 0.8. A positivity bound borrowed from the two-current vacuum polarization would be wrong here.

**Absolute normalization when a UV condition exists.** These free densities are bounded with no atom at zero. A uniform componentwise bound before projector weights is \(M_s=2P/3+2U\), \(M_f=8P/6+2(|d|+2U)\), from simplex area 1/2, \(0\le D\le U\), and \(\int B=P/6\). With absolute projector weights their sums bound the projected density, so \(|F(T)-c|\le M\log(1+TU)/T\). Summing 18 scale differences up to \(T=2^{28}\) recovers the loop intercepts +1/180 and −1/90 with tail bounds below \(8.03\times10^{-8}\) in normalized units. It recovers \(F(0)-F(\infty)\), **not** a finite extra \(c\). The UV falloff was proved for these kernels, not inferred for confined QCD from asymptotic freedom alone.

**Higher derivatives.** A term \((\Box C)FF\) shifts the normalized answer by \(-4c_8t\) in this geometry; \((\Box^2 C)FF\) shifts it by \(16c_{10}t^2\) (absorbing powers of mass into coefficient units). The first difference retains both. Across scales \(\epsilon/m=1/8,1/4,1/2\), weights (4,−5,1) also remove the linear term; the dimension-ten example still has gain 0.703125. Multiple tensor contacts can give the same polynomial on one ray. Do not call their sum an independently measured Wilson coefficient.

**Finite cutoff.** On a scalar link lattice with \(mL=24\), use the same torus for modes 1 and 2 and each of four spacings, reusing all matched prior values. In loop units add a known Maxwell template of arbitrary strength using the previously tested rectangle/corner prescription. Its independent coordinate-space circulation is subtracted with the exact frozen polynomial. Bank 1 is null; bank 2 has a finite difference that cannot be discarded. The two injected strengths cancel on both banks without fitting. This is a test of an *explicit external* contact: it does not establish the counterterm or other cutoff errors of an interacting ensemble. The raw scalar differences approach their continuum comparisons; at 96⁴ the fractional discrepancies are still −3.56% and +12.88%. In particular, differencing did not remove all matter discretization errors or finite-volume effects.

See numerical scale differences (not bundled here), exact moments (not bundled here), [UV/contact checks](evidence-001.zip) (archive member: `uv-and-contact-control.csv`), and paired lattices (not bundled here).

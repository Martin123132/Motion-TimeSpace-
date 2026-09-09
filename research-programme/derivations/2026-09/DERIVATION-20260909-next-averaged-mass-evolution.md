# Next averaged mass evolution: an explicit nonzero forcing law

2026-09-09 BST. Private continuation; no GitHub action.

## 1. What is being closed

The preceding calculation left the boundary mean c2(v) undetermined. This
step evaluates its actual order-u epsilon-squared temporal flux. The result
is a differential law with an explicit forcing, not a declaration that c2
is constant. The scalar equation provides an independent compatibility test.
Actual completed validation, rather than this note's existence, is required.

Preserved owners:

- `DERIVATION-20260909-wave-energy-flux-and-mean-mass.md`: exact improved-mass
  identities, P2, K20 and the previous 23-check result.
- `DERIVATION-20260908-coupled-wave-harmonics-and-subleading-mass.md`: the
  explicit ordinary B1,B3 and coupled D1,D3 transport solutions.
- `scripts/wave_next_mean_evolution_20260909.py`: direct series extraction,
  independent scalar projection, geometric and dimensional checks.

Retain the same spherical action, not a new parent theory:

```text
L = -X/2 - m_chi^2 chi^2/2 + b2 X^2 + b3 X^3 - u W X,
X=(grad chi)^2, W=C_abcd C^abcd, kappa=4pi G,
ds^2=-exp(2delta)F dv^2+2exp(delta)dvdr+r^2 dOmega^2,
F=1-2mu/r-Lambda r^2/3, theta=v/epsilon.
```

Work to first order in u, on a finite smooth annulus away from r=0. G and the
retained couplings are inputs; this step does not derive their numerical
values. Partial_v below is the slow derivative of coefficient functions.
The actual time derivative is D_v=partial_v+epsilon^-1 partial_theta.

The previously selected order-u epsilon incoming amplitude h is zero, with
its initial homogeneous mass offset matched to the reference. The physical
mass and improved bookkeeping mass remain distinct:

```text
mathfrak_m = mu-kappa K,
Delta mathfrak_m = u epsilon^2 N2 + higher orders,
<N2> = c2(v)+kappa[P2(v,r)-P2(v,R)],  R=r0 fixed.
```

## 2. The next incoming data are explicit

Extend the normalized scalar candidate by

```text
chi=(1-u W_ref)chi_ref
    +u epsilon^2[D1 sin(theta)+D3 sin(3theta)]
    +u epsilon^3 sum_(n=1,3,5) E_n(v,r) cos(n theta)+...,

chi_ref=epsilon A cos(theta)/r
        +epsilon^2[B1 sin(theta)+B3 sin(3theta)]
        +epsilon^3 sum_(n=1,3,5) C_n(v,r) cos(n theta)+... .
```

B1,B3,D1,D3 vanish at R by the previously selected boundary data, but their
radial derivatives do not. Set E1(v,R)=g(v)/R. Higher incident harmonics can
be specified independently; they cannot contribute to this mean at this
order. A sine first-harmonic control is also checked and does not supply the
mean. It is set to zero in the selected transport solution.

Allow the next lapse response

```text
delta = delta_ref+u[epsilon d1+epsilon^2 ell2]+...,
ell2=ell20+ell22 cos(2theta)+ell24 cos(4theta),
sigma_b=<ell2(v,R,theta) sin^2(theta)>
       =ell20(v,R)/2-ell22(v,R)/4.
```

g and sigma_b are boundary preparation/clock-normalization data, not fitted
fundamental couplings. The simple matched choice is g=0 and ell2(v,R)=0.
The already fixed lower-order d1 is not removed by making that next-order
choice. Changing a boundary clock while holding a coordinate-time wave
fixed need not preserve the same physical preparation; no gauge-invariant
detector rate is inferred from a coordinate coefficient alone.

## 3. Derive the ordinary curvature terms that enter the mean

Write the ordinary order-epsilon-squared mass harmonics as mu22 cos(2theta)
and mu24 cos(4theta). Direct temporal integration gives

```text
T2=-A A'-A r B1+3A r B3+F0 A^2/(2r)-2b2 A^4/r^3,
T4=-3A r B3+b2 A^4/r^3,
mu22=-kappa(T2+A A'/2)/2,    mu24=-kappa T4/4,
F22=-2mu22/r,                F24=-2mu24/r.
```

Their radial derivatives also satisfy the ordinary radial constraint.
Although F22 enters the metric only at epsilon squared, its fast derivative
enters the order-u epsilon-squared improved flux. Its contribution to the
phase mean is

```text
16mu0 A^2 F22/r^5+8mu0 A^2 partial_r F22/r^4.
```

It cannot be discarded on metric-amplitude counting alone.

The ordinary on-shell spherical Weyl identity is

```text
U=12mu/r^3+4kappa[X/2-V-3b2X^2-5b3X^3],  W=U^2/3.
```

The needed curvature harmonics are therefore

```text
U22=kappa[A A'/r^3-2A^2/r^4+6mu0 A^2/r^5
          +(52/3)b2 A^4/r^6+2A B1/r^2-22A B3/r^2],
U24=kappa[A B3/r^2-b2 A^4/(3r^6)],
W22=8mu0 U22/r^3,
W24=8mu0 U24/r^3-kappa^2 A^4/(6r^6).
```

The U22 formula is independently checked by expanding the metric curvature,
including the ordinary order-epsilon-cubed radial lapse derivative. The
unspecified mean W20 cancels from the required projections; it is not set
to zero. W24 cancels from the mean but is supplied for the higher scalar
transport harmonics.

## 4. The explicit boundary mean law

Let M=mu0(v), R=r0, f=1-2M/R-Lambda R^2/3 and A'=partial_v A. Define the
fully specified coefficient B_forced by

```text
B_forced = (5/3)kappa^2 A^6/R^6

 + kappa M/R^8 {
     A^4[(36+132f)R-180M-8m_chi^2 R^3]
     -36R^2 A^3 A'-(3632/3)b2 A^6/R }

 + 24f M^2/R^8 {
     6R A A'+A^2[m_chi^2 R^2-9f-6+18M/R] }

 + b2 M^2/R^10 {
     A^4[1440+3264f-432m_chi^2 R^2-4320M/R]
     -1440R A^3 A' }

 + M^2 A^6(1296b3-11200b2^2)/R^12.
```

Then the boundary mean evolves according to

```text
c2'(v)=kappa[B_forced(v)+A(v)g(v)-A(v)^2 sigma_b(v)].       (1)

c2(v)=c2(v0)+kappa integral_(v0)^v
       [B_forced(s)+A(s)g(s)-A(s)^2 sigma_b(s)] ds.         (2)
```

For g=sigma_b=0, the mean is forced by B_forced, which is generally nonzero.
It is not sign-definite for all allowed inputs. The formula is not a universal
positive absorption or damping theorem. In particular, the sextic term b3
really enters here; its absence at the preceding order did not license
dropping it now.

Dimensions in the retained four-dimensional conventions are

```text
[A]=L^-1, [G]=L^2, [M]=L, [u]=[b2]=L^4, [b3]=L^8,
[g]=L^-7, [sigma_b]=L^-6, [B_forced]=L^-8, [c2]=L^-5.
```

Consequently u epsilon^2 c2 has the geometric-mass dimension L. The runner
checks the full forcing under length rescaling, not just individual terms.
An algebraic test-wave coefficient control at kappa=b2=b3=Lambda=m_chi=0,
A=1, A'=0, M=1, R=4 gives B_forced=-9/8192. This is a coefficient-only
nonzero test, not an empirical prediction or a nonzero mass rate at G=0.

## 5. The scalar equation independently agrees

The scalar operator is evaluated in its original weighted-current form,
not inferred from conservation. Normalization must be handled off shell:
for the canonical block alone,

```text
E_chi[(1-uW)psi]
 =(1+uW)E_psi -u psi Box W+2u m_chi^2 W psi+O(u^2).
```

The prefactor is 1+uW, not 1-uW. Nonlinear kinetic and induced metric terms
are included by direct substitution in the companion, not discarded using
this canonical illustration.

At the required order, the ordinary and coupled scalar residuals consist
of first, third and fifth sine harmonics. Each has the transport form

```text
R_n - (2n/r) partial_r(r Y_n)=0,  n=1,3,5,
Y_n=C_n for the ordinary system, E_n for the coupled response,

Y_n(v,r)=[R Y_n(v,R)+(1/(2n)) integral_R^r rho R_n(v,rho) d rho]/r. (3)
```

The extracted forcing expressions are saved in the completed run's
`ordinary_transport_forcings` and `coupled_transport_forcings` records.
They contain the already derived B,D functions and their slow derivatives;
the coupled records substitute the required W22,W24. They do not contain
the next unknown Y_n or an invented numerical closure. These are explicit
finite-annulus quadratures, not a convergence theorem for the full series.

The next radial lapse equation is also derived:

```text
partial_r ell2 = kappa[-12W0 A^2 cos^2(theta)/r^3
                      +(2/r)(partial_rr j2+2 partial_r j2/r)]. (4)
```

Here j2 is the previously sourced curvature multiplier. Integrating (4)
from R with the stated boundary lapse gives ell2, rather than treating its
interior profile as arbitrary.

Let T=<order-u epsilon-squared improved temporal flux>/kappa, and let
E_sin1 denote the independently extracted normalized scalar residual at
this order. Substitution of the earlier B,D transport laws and (4) gives
the identity

```text
partial_r T-partial_v partial_r P2+(A r/2)E_sin1=0.        (5)
```

Thus solving the actual scalar transport makes the radial and temporal
mean-mass constraints agree. This is the check that prevents (1) from being
only a boundary formula unrelated to the interior solution.

## 6. Restore the physical mass and state the remaining limit

The physical, rather than improved, mean coefficient is

```text
<M2(v,r)>=c2(v)+kappa[P2(v,r)-P2(v,R)+K20(v,r)],           (6)

partial_v <M2(v,R)>
 =kappa[B_forced+A g-A^2 sigma_b+partial_v K20(v,R)].      (7)
```

K20 and P2 are the explicit functions in the previous energy-flux note.
They have not been subtracted from the physical result. Combining (2) and
(6) now fixes this finite-order mean profile for specified initial and
boundary data. Its change is bounded by the integral of the absolute right
side, plus the explicit changes of P2 and K20. This is a coefficient bound,
not an error bound relative to an exact solution.

All inverse-radius terms remain restricted to an annulus. There are no new
1/F0 poles in the displayed forcing, but this does not prove regularity of
a black-hole centre. The kinetic normalization 1+2uW>0 and the retained
derivative/EFT regime are still required. No claim is made that fixed-u
epsilon -> 0 is a uniformly controlled limit.

Next finite target: evaluate the transport quadratures and assemble the
next-order reference and coupled fields, then test the leftover equations
as epsilon changes on a specified finite annulus. Apply the same residual
tests to both, keeping the ordinary baseline distinct from the O4 increment.
That is the route toward a controlled approximation rather than endlessly
adding formal orders or claiming an interior solution from an average.

## 7. Verification and retained history

Completed run:
`source-intake/navier-stokes/20260909/next-mean-evolution-final/`.
Actual result: **50/50 symbolic checks passed**, each with zero remainder,
completed `2026-09-09T00:02:27.936820+00:00`. The status and COMPLETE marker
agree. The live script and executed snapshot have matching SHA-256:
`6af67cae30e2b73999629a5df32fbce1e76cc8b9fee7216af0e3b6cc826fe55d`.
All three input hashes match their preserved source files. The claim flag
remains false: finite-order algebra is not completed MTS or a full PDE proof.

The source compiles in memory without creating __pycache__. A separate
inspection of all six serialized transport forcings finds only the owned
functions A, mu, B1, B3, D1 and D3 (subsets as appropriate), with no hidden
next-scalar or unsourced curvature function. When parsing these expressions
in SymPy, map `Lambda` explicitly to a Symbol; otherwise the parser selects
SymPy's built-in Lambda class. No energy-flux worker remains running.

Each run keeps an executed-source snapshot and input hashes. Jobs run
serially, one logical CPU at BelowNormal priority, with library threads
limited to one. No full PDE evolution is launched here.

Earlier attempts remain intact:

- `next-mean-evolution-initial`: 17 checks for an incomplete ansatz;
  SUPERSEDED.json records the missing fast-differentiated F22 contribution
  and boundary derivative-ordering issue. Its completion marker does not
  establish the complete mean law.
- `next-mean-evolution-coupled`: 31/33, with a diagnosed wrong sign in the
  new checker's off-shell normalization prefactor. No failed constraint was
  accepted or overwritten.
- `next-mean-evolution-verified`: 39/40; scalar/mass compatibility passes.
  The remaining failure is a transcribed expected rational in a test-wave
  control, not a change to the derived forcing. DIAGNOSIS.json preserves it.

The older D4/stellar numerical state is unchanged. RH, Desktop Commander
and public repositories are outside this continuation's modifications.

# 4910 - Free metric TTT projection and Weyl-cubic arbitration

Marker: `MTS_FREE_METRIC_TTT_PROJECTOR_ARBITRATION_4910`

Checkpoint 4911 completes the selected geometric construction. The twelve raw
integrated `a6` columns have an eight-dimensional cubic-response quotient;
the four dependencies and quotient-invariant Ricci-flat map recover the known
source vector. The remaining gate is independent exact free-lattice
multi-geometry recovery, not construction of a twelve-column inverse.

## Decision

Checkpoint 4909 constructed a nonzero transverse-traceless Weyl-cubic
template and proposed using four momentum scales to remove `q^0`, `q^2`, and
`q^4` terms before dividing the `q^6` response by that template. This
checkpoint implements that proposal first in the exactly solvable free scalar
theory.

The triangle-plus-seagull metric response is implemented in momentum space
and independently as a dense real-space determinant derivative. They agree
to better than `3.5e-18` on complete `3^4` and `4^4` lattices. The numerical
pipeline itself is therefore correct.

The proposed **single-triplet Weyl projector is not correct**. Across six fit
choices on `24^4` and `32^4` lattices it gives

\[
-3.4425\times10^{-5}
\le \zeta_{\rm naive}
\le -2.8254\times10^{-5},
\]

whereas the known continuum massive-real-scalar coefficient at `m=1` is

\[
\boxed{
\zeta_s=\frac1{30240(4\pi)^2}
=2.09410515\times10^{-7}.
}
\]

Every naive fit has the opposite sign and is `134.9--164.4` times larger in
absolute magnitude. This discrepancy is not used to alter the known scalar
coefficient. It diagnoses the projector.

The reason is exact. A nonzero real periodic Euclidean TT perturbation is
off-shell and has nonzero Ricci curvature. Its `q^6` response therefore mixes
the target Weyl cubic with derivative-curvature and Ricci-cubic operators in
the full scalar `a6` tensor. Finite lattice regulator effects are also present
because the test uses `am=1`. Momentum-power subtraction alone cannot
separate operators that all scale as `q^6`.

There is also a flat-torus no-go: a real periodic Euclidean perturbation that
is linearized Ricci-flat has only a constant harmonic representative, whose
linearized Weyl tensor is zero. One real TT source cannot simultaneously be a
nonzero Weyl probe and an on-shell Ricci-flat projector.

The corrected route is a full off-shell template inversion:

\[
M_{rA}
=\partial_1\partial_2\partial_3
\int\sqrt g\,\mathcal O_A^{(6)}[g_r]\big|_0,
\]

\[
\boxed{
c=(M^T\Sigma^{-1}M)^{-1}M^T\Sigma^{-1}y,
}
\]

followed by the proved Ricci-flat map

\[
\boxed{\zeta_{C^3}=v_Ac_A.}
\]

The interacting long run is deliberately not launched because its numerator
cannot yet be mapped uniquely to `C^3`. This prevents a large computation
from producing a precise but wrongly labelled coefficient.

The mass-gap pilot from 4909 is retained as separate two-point evidence.
Neither `c_6` nor any naive fit enters the action:

\[
\boxed{\Gamma_{\rm MTS,res}=0.}
\]

## 1. Symmetric densitized-metric lattice stencil

For the free validation field, the Euclidean scalar action is discretized as

\[
\begin{aligned}
S[\varphi,\mathcal H]={}&
\frac14\sum_x\mathcal H^{\mu\nu}(x)
\left[
\Delta^+_\mu\varphi\,\Delta^+_\nu\varphi
+\Delta^-_\mu\varphi\,\Delta^-_\nu\varphi
\right]\\
&+\frac12m^2\sum_x\sqrt{\det\mathcal H(x)}\,\varphi_x^2.
\end{aligned}
\]

At `H=I`, this is exactly the standard nearest-neighbour lattice scalar. The
forward/backward average is reflection symmetric. The kinetic term is linear
in the fundamental densitized inverse metric, while the exact second and
third volume seagulls are those derived in 4909.

For a complex Fourier source

\[
h_i^{\mu\nu}(x)=e_i^{\mu\nu}e^{iq_i\cdot x},
\qquad q_1+q_2+q_3=0,
\]

the one-source lattice vertex between momentum `p` and `p+q` is

\[
\boxed{
V_i(p+q,p)=\frac12\left[
a^\dagger(p+q)e_i a(p)
+b^\dagger(p+q)e_i b(p)
\right],
}
\]

where

\[
a_\mu(p)=e^{ip_\mu}-1,
\qquad
b_\mu(p)=1-e^{-ip_\mu}.
\]

The volume contacts are

\[
K_{ij}=-\frac{m^2}{2}\operatorname{tr}(e_i e_j)
e^{i(q_i+q_j)\cdot x},
\]

\[
K_{123}=\frac{m^2}{2}
[\operatorname{tr}(e_1e_2e_3)+\operatorname{tr}(e_1e_3e_2)].
\]

These vertices enter the complete determinant identity from 4908; no contact
term is fitted.

## 2. Independent dense validation

The free response is evaluated in two ways.

1. Momentum implementation: enumerate all lattice loop momenta and apply the
   exact source shifts.
2. Dense implementation: construct every forward/backward derivative matrix,
   every source matrix, the full propagator, and the six determinant trace
   terms directly.

For `m=1.2` and the scale-one TT triplet:

| lattice | momentum `W123/V` | dense `W123/V` | absolute residual |
|---:|---:|---:|---:|
| `3^4` | `0.007859255838230049` | `0.007859255838230049` | `6.09e-21` |
| `4^4` | `0.007918231060922168` | `0.007918231060922164` | `3.47e-18` |

This validates the triangle orientations, all three pair seagulls, the third
volume contact, Fourier normalization and lattice propagator independently.

## 3. Exact free response grid

The full free determinant response is then calculated at `m=1` for
`s=0,...,6` on `24^4` and `32^4`. The imaginary residual is identically zero
at printed precision. Representative rows are

| `N` | `s` | `k=2 pi s/N` | `W123/V` |
|---:|---:|---:|---:|
| `24` | `0` | `0` | `0.00557993382281267` |
| `24` | `4` | `1.04720` | `0.00550271414027420` |
| `24` | `6` | `1.57080` | `0.00548264982349967` |
| `32` | `0` | `0` | `0.00557993382285922` |
| `32` | `4` | `0.78540` | `0.00552794470205769` |
| `32` | `6` | `1.17810` | `0.00549278262225164` |

Increasing `N` here improves momentum resolution and volume. It is not a
continuum limit because `am=1` remains fixed.

## 4. The attempted single-triplet extraction

For each lattice and maximum scale `s_max=4,5,6`, fit

\[
\frac{W_{123}}V
=A_0+A_2k^2+A_4k^4+A_6k^6+A_8k^8.
\]

The attempted coefficient is

\[
\zeta_{\rm naive}=A_6/\mathcal T_{C^3},
\qquad
\mathcal T_{C^3}=0.113854701827611.
\]

The six outputs are

| `N` | `s_max` | `zeta_naive` | `zeta_naive/zeta_s` |
|---:|---:|---:|---:|
| `24` | `4` | `-2.93811e-5` | `-140.30` |
| `24` | `5` | `-3.19378e-5` | `-152.51` |
| `24` | `6` | `-3.44254e-5` | `-164.39` |
| `32` | `4` | `-2.82537e-5` | `-134.92` |
| `32` | `5` | `-2.95669e-5` | `-141.19` |
| `32` | `6` | `-3.12775e-5` | `-149.36` |

No fit has the correct sign or lies within a factor of two. The fit-window
dependence also shows unresolved higher-order contamination. The gate fails
before any interacting data are generated.

## 5. Why momentum powers are insufficient

The minimal scalar `a6` source archived at checkpoint 4881 contains, before
Ricci-flat reduction:

- derivative structures built from `R`, `R_mn`, and `R_mnrs`;
- `R^3`;
- `R R_mn R^mn`;
- `R R_mnrs R^mnrs`;
- `R_m^n R_n^r R_r^m`;
- two-Ricci--one-Riemann contractions;
- Ricci--two-Riemann contractions;
- the two Riemann-cubic contractions.

After integration by parts and Bianchi identities the number of independent
directions decreases, but it is not one on an off-shell background. Every
retained six-derivative direction contributes at order `q^6`. Removing
`q^0`, `q^2`, and `q^4` does not distinguish them.

The known coefficient `1/[30240(4pi)^2m^2]` is the Ricci-flat/on-shell
combination. Dividing an off-shell response by only the Weyl template assumes
the Ricci coefficients vanish, which the parent determinant explicitly
contradicts.

Finite lattice effects are a second issue. A continuum check requires

\[
am\to0,
\qquad Nam\to\infty,
\]

and agreement across stencils. The current failure is therefore not used to
estimate a replacement coefficient; it proves the proposed extraction is not
claim-safe even before this extrapolation.

## 6. Real Euclidean on-shell projector no-go

On the flat Euclidean torus, impose de Donder gauge,

\[
\partial^\mu(h_{\mu\nu}-\tfrac12\delta_{\mu\nu}h)=0.
\]

The linearized Ricci tensor becomes

\[
\boxed{R_{\mu\nu}^{(1)}=-\frac12\partial^2h_{\mu\nu}.}
\]

Ricci-flatness requires `partial^2 h_mn=0`. A periodic harmonic tensor has
only its zero Fourier mode. That mode is constant, so all derivatives and its
linearized Riemann and Weyl tensors vanish. Hence

\[
\boxed{
\text{real periodic Euclidean Ricci-flat perturbation}
\quad\Longrightarrow\quad C^{(1)}=0.
}
\]

This is why changing the real TT polarization cannot repair the single-source
projector. A nonzero real Euclidean Weyl probe is necessarily off-shell.

## 7. Corrected full-basis projector

Let `O_A^(6)` be a complete integrated six-derivative basis after proving all
boundary, Bianchi and integration-by-parts identities. For each independent
source geometry `r`, calculate

\[
\boxed{
M_{rA}=\partial_{123}
\int\sqrt g\,\mathcal O_A^{(6)}[g_r]\big|_0.
}
\]

The measured response must first have its lower derivative pieces removed,

\[
y_r=W_{123,r}-y_r^{(q^0)}-y_r^{(q^2)}-y_r^{(q^4)}.
\]

With full covariance `Sigma`, solve

\[
\boxed{
c=(M^T\Sigma^{-1}M)^{-1}M^T\Sigma^{-1}y.
}

Activation requires

\[
\operatorname{rank}M=N_{\rm basis},
\]

reported singular values, a stable condition number, and leave-one-geometry
tests. The physical Weyl coefficient is then obtained only through the
separately proved Ricci-flat reduction vector,

\[
\boxed{\zeta_{C^3}=v_Ac_A.}
\]

The free scalar must reproduce the known coefficient under this full chain
before the interacting motion scalar is run. A complex-null on-shell
three-graviton amplitude is retained as an analytic crosscheck, not used as a
direct finite-volume Monte Carlo source.

## 8. Interacting-run decision

| gate | result |
|---|---|
| exact free triangle and seagulls | pass |
| free known-`C^3` recovery by single TT division | fail |
| real periodic Euclidean on-shell source | theorem-blocked |
| full off-shell template matrix | not yet constructed |
| interacting TTT long run | **do not run** |
| active residual | zero preserved |

This is not avoiding a difficult computation. It prevents spending hours on
an interacting numerator whose operator label is mathematically ambiguous.
The 4909 mass result remains valid as a finite-cutoff two-point pilot and is
not erased by a three-point projector failure.

## 9. Local GR, Newton and Maxwell

No failed fit or diagnostic number enters the low-energy action. Therefore:

- the massless spin-two pole remains the calibrated Einstein pole;
- `G_N=1/(8pi M_R^2)` remains the one global Newton calibration;
- linear Newton and PPN response are unchanged;
- no scalar fifth-force coupling is activated;
- Maxwell propagation and Poynting Hilbert stress remain unchanged;
- the future strong-gravity gate remains

  \[
  |\zeta_{C^3}|q^4/M_R^2\ll1.
  \]

The active decision is

\[
\boxed{c_6\ \text{not promoted},\qquad\Gamma_{\rm MTS,res}=0.}
\]

## 10. Arbitration

```text
FREE METRIC TTT
    -> IMPLEMENTED EXACTLY
    -> DENSE AND MOMENTUM ROUTES AGREE TO 3.5e-18

SINGLE TT q6 / WEYL TEMPLATE
    -> ATTEMPTED
    -> WRONG SIGN IN 6 OF 6 FITS
    -> MAGNITUDE WRONG BY FACTOR 134.9--164.4
    -> REJECTED

ROOT CAUSE
    -> REAL EUCLIDEAN NONZERO TT SOURCE IS OFF SHELL
    -> FULL a6 RICCI AND DERIVATIVE DIRECTIONS ALSO SCALE AS q6
    -> FINITE LATTICE REGULATOR NOT YET EXTRAPOLATED

CORRECTED ROUTE
    -> FULL OFF-SHELL TEMPLATE MATRIX
    -> RANK AND CONDITION-NUMBER GATE
    -> CORRELATED BASIS INVERSE
    -> PROVED RICCI-FLAT MAP TO C3

INTERACTING LONG RUN
    -> WITHHELD UNTIL FREE COEFFICIENT RECOVERY

ACTIVE Gamma_MTS,res
    -> 0
```

No GitHub action or public residual claim follows from this checkpoint.

## Next target

`4911-Y5-R2FR-full-off-shell-a6-template-basis-and-interacting-Weyl-cubic-projector.md`

Checkpoint 4911 must construct the integrated scalar `a6` template basis,
generate enough independent real source triples to prove full matrix rank,
and recover the free coefficient after the Ricci-flat map. Only then should
the same observables be attached to the interacting sampler.

## Sources

- `post-checkpoint-work/4909-Y5-R2FR-renormalized-motion-scalar-measure-mass-gap-and-stress-three-point-matching.md`.
- `post-checkpoint-work/4908-Y5-R2FR-microscopic-MTS-metric-three-point-vertex-and-Weyl-cubic-coefficient-or-zero-residual-theorem.md`.
- `post-checkpoint-work/4881-Y5-R2FR-compact-matter-interior-EOS-contact-matching-and-Riemann-cubed-coefficient-owner-gate.md`.
- `post-checkpoint-work/4905-Y5-R2FR-first-nontrivial-MTS-to-SM-gravity-operator-basis-and-independent-observable-gate.md`.
- `post-checkpoint-work/source-intake/heat_kernel_a6/4881/hep-th-0306138.tar`.
- `post-checkpoint-work/scripts/Y5_R2FR_4910_free_metric_TTT_projector_arbitration.py`.
- `post-checkpoint-work/source-intake/microscopic_vertex/4910/PROVENANCE.md`.

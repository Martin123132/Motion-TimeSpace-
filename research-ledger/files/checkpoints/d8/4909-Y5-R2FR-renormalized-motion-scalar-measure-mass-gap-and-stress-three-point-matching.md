# 4909 - Motion-scalar lattice measure, mass gap and stress-three-point matching

Marker: `MTS_RENORMALIZED_MOTION_SCALAR_GAP_STRESS_THREE_POINT_4909`

## Decision

Checkpoint 4908 reduced the interacting motion-scalar problem to the
dimensionless theory

\[
S=\int d^4y\left[
\frac12(\partial\phi)^2+\frac34|\phi|^{4/3}
\right],
\qquad
m_{\rm gap}=c_m\lambda^{3/8},
\qquad
\zeta_{\psi}=c_6\lambda^{-3/4}.
\]

This checkpoint performs the first nonperturbative calculation rather than
returning `c_m` and `c_6` as unexplored labels.

1. A positive finite-cutoff four-dimensional lattice measure is defined
   directly from the printed potential.
2. The checkerboard Metropolis-plus-overrelaxation sampler is verified against
   exact local action differences and a free lattice scalar.
3. Six interacting runs at four cutoffs, including one seed replication and
   one finite-volume pair, give a provisional dimensionless mass ratio near
   one.
4. The exact connected third-response estimator is verified twice against
   Gaussian determinant calculations.
5. Exact densitized-metric seagulls are derived.
6. A nonzero transverse-traceless momentum triplet is constructed whose
   Weyl-cubic template scales exactly as the sixth power across four momentum
   scales.

The mass-gap result is promising but **not promoted**. The constant pilot fit
is

\[
\boxed{c_m^{\rm pilot}=1.02129\pm0.02408\quad({\rm statistical})}
\]

with `chi2/dof=0.948`. Linear-in-cutoff and linear-in-cutoff-squared
intercepts are

\[
0.95863\pm0.11541,
\qquad
0.99099\pm0.05678.
\]

Their conservative two-sigma union is `[0.728,1.189]`. This is evidence that
the literal one-parameter trajectory is not obviously losing its mass scale;
it is not yet a continuum prediction because the smallest `a mu` is `0.4`,
only one finite-volume comparison exists, and no alternative discretization
or mass-counterterm trajectory has been compared.

The stress-three-point machinery is now executable, but the interacting
four-momentum projection has not yet been sampled. Therefore `c_6` remains
unpromoted and

\[
\boxed{\Gamma_{\rm MTS,res}=0}
\]

continues to be the active action. No local-GR, Newton or Maxwell conclusion
is changed by the pilot.

## 1. Finite lattice definition

For lattice spacing `a`, define the dimensionless field

\[
\varphi_n=a\psi(x_n),
\qquad
\widehat\mu=a\mu,
\qquad
\mu=\lambda^{3/8}.
\]

The Euclidean lattice action is

\[
\boxed{
S_a=\sum_n\left[
\frac12\sum_{\alpha=1}^4
(\varphi_{n+\hat\alpha}-\varphi_n)^2
+\frac12r_a\varphi_n^2
+\frac34g_a|\varphi_n|^{4/3}
\right],
}
\]

with

\[
g_a=\widehat\mu^{8/3}.
\]

For finite volume and `g_a>0`, the Boltzmann weight is positive and the onsite
potential confines the constant mode. The literal printed-action trajectory
is

\[
\boxed{r_a=0,\qquad g_a=\widehat\mu^{8/3}.}
\]

Calling this a renormalized one-parameter theory requires simultaneous
limits

\[
\widehat\mu\to0,
\qquad
N\widehat\mu\to\infty,
\]

and convergence of

\[
\boxed{c_m(a,L)=\frac{a m_{\rm gap}}{\widehat\mu}.}
\]

The `r_a=0` condition is not protected by the `Z2` symmetry: a quadratic term
is symmetry-allowed under coarse graining. The literal trajectory is therefore
tested, not silently assumed to be counterterm-complete.

## 2. Sampler and exact local validation

The lattice is bipartite. All even sites can be updated together while their
odd neighbours are fixed, and conversely. For a proposal `old -> new`, the
implemented local action difference is

\[
\Delta S_n
=4(\varphi_{new}^2-\varphi_{old}^2)
-(\varphi_{new}-\varphi_{old})\sum_{nn}\varphi_{nn}
+\frac{r_a}{2}(\varphi_{new}^2-\varphi_{old}^2)
+\frac{3g_a}{4}
(|\varphi_{new}|^{4/3}-|\varphi_{old}|^{4/3}).
\]

Sixty-four random one-site changes were compared with a complete action
recalculation. The maximum absolute discrepancy is

```text
4.65635e-14.
```

An involutive overrelaxation proposal preserves the quadratic local action,

\[
\varphi'_n
=\frac{2\sum_{nn}\varphi_{nn}}{8+r_a}-\varphi_n,
\]

and is accepted against the exact change in the fractional potential. It is
combined with random-walk Metropolis updates, so ergodicity does not depend on
the overrelaxation move alone.

## 3. Free-theory calibration

For `g_a=0` and bare lattice mass `am_0=0.7`, the exact zero-spatial-momentum
decay mass is

\[
aE_0=2\operatorname{arsinh}(am_0/2).
\]

The checkpoint run gives

```text
exact aE0       = 0.686443...;
measured aE0    = 0.691756 +/- 0.042703;
relative error  = 0.774%.
```

This passes before the interacting mass is interpreted. The mass estimator
fits the periodic correlator

\[
C(t)=A[e^{-amt}+e^{-am(N-t)}]
\]

and uses blocked delete-one jackknife errors. The effective-mass medians track
the fit values in all runs.

## 4. Interacting mass-gap pilot

The checkpoint profile contains the following independent interacting rows:

| `a mu` | `N` | `N a mu` | `a m` | `c_m=a m/(a mu)` |
|---:|---:|---:|---:|---:|
| `0.8` | `8` | `6.4` | `0.83887 +/- 0.05713` | `1.04858 +/- 0.07141` |
| `0.6` | `10` | `6.0` | `0.64792 +/- 0.03474` | `1.07987 +/- 0.05789` |
| `0.6` | `12` | `7.2` | `0.65846 +/- 0.03862` | `1.09743 +/- 0.06436` |
| `0.5` | `12` | `6.0` | `0.46408 +/- 0.02196` | `0.92816 +/- 0.04391` |
| `0.5` | `12` | `6.0` | `0.52915 +/- 0.02395` | `1.05830 +/- 0.04790` |
| `0.4` | `16` | `6.4` | `0.41866 +/- 0.02194` | `1.04664 +/- 0.05485` |

At `a mu=0.6`, increasing the box from `N=10` to `N=12` changes `c_m` by

\[
0.01756\pm0.08657,
\]

only `0.203` standard deviations. No finite-volume effect is resolved by that
single comparison.

The two `a mu=0.5`, `N=12` seeds differ by `2.003` combined standard
deviations. This is below the predeclared three-sigma inconsistency threshold
but warns against quoting only the smaller jackknife error from either run.

After selecting the largest volume at each cutoff and combining equal-volume
replicates, the cutoff aggregates span

```text
0.98759 <= c_m <= 1.09743.
```

The constant fit has `chi2/dof=0.948`; neither a resolved cutoff drift nor a
continuum limit is claimed. The honest status is

```text
finite positive mass gap on every sampled lattice = yes;
literal one-parameter trajectory already falsified = no;
continuum c_m promoted                            = no;
provisional scale                                 = m_gap approximately mu.
```

## 5. Connected third-response identity

For `W=-log Z` and three independent background sources,

\[
\boxed{
\begin{aligned}
W_{123}={}&\langle S_{123}\rangle
-\operatorname{Cov}(S_1,S_{23})
-\operatorname{Cov}(S_2,S_{13})
-\operatorname{Cov}(S_3,S_{12})\\
&+\langle\delta S_1\delta S_2\delta S_3\rangle.
\end{aligned}}
\]

This is the interacting Monte Carlo form of the determinant
triangle-plus-seagull identity derived in 4908.

Two independent Gaussian tests close.

1. A mass-source third derivative on a `6^4` free lattice has

   ```text
   exact W'''      = 10.6421410;
   estimate        = 10.1084...;
   relative error  = 5.02%;
   pull            = -0.700.
   ```

2. A rank-five Gaussian with distinct `K_i`, `K_ij`, and `K_123` gives

   ```text
   exact W_123     = 0.00474145736;
   estimate        = 0.00484579055;
   standard error  = 0.000157524;
   pull            = 0.662.
   ```

The second test explicitly validates all three covariance seagulls and the
connected triple insertion, not just a one-parameter derivative.

## 6. Densitized-metric seagulls

The integrated parent uses the densitized inverse metric

\[
\mathcal H^{\mu\nu}=\sqrt g\,g^{\mu\nu},
\qquad
\sqrt g=\sqrt{\det\mathcal H}
\]

in Euclidean signature. Write

\[
\mathcal H=I+\epsilon_1h_1+\epsilon_2h_2+\epsilon_3h_3,
\qquad
\operatorname{tr}h_i=0.
\]

The kinetic term is linear in `H`. All local scalar-potential seagulls follow
from the volume:

\[
\boxed{
\partial_i\sqrt{\det\mathcal H}\big|_0=0,
}
\]

\[
\boxed{
\partial_i\partial_j\sqrt{\det\mathcal H}\big|_0
=-\frac12\operatorname{tr}(h_i h_j),
}
\]

\[
\boxed{
\partial_1\partial_2\partial_3
\sqrt{\det\mathcal H}\big|_0
=\frac12\left[
\operatorname{tr}(h_1h_2h_3)
+\operatorname{tr}(h_1h_3h_2)
\right].
}
\]

An exact symbolic noncommuting-matrix test gives `(0,-3,18)` for both direct
derivatives and these formulas. Thus the future lattice `S_ij` and `S_123`
are fixed by the same parent variable rather than chosen to make a Ward test
pass.

## 7. Nonzero Weyl-cubic source triplet

Use Euclidean integer momenta

\[
q_1=(1,0,0,0),
\quad q_2=(0,1,0,0),
\quad q_3=(-1,-1,0,0),
\]

and deterministic normalized polarizations satisfying

\[
q_i^\mu e^{(i)}_{\mu\nu}=0,
\qquad
\operatorname{tr}e^{(i)}=0.
\]

The largest closure, transverse and trace residuals are respectively

```text
0;
9.11e-17;
2.08e-16.
```

The fully symmetrized linearized Weyl-cubic contraction is nonzero:

\[
\boxed{\mathcal T_{C^3}(1)=0.113854701827611.}
\]

Scaling all three momenta by `s=1,2,3,4` gives ratios

```text
1, 64, 729, 4096,
```

exactly `s^6` to a maximum residual below `8e-13`. This supplies a real
four-scale projection target. It is not a symbolic request to “find a useful
background later.”

## 8. What remains before `c_6` is a result

The interacting calculation must now:

1. implement one symmetric covariant lattice stencil for off-diagonal
   densitized-metric sources;
2. measure `S_i`, `S_ij`, and `S_123` for the constructed TT triplet;
3. verify the lattice stress Ward identity including contact terms;
4. measure at least four momentum scales;
5. separate `q^0`, `q^2`, `q^4`, and `q^6` pieces;
6. divide the `q^6` response by the nonzero Weyl template;
7. repeat across volume, cutoff, seed and discretization;
8. keep the result independent of any gravity, galaxy or compact-body target.

**4910 supersession:** steps 4--6 above are necessary but not sufficient.
The exact free end-to-end test proves that one real Euclidean TT geometry has
multiple off-shell six-derivative Ricci and derivative-curvature components.
The `q^6` numerator must be resolved through a full geometric template matrix
before division by the Weyl component. The standalone template remains a
valid nonzero column, not a complete projector.

The free-single-pole substitution using the provisional constant mass fit
would give

\[
c_6^{\rm pole\ diagnostic}=2.0077\times10^{-7}.
\]

It is **not** an interacting result and is written only as a pipeline scale.
Replacing the stress-three-point measurement with this number would recreate
the Gaussian assumption that checkpoint 4908 rejected.

## 9. Local known-limit gate

Nothing in the finite lattice pilot has entered the active low-energy action.
Consequently:

- `M_R` and the once-calibrated `G_N` remain unchanged;
- the massless spin-two propagator remains the Einstein propagator;
- no scalar fifth force is activated;
- no direct MTS--Maxwell operator is inserted;
- electromagnetic energy and Poynting momentum remain Hilbert stress;
- `Gamma_MTS,res=0` remains the current local-GR/Maxwell-safe baseline.

The first possible promotion remains a pure metric `C^3` coefficient, which
has no flat quadratic metric variation. Even a future nonzero `c_6` must pass
`|zeta|q^4/M_R^2 << 1` in every local arena.

## 10. Arbitration

```text
FINITE LATTICE MEASURE
    -> DEFINED DIRECTLY FROM PRINTED |psi|^(4/3) POTENTIAL
    -> POSITIVE AND CONFINING AT FINITE CUTOFF

NUMERICAL PIPELINE
    -> LOCAL ACTION DIFFERENCE PASSES AT 4.66e-14
    -> FREE MASS CALIBRATION PASSES AT 0.77%
    -> DISTINCT CONNECTED THIRD RESPONSE PASSES AT 0.66 SIGMA

MOTION-SCALAR MASS GAP
    -> SIX INTERACTING RUNS, FOUR CUTOFFS
    -> PROVISIONAL c_m NEAR 1
    -> NO RESOLVED DRIFT IN CURRENT WINDOW
    -> CONTINUUM VALUE NOT PROMOTED

STRESS THREE-POINT
    -> DENSITIZED SEAGULLS DERIVED
    -> NONZERO TT WEYL-CUBIC TRIPLET CONSTRUCTED
    -> FOUR EXACT q^6 TEMPLATE SCALES CONSTRUCTED
    -> INTERACTING TTT MEASUREMENT NOT YET RUN

ACTIVE ACTION
    -> c_m NOT PROMOTED
    -> c_6 NOT PROMOTED
    -> Gamma_MTS,res=0
```

No GitHub action or public claim follows from this checkpoint.

## Next target

`4910-Y5-R2FR-motion-scalar-cutoff-volume-extrapolation-and-TTT-Weyl-cubic-projection.md`

Checkpoint 4910 should add the densitized-metric source observables to the
sampler, recover the known free-scalar Weyl coefficient as an end-to-end
projection test, and only then run the interacting four-scale TTT measurement.
The existing `--profile long` mass run should not be launched by itself,
because more mass statistics without the TTT observable would not close the
actual residual coefficient.

## Sources

- `post-checkpoint-work/4908-Y5-R2FR-microscopic-MTS-metric-three-point-vertex-and-Weyl-cubic-coefficient-or-zero-residual-theorem.md`.
- `core-mts-framework/action-principle/the-fundamental-action-of-motion-timespace-field-theory.md`.
- `post-checkpoint-work/4876-Y5-R2FR-integrated-H-parent-action-saddle-regulator-and-induced-coefficient-matching-to-GN-Lambda-and-R2.md`.
- `post-checkpoint-work/4881-Y5-R2FR-compact-matter-interior-EOS-contact-matching-and-Riemann-cubed-coefficient-owner-gate.md`.
- `post-checkpoint-work/4904-Y5-R2FR-current-unified-action-assembly-Ward-identity-and-parameter-prediction-ledger.md`.
- `post-checkpoint-work/scripts/Y5_R2FR_4909_motion_scalar_lattice_gap_stress_three_point.py`.
- `post-checkpoint-work/source-intake/microscopic_vertex/4909/PROVENANCE.md`.

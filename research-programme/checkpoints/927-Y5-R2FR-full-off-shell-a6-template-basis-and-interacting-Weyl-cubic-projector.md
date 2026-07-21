# 4911 - Full off-shell `a6` template quotient and Weyl-cubic projector

Marker: `MTS_FULL_OFFSHELL_A6_TEMPLATE_PROJECTOR_4911`

Checkpoint 4912 independently validates this quotient with the directly
integrated free determinant at two masses. It also completes the traceful
mass-volume contacts, rejects the contaminated absolute coarse-lattice route,
and selects same-regulator matched subtraction for the interacting test.

## Decision

Checkpoint 4910 proved that one real Euclidean TT response cannot be divided
by one Weyl-cubic template: the source is off shell and all six-derivative
curvature directions mix at the same momentum order. This checkpoint builds
the required full geometric response instead of adding another placeholder.

The hash-locked minimal-scalar `a6` formula is reduced on a closed periodic
four-manifold to twelve integrated columns. Their exact mixed third metric
responses are evaluated with a nilpotent three-source algebra, so the metric,
inverse metric, determinant, connection, curvature, covariant derivatives and
measure are all included without a finite-difference amplitude.

The twelve raw columns have **rank eight**, not twelve. Four dependencies are
resolved to rational coefficients with relative residual below
`8.74e-16`. A pivoted rank-eight quotient has retained condition number
`51.42`. All twelve leave-one-geometry fits remain rank eight; their largest
condition number is `167.13`.

The Ricci-flat quotient map is derived from those identities. When the
source-backed scalar `a6` vector is projected through the rank-eight inverse,
the response is reconstructed to `5.66e-16` relative and gives

\[
\boxed{
\zeta_s=2.094105151337765\times10^{-7}
}
\]

at `m=1`, against the exact value

\[
\frac{1}{30240(4\pi)^2}
=2.0941051513379998\times10^{-7}.
\]

This closes the **geometric projector** that checkpoint 4910 was missing. It
does not yet independently recover the coefficient from the free lattice
determinant: the response used in this calibration is the sourced heat-kernel
vector `y=M c_a6`. The next test must feed exact multi-geometry lattice
responses into the same quotient and take a genuine cutoff/volume sequence.
The interacting run remains withheld and

\[
\boxed{\Gamma_{\rm MTS,res}=0.}
\]

## 1. Sourced integrated basis

For a minimal scalar (`E=0`, bundle curvature zero), the primary formula in
`ch4.tex` contains the gravitational terms

\[
\begin{aligned}
7!\,a_6={}&18R_{;iijj}+17(\nabla R)^2-2(\nabla R_{mn})^2
-4\nabla_nR_{jk}\nabla_kR_{jn}+9(\nabla R_{mnrs})^2\\
&+28R\Box R-8R_{mn}\Box R^{mn}
+24R_{jk}R_{jn;kn}+12R_{mnrs}\Box R^{mnrs}\\
&+\frac{35}{9}R^3-\frac{14}{3}RR_{mn}R^{mn}
+\frac{14}{3}RR_{mnrs}R^{mnrs}-\frac{208}{9}R_m{}^nR_n{}^rR_r{}^m\\
&-\frac{64}{3}R_{ij}R_{kl}R_{ikjl}
-\frac{16}{3}R_{jk}R_{jnli}R_{knli}
-\frac{44}{9}I_1-\frac{80}{9}I_2.
\end{aligned}
\]

On the boundaryless periodic domain, the total derivative vanishes and
covariant integration by parts gives the twelve-column numerator

\[
\boxed{
(-11,6,-28,-3,35/9,-14/3,14/3,-208/9,
-64/3,-16/3,-44/9,-80/9).
}
\]

The columns are

\[
\begin{array}{llll}
D_1=(\nabla R)^2,&D_2=(\nabla R_{mn})^2,
&D_3=\nabla_nR_{jk}\nabla_kR_{jn},
&D_4=(\nabla R_{mnrs})^2,\\
C_1=R^3,&C_2=RR_{mn}R^{mn},
&C_3=RR_{mnrs}R^{mnrs},
&C_4=R_{jk}R_{jn}R_{kn},\\
C_5=R_{ij}R_{kl}R_{ikjl},
&C_6=R_{jk}R_{jnli}R_{knli},
&C_7=I_1,&C_8=I_2.
\end{array}
\]

No derivative or Ricci direction is discarded before the numerical rank test.

## 2. Exact mixed-source engine

The fundamental source is the densitized inverse metric

\[
\mathcal H^{\mu\nu}
=\delta^{\mu\nu}+\epsilon_1h_1^{\mu\nu}
+\epsilon_2h_2^{\mu\nu}+\epsilon_3h_3^{\mu\nu}.
\]

The calculation uses three commuting nilpotent variables,
`epsilon_i^2=0`. Their product coefficient is exactly the mixed derivative
`partial_1 partial_2 partial_3`; no small source amplitude or subtraction of
large nearly equal numbers is used. In four dimensions,

\[
\sqrt g=\sqrt{\det\mathcal H},\qquad
g^{\mu\nu}=\mathcal H^{\mu\nu}/\sqrt g,\qquad
g_{\mu\nu}=\sqrt g\,(\mathcal H^{-1})_{\mu\nu}.
\]

The engine constructs the Levi-Civita connection, full Riemann tensor, Ricci
tensor, scalar curvature and first covariant derivatives, contracts every
index with the exact inverse metric, multiplies by `sqrt(g)`, and integrates
spectrally on a periodic torus.

Twelve deterministic random real source triples obey `q1+q2+q3=0`. Their
metric and curvature symmetry residuals remain below `1.852e-12`. Repeating
the first two complete calculations on `8^4` instead of `6^4` changes the
template vector by at most `2.414e-15` relative. The mixed source contains no
frequency above the resolved spectral band, so this is an exact grid
arbitration rather than a claimed spacetime continuum limit.

## 3. Rank-eight quotient

After column normalization, the singular values are

\[
\begin{aligned}
&(2.92576,1.39423,1.03866,0.457893,0.375827,0.219656,
0.121837,0.0568994,\\
&\qquad 1.17\times10^{-16},7.28\times10^{-17},
2.16\times10^{-17},1.04\times10^{-17}).
\end{aligned}
\]

The unambiguous numerical rank is eight. Pivoted QR selects

\[
\boxed{(D_1,D_4,C_7,C_4,C_8,C_1,C_3,C_5)}
\]

as one convenient quotient basis. Rational reconstruction of the four
dependent cubic-response columns gives

\[
\boxed{D_3=\tfrac14D_1-C_4+C_5,}
\]

\[
\boxed{
\begin{aligned}
D_2={}&\tfrac14D_1+\tfrac14D_4-\tfrac5{36}C_7
-\tfrac89C_4-\tfrac{11}{9}C_8-\tfrac1{72}C_1
+\tfrac1{24}C_3+\tfrac43C_5,
\end{aligned}}
\]

\[
\boxed{
C_2=-\tfrac19C_7+\tfrac89C_4+\tfrac29C_8
+\tfrac5{36}C_1+\tfrac1{12}C_3+\tfrac23C_5,
}
\]

\[
\boxed{
C_6=\tfrac29C_7+\tfrac29C_4-\tfrac49C_8
-\tfrac1{36}C_1+\tfrac1{12}C_3+\tfrac23C_5.
}
\]

These are identities of the integrated cubic response around flat space—the
object required for TTT projection. They are not used to claim that a chosen
local density is unique before boundary terms and field redefinitions.

## 4. Ricci-flat map and sign convention

On a Ricci-flat metric, `D1=D2=D3=C1=...=C6=0`. The `C2` or `C6` identity
then gives

\[
\boxed{C_8=\tfrac12C_7.}
\]

The `D2` identity gives

\[
0=\tfrac14D_4-\tfrac5{36}C_7-\tfrac{11}{9}C_8,
\qquad
\boxed{D_4=3C_7}
\]

in the geometric engine convention.

For the same traceless `H` polarization, `g_mn=delta_mn-h_mn+O(h^2)`.
Consequently the engine's linearized Weyl tensor is the negative of the
checkpoint-4909 source convention. Derivative-squared columns do not change,
whereas cubic-curvature columns and the target `C^3` do. In the 4909 target
normalization the quotient functional is

\[
\boxed{
v_{RF}=(0,0,0,-3,0,0,0,0,0,0,-1,-1/2).
}
\]

It annihilates all four measured null directions below `8.89e-16`; the
largest leave-one-geometry value is `5.42e-15`. The physical Ricci-flat
coefficient is therefore quotient-invariant.

## 5. Free source-vector recovery

After converting the source convention into the engine convention, the
minimal-scalar vector is

\[
c_{a6}=\frac1{7!}
(-11,6,-28,-3,-35/9,14/3,-14/3,208/9,
64/3,16/3,44/9,80/9).
\]

For `y=M c_a6`, the normalized pseudoinverse gives a different coefficient
representative, as it must in a rank-eight quotient, but

\[
\frac{\|M\hat c-y\|}{\|y\|}=5.6624\times10^{-16},
\]

and

\[
v_{RF}\cdot\hat c=v_{RF}\cdot c_{a6}=-\frac1{15120}.
\]

The Euclidean proper-time determinant contributes the overall
`-1/[2(4 pi)^2 m^2]`, yielding

\[
\boxed{
\zeta_s=\frac1{30240(4\pi)^2m^2}.
}
\]

All twelve leave-one-geometry inversions retain rank eight. Their largest
absolute error in `zeta_s` is `3.62e-19`.

## 6. What is and is not closed

Closed here:

- the complete sourced minimal-scalar integrated `a6` input;
- exact nonlinear mixed metric templates for all twelve raw columns;
- the rank-eight TTT quotient and four rational dependencies;
- the Ricci-flat quotient functional including the `H`/metric sign map;
- recovery of the known coefficient from the sourced quotient response;
- grid and leave-one-geometry stability of the geometric inverse.

Still open:

- independent recovery from exact free lattice determinant responses;
- `am -> 0` and `N am -> infinity` with at least two stencils;
- a covariance-weighted inverse for Monte Carlo data;
- the interacting motion-scalar stress TTT numerator;
- metric/ghost, bath and Wilsonian boundary contributions to the total parent
  coefficient.

Therefore:

```text
single TT projector                    = rejected at 4910;
full geometric a6 quotient             = derived and validated;
known sourced scalar quotient          = recovered;
independent free lattice recovery      = next required gate;
interacting long run                   = withheld;
GR/Newton/PPN                          = unchanged;
Maxwell/Poynting                       = unchanged;
Gamma_MTS,res                          = 0.
```

## 7. Next target

`4912-Y5-R2FR-free-lattice-multigeometry-a6-response-and-continuum-projector-recovery.md`

The next checkpoint must calculate exact free determinant TTT responses for
the rank-eight source ensemble, separate `q0`, `q2`, `q4` and regulator terms,
and recover the same quotient coefficient while `am` decreases and `Nam`
increases. Only that independent success permits the interacting sampler to
start.

No GitHub action or public claim is authorized.

## Sources

- `post-checkpoint-work/source-intake/heat_kernel_a6/4881/hep-th-0306138.tar`
- `post-checkpoint-work/4881-Y5-R2FR-compact-matter-interior-EOS-contact-matching-and-Riemann-cubed-coefficient-owner-gate.md`
- `post-checkpoint-work/4905-Y5-R2FR-first-nontrivial-MTS-to-SM-gravity-operator-basis-and-independent-observable-gate.md`
- `post-checkpoint-work/4908-Y5-R2FR-microscopic-MTS-metric-three-point-vertex-and-Weyl-cubic-coefficient-or-zero-residual-theorem.md`
- `post-checkpoint-work/4910-Y5-R2FR-motion-scalar-cutoff-volume-extrapolation-and-TTT-Weyl-cubic-projection.md`
- `post-checkpoint-work/scripts/Y5_R2FR_4911_full_offshell_a6_template_projector.py`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_4911_DECISION.csv`

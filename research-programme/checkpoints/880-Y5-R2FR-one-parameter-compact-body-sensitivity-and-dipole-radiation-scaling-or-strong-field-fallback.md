# 4864 - Public-branch compact-body sensitivity and dipole-radiation gate

Marker: `COMPACT_BODY_SENSITIVITY_DIPOLE_4864`

Decision: `PUBLIC_BRANCH_COMPACT_SENSITIVITY_REGULAR_AND_TRIPLE_DIPOLE_SMOKE_WINDOW_SURVIVES_SIGMA_PRIME_STRONG_PREFERRED_FRAME_OPEN_PRIVATE_NONCLAIM`

## Scope

This checkpoint projects the selected public `gHat` coefficient surface into the compact-body variables and radiation formulas of Gupta et al. It does not identify MTS with Einstein-aether theory as a microscopic theory. It tests the already selected local correspondence action in a source-backed strong-field language.

The galaxy programme is also rebased as an existing empirical pillar from the current read-only `MTS-Galaxy-Lab-` snapshot. No galaxy-repository file is modified.

## Exact coefficient map

Write `d=rp`, with `0<p<=p_uniform` and `0<r<=1/3`. In the public matter frame,

\[
c_a=\frac{2rp}{1+r},\qquad
c_\theta=\frac{2p}{(1+r)(1-p)},\qquad
c_\sigma=0,\qquad
c_\omega=p(1+r-rp).
\]

The PPN and mode quantities become

\[
\alpha_1=-\frac{8rp}{1+r},\qquad
\alpha_2=-\frac{rp(1-3r)}{1+r},
\]

\[
c_T^2=1,\qquad
c_V^2=\frac{(1+r)(1+r-rp)}{4r},\qquad
c_S^2=\frac1{3r},\qquad Z=1+r.
\]

All ten identities are verified symbolically by the 4864 generator.

## Compact-body sensitivity

Gupta et al. define the rescaled sensitivity `s=sigma/(1+sigma)` and give its Tolman VII expansion through `C^3`. Substitution of the public surface cancels every apparent `alpha1` and `c_omega` pole:

\[
\boxed{s=pF(p,r,C)+O(C^4).}
\]

The first two reduced coefficients are

\[
\frac{S_1}{p}=\frac{10r(3r+11)}{21(1+r)},
\]

\[
\frac{S_2}{p}=\frac{5r}{63063(1+r)^2}
\left[1377pr^3+3666pr^2+7793pr-27117r^3-143271r^2-209761r-93607\right].
\]

The exact `S3/p` rational polynomial is retained in the executable output. At the worst public endpoint `r=1/3`,

\[
F=\frac{10}{7}C
+\frac{5(1146p-67669)}{126126}C^2
+\frac{788040p^2-19596941p+975961420}{90053964}C^3.
\]

An exact multivariate Bernstein-basis certificate proves `partial_C F>=0` and `partial_r F>=0` on

```text
0 <= p <= 1.393e-6,
0 <= r <= 1/3,
0 <= C <= 0.3.
```

At `r=1/3,C=0.3`, `partial_p F<0` throughout this interval. Therefore

\[
\boxed{0\le F\le F_{\max}=\frac{204098}{425425}=0.479750837397896\ldots}
\]

and `s<=p Fmax` without a grid-only assumption.

## Triple-system gate

For PSR J0337+1715, Gupta et al. quote

\[
\delta_a=(0.5\pm1.8)\times10^{-6}.
\]

The exact map from rescaled sensitivity is

\[
|\delta_a|=\frac{2|s|}{2-s}.
\]

Using the conservative positive two-sigma envelope `delta_max=4.1e-6` gives

\[
p<8.54609\times10^{-6}.
\]

This is over six times weaker than the existing uniform weak-field corridor

\[
p_{\rm uniform}=1.3928203230\times10^{-6}.
\]

At `p_uniform`, the worst compactness envelope predicts `delta_a<=6.68207e-7`.

The same endpoint gives `|alpha1|<=2p_uniform=2.78564e-6`, below the `2.4e-5` joint binary-plus-triple magnitude reported by Gupta et al.

## Binary-radiation gate

For a quasi-circular binary at negligible preferred-frame center-of-mass velocity,

\[
R_D=\frac5{32}\frac{\zeta_2(s_1-s_2)^2}{v^2}.
\]

On the public surface,

\[
p\zeta_2\longrightarrow
\sqrt{3r}(1+r)+\frac{16\sqrt r}{3(1+r)^2}.
\]

Both terms are monotone on `0<r<=1/3`; the exact finite-`p` maximum is also at `r=1/3`. Hence `s=O(p)` and `zeta2=O(1/p)` combine to give

\[
\boxed{R_D=O(p),}
\]

not a divergent strong-field endpoint.

For PSR J1738+0333, using the source masses, period and period derivative gives

```text
C_NS(nominal 12.4 km) = 0.17386069
v^2                     = 1.40012874e-6
Pbdot_GR                = -2.74609332e-14
two-sigma extra-loss allowance = 0.17621640
```

The deliberately stronger envelope `C_NS<=0.3`, `C_WD<=1e-4`, with no cancellation or reduced-prefactor credit, gives

```text
R_D/p                   = 7.87820349e4
R_D(p_uniform)          = 0.10972922
p_dipole,max            = 2.23675866e-6
```

Inflating the complete sensitivity amplitude by the source-reported `3%` equation-of-state variation gives

```text
R_D,3%                  = 0.11641173
p_dipole,max,3%         = 2.10835956e-6
```

and still leaves the weak-field corridor intact. The envelope could tolerate a common sensitivity increase of `26.7%` before touching this smoke boundary.

The quadrupole combinations are regular:

\[
\lim_{p\to0}\frac{\Psi_1-1}{p}
=\frac{3r^3\sqrt{3r}}{2(1+r)},
\]

\[
\lim_{p\to0}\Psi_2=-3\sqrt3r^{5/2},
\]

\[
\lim_{p\to0}p\Psi_3
=\frac{8r^{3/2}}{(1+r)^4}
+\frac{3\sqrt3}{2}(1+r)r^{3/2}.
\]

At the worst endpoint their fractional scale at `p_uniform` is below `4e-8`, negligible beside the deliberately un-cancelled dipole term.

## Galaxy pillar accounting

The current public snapshot at commit `5c2fc082adcc67d779cfd99d5b6e9a9c9ac5fcbd` contains:

- 175 bundled SPARC-derived LTGs and 16 ATLAS3D ETGs;
- locked constants and reproducible case/claim/QA exports;
- route-stratified holdouts, null tests, bootstrap and jackknife tooling;
- the v18.10 release candidate with all-galaxy mean RMSE `21.90 km/s`, clean mean RMSE `19.33 km/s`, and median high-RMSE holdout gain `66.68%`;
- later v18.38 metadata with `71.44%` clean high-RMSE gain, zero protected regression and a positive branch-shuffle margin.

This is substantial empirical work and is now treated as such in the unified spine. The important caveat is also retained: the later release candidate still uses its exact tested support cache as the source of truth, and the native expression is not yet a compact parent-derived law.

## Decision

The public `gHat` branch survives the first source-backed compact-body sensitivity, triple-system and dipole-radiation smoke gate. This is meaningful progress: the small-`p` compact-body limit is regular and leaves a nonempty observational window.

It is not full strong-field closure. Gupta et al. explicitly warn that existing strong-field `hat alpha1` and `hat alpha2` priors require derivatives of the sensitivities. Equation 80 determines `s`, not the independent second velocity response `sigma'`. A full stellar ODE/likelihood remains desirable, and the next hard derivation is therefore the second sensitivity response.

Next: `4865-Y5-R2FR-second-sensitivity-derivative-and-strong-field-preferred-frame-gate-or-public-branch-fallback.md`.

Sources: [Gupta et al. 2021](https://arxiv.org/abs/2104.04596); [Foster 2006](https://arxiv.org/abs/gr-qc/0602004); [MTS Galaxy Lab snapshot](https://github.com/Martin123132/MTS-Galaxy-Lab-/tree/5c2fc082adcc67d779cfd99d5b6e9a9c9ac5fcbd).

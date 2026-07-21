# 4919 - Vacuum 1PI factorization, curvature-Higgs reduction and hidden-VEV gate

Marker: `MTS_VACUUM_1PI_HIGGS_HIDDEN_VEV_GATE_4919`

## Decision

Checkpoint 4918 removed the state-flow contact from the declared active
metric-only baseline but left flow-independent vacuum mixed operators open.
The next operator pass now gives a constructive result rather than another
missing-coefficient ledger.

The active parent inherited from checkpoint 4905 factorizes at fixed metric:

\[
S_{\rm parent}[\chi,\Phi,g]
=S_X[\chi,g]+S_{\rm SM}[\Phi,g].
\]

Therefore its fixed-metric path integral, connected generator and 1PI
functional factorize. In particular,

\[
\boxed{
\frac{\delta^2\Gamma}
{\delta\bar\chi\,\delta\bar\Phi}=0
}
\]

for every direct hidden--visible vertex. This remains true if an invariant
hidden even operator has a nonzero vacuum expectation value: the expectation
value changes `Gamma_X[g]`, not a Standard-Model coefficient. A direct term
such as `I_X H^dagger H`, `I_X F^2` or `I_X bar f f` requires a mixed parent
vertex that is absent from the active action.

The result does **not** remove internal-graviton diagrams. Those are a
separate gravity-mediated 1PI class and form the next target.

The apparently surviving operator

\[
\xi_H R H^\dagger H
\]

is not a direct MTS portal on this parent. It is the ordinary symmetry-allowed
curved-Standard-Model coefficient. It also cannot simply be called zero or
discarded. After the vacuum part is absorbed into the measured Planck residue,
an explicit metric redefinition moves it to a correlated Higgs--trace
operator. Diagonalizing the Higgs--metric kinetic system then proves that its
curvature-induced force has

\[
\boxed{
0\leq\alpha_\xi
=\frac{2x}{1+6x}<\frac13,
\qquad
x=\frac{\xi_H^2v^2}{\overline M_{\rm Pl}^2},
}
\]

for every real `xi_H`, without selecting or fitting `xi_H`. Its only pole is
the physical Standard-Model Higgs. With `m_h=125.13 GeV`,

\[
\boxed{\lambda_h=1.5769758\times10^{-18}\ {\rm m}.}
\]

At a one-femtometre positive gap, the curvature-induced point-force ratio is
already below `10^-273.071`. At the shortest Eot-Wash separation of
`52 micrometres`, its log-base-ten upper bound is
`-1.4320646657080e13`. The low-momentum expansion is a local `T_SM^2`
contact and has exactly zero cross support for separated bodies.

For clocks or test bodies inside matter, where support does overlap, canonical
normalization also gives

\[
g_\xi^2\leq\frac{1}{6\overline M_{\rm Pl}^2}.
\]

Using a deliberately conservative laboratory mass-density envelope of
`3.0e4 kg m^-3`, the corresponding local fractional clock/mass shift is below
`2.32073e-58`, and the contact self-energy fraction is below
`1.16036e-58`. Thus the curvature-Higgs channel is locally harmless without
pretending its finite renormalized coefficient has been predicted.

```text
direct fixed-metric MTS--SM vacuum portals = exact zero;
hidden odd one-point functions              = zero on selected invariant branches;
hidden even condensate direct portals       = exact zero by factorization;
ordinary total xi_H                         = allowed and not predicted;
R HdagH basis monomial                      = moved, not erased;
physical curvature-induced pole             = 125.13 GeV Higgs only;
curvature-induced Yukawa strength           = alpha_xi < 1/3 for all real xi_H;
R10/PPN/clock/orbit exterior residual        = exponentially negligible;
overlap contact clock/WEP residual           = bounded below 2.32e-58;
internal-graviton mixed running              = still open;
pure-metric vacuum residuals                 = remain in their existing ledger.
```

## 1. Fixed-metric factorization theorem

Introduce independent sources for the hidden and visible fields while holding
the public metric fixed. The parent action gives

\[
Z[g,J_X,J_{\rm SM}]
=\int D\chi\,e^{iS_X+iJ_X\chi}
 \int D\Phi\,e^{iS_{\rm SM}+iJ_{\rm SM}\Phi}
=Z_X[g,J_X]Z_{\rm SM}[g,J_{\rm SM}].
\]

Hence

\[
W[g,J_X,J_{\rm SM}]
=W_X[g,J_X]+W_{\rm SM}[g,J_{\rm SM}],
\]

and the independent Legendre transform gives

\[
\boxed{
\Gamma[g,\bar\chi,\bar\Phi]
=\Gamma_X[g,\bar\chi]+\Gamma_{\rm SM}[g,\bar\Phi].
}
\]

Every fixed-metric mixed functional derivative therefore vanishes. In a local
operator expansion this sets the direct hidden-threshold contributions to

\[
I_XH^\dagger H,
\quad I_XF_{\mu\nu}F^{\mu\nu},
\quad I_X\bar f f,
\quad (\nabla I_X)J_{\rm SM}
\]

to zero. This is an action theorem, not a numerical cancellation.

Integrating the hidden field around a saddle or vacuum state gives

\[
\Gamma_{\rm eff}[g,\Phi]
=\Gamma_X[g;\langle\chi\rangle]
+\Gamma_{\rm SM}[g,\Phi].
\]

An odd or even hidden expectation value may alter the cosmological term,
Einstein residue, curvature coefficients or nonlocal pure-metric form
factors. It cannot manufacture a visible operator when the parent Hessian has
no mixed block.

The theorem has a precise boundary. Once the metric is integrated over,
graviton lines can connect hidden and visible stress vertices. Checkpoints
4917--4918 closed the state-flow contact on the active branch. Vacuum
graviton-mediated running remains to be calculated rather than being hidden
inside the factorization statement.

## 2. Hidden vacuum branches

The direct-portal theorem does not require every hidden condensate to vanish,
but the selected invariant branches can still be stated accurately.

### 2.1 Motion scalar

The printed dimensionless potential is

\[
V(\varphi)=\frac34|\varphi|^{4/3}\geq0,
\]

with equality only at `varphi=0`. The finite-cutoff lattice measure of
checkpoint 4909 is positive, confining and `Z2` even, so its finite-volume odd
one-point function vanishes:

\[
\langle\varphi\rangle=0.
\]

This does not promote the provisional lattice mass gap to a continuum theorem
and does not independently exclude spontaneous breaking in every continuum
completion.

### 2.2 Canonical memory scalar

On the flat `T=R=0` vacuum anchor, the positive quartic branch has `M=0`.
The density/curvature-supported nonzero branch studied in checkpoints
4885--4886 is not silently imported: its significant cosmological version was
demoted after the local scalar and Cassini analysis. If such a branch is
reintroduced, factorization must be changed by an explicit matter vertex and
the extension gates apply.

### 2.3 Bath oscillators

A zero-source invariant equilibrium has zero coherent displacement,

\[
\langle\chi_\Omega\rangle=0,
\]

while quadratic fluctuations remain nonzero and contribute to the hidden
determinant. A coherent displacement is a prepared nonvacuum state and belongs
to `Gamma_MTS,res`, not the active metric-only baseline.

Thus the honest result is stronger than proving three zeros separately:
even if an invariant quadratic condensate survives, it still has no direct
visible portal on the factorized parent.

## 3. Curvature-Higgs basis reduction

Write the ordinary curved-SM action as

\[
S_J=\int d^4x\sqrt{-g}\left[
\left(\frac{M_R^2}{2}+\xi_H H^\dagger H\right)R
+\mathcal L_{\rm SM}
\right].
\]

With

\[
H=\frac1{\sqrt2}\binom{0}{v+h},
\qquad
X_v:=H^\dagger H-\frac{v^2}{2}=vh+\frac{h^2}{2},
\]

the vacuum residue is

\[
\boxed{
\overline M_{\rm Pl}^2=M_R^2+\xi_Hv^2.
}
\]

The remaining local monomial is `xi_H X_v R`. At first EFT order perform the
inverse-metric redefinition

\[
\delta g^{\mu\nu}
=\frac{2\xi_H}{\overline M_{\rm Pl}^2}X_vg^{\mu\nu}.
\]

Using `g^{mu nu}G_{mu nu}=-R` in four dimensions,

\[
\delta S_{\rm EH}
=-\int d^4x\sqrt{-g}\,\xi_HX_vR,
\]

so the curvature monomial cancels. But the matter variation is

\[
\delta S_{\rm SM}
=-\frac12\int\sqrt{-g}\,T^{\rm SM}_{\mu\nu}\delta g^{\mu\nu}
=-\int\sqrt{-g}\,
\frac{\xi_H}{\overline M_{\rm Pl}^2}X_vT_{\rm SM}.
\]

Therefore

\[
\boxed{
\xi_HX_vR
\quad\Longleftrightarrow\quad
-\frac{\xi_H}{\overline M_{\rm Pl}^2}
\left(vh+\frac{h^2}{2}\right)T_{\rm SM}
}
\]

at this order. The operator has moved basis; it has not disappeared.

## 4. Canonical Higgs pole and strength theorem

The exact vacuum quadratic diagonalization is most transparent through the
Einstein-frame factor

\[
\Omega^2
=\frac{M_R^2+2\xi_HH^\dagger H}
{\overline M_{\rm Pl}^2}.
\]

At the vacuum, `Omega=1` and the physical Higgs fluctuation has

\[
\boxed{
Z_h=1+\frac{6\xi_H^2v^2}{\overline M_{\rm Pl}^2}
=1+6x>0.
}
\]

Writing `h_c=sqrt(Z_h) h`, the curvature-induced trace coupling is

\[
\boxed{
g_\xi
=\frac{\xi_Hv}
{\overline M_{\rm Pl}^2\sqrt{Z_h}}.
}
\]

Two nonrelativistic point sources therefore receive the extra Yukawa
potential

\[
\frac{V_\xi(r)}{V_N(r)}
=\alpha_\xi e^{-r/\lambda_h},
\qquad
\alpha_\xi=2\overline M_{\rm Pl}^2g_\xi^2
=\frac{2x}{1+6x}.
\]

For `x>=0`,

\[
\frac13-\alpha_\xi
=\frac{1}{3(1+6x)}>0.
\]

This proves the coefficient-independent strength envelope. It is specifically
the curvature-induced increment. Ordinary Standard-Model Higgs exchange is
already part of the known SM limit and is not relabelled as an MTS residual.

Integrating out the physical Higgs gives

\[
\boxed{
\Delta\Gamma_{\rm trace}
=\frac{g_\xi^2}{2}
\int\sqrt{-g}\,
T_{\rm SM}(m_h^2-\Box)^{-1}T_{\rm SM}.
}
\]

At `q^2<<m_h^2`,

\[
\Delta\mathcal L
=\frac{g_\xi^2}{2m_h^2}T_{\rm SM}^2
+O(\Box/m_h^4),
\]

with

\[
\frac{g_\xi^2}{2m_h^2}
<\frac{1}{12\overline M_{\rm Pl}^2m_h^2}
=8.97393\times10^{-43}\ {\rm GeV}^{-4}.
\]

In the original curvature basis the same low-energy pole contributes

\[
\Delta a_{R,H}
=\frac{\xi_H^2v^2}{2Z_hm_h^2}.
\]

The value depends on `xi_H`, while the local force and contact envelopes do
not.

## 5. Arena projections

For a point Yukawa potential, the point-force ratio is

\[
\left|\frac{\Delta F_\xi}{F_N}\right|
\leq\frac13(1+s)e^{-s},
\qquad s=\frac r{\lambda_h}.
\]

The calculation is performed in logarithms to avoid numerical underflow.

| arena | distance | `r/lambda_h` | log10 potential upper | log10 point-force upper |
|---|---:|---:|---:|---:|
| one femtometre | `1e-15 m` | `6.3412e2` | `-275.874` | `-273.071` |
| atomic | `1e-10 m` | `6.3412e7` | `-2.7539706e7` | `-2.7539698e7` |
| R10 | `52e-6 m` | `3.2981e13` | `-1.4320646657094e13` | `-1.4320646657080e13` |
| Galileo altitude | `2.3229e7 m` | `1.4724e25` | `-6.3971981e24` | `-6.3971981e24` |
| one Earth radius | `6.371e6 m` | `4.0400e24` | `-1.7545546e24` | `-1.7545546e24` |

The full pole is exponentially small rather than mathematically zero. The
strict low-`q` contact expansion has exactly zero cross support whenever the
source supports have a positive gap. These statements are not interchangeable.

For overlapping ordinary matter, let `rho_E` be the local rest-energy
density. The induced field and contact self energy obey

\[
|\delta\ln m|\lesssim
\frac{\rho_E}{6\overline M_{\rm Pl}^2m_h^2},
\qquad
\frac{|\Delta\rho|}{\rho_E}
\lesssim
\frac{\rho_E}{12\overline M_{\rm Pl}^2m_h^2}.
\]

At the declared laboratory-density envelope these are `2.32073e-58` and
`1.16036e-58`. This bounds rather than erases possible composition-dependent
self-energy. It is far below current clock or WEP sensitivity.

Classical Maxwell theory has `T_Maxwell=0` in four dimensions, so the tree
trace channel vanishes. The Standard-Model trace anomaly and ordinary
Higgs--photon loop are not zero, but they retain the same Higgs pole and are
not a long-range MTS force.

## 6. Coefficient ownership

The coefficient ledger is now:

\[
\boxed{
\xi_H^{\rm direct\ MTS}=0
}
\]

for hidden loops at fixed metric, while

\[
\xi_H^{\rm total}(\mu)
=\xi_H^{\rm SM}(\mu)
+\xi_H^{\rm graviton}(\mu)
+\xi_H^{\rm finite}(\mu)
\]

remains an ordinary renormalized EFT coefficient. Setting the direct MTS
piece to zero does not set the total coefficient to zero.

The 2012 Atkins--Calmet collider result `|xi_H|<2.6e15` is retained only as a
historical algebra cross-check. At that value the present normalization gives
`Z_h=1.4146007` and `alpha_xi=0.0976956`. It is not treated as a current
likelihood or as an MTS prediction.

## 7. Gate arbitration

| gate | result |
|---|---|
| direct fixed-metric hidden--SM vacuum portal | closed exactly |
| hidden odd VEVs | zero on selected invariant branches |
| hidden even condensate portal | closed exactly without requiring condensate zero |
| curvature-Higgs field basis | reduced to correlated trace kernel |
| canonical kinetic sign | positive for every real `xi_H` |
| extra pole | none; physical Higgs only |
| strength | `alpha_xi<1/3` without a coefficient fit |
| separated-source R10/PPN/clock/orbit | passed for this channel |
| overlapping clock/WEP self contact | bounded below `2.33e-58` |
| classical Maxwell trace channel | zero |
| total finite `xi_H` prediction | open |
| internal-graviton mixed 1PI running | open |
| public unified-theory claim | not made |

The important advance is that local safety of this channel no longer waits
for a numerical parent value of `xi_H`. The canonical normalization itself
bounds the strength, and the measured Higgs mass fixes the range.

## 8. Limits

This checkpoint does not prove:

- that the total renormalized `xi_H(mu)` is zero or predicted by MTS;
- that no graviton-mediated hidden--visible running exists;
- that the provisional motion-scalar mass gap has a continuum limit;
- that every possible nonvacuum hidden state has zero one-point functions;
- that Higgs collider or high-curvature constraints are automatically passed;
- that pure-metric `C^3` and nonlocal vacuum residuals vanish;
- strong-field equivalence for compact objects.

It does prove that a hidden VEV cannot bypass fixed-metric factorization, and
that the ordinary curvature-Higgs channel cannot produce an observable
long-range local-gravity residual on the selected active branch.

## 9. Reproducibility

Research script:

`post-checkpoint-work/scripts/Y5_R2FR_4919_vacuum_1PI_higgs_hidden_vev.py`

Validation script:

`post-checkpoint-work/scripts/Y5_R2FR_4919_vacuum_1PI_higgs_hidden_vev_validation.py`

Evidence tables:

- `P8_Y5_R2FR_4919_FACTORIZATION.csv`
- `P8_Y5_R2FR_4919_HIDDEN_VACUUM.csv`
- `P8_Y5_R2FR_4919_CURVATURE_HIGGS_BASIS.csv`
- `P8_Y5_R2FR_4919_HIGGS_TRACE_KERNEL.csv`
- `P8_Y5_R2FR_4919_LOCAL_RANGE_PROJECTION.csv`
- `P8_Y5_R2FR_4919_COEFFICIENT_OWNERSHIP.csv`
- `P8_Y5_R2FR_4919_GATE_DECISION.csv`
- `P8_Y5_R2FR_4919_SOURCE_REGISTER.csv`

Primary external calibration/context:

- [Particle Data Group 2026 Higgs listing](https://pdg.lbl.gov/encoder_listings/s126.pdf).
- [NIST CODATA Fermi coupling constant](https://physics.nist.gov/cgi-bin/cuu/Value?gf).
- [Atkins and Calmet, nonminimal Higgs coupling](https://arxiv.org/abs/1211.0281).
- [Lee et al., 2020 short-range gravity test](https://arxiv.org/abs/2002.11761).

## 10. Next target

`4920-Y5-R2FR-graviton-mediated-curvature-Higgs-running-and-current-Higgs-coupling-bound-or-vacuum-local-GR-promotion-gate.md`

Compute the mixed diagrams not covered by fixed-background factorization,
separate scheme-dependent running from on-shell Higgs observables, update the
historical collider comparator with current primary coupling data, and decide
whether the invariant-vacuum local-GR certificate can be promoted while
leaving pure-metric higher-curvature residuals explicitly separate.

No GitHub action or public claim is authorized.

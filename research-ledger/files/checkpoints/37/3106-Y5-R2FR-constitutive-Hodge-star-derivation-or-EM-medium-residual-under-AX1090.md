# 3106 - Y5 R2FR constitutive Hodge-star derivation or EM-medium residual under AX1090

**Purpose:** follow `3105` properly. The question is whether MTS can derive the public electromagnetic Hodge structure

```text
H = Z_Q *_{g_pub} F
```

from a background/flow/constitutive law, rather than merely assuming metric Maxwell. This also records the Newton-constant point: GR uses an empirical coupling constant; reducing to GR/Newton needs calibration to `G`, while deriving `G` is a separate higher-value target.

**Verdict:** the EM constitutive route is promising but not closed by the current corpus. It can plausibly derive the public light cone/Hodge side if MTS supplies a local reciprocal nonbirefringent positive constitutive tensor. Current files mostly address EM kinetic ownership and alpha drift, not a parent `chi -> Hodge` derivation. Therefore the route is retained as a real derivation target, with explicit EM-medium residuals if it fails.

## Source Register

| source_id | source | role |
|---|---|---|
| SRC3106_0 | `3105-Y5-R2FR-EM-wave-Poynting-public-geometry-route-under-AX1090.md` | Poynting route and double-counting guard |
| SRC3106_1 | `1057-Y5-R10-unique-Maxwell-subblock-no-independent-F2-ban-or-balpha-retention.md` | unique Maxwell subblock target; no-independent-`F_Q^2` not derived |
| SRC3106_2 | `1109-Y5-R10-no-independent-lambda-F2-theorem-or-finite-alpha-coefficient-acquisition.md` | universal lambda is calibration-only; nonuniversal lambda is finite alpha residual |
| SRC3106_3 | `1234-Y5-R10-EM-owner-uniqueness-or-quark-gluon-edge-owner-proof.md` | EM owner uniqueness still blocked by unique `F_Q^2`, current normalization, and readout descent |
| SRC3106_4 | `1014-Y5-R10-PiM-commutator-projector-variation-zero-or-coefficient-bound.md` | Hodge/projector metric-dependence can carry stress unless handled |
| SRC3106_5 | `1135-Y5-R10-FD-gradient-flow-constitutive-law-or-epsilon-closure-demotion.md` | constitutive-law analogy exists but was not derived from parent variables |
| SRC3106_6 | `1012-Y5-R10-Y5-source-normalization-owner-or-q_loc-bound-implementation.md` | constant/universal coupling and measured-GM source normalization remain separate blockers |
| SRC3106_7 | `1148-Y5-R10-cR11-source-normalization-owner-or-zero-theorem.md` | local source normalization needs same coframe, constant coupling, and parent source charge |

## Constitutive Starting Point

Do not start by assuming metric Maxwell. Start with the premetric form:

```text
dF = 0
dH = J
H^{mu nu} = (1/2) chi^{mu nu alpha beta} F_{alpha beta}.
```

Here:

```text
F = electromagnetic field strength
H = excitation/response two-form density
J = electric current
chi = MTS/public-background constitutive tensor
```

The target is to show that in the compact local branch

```text
chi^{mu nu alpha beta}
  = Z_Q sqrt(-g_pub) (g_pub^{mu alpha} g_pub^{nu beta}
                    - g_pub^{mu beta} g_pub^{nu alpha})
    + topological_axion_piece_if_fixed
```

so that

```text
H = Z_Q *_{g_pub} F.
```

This is the exact mathematical version of “the Poynting vector works on the background field”: the background must define the Hodge/constitutive map that turns `F` into `H`, and the energy flux then follows from the same public structure.

## Derivation Attempt

The route would close if MTS proves all of these:

| clause_id | clause | mathematical role | current status |
|---|---|---|---|
| CHS3106_0_local_linear | `chi` is local, linear, and fixed before readout | avoids post-fit optical medium | not parent-derived here |
| CHS3106_1_reciprocal | `chi^{mu nu alpha beta}=chi^{alpha beta mu nu}` up to fixed topological term | gives action principle `S_EM=-1/2 int F wedge H` | not parent-derived here |
| CHS3106_2_no_skewon | dissipative/skewon part vanishes | prevents non-Hilbert EM stress and preferred-frame loss | not parent-derived here |
| CHS3106_3_nonbirefringent | Fresnel quartic is a double light cone | derives conformal class `[g_pub]` | not parent-derived here |
| CHS3106_4_positive_energy | EM energy density and Poynting flux are positive in local branch | fixes physical sign/time orientation | not parent-derived here |
| CHS3106_5_impedance_owner | scalar `Z_Q` is quotient-owned/fixed representation data | prevents `b_alpha` and impedance drift | blocked by prior EM-owner work |
| CHS3106_6_same_public_metric | the `g_pub` in `*_{g_pub}` is the same metric used by matter/clocks/source | prevents optical-metric versus matter-metric split | needs public geometry rule |
| CHS3106_7_radiative_readout | effective/readout reductions do not regenerate `f(Xhat)F^2` | protects the tree-level route | unsigned in prior alpha-owner work |

If `CHS3106_0..7` pass, then EM waves do derive the public cone/Hodge structure:

```text
MTS chi
  -> nonbirefringent Fresnel cone
  -> [g_pub]
  -> H = Z_Q *_{g_pub} F
  -> T_EM_munu and Poynting flux in the same public geometry.
```

## What This Would Buy Us

If the constitutive theorem closes, it strengthens the local-GR branch in three ways:

1. **Public cone:** photons select the same local null cone as `g_pub`.
2. **Public stress:** Poynting flux is `T_EM^{0i}` in the same Hilbert stress ledger.
3. **No EM hidden source:** `Lie_vX Z_Q=0` removes alpha/impedance drift and prevents EM waves from sourcing hidden fifth-force terms.

This is not cosmetic. It would make the public metric less arbitrary: it would be the metric reconstructed from local wave propagation and energy flux.

## What It Still Does Not Buy Us

Even with the EM Hodge route closed, the gravitational left-hand operator is still not automatically EH.

The following theories can share the same local EM cone unless extra clauses exclude them:

```text
Einstein-Hilbert
f(R) or R^2 corrections
scalar-tensor gravity with quotient-fixed EM
torsion/nonmetricity sectors invisible to metric Maxwell at leading order
topological/boundary residuals
```

Therefore:

```text
EM/Hodge route derives or strengthens g_pub and T_EM.
EH/Newton route still needs S_pub principal-operator selection plus E_res_munu closure.
```

That split is the honest answer.

## EM-Medium Residual Vector

If the Hodge theorem does not close, retain:

| residual_id | residual | observable pressure | required closure |
|---|---|---|---|
| EMR3106_0_Delta_chi | nonmetric constitutive deviation | birefringence, anisotropic light speed, polarization-dependent propagation | prove metric Hodge reduction or bound `Delta_chi` |
| EMR3106_1_skewon | dissipative/nonreciprocal response | energy nonconservation, preferred-frame EM propagation | prove reciprocal action or bound skewon |
| EMR3106_2_axion | pseudoscalar/topological EM term | polarization rotation if spacetime-varying | fixed topological constant or sourced bound |
| EMR3106_3_impedance | `Z_Q` drift or hidden dependence | alpha drift, clocks, WEP composition, EM spectra | quotient-owned `Z_Q` or finite `b_alpha` row |
| EMR3106_4_optical_metric_split | photons see `g_EM != g_pub` | Shapiro/lightcone/clock/PPN mismatch | same public metric theorem |
| EMR3106_5_medium_stress | `chi` depends on hidden/domain variables | extra stress in `E_res_munu` | vary medium variables or bound stress |

These are not “vibes missing”; they are the exact ways the EM-wave route can fail.

## Newton Constant / Coupling Guard

The user point is correct:

```text
Newtonian gravity uses G as an empirical proportionality constant.
GR uses kappa = 8 pi G / c^4 as an empirical coupling in the field equation.
GR does not derive the numerical value of G.
```

So for MTS we must separate:

| level | target | status needed |
|---|---|---|
| G0_form | derive the form of the local equation | `G_munu + Lambda g_munu = kappa_* T_munu` or EH plus bounded residuals |
| G1_calibration | match the coupling to measured Newtonian gravity | `kappa_* = 8 pi G_meas/c^4` after source/GM transfer |
| G2_derivation | derive `G` or Planck scale from MTS primitives | parent action scale, cell measure, density, or normalization theorem |

Passing `G0` and `G1` is enough to say MTS reduces to GR/Newton in the same way GR reduces to Newton: the constant is measured/calibrated. Passing `G2` would be a bigger theoretical win, but it is not required for the first local-GR reduction.

The anti-circularity rule is:

```text
Do not use orbital GM as proof of the source charge before the Gauss/Poisson/source-transfer theorem.
```

But after the field equation and source charge are derived, calibration to measured `G` is legitimate. That is exactly how GR is normally used.

## Coupling Derivation Possibility

MTS could try to derive `G` only if it supplies a parent normalization law such as:

```text
1 / (2 kappa_*) = N_parent / L_parent^2
```

or

```text
kappa_*^{-1} = action_scale * cell_density * public_measure_factor
```

with all quantities fixed before readout. Without that, `kappa_*` is a universal coupling constant, not a derivation failure.

This means the project should not die on “does MTS derive G?” The first target is:

```text
derive the field equation form and prove the same source charge couples universally.
```

Then separately:

```text
try to derive the numerical coupling scale if MTS primitives contain the needed action/measure/cell normalization.
```

## Claim Status

No Maxwell-owner pass, no EM-medium pass, no `b_alpha=0`, no local-GR pass, no Newton pass, no PPN pass, and no derived-`G` claim follows from this checkpoint.

What is now clearer:

```text
EM wave/Poynting route can derive public cone/Hodge/stress if chi -> metric Hodge is parent-signed.
It cannot alone derive EH.
G calibration is allowed for GR reduction; G derivation is optional extra theory strength.
```

## Next Best Step

Write:

```text
3107-Y5-R2FR-Newton-constant-calibration-vs-parent-scale-derivation-under-AX1090.md
```

Task: formalize the `G0/G1/G2` split. First prove what is actually required for “reduces to GR/Newton”; then search the MTS primitives for a parent action scale/cell measure that could derive `kappa_*`. If no such primitive exists, keep `kappa_*` as a universal calibrated constant rather than pretending this is a fatal flaw.

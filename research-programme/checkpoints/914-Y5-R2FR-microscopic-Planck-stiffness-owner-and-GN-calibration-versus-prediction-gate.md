# 4898 - Microscopic Planck stiffness owner and Newton calibration-versus-prediction gate

Marker: `MTS_GN_CALIBRATION_VERSUS_PREDICTION_GATE_4898`

## Decision

This checkpoint resolves the immediate target without pretending to derive a
number that the current parent does not determine.

The integrated-`H` branch derives the **structure** of gravity:

- an integrated public metric modulo `Diff`;
- a positive massless spin-2 pole;
- the nonlinear Ward identity;
- one conserved Hilbert source, including Maxwell/Poynting stress;
- Newton, `gamma_PPN=beta_PPN=1`, and the exact Einstein-vacuum branch in the
  domains already certified by checkpoints 4879 and 4880.

Its numerical stiffness is not microscopically predicted. The complete local
matching equation contains more independent quantities than the one measured
Newton constant can identify. The exact rank is one, with nullity at least two
even after the spectrum weight is frozen.

The correct current field-theory specification is therefore

```text
gravity/source structure  -> derived conditionally from the integrated-H parent
Newton strength           -> calibrated once to CODATA G
arena-specific retuning   -> forbidden; count = 0
microscopic prediction G  -> open and not claimed
```

This closes the `MTS -> calibrated GR/Newton source strength` correspondence
problem. It does not close the deeper origin-of-`G` problem.

## 1. Counterterm-complete stiffness relation

Checkpoint 4876 gives the massless proper-time matter anchor

\[
M_{\rm loop}^2
=\frac{W_1\Lambda_{\rm UV}^2}{96\pi^2},
\qquad
W_1=\sum_s(1-6\xi_s)+2N_D-4N_V.
\]

The observable coefficient is not this term by itself. The complete
renormalized two-derivative relation is

\[
\boxed{
M_R^2(\mu)=M_{\rm EH,boundary}^2(\mu)
+\frac{W_1\Lambda_{\rm UV}^2}{96\pi^2}
+\Delta M_{\rm threshold}^2(\mu)
+\Delta M_{H+\rm gh}^2(\mu).
}
\]

Here `M_EH,boundary^2` includes the legal local Einstein-Hilbert matching
coefficient. `Delta M_threshold^2` contains massive thresholds and phase
changes, while `Delta M_H+gh^2` denotes the regulator-consistent integrated
metric/gauge/ghost contribution not included in the matter weights of 4877.

Only the sum is observable through

\[
\boxed{G_N=\frac{1}{8\pi M_R^2}}.
\]

The often-used scalar expression

\[
G_N=\frac{12\pi}
{N_s(1-6\xi)\Lambda_{\rm UV}^2}
\]

is exact only on the additional branch

```text
M_EH,boundary^2 = 0;
Delta M_threshold^2 = 0;
Delta M_H+gh^2 = 0;
W1 = N_s(1-6 xi).
```

Those are physical boundary/completion conditions, not algebraic identities.
Checkpoint 4875 already states that `M0^2=0` is a UV boundary choice rather
than a radiatively protected theorem.

## 2. Microscopic owner audit

| quantity | present status | consequence |
|---|---|---|
| integrated `H` and `Diff` | parent-owned | gravitational field space and Ward identity close |
| `W1` / full spectrum | real/complex primitive count and completed statistics are not uniquely fixed | blocks numerical prediction |
| scalar `xi_s` | not selected by a parent symmetry or RG fixed point | blocks numerical prediction |
| `Lambda_UV` | conditional cutoff; no independent non-gravitational MTS value | blocks numerical prediction |
| `M_EH,boundary^2` | allowed renormalized relevant coupling | blocks pure-induced prediction |
| massive thresholds | full selected spectrum not calculated | blocks numerical prediction |
| integrated-`H`/ghost matching | gauge-consistent total not calculated | blocks numerical prediction |
| physical `M_R^2` | one global observational calibration exists | closes current correspondence strength |

This is not another missing-symbol list. The next section proves that these
open owners create a genuine non-identifiability, so further rearrangement of
the scalar formula cannot derive `G_N`.

## 3. Exact identifiability theorem

Put `y=Lambda_UV^2` and combine the omitted finite terms into `Delta M^2`.
The measured constraint is

\[
F(M_b^2,W_1,y,\Delta M^2)
=M_b^2+\frac{W_1y}{96\pi^2}+\Delta M^2-M_{\rm obs}^2=0.
\]

Its Jacobian is the nonzero row

\[
DF=\left(
1,
\frac{y}{96\pi^2},
\frac{W_1}{96\pi^2},
1
\right).
\]

Therefore

\[
\boxed{\operatorname{rank}(DF)=1.}
\]

If `W1` is still unfixed, four continuous matching quantities are constrained
by one observation and the local nullity is three. Even if an independently
derived discrete spectrum fixes `W1`, the variables
`(M_b^2,y,Delta M^2)` retain nullity two. Hence `G_N` determines one
renormalized combination, not its microscopic decomposition.

The generator supplies two constructive checks.

1. For every positive `W1`, the pure-induced ray

   \[
   \frac{\Lambda_{\rm UV}}{\overline M_{\rm Pl}}
   =4\pi\sqrt{\frac6{W_1}}
   \]

   reproduces exactly the same `G_N`. Rows at
   `W1=(0.1,1,10,100,1000)` all close to machine precision.

2. The selected minimal `complex psi + M + U(1)` branch has `W1=-1`.
   For any chosen cutoff ratio `r=Lambda_UV/Mbar_Pl`, one matching value

   \[
   \frac{M_{\rm EH,boundary}^2}{\overline M_{\rm Pl}^2}
   =1+\frac{r^2}{96\pi^2}
   \]

   gives the same physical stiffness. At `r=4 pi sqrt(6)` this ratio is
   exactly two, reproducing checkpoint 4885.

These are not candidate predictions. They are an explicit proof that the
current equation is a many-to-one calibration map.

## 4. One global numerical calibration

The latest CODATA set available from NIST as checked on `2026-07-11` is the
2022 adjustment. It gives

\[
G_N=6.67430(15)\times10^{-11}
\ {\rm m^3\,kg^{-1}\,s^{-2}}.
\]

Using exact `h`, `c`, and `e`, the generator obtains

\[
\boxed{
\overline M_{\rm Pl}
=\sqrt{\frac{\hbar c}{8\pi G_N}}
=4.34136\times10^{-9}\ {\rm kg}
=2.43532\times10^{18}\ {\rm GeV}/c^2.
}
\]

The relative standard uncertainty in `Mbar_Pl` is one half that of `G_N`.
The exact machine-readable values and propagated uncertainties are written to
the 4898 CODATA evidence rows.

This consumes one measured relevant coupling. It does not use a separate
`G_N` for R10, PPN, clocks, orbital dynamics, Maxwell stress, strong vacuum,
or cosmology.

## 5. Global source-coupling certificate

With `M_R` fixed once, the selected branch has

\[
M_R^2G_{\mu\nu}=T^{\rm matter}_{\mu\nu}
+T^{\rm EM}_{\mu\nu}+T^{\rm residual}_{\mu\nu},
\]

and the `Diff` Ward identity enforces conservation of the total source. The
same pole residue fixes all weak-source exchange amplitudes. This gives the
following current split:

| arena | use of `G_N` | residual issue not repaired by retuning `G` |
|---|---|---|
| Newton/R10 | same CODATA row | apparatus projection of any extra MTS residual |
| PPN/clocks/orbits | same row | nonminimal active-flow or composite-body residuals |
| Maxwell/Poynting gravity | same row | primitive `U(1)` normalization and `alpha` |
| strong Einstein vacuum | same row | strong matter and higher-curvature operators |
| metric-only cosmology | same row | any genuinely new cosmological extension |

Thus a failure in a future residual calculation cannot be hidden by changing
`G_N` in that arena. Conversely, the absence of a microscopic prediction of
`G_N` is not a failure to reduce to GR: GR itself is specified by a measured
Newton coupling.

## 6. Microscopic-prediction re-entry gate

Calling `G_N` an MTS prediction requires all ten clauses simultaneously:

1. complete primitive spectrum and statistics;
2. parent-owned curvature weights `xi_s`;
3. an independently derived `Lambda_UV`;
4. a derived Einstein-Hilbert UV boundary condition;
5. complete massive thresholds and phase changes;
6. regulator-consistent integrated-`H`/ghost matching;
7. scheme-independent renormalized prediction;
8. higher-loop stability or a quantitative sensitivity bound;
9. one resulting value reused in every arena;
10. an a priori uncertainty interval compared with CODATA.

Only clause 9 is currently closed. The gate is an AND, not a score. The
microscopic-prediction flag is therefore false.

## 7. Arbitration

```text
PLANCK STIFFNESS OPERATOR
    -> DERIVED RENORMALIZED EH OPERATOR

MTS -> GR/NEWTON SOURCE CORRESPONDENCE
    -> STRUCTURE DERIVED
    -> STRENGTH CALIBRATED ONCE
    -> ZERO ARENA-SPECIFIC G RETUNES

MICROSCOPIC NUMERICAL PREDICTION OF G
    -> RANK-DEFICIENT
    -> OPEN
    -> NOT CLAIMED
```

This is a forward result: it removes the impossible demand that the present
incomplete microscopic spectrum somehow determine four matching quantities
from one number, while preserving a precise route by which a future UV
completion could genuinely predict that number.

No GitHub action or public claim follows from this checkpoint.

## Sources

- `post-checkpoint-work/4875-Y5-R2FR-collective-metric-path-integral-massless-spin2-pole-and-Weinberg-Witten-evasion-or-induced-background-only-demotion.md`.
- `post-checkpoint-work/4876-Y5-R2FR-integrated-H-parent-action-saddle-regulator-and-induced-coefficient-matching-to-GN-Lambda-and-R2.md`.
- `post-checkpoint-work/4877-Y5-R2FR-MTS-bath-signed-spectrum-sum-rules-and-nonlocal-form-factor-completion-or-renormalized-vacuum-freeze.md`.
- `post-checkpoint-work/4879-Y5-R2FR-source-size-contact-matching-and-second-order-beta-completion-plus-gauge-invariant-light-kernel-or-strict-EFT-local-GR-promotion-gate.md`.
- `post-checkpoint-work/4880-Y5-R2FR-selected-metric-branch-local-GR-certificate-domain-of-validity-and-strong-field-entry-gate.md`.
- `post-checkpoint-work/4885-Y5-R2FR-Gamma-memory-determinant-and-nonminimal-weight-from-closed-bath-or-three-boson-branch-demotion-gate.md`.
- [NIST current fundamental constants](https://physics.nist.gov/cuu/Constants/).
- [NIST 2022 CODATA wall chart](https://physics.nist.gov/cuu/pdf/wall_2022.pdf).
- [2022 CODATA recommended-values paper](https://physics.nist.gov/cuu/pdf/RevModPhys.97.025002.pdf).

## Next target

`4899-Y5-R2FR-primitive-U1-normalization-and-Maxwell-charge-calibration-versus-alpha-prediction-gate.md`

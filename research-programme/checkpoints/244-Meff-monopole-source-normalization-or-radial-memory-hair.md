# 244 - M_eff Monopole Source Normalization or Radial Memory Hair

Private local-derivation checkpoint. This is not a public `G_eff`, PPN,
local-GR, or field-theory completion claim.

## 1. Trigger

Checkpoint 243 left the next local gate:

```text
N1_Meff.
```

Purpose:

```text
derive why the local exterior source is only a conserved monopole M_eff,
with no radial memory hair or G_eff drift.
```

## 2. Machine Artifact

Script:

```text
scripts/Meff_monopole_source_normalization_or_radial_memory_hair.py
```

Run:

```text
runs/20260601-000061-Meff-monopole-source-normalization-or-radial-memory-hair
```

Command:

```text
python scripts/Meff_monopole_source_normalization_or_radial_memory_hair.py --timestamp 20260601-000061
```

Status:

```text
N1_Meff_monopole_conservation_gate_derived_conditionally_radial_memory_hair_parent_source_identity_open_no_promotion
```

Claim ceiling:

```text
N1_Meff_conditional_flux_gate_no_Geff_or_PPN_promotion
```

## 3. Monopole Flux Theorem

For the compact exterior shell:

```text
Sigma_ext ~= S^2 x I.
```

The absolute cohomology is:

```text
H^2(Sigma_ext) = R.
```

This is the ordinary enclosed mass/Gauss-flux class.

It must not be erased.

Define:

```text
M_eff(r) := (1 / 4 pi G) int_{S^2_r} Pi_M J.
```

If the exterior annulus obeys:

```text
d(Pi_M J) = 0,
```

then:

```text
M_eff(r_2) - M_eff(r_1)
= int_{S^2 x [r_1,r_2]} d(Pi_M J)
= 0.
```

Therefore:

```text
M_eff(r) = constant.
```

That is the N1 gate.

## 4. Radial Memory Hair

Radial memory hair means:

```text
dM_eff/dr != 0,
```

or equivalently:

```text
G_eff(r) M_bare
```

acts like a radial source profile instead of a conserved monopole.

That would reopen:

```text
G_eff/G - 1,
beta - 1,
and exterior no-hair.
```

So the local branch requires:

```text
ordinary mass flux -> M_eff,
relative memory exchange -> P_mem J_rel,
trace-free shear -> Pi_TF,
direct matter/clock vertices -> Pi_matter.
```

No sector is allowed to hide in `G_eff(r)`.

## 5. What Is Actually Derived

Derived conditionally:

```text
Pi_M extracts the absolute S^2 harmonic flux,
d(Pi_M J)=0 in the exterior,
therefore M_eff is radially conserved.
```

This is stronger than:

```text
assume source normalization is fine.
```

It says exactly what must be true:

```text
the parent source identity must give a closed Pi_M flux in compact exterior
vacuum.
```

## 6. What Is Still Open

Still not parent-derived:

```text
Pi_M from the boundary symplectic metric,
d(Pi_M J)=0 from the parent source identity,
absolute calibration of M_eff,
N4 exact relative memory,
N5 projector-stress Bianchi cancellation,
N6 auxiliary no-hair,
metric-only Einstein-Hilbert exterior.
```

So this checkpoint does not claim:

```text
MTS predicts G_eff,
MTS passes PPN,
MTS derives beta = 1,
MTS derives local GR.
```

## 7. Coefficient Status

| residual | status after 244 |
|---|---|
| `G_eff/G - 1` | conditionally monopole-only if `N1` holds |
| `beta - 1` | still open; conserved `M_eff` is necessary but not sufficient |
| `gamma - 1` | unchanged; conditionally zero if `N2` holds |
| `Phi - Psi` | unchanged; conditionally zero if `N2` holds |
| `epsilon_matter` | unchanged; conditionally zero from `N3` |
| `alpha_clock` | unchanged direct-vertex gate; metric/C branch still open |

The local branch now has this shape:

```text
N3 -> direct matter/clock vertices,
R_loc -> local C trace source,
N2 -> gamma/slip,
N1 -> monopole source normalization,
N4/N5/N6 -> q_loc and no exterior memory hair,
EH exterior -> beta.
```

## 8. Gate Results

| gate | result |
|---|---|
| all cited local sources exist | pass |
| absolute `H^2` mass class preserved | pass |
| `M_eff` conserved in exterior | conditional pass |
| radial memory hair excluded by parent action | fail |
| `G_eff`/source normalization public pass claimed | fail |
| local GR or PPN promoted | fail |

## 9. Decision

Decision:

```text
N1_Meff_monopole_conservation_gate_derived_conditionally_radial_memory_hair_parent_source_identity_open_no_promotion
```

Meaning:

```text
N1_Meff now has a sharp conditional flux theorem: preserve the absolute S^2
mass class as M_eff, prove its exterior flux is closed, and radial source hair
is gone.
```

Main gain:

```text
G_eff/source normalization is no longer a vague fitted closure; it is reduced
to Pi_M flux closure plus no radial hair.
```

Main failure:

```text
Pi_M flux closure, absolute M_eff calibration, and projector/Bianchi ownership
remain parent gaps.
```

## 10. Next Target

Create:

```text
245-exact-relative-memory-or-projector-stress-bianchi.md
```

Purpose:

```text
attack N4/N5: after ordinary mass is preserved as M_eff, prove the relative
memory sector is exact/pure gauge and that projector stress does not fake
conservation.
```

Pass condition:

```text
P_mem J_rel = d_rel A_rel,
d_rel(P_mem J_rel)=0,
and the variation of Pi_M/P_mem either vanishes or is retained in a Bianchi-safe
stress ledger.
```

Fail condition:

```text
relative memory is declared harmless after projecting out the pieces that hurt.
```

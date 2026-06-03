# 231 - Jrel Cohomology Projector or Local EH Limit

Private local-derivation checkpoint. This is not a public local-GR, PPN,
clock, WEP, or field-theory completion claim.

## 1. Trigger

Checkpoint 230 reduced the beta/local-exterior problem to:

```text
derive J_rel exactness/triviality in the exterior memory sector,
or derive the local Einstein-Hilbert exterior limit.
```

This checkpoint attacks `J_rel` first.

The useful question is:

```text
Does compact-shell topology force the projected memory current into an exact
class, without accidentally deleting ordinary mass flux?
```

## 2. Machine Artifact

Script:

```text
scripts/Jrel_cohomology_projector_or_local_EH_limit.py
```

Run:

```text
runs/20260601-000048-Jrel-cohomology-projector-or-local-EH-limit
```

Command:

```text
python scripts/Jrel_cohomology_projector_or_local_EH_limit.py --timestamp 20260601-000048
```

Status:

```text
Jrel_local_projector_relative_cohomology_sufficient_gate_derived_parent_projector_open_no_PPN_promotion
```

Claim ceiling:

```text
Jrel_cohomology_sufficient_gate_no_parent_projector_or_local_EH_promotion
```

## 3. Shell Cohomology

Model the compact exterior spatial shell as:

```text
Sigma_ext ~= S^2 x [R_inner, R_outer].
```

Then:

```text
H^1(Sigma_ext) = 0,
H^2(Sigma_ext) = R,
H^2(Sigma_ext, partial Sigma_ext) = 0.
```

Interpretation:

| class | meaning |
|---|---|
| `H^1 = 0` | closed one-form memory currents are exact |
| `H^2 = R` | absolute `S^2` flux can carry ordinary enclosed charge/mass |
| `H^2_relative = 0` | relative two-form memory flux has no cohomology obstruction |

This is the important split.

The dangerous nonzero class is:

```text
H^2(Sigma_ext) = R.
```

That is exactly why we must not identify `J_rel` with ordinary mass/Gauss flux.

Mass flux must become:

```text
M_eff.
```

Memory exchange must become:

```text
J_rel.
```

## 4. The Projector

Define a required memory projector:

```text
P_mem J_rel =
J_rel - Pi_mass J_rel - Pi_shear J_rel.
```

It must satisfy:

```text
integral_{S^2_r} P_mem J_rel = 0,
Pi_shear P_mem J_rel = 0,
A_rel|partial Sigma_ext = pure gauge,
d_rel P_mem J_rel = 0.
```

Then the current lives in:

```text
H^2(Sigma_ext, partial Sigma_ext).
```

But:

```text
H^2(Sigma_ext, partial Sigma_ext) = 0.
```

Therefore:

```text
P_mem J_rel = d_rel A_rel.
```

and:

```text
d_rel P_mem J_rel = 0.
```

With the checkpoint-221 source identity:

```text
q_loc^nu = -P_loc d_rel J_rel^nu,
```

the projected memory part gives:

```text
q_loc^nu = 0.
```

This is a real mathematical gain.

It does not derive the parent projector.

## 5. What This Proves

This checkpoint proves a sufficient topological gate:

```text
if the parent theory supplies P_mem,
and P_mem removes ordinary mass flux plus tangential shear,
and the memory current is closed with relative boundary primitive,
then local exterior J_rel exactness follows from shell cohomology.
```

That is stronger than:

```text
assume J_rel is exact.
```

It becomes:

```text
derive P_mem, and topology does the exactness work.
```

## 6. What This Does Not Prove

Still not derived:

```text
P_mem from the parent action,
the source identity from the parent variation,
the X/no-hair constraint algebra,
the exterior Einstein-Hilbert metric operator,
the matter/clock universal coupling action.
```

So the local branch improves, but does not promote.

The exact status is:

```text
J_rel exactness has a cohomology theorem gate;
q_loc silence remains conditional;
beta remains conditional;
local GR remains unpromoted.
```

## 7. Coefficient Status

| residual | checkpoint 231 status |
|---|---|
| `gamma - 1` | unchanged scalar-boundary/no-shear sufficient route |
| `Phi - Psi` | unchanged scalar-boundary/no-shear sufficient route |
| `G_eff/G - 1` | mass class separated into `M_eff`; source normalization open |
| `alpha_clock` | unchanged universal metric coupling contract |
| `epsilon_matter` | unchanged universal metric coupling contract |
| `beta - 1` | strengthened by J_rel cohomology gate, not parent-derived |

This is the local scoreboard:

```text
gamma/slip: scalar-boundary route;
q_loc: cohomology/projector route;
beta: exterior no-hair plus local EH route;
clock/WEP: universal coupling route.
```

Every route is sharper.

None is promoted.

## 8. Gate Results

| gate | result |
|---|---|
| all cited local sources exist | pass |
| shell cohomology computed | pass |
| mass flux danger separated | pass |
| `J_rel` exactness has non-cheating route | pass |
| beta route strengthened by cohomology | pass |
| parent `P_mem` projector derived | fail |
| local EH exterior limit derived | fail |
| local GR or PPN promoted | fail |

The pass rows are exactly the kind of footwork we want.

The fail rows are exactly why this is not a claim.

## 9. Decision

Decision:

```text
Jrel_local_projector_relative_cohomology_sufficient_gate_derived_parent_projector_open_no_PPN_promotion
```

Meaning:

```text
the local J_rel exactness route now has a real topology gate. On a compact
exterior shell, absolute H^2 carries the ordinary enclosed mass/flux danger and
must be kept as M_eff, not J_rel. After projecting J_rel to memory exchange,
removing S^2 harmonic flux and tangential shear, and imposing relative
pure-gauge boundary primitive, H^2(Sigma,partial Sigma)=0 forces closed
projected memory flux to be exact.
```

Main gain:

```text
J_rel exactness is no longer only a hope.
```

Main failure:

```text
P_mem, the source identity, no-hair algebra, and local EH limit remain parent
gaps.
```

## 10. Next Target

Create:

```text
232-parent-Pmem-projector-or-source-identity-variation.md
```

Purpose:

```text
derive the parent P_mem projector or derive the source identity from variation.
```

Pass condition:

```text
P_mem appears from the parent constraint/symplectic structure,
not as a post-hoc filter.
```

or:

```text
nabla_mu Khat^{mu nu} - nabla^nu Gamma_eff
= S_L^nu + d_rel J_rel^nu
```

is derived with all boundary and auxiliary stresses retained.

Fail condition:

```text
P_mem is invented after the fact to erase the dangerous cohomology class.
```

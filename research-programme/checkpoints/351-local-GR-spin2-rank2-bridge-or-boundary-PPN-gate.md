# 351 - Local GR Spin-2 Rank-2 Bridge Or Boundary PPN Gate

Private derivation checkpoint. This is not a public local-GR, PPN, CMB, cosmology, or `B_mem = 2/27` derivation claim.

## 1. Purpose

Checkpoint 350 found a tempting bridge:

```text
local GR has two physical spin-2 polarizations
rank(P_active)=2 wants a numerator two
```

This checkpoint tests whether that is a derivation or just a seductive coincidence.

Short answer:

```text
the spin-2 fact is real,
but it does not derive rank(P_active)=2 for the FLRW memory amplitude.
```

So the amplitude stays closure-locked and the next serious route is boundary no-hair plus PPN residuals.

## 2. Run Ledger

Script:

```text
scripts/local_GR_spin2_rank2_bridge_or_boundary_PPN_gate.py
```

Run directory:

```text
runs/20260601-230000-local-GR-spin2-rank2-bridge-or-boundary-PPN-gate
```

Command:

```text
python scripts/local_GR_spin2_rank2_bridge_or_boundary_PPN_gate.py --timestamp 20260601-230000
```

Status:

```text
spin2_rank2_bridge_rejected_as_amplitude_derivation_boundary_PPN_gate_selected
```

Claim ceiling:

```text
no_rank2_Bmem_or_local_GR_promotion_spin2_is_PPN_consistency_only
```

Outputs:

```text
results/source_register.csv
results/spin2_rank2_bridge_tests.csv
results/SO3_representation_ledger.csv
results/rank2_decision_ledger.csv
results/boundary_PPN_next_gate.csv
results/gate_results.csv
results/decision.csv
```

## 3. The Temptation

If the local branch genuinely reduces to Einstein-Hilbert GR, the local propagating gravitational field has:

```text
two physical massless tensor polarizations.
```

That is exactly the kind of number we would like to see if we are trying to derive:

```text
rank(P_active) = 2.
```

This is not silly.
It is a fair thing to test because it points the amplitude numerator toward the GR-reduction problem rather than arbitrary cell numerology.

But the bridge must pass a representation test.

## 4. Representation Test

The local GR tensor modes are:

```text
h_ij^TT
```

with:

```text
partial^i h_ij^TT = 0,
delta^ij h_ij^TT = 0.
```

They are transverse-traceless tensor perturbations.
In rotational language they are anisotropic tensor objects, not isotropic scalar background loads.

The FLRW memory branch uses:

```text
Q^i_j = X_FLRW delta^i_j.
```

This is an isotropic scalar load.
Its trace is:

```text
Q^i_i = 3 X_FLRW.
```

Therefore a direct linear identification fails:

```text
two TT tensor polarizations != two FLRW scalar memory modes.
```

The trace makes the failure sharp:

```text
Tr(h^TT) = 0,
Tr(Q) = 3 X_FLRW.
```

So the direct map:

```text
local spin-2 count -> FLRW B_mem numerator
```

is not a derivation.

## 5. Could A Quadratic Route Work?

A quadratic tensor scalar is allowed in principle:

```text
h_ij^TT h_TT^ij.
```

That object is scalar.
But it is:

```text
second order,
state/spectrum dependent,
normalization dependent,
not a fixed rank fraction.
```

So it cannot derive:

```text
B_mem = 2/27
```

as a universal parent amplitude.

It may be relevant later for perturbations/backreaction, but it is not the missing rank theorem.

## 6. Rank-2 Decision

The honest status is:

| Candidate origin | Verdict | Why |
|---|---:|---|
| local GR two polarizations | reject as amplitude derivation | true spin-2 fact, wrong representation for FLRW scalar trace |
| finite-fibre rank-2 readout | closure locked | active plane remains noncanonical |
| quadratic tensor scalar | later perturbation only | scalar possible, amplitude state-dependent |
| boundary no-hair / PPN | selected next | directly attacks local GR recovery |

So:

```text
rank(P_active)=2
```

stays:

```text
closure/theorem target,
not parent-derived.
```

## 7. What This Means For GR

The spin-2 test is not wasted.

It tells us:

```text
if local GR is recovered,
then the physical propagating sector has the correct two tensor polarizations.
```

But that is a consistency check after the local GR branch is derived.
It is not a shortcut to the FLRW amplitude.

The right next target remains the local reduction:

```text
quotient P_D -> local no-bulk-stress
boundary terms -> no trace-free/shear support
bulk exterior -> Einstein-Hilbert
PPN vector -> below bounds
```

That is the route that can make:

```text
MTS -> GR -> Newton/PPN
```

real rather than decorative.

## 8. Boundary PPN Gate To Build Next

The next checkpoint should attack the residual local exterior terms.

It must separate:

| Residual class | Required result | PPN risk |
|---|---|---|
| boundary trace mode | only monopole/renormalized mass survives | `gamma`, `beta`, Poisson shifts |
| boundary trace-free shear | vanishes or decays fast enough | anisotropic potentials, lensing slip |
| vector/preferred-frame terms | no local vector background survives | preferred-frame PPN parameters |
| clock/ruler coupling | all matter sees one metric | WEP/redshift/lensing violations |
| residual bulk MTS support | zero after quotient `P_D` silence | fifth-force / modified Poisson source |

That gate is closer to the core aim than another amplitude chase.

## 9. Gate Results

| Gate | Result | Meaning |
|---|---:|---|
| source paths exist | pass | cited checkpoints and script exist |
| two GR tensor polarizations valid | pass as consistency | valid only inside conditional local EH branch |
| spin-2 to rank-2 amplitude derivation | fail | TT tensor sector does not linearly equal FLRW scalar trace readout |
| quadratic tensor backreaction derives `2/27` | fail | state-dependent, not fixed rank/dim theorem |
| rank-2 closure lock preserved | pass | `rank(P_active)=2` stays closure/theorem target |
| local GR or PPN promoted | fail | no boundary/no-hair or PPN vector yet |
| next boundary PPN gate selected | pass | proceed to boundary no-hair residuals |
| claim ceiling enforced | pass | no rank/amplitude/local-GR promotion |

## 10. Decision

```text
spin2_rank2_bridge_rejected_as_amplitude_derivation_boundary_PPN_gate_selected
```

This is a useful negative result.
It stops us from kidding ourselves that:

```text
two tensor polarizations = two memory rank modes.
```

The number matches, but the representation does not.

So the project gets cleaner:

```text
rank 2 remains closure,
GR recovery remains the main gate,
boundary no-hair / PPN is now the next target.
```

## 11. Next Target

Next checkpoint:

```text
352-boundary-nohair-and-PPN-residual-vector-gate.md
```

Task:

```text
derive or bound the boundary residual tensor after quotient P_D silence,
decompose it into trace / trace-free shear / vector / clock sectors,
and produce the symbolic PPN residual vector.
```

If that gate closes, the local GR branch starts looking serious.
If it fails, the local branch remains a modified-exterior closure branch.

# 4072 - Local Motion-Frame Gauge Action Or Effective-GR Demotion

- Timestamp: `2026-07-02T02:18:11+00:00`
- Status: `private_nonclaim_checkpoint`
- Decision: `LOCAL_MOTION_FRAME_GAUGE_ACTION_WRITTEN_AS_FORMAL_CANDIDATE_NOT_CURRENT_MTS_DERIVED_EFFECTIVE_GR_DEMOTION_ACTIVE`
- Public GR/Newton/PPN claim: `false`
- GitHub action: `false`

## What Was Written

4072 writes the actual parent-action candidate that 4071 demanded:

```text
Q_4072 = {X^A=L_* Psi^A, B^A, omega^AB, eta_AB, kappa_eff, A_3, matter, EM, auxiliary fields}

e^A = D_omega X^A + B^A
g_obs = eta_AB e^A e^B

S_EC = (4 kappa_eff)^-1 ∫ epsilon_ABCD e^A∧e^B∧R^CD[omega]
      - (Lambda_eff / 12 kappa_eff) ∫ epsilon_ABCD e^A∧e^B∧e^C∧e^D
```

with optional torsion constraint/stiffness, topological `kappa_eff`, same-coframe matter/EM, and a memory-invariant sector.

## What Closed

- The action form is now explicit.
- The gauge transformation law is explicit.
- The route from Cartan action to EH, then to 4063 Newton/PPN readout, is explicit.
- The exact-gradient flatness trap is avoided by `B^A`.

## What Did Not Close

The current MTS corpus does **not** yet derive this action. It contains motion/flow/memory/frame clues, but not a parent-signed local motion-frame gauge action.

So the honest status is:

```text
motion_frame_gauge_action = formal_private_candidate
current_MTS_derivation = false
effective_GR_demotion = active_if_not_adopted_or_derived
```

## Fork

Either:

1. adopt/derive this as MTS parent infrastructure, then continue closing torsion, EM-Hodge, same-coframe, and kappa gates; or
2. demote the Cartan/EH local branch to an effective-GR input and keep MTS as a residual/testable extension around it.

## Next

`4073` should decide formal adoption or demotion in the workbench, rather than leaving this fork vague.

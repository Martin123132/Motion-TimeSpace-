# 4074 - Flow-Solder Field Parent Signature Or Effective Tetrad Demotion

- Timestamp: `2026-07-02T02:33:25+00:00`
- Status: `private_nonclaim_checkpoint`
- Decision: `FLOW_SOLDER_PARENT_SIGNATURE_NOT_DERIVED_EFFECTIVE_TETRAD_DEMOTION_CONTRACT_STAGED`
- Public GR/Newton/PPN claim: `false`
- GitHub action: `false`

## Result

4074 attacks the exact thing that was still too hand-wavy after the motion-frame gauge adoption:

```text
e^A = D_omega X^A + B^A
B'^A = Lambda^A_B B^B - D'a^A
g_obs = eta_AB e^A e^B
```

The result is a useful no-go, not a vibe-check:

```text
current scalar/gradient/routing MTS flow variables do not derive B^A.
```

The reason is structural. `B^A` is not merely "flow". It is an internal-vector-valued one-form with an inhomogeneous local-translation compensator term. A scalar field, scalar clock, scalar memory term, exact gradient, speed-budget split, Poynting vector, or Hilbert stress readout transforms tensorially/homogeneously once the frame is chosen. None of them can supply the `-D'a^A` shift without importing the very gauge object we are trying to derive.

## What Was Proved

Under the current corpus primitives:

```text
psi/Psi, Gamma, chi, tau, d psi, motion-load, clock residue, spatial routing
```

any local object built algebraically from scalar flow data transforms as a scalar/tensor/readout. It can constrain norms, source couplings, Hodge consistency, or clock strain, but it cannot become the Cartan translation compensator `B^A`.

So the branch cannot honestly claim:

```text
MTS flow -> B^A -> e^A -> GR
```

yet.

## Poynting Vector Route

This also answers the Poynting-vector suspicion cleanly.

Poynting flow is valuable, but downstream. It is Maxwell/Hilbert stress measured through a Hodge star and observer coframe. It can test whether EM, clocks, matter, and gravity are using the same `e_obs`, but it cannot be the first source of `B^A` without circularly assuming the coframe/Hodge structure.

## The Forward Repair

There is still a precise route that would make this work:

```text
Theta^A = parent-owned flow coframe
Theta'^A = Lambda^A_B Theta^B
Theta^A = D_omega X^A + B^A
B^A = Theta^A - D_omega X^A
g_obs = eta_AB Theta^A Theta^B
```

If MTS can derive a non-degenerate rank-four `Theta^A` from clock plus spatial observer routing without smuggling a tetrad, the local GR branch becomes serious again.

## Demotion Contract

Until that repair closes, local gravity must be treated as:

```text
effective tetrad / Einstein-Cartan / GR baseline
plus MTS residuals
```

The residuals to score are:

```text
epsilon_B_derivation
epsilon_torsion
epsilon_nonmetricity
epsilon_kappa_normalization
Delta_Hodge_EM
epsilon_clock_strain
source_label_leak
Qcoh / Noether deformation
Delta_ref_frame_profile_over_MH
```

## Decision

This is not the branch dying. It is the branch losing the right to smuggle the tetrad.

4074 says:

```text
Either derive Theta^A properly next,
or use effective GR as the baseline and score MTS residuals honestly.
```

## Next

`4075` should try one concrete repair:

```text
clock one-form + spatial observer routing triad -> Theta^A
```

If that route imports a tetrad in disguise, switch immediately to the effective-GR residual scorer.

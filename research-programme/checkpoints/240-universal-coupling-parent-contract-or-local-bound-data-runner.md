# 240 - Universal Coupling Parent Contract or Local-Bound Data Runner

Private local-derivation checkpoint. This is not a public WEP, clock, PPN,
local-GR, or field-theory completion claim.

## 1. Trigger

Checkpoint 239 found the sharpest local-bound pressure:

```text
direct matter/composition coupling is the first disaster channel.
```

Numerically, even a `1e-6` direct matter leak is far too large in the current
closure map:

```text
ratio_to_bound ~= 7.9e3.
```

So the next target is:

```text
N3_universal_coupling.
```

## 2. Machine Artifact

Script:

```text
scripts/universal_coupling_parent_contract_or_local_bound_data_runner.py
```

Run:

```text
runs/20260601-000057-universal-coupling-parent-contract-or-local-bound-data-runner
```

Command:

```text
python scripts/universal_coupling_parent_contract_or_local_bound_data_runner.py --timestamp 20260601-000057
```

Status:

```text
universal_coupling_contract_derives_Pi_matter_zero_conditionally_C_trace_source_and_parent_selection_open_no_promotion
```

Claim ceiling:

```text
N3_direct_coupling_theorem_conditional_no_WEP_or_PPN_pass_claim
```

## 3. Exact Contract

Let the parent non-matter variables be:

```text
Z_I in {X, J_rel, V_def, P_mem, C_direct, ...}.
```

The universal-coupling contract is:

```text
S_matter = sum_A S_A[Psi_A, ehat, omega[ehat], constants_A],
```

where every matter and clock species sees the same observed coframe:

```text
ehat^a_mu,
ghat_mu_nu = eta_ab ehat^a_mu ehat^b_nu.
```

At fixed observed coframe:

```text
(delta S_matter / delta Z_I)|_{ehat,Psi} = 0.
```

That is the clean version of:

```text
Pi_matter = 0 on direct memory-matter vertices.
```

## 4. The Derived Part

The variation is simple but powerful.

If matter has no direct `Z_I` argument, then:

```text
c_matter^direct = 0,
c_clock^direct = 0.
```

This is not:

```text
c_matter is very small.
```

It is:

```text
the coefficient does not exist in the matter action.
```

So the WEP/composition channel is avoided by action structure, not by tuning.

This is the correct response to the checkpoint-239 pressure result.

## 5. Ward Identity

Diffeomorphism invariance gives the matter-sector identity:

```text
nabla_hat_mu T_hat^{mu}{}_{nu} = 0
```

on matter shell, provided:

```text
(delta S_matter / delta Z_I)|_{ehat,Psi} = 0.
```

If a direct memory-matter vertex exists, the identity instead contains an extra
force/source term:

```text
nabla_hat_mu T_hat^{mu}{}_{nu}
~ (delta S_matter / delta Z_I) partial_nu Z_I.
```

That term is exactly what the local branch cannot afford.

## 6. Forbidden Vertices

The contract forbids:

| vertex | reason |
|---|---|
| `m_A(Z)` | species-dependent masses create composition dependence |
| `alpha_EM(Z)` or `f_A(Z)F^2` | clocks/spectroscopy become direct memory probes |
| `q_A X_mu J_A^mu` | fifth-force/composition current |
| `lambda_A V_def O_A` | defect potential talks to matter outside geometry |
| `P_mem J_rel` inside matter action | projector would be deleting a force by hand |

Allowed:

```text
one observed metric/coframe for all species.
```

Allowed only as a separate common-mode/screened branch:

```text
constant unit rescaling,
or dynamic conformal C only if C-silence is separately derived.
```

## 7. Important Catch

Universal coupling does not automatically make the conformal branch quiet.

If:

```text
ghat_mu_nu = exp(C) g_mu_nu,
```

then:

```text
delta S_matter / delta C
= 1/2 sqrt(-ghat) T_hat.
```

For dust:

```text
T_hat ~= -rho.
```

So dynamic `C` is still matter-sourced unless the parent action supplies:

```text
screening,
fixed-point saturation,
constraint cancellation,
or local common-mode freezing.
```

This means checkpoint 240 improves N3, but it does not solve local GR.

## 8. What Improved

Before this checkpoint:

```text
Pi_matter was a required projector.
```

After this checkpoint:

```text
Pi_matter has an exact action condition:
S_matter has no direct memory-sector argument at fixed observed coframe.
```

That condition gives:

```text
c_matter^direct = 0,
c_clock^direct = 0.
```

So the most brutal checkpoint-239 channel is conditionally removed.

## 9. What Still Fails

Still not derived:

```text
why the deeper MTS parent action forces this matter form,
why dynamic C is locally silent,
why no trace-free exterior stress appears,
why M_eff is the only mass/source remnant,
why projector stress cancels,
why auxiliary X/J_rel/V_def hair cannot propagate.
```

So this does not promote:

```text
MTS passes WEP,
MTS passes clock tests,
MTS passes PPN,
MTS derives local GR.
```

## 10. Gate Results

| gate | result |
|---|---|
| all cited local sources exist | pass |
| universal matter/coframe contract written | pass |
| direct `Pi_matter` source removed | conditional pass |
| WEP/direct composition coefficient zero | conditional pass |
| dynamic `C` trace source cleared | fail |
| parent selection of universal matter action derived | fail |
| local GR or PPN promoted | fail |

The useful win is conditional and exact.

The promotion gates remain shut.

## 11. Decision

Decision:

```text
universal_coupling_contract_derives_Pi_matter_zero_conditionally_C_trace_source_and_parent_selection_open_no_promotion
```

Meaning:

```text
N3 can be sharpened into an action theorem: if every matter and clock species
couples only to one observed metric/coframe, then direct memory-matter and
direct memory-clock coefficients vanish exactly.
```

Main gain:

```text
the WEP channel is no longer a fitted small number; it is zero by absence.
```

Main failure:

```text
the parent principle selecting this matter action is not derived, and dynamic
C still carries a trace-source hazard.
```

## 12. Next Target

Create:

```text
241-C-silence-screening-or-parent-selection-theorem.md
```

Purpose:

```text
either derive why C is locally frozen/screened/common-mode,
or derive why the parent action selects strict metric/coframe coupling with no
dynamic conformal trace source in the local branch.
```

Pass condition:

```text
delta S_matter/delta C is absent locally,
or C has a parent-derived screening/fixed-point equation that makes local
gradients and drift negligible.
```

Fail condition:

```text
C-silence is assumed because local bounds require it.
```

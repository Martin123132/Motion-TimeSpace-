# 241 - C-Silence Screening or Parent-Selection Theorem

Private local-derivation checkpoint. This is not a public BAO, WEP, clock,
PPN, local-GR, or field-theory completion claim.

## 1. Trigger

Checkpoint 240 improved `N3_universal_coupling`:

```text
direct memory-matter and memory-clock coefficients vanish if matter sees only
one observed metric/coframe.
```

But it also exposed the next wall:

```text
if the observed metric contains a dynamic conformal C, matter trace sources C.
```

So this checkpoint asks:

```text
can local C-silence be derived,
or does the naive conformal branch fail?
```

## 2. Machine Artifact

Script:

```text
scripts/C_silence_screening_or_parent_selection_theorem.py
```

Run:

```text
runs/20260601-000058-C-silence-screening-or-parent-selection-theorem
```

Command:

```text
python scripts/C_silence_screening_or_parent_selection_theorem.py --timestamp 20260601-000058
```

Status:

```text
C_silence_no_go_for_unscreened_conformal_trace_branch_strict_metric_or_screened_zero_mode_required_no_promotion
```

Claim ceiling:

```text
C_silence_theorem_conditions_only_no_local_GR_or_BAO_promotion
```

## 3. The Equation

There are two distinct local branches.

Strict local metric/coframe branch:

```text
ghat_mu_nu = g_mu_nu locally, up to constant unit rescaling,
(delta S_matter / delta C)|ghat = 0.
```

Dynamic conformal branch:

```text
ghat_mu_nu = exp(C) g_mu_nu,
delta S_matter / delta C = 1/2 sqrt(-ghat) T_hat.
```

Therefore:

```text
E_C[C,Z,g] + 1/2 sqrt(-ghat) T_hat = 0.
```

For dust:

```text
T_hat ~= -rho.
```

So ordinary matter sources `C`.

## 4. Plateau No-Go

Suppose the local branch wants:

```text
C(x) = C_*,
partial_mu C = 0
```

over a local exterior/readout patch.

For two independent matter traces `T_1` and `T_2`, the plateau equation gives:

```text
E_C(C_*) + beta_C T_1 = 0,
E_C(C_*) + beta_C T_2 = 0.
```

Subtract:

```text
beta_C (T_1 - T_2) = 0.
```

For arbitrary local matter traces:

```text
beta_C = 0,
```

unless a parent-owned cancellation/screening term is present.

This is the no-go:

```text
an unscreened dynamic conformal C cannot be assumed locally silent.
```

## 5. Escape Routes

The local branch has only honest exits:

| route | status |
|---|---|
| strict local metric/coframe | sufficient if parent-selected |
| coherent domain zero-mode `C_D` | viable candidate, projector not derived |
| heavy/stiff residual `C` mode | possible side route, local gate is stiff |
| trace sequestering/cancellation | possible only if Bianchi-safe and parent-owned |
| ordinary light dynamic conformal `C` | rejected as local-silence route |

So the cleanest local-GR route is:

```text
C is not a local matter-metric degree of freedom.
```

The second-best route is:

```text
C has a parent-derived domain/zero-mode projector and only screened residuals.
```

## 6. Suppression Bound

Using:

```text
B_mem = 2/27,
```

the required response fractions are:

| gate | required response fraction |
|---|---:|
| local `Delta C` gate | `0.000621` |
| BAO `150 Mpc` spatial gate | `0.074786` |
| fixed-alpha BAO `dot_C/H` gate | `0.152356` |
| shared-alpha BAO `dot_C/H` gate | `0.244073` |

The local gate is the hard one.

Meaning:

```text
BAO-scale C smoothness is not the worst problem;
local trace response is.
```

## 7. What Was Derived

Derived:

```text
local C plateau + arbitrary matter trace
=> beta_C = 0
```

unless:

```text
parent-owned cancellation,
screening,
or domain projection
```

is present.

So the naive branch:

```text
matter universally sees exp(C)g_mu_nu and C is an ordinary local scalar
```

is not a viable local-GR silence theorem.

## 8. What Improved

Before this checkpoint:

```text
C-silence was a required screening/fixed-point mechanism.
```

After this checkpoint:

```text
the unscreened conformal route is explicitly rejected,
and the surviving routes are strict local metric selection or parent-owned
screening/domain projection.
```

That is progress because it removes a tempting but cheating move.

## 9. What Still Fails

Still not derived:

```text
why the parent action selects strict local coframe coupling,
or why a domain projector suppresses local C residuals,
or how the cancellation/screening stress enters the Bianchi ledger.
```

So this checkpoint does not promote:

```text
local GR,
PPN safety,
BAO support,
CMB support,
or a completed parent action.
```

## 10. Gate Results

| gate | result |
|---|---|
| all cited local sources exist | pass |
| `C` trace-source equation written | pass |
| unscreened conformal plateau no-go derived | pass |
| strict local metric escape identified | conditional pass |
| screening/domain projector parent-derived | fail |
| local GR or BAO support promoted | fail |

## 11. Decision

Decision:

```text
C_silence_no_go_for_unscreened_conformal_trace_branch_strict_metric_or_screened_zero_mode_required_no_promotion
```

Meaning:

```text
dynamic conformal C is not locally silent just because coupling is universal.
The parent must either remove C from the local matter metric, or derive a real
screening/domain projector/cancellation.
```

Main gain:

```text
we have a no-go for the naive C route and a cleaner target for the surviving
local branch.
```

Main failure:

```text
the surviving branch is not yet selected by the parent action.
```

## 12. Next Target

Create:

```text
242-strict-local-coframe-branch-or-domain-projector-action.md
```

Purpose:

```text
derive why the observed local matter coframe is strict metric/coframe only,
or derive a Bianchi-safe domain projector that suppresses local C residuals.
```

Pass condition:

```text
the parent action forces beta_C = 0 locally,
or derives Pi_D plus the missing stress terms so local C residuals are
suppressed without violating conservation.
```

Fail condition:

```text
C is declared silent because local tests require it.
```

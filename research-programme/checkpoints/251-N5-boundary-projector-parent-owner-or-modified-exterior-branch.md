# 251 - N5 Boundary Projector Parent Owner or Modified Exterior Branch

Private derivation checkpoint. This does not promote local GR, PPN, Cassini,
MICROSCOPE, clocks, beta, or the parent action.

## 1. Trigger

Checkpoint 250 left the local branch in a cleaner but still blocked state:

```text
N5 projector stress is the sharpest obstruction to metric-only EH exterior.
```

So the next derivation target is exact:

```text
either construct conditions under which T_projector has no bulk exterior
metric variation, or admit that the local branch is a modified-exterior branch.
```

## 2. Machine Artifact

Script:

```text
scripts/N5_boundary_projector_parent_owner_or_modified_exterior_branch.py
```

Run:

```text
runs/20260601-000068-N5-boundary-projector-parent-owner-or-modified-exterior-branch
```

Command:

```text
python scripts/N5_boundary_projector_parent_owner_or_modified_exterior_branch.py --timestamp 20260601-000068
```

Status:

```text
N5_topological_projector_route_derived_as_conditional_contract_Hodge_projector_no_go_modified_exterior_fork_no_local_GR_promotion
```

Claim ceiling:

```text
N5_contract_only_no_parent_action_or_PPN_promotion
```

## 3. Exact N5 Target

The exterior metric variation must have this form on shell:

```text
delta_g S_projector =
  1/2 int_E sqrt(-g) T_projector_mn delta g^mn
  + boundary.
```

Metric-only local GR requires:

```text
T_projector_mn|bulk = 0.
```

Boundary-only is also acceptable only if the boundary stress is already owned
and does not reintroduce trace-free angular shear.

## 4. Sufficient Route

There is a clean conditional route:

```text
P_mem must be a metric-independent relative/topological chain projector.
```

The sufficient contract is:

```text
delta_g P_mem|E = 0,
d_rel P_mem = P_mem d_rel,
L_projector|E = dB_projector or has no bulk metric dependence.
```

Then:

```text
delta_g S_projector|bulk = 0,
T_projector_mn|bulk = 0.
```

This is the first real N5 mechanism rather than a wish. It says the local
projector cannot be an orthogonal/least-energy metric projection; it has to be
topological at the level of the exterior relative complex.

## 5. Hodge Projector No-Go

The tempting alternative is:

```text
P_mem = Hodge/orthogonal harmonic projector.
```

That fails generically as a metric-only rescue because the Hodge star,
codifferential, Laplacian, Green operator, and harmonic projector all depend on
the metric:

```text
delta_g Pi_H(g) generically contains delta_g Delta_g terms.
```

Therefore:

```text
delta_g P_mem != 0 generically,
T_projector_mn|bulk != 0 generically.
```

So this route may be mathematically elegant, but it punches us in the ribs:
it retains projector stress and blocks vacuum EH reduction.

## 6. Modified Exterior Fork

If projector stress is retained honestly, the local equation is:

```text
G_mn + Lambda g_mn = 8 pi G T_projector_mn.
```

That is not a local-GR derivation. It may still be a valid MTS branch if the
source is conserved, small, and observationally bounded, but it becomes:

```text
modified exterior first,
local-GR limit second.
```

That branch must be tested as a deformation, not announced as GR recovered.

## 7. What Improved

Checkpoint 249 said:

```text
boundary-only projector stress is not derived.
```

Checkpoint 251 improves that to:

```text
boundary/zero stress is derivable if the parent action uses a
metric-independent relative/topological projector.
```

The cost is strict:

```text
if the projector is Hodge/orthogonal/least-energy, N5 fails as a metric-only
local-GR route unless a new source-annihilation theorem is proved.
```

## 8. Claim Policy

Allowed:

```text
N5 has a conditional sufficient mechanism.
```

Forbidden:

```text
N5 is solved in the parent theory,
MTS derives local GR,
MTS passes PPN,
MTS passes Cassini/MICROSCOPE/clocks.
```

Not supported:

```text
the local branch is dead.
```

Correct status:

```text
N5 has a viable topological route, but parent ownership is still open.
```

## 9. Decision

Decision:

```text
N5_topological_projector_route_derived_as_conditional_contract_Hodge_projector_no_go_modified_exterior_fork_no_local_GR_promotion
```

Meaning:

```text
we found the shape of the bridge, not the completed bridge.
```

Main gain:

```text
N5 is no longer just "please vanish"; it now has an exact contract.
```

Main blocker:

```text
the parent action must actually implement this topological projector and show
it reduces to the same FLRW/cosmology memory projector.
```

## 10. Next Target

Next:

```text
252-topological-projector-parent-action-skeleton.md
```

Purpose:

```text
write the minimal parent-action skeleton that owns P_mem as a relative
cohomology chain projector, then check whether the same object can reduce to
the FLRW memory projection rather than becoming a local-only patch.
```

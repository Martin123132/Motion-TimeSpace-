# Parent-Action Or Empirical-Pillar Decision

## 1. Purpose

This file follows:

```text
17-post-checkpoint-promotion-gate-summary.md
```

The question is:

```text
After the local motion-load branch became closure-only, should the next move be
a new parent action attempt or a return to empirical pillars?
```

Short answer:

```text
two-track, parent first. Write the constrained parent-action skeleton next,
then return to empirical pillar testing with the new screening discipline.
```

## 2. Machine Run

Implemented:

```text
scripts/parent_action_or_empirical_pillar_decision.py
```

Successful run:

```text
runs/20260530-233024-parent-action-or-empirical-pillar-decision/status.json
```

Readout:

```text
parent_action_or_empirical_decision_two_track_parent_first
```

Next target:

```text
19-constrained-parent-action-skeleton.md
```

## 3. Decision

The selected strategy is:

```text
two_track_parent_first.
```

Meaning:

```text
1. First write a constrained parent-action skeleton.
2. Do not claim it works unless it closes the exact gates.
3. Then return to empirical pillars using the closure/deviation screening tools.
```

Why not empirical-only?

```text
Because empirical fits without a parent action risk becoming another
phenomenological dark-sector model, not a fundamental field theory.
```

Why not derivation-only?

```text
Because the programme needs data pressure; otherwise it can become beautiful
but unconstrained mathematics.
```

## 4. Ordered Tracks

The ordered tracks are:

```text
1. parent_action_skeleton:
19-constrained-parent-action-skeleton.md

2. empirical_pillar_queue:
20-empirical-pillar-test-queue.md

3. promotion_patch:
deferred_main_workbench_patch_plan.md

4. raw_local_likelihoods:
deferred_local_raw_likelihood_plan.md
```

The main workbench still remains untouched.

## 5. Parent-Action Requirements

The next parent-action skeleton must define:

```text
fields:
metric/coframe, load/capacity variable, R_AB, matter fields.

constraint sector:
whether R_AB=0 is first-class, multiplier-imposed, or emergent.

source matching:
how Q_R=0 or Pi_R=0 follows for compact sources.

local limit:
Newtonian limit, gamma=1, beta=1, universal matter coupling.

cosmology bridge:
how FLRW/cosmology variables come from the same action.

test hooks:
q_R, delta_beta, alpha_clock, epsilon_matter, cosmology amplitudes.
```

Forbidden:

```text
hide GR field equations as definitions;
call multiplier closure a derivation;
assume source neutrality;
fit p=1 from observations;
mix derived variables with fitted closure knobs.
```

## 6. Empirical Pillar Readiness

Current readiness:

```text
local PPN/clocks:
ready as screening, not raw likelihood.

cosmology:
ready for robustness return.

galaxies:
separate repo/thread; empirical pillar only.

EM/time:
needs variable/action mapping before tests.

orbital systems:
partly ready through local PPN sensitivity.
```

## 7. Gate Verdict

Passes:

```text
source 17 complete;
parent action needed;
best default selected.
```

Conditional pass:

```text
empirical tests ready, but only under their own robustness discipline.
```

Fails:

```text
derived local GR available;
main workbench edit allowed;
empirical claim allowed now.
```

Status:

```text
next move is parent-action skeleton;
empirical work follows as disciplined pillar testing;
no main mutation yet.
```

## 8. Next Target

Create:

```text
19-constrained-parent-action-skeleton.md
```

Purpose:

```text
write the minimal action skeleton that could, in principle, turn the local
closure R_AB=0 into a theorem, while explicitly marking which pieces are
derived, postulated, or still closure.
```

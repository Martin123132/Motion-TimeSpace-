# Motion-TimeSpace Research Programme

Motion-TimeSpace (MTS) is an open, work-in-progress research programme exploring whether motion, time, space, memory, and observed gravitational/cosmological structure can be organized into a disciplined field-theoretic framework.

This repository is not presented as a completed theory of physics. It is a public research workbench: derivation attempts, claim ceilings, empirical scorecards, red-team ledgers, and scripts for checking whether parts of the framework survive contact with data and known limits.

## Current Status

The project currently has three active layers:

1. **Empirical closure branch** - a late-time SN+BAO cosmology branch that remains competitive under initial robustness checks.
2. **GR/Newton derivation programme** - a finite theorem-stack route toward source-normalized Newtonian recovery and local GR/PPN silence.
3. **Parent-action formalization** - ongoing attempts to replace closure assumptions with parent-derived variational, projector, domain, source, conservation, and quotient-kernel identities.

The latest public update advances the local-GR/Newton branch from checkpoint `484` to checkpoint `513`. The strongest new result is an exact conditional quotient-kernel theorem: if public local response descends through a parent quotient `q`, the generic `DeltaKTF` transition-shell variation is vertical in `ker(Dq)`, and boundary/exact-current terms are silent, then the local shell projection vanishes. Those parent signatures are not yet proven.

The strongest honest claim is:

> MTS has a live empirical closure branch and a coherent derivation programme toward GR/Newton, including a conditional quotient-kernel route for local shell silence, but it does not yet derive local GR, PPN recovery, Newtonian mechanics, or a completed unified field theory.

## Start Here

- `CLAIM_CEILING.md` - what the repository does and does not currently claim.
- `PROJECT_MAP.md` - guide to the public structure.
- `docs/status/STATUS-2026-07-06.md` - current project status snapshot.
- `docs/theory-gates/LOCAL-GR-NEWTON-GATES.md` - the key GR/Newton/PPN promotion gates.
- `research-programme/checkpoints/106-canonical-R-cosmology-robustness-summary.md` - cosmology robustness summary.
- `research-programme/checkpoints/399-local-GR-status-for-human-review.md` - local GR/Newton status memo.
- `research-programme/checkpoints/460-source-normalized-Newton-branch-theorem-stack.md` - finite Newton theorem stack.
- `research-programme/checkpoints/484-parent-local-zero-action-clause-attempt.md` - earlier parent-local-zero clause attempt.
- `research-programme/checkpoints/513-nonlocal-owner-kernel-theorem-or-shell-projection-arena-transfer-matrix.md` - latest local shell/kernel gate.

## Repository Layout

```text
.
├── CLAIM_CEILING.md
├── PROJECT_MAP.md
├── docs/
│   ├── status/
│   └── theory-gates/
├── research-programme/
│   ├── checkpoints/
│   ├── scripts/
│   └── source-intake/
├── data/
└── archive/
    └── legacy-pre-formalization-2026-06/
```

## Reproducibility Notes

The repository includes scripts and compact residual/register artifacts, but not large third-party datasets, virtual environments, or raw generated run folders.

Large data products should be downloaded from their original public sources where licensing permits. Local machine paths appearing in historical artifacts are retained where they help provenance, but should not be read as portable execution paths.

## Research Ethos

This work is deliberately conservative about claims. A branch can be useful, promising, or competitive without being promoted to a completed theory. Promotion requires derivation, consistency with known limits, and empirical robustness.

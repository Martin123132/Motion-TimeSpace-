# 5237 - Bounded multi-event direct A00 causal runner

## Decision

`ADOPT_BOUNDED_MULTI_EVENT_DIRECT_A00_RUNNER_AND_EXTEND_TO_ENDPOINT_SUMMAND`.

This checkpoint converts the 5235/5236 hand-selected slices into a
deterministic, cached and time-bounded runner.  It selects the strongest real
event in every direct-family/tranche stratum and expands every reciprocal
component before looking at the new roots.

## Coverage

- Direct residue families: `6`.
- Family/tranche strata: `12`.
- Reciprocal components: `16`.
- Component-coordinate jobs: `48`.
- Distinct source events: `12`.
- Outer coordinates: `soft_energy`, `soft_cosine`, and `decay_cosine`.
- Passed jobs: `48/48`.

The dry run fixed the manifest before execution and bounded the job count,
surface scans, roots, topology steps, quadrature orders and wall-clock time.
Each job is independently cached by an input hash.

## Causal result

The all-channel scans found `51`
geometric roots.  The branch-aware winding audit retained
`21` as active and rejected
`30` as inactive.  Residues were fitted
only for active roots; inactive denominator zeros were never subtracted.

Active roots occurred in `18` of the `48` component
slices.  Multi-root overlaps were integrated as patch unions, so overlapping
windows are not double counted.

## Pooled convergence

Relative to the pooled order-512 subtracted result:

- raw order-32 error:
  `0.154837995944`;
- subtracted order-32 error:
  `9.42087689647e-07`;
- subtracted order-128 error:
  `2.06620246408e-07`;
- order-32 improvement:
  `164356.245863x`.

## Failed jobs

- None.

## Scope

This validates a bounded direct-summand computation, not the full
multidimensional A00 coefficient.  Endpoint-owned families still require
their own positive-residue implementation.  No numeric UV, local-GR, or
full-MTS claim is made.

## Next target

Build the endpoint-owned analogue using the same branch tracker and causal
gate, then combine direct and endpoint patch unions in a bounded
multi-event A00 coefficient run.

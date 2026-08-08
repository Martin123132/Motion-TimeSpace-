# 5334 - D4 outer regulator ladder controller

## Derived target

Checkpoint 5324 fixes the missing paired-GL4 outer decay node without an
angular fit:

```text
decay node                       = D4_OUTER;
absolute decay cosine            = 0.8568306300360823;
paired signed Gauss weight       = 0.3461155709117663;
physical phase-space weight      = 0.08652889272794158;
endpoint cap still excluded      = 0.0050000000000000044.
```

The new controller consumes the source-owned 5324 topology rather than
transferring the D2 midpoint geometry.  Its strict coarse preflight derives
`55/55` cubature cells, `13/13` stable soft panels, `78` Q2/Q4 nodes and
`440/440` passing MC04-MC12 identity probes.

## E0025 topology scan

The real coarse scan completed in `3859.23 s`:

```text
completed nodes                  = 78/78;
inner nodes passing              = 78/78;
geometric poles                  = 215;
material simple poles            = 30;
in-support material poles        = 30;
unresolved poles                 = 0;
inner relative error budget      = 4.62860343168e-8;
coarse outer relative change     = 9.37557658956e-1.
```

The large outer change is not accepted as a fixed-decay result.  It localizes
the required event-aligned refinement to panels `8|10|12|13`; no finite value
or angular claim is taken from the coarse scan.

## Support-event derivation

The initial material-pole audit derived six regulator-specific events from the
coarse pole inventory:

```text
support entries                  = 2;
branch deaths                    = 4;
event panels                     = 8|10;
maximum support-margin violation = 0;
maximum branch-error violation   = 0;
maximum panel violation          = 0;
maximum source-bracket violation = 0.
```

These events are interior pole-support strata inside the independent 5324
energy-topology panels.  They are not required to coincide with the 5324
energy-surface boundaries.  The initial mistaken coincidence gate was rejected
and replaced by panel containment, source bracketing, zero support-margin and
branch-death tolerance checks.

## Adaptive event-closure derivation

The original depth-three tree then completed all `468/468` nodes with zero
inner failures, but two of its `31` leaves failed the outer gate and its
conservative relative error was `0.0268791485714`.  Rather than raising the
depth limit, the completed tree was audited for material-pole support-state
changes.  It exposed two crossings absent from the coarse inventory:

```text
panel 8  MC04_SP_DP direct:L:s01
  SUPPORT_ENTRY at x = 0.8088885232984413;
  signed support margin = 3.83693077310e-13.

panel 12 MC04_SM_DM direct:shared:s13
  SUPPORT_EXIT at x = 0.8708639328146937;
  signed support margin = 6.73251454586e-11.
```

The audit finds eight adaptive support transitions: six are independently
covered by the coarse events and exactly these two are uncovered.  Both new
roots satisfy the source bracket and `1e-10` support-margin contract; all `9/9`
event-audit gates pass.  The live plan therefore has eight events in panels
`8|10|12`: three support entries, one support exit and four branch deaths.
Their left/root/right branch states were independently re-evaluated against
the unchanged cubature contract and locked to the immutable pre-extension
manifest, so the event proof does not depend on subsequently overwritten live
aggregate tables.

Only panels `8|12` change geometry.  Exact node-coordinate and mapped-weight
identity allowed `240` unaffected shards to migrate to the extended plan hash;
all `228` old shards in changed panels were forced to recompute.  No numerical
result was reused across changed geometry, and all `10/10` migration gates pass.

## Saved refinement state

After a two-hour extended-plan run, the latest one-hour continuation ran for
`3617.86 s` and stopped at a resumable shard boundary:

```text
encountered nodes                = 414;
complete-pass shards             = 413;
pending shards                   = 1;
failed shards                    = 0;
adaptive panels                  = 34;
saved adaptive leaves            = 29;
decision = D4_OUTER_EVENT_ALIGNED_E0025_PAUSED__RESUME_SHARDS.
```

Every one of the `413` current-plan completed shard results is
`NODE_POLE_SUBTRACTED_ENERGY_INTEGRAL_ACCEPTED`; the latest completed node is
`P12_P12S02R_Q08_N01`, whose Q4/Q8 inner comparison has relative change
`3.40686780251e-15` and zero unresolved poles.  The method is now the
inventory-derived `EIGHT_SUPPORT_EVENTS_SQUARED_Q4_Q8_ADAPTIVE`, the
status and claim fields are D4_OUTER-owned, and all `9/9` semantic gates pass.
The full numerical validation remains intentionally incomplete because one
encountered node and the subsequent adaptive tree are still unfinished.

The exact next action is to resume the same E0025 runner.  Existing shards are
hash-checked and skipped; the scan must not be restarted or replaced by an
angular closure.

```powershell
.\.venv-score\Scripts\python.exe .\scripts\Y5_R2FR_5334_D4_outer_regulator_ladder_controller.py --mode refinement-run --max-runtime-hours 2
```

After E0025 validates, run the six remaining regulator targets.  The old D2
E040 owner-channel certificate is explicitly disabled: a D4-specific
certificate must be derived only if an actual unresolved D4 pole requires it.

## Claim and integrity boundary

This checkpoint has advanced the missing GL4 outer node from a topology-only
contract to a real, partially evaluated fixed-decay calculation.  It has not
yet produced the D4_OUTER regulator-zero value, GL2/GL4 angular comparison,
endpoint-cap bound, phase-space coefficient, UV coefficient, local GR or full
MTS claim.

The protected formalization-workbench digest remains
`0ec1bc6012136ffc6b28a1512aca6ce712b6decd2ff793310a9bd61775f3db1f`.
Generated `.pyc` count is zero.  No GitHub action occurred.  Runs remain
single-threaded and BelowNormal.

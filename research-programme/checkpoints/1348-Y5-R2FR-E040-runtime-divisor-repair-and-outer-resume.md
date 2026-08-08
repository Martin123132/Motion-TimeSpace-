# 5332 - E040 runtime divisor repair and outer resume

## Result

Checkpoint 5330 is rebound to the final checkpoint-5327 source through an
immutable 30-pole certification seed.  This removes the prior provenance cycle
in which an evolving controller aggregate invalidated the theorem certificate
that the same controller needed to load.

The source-bound theorem rerun passes all validation gates:

```text
certified seed poles                     = 30/30;
removable bounded-zero                   = 21;
stable material                          = 9;
maximum removable residue envelope       = 5.56243897158e-9;
maximum material relative spread         = 4.14071207473e-5;
5327 source SHA-256                       = 9775380723fcc31bbb3806cc85e3a5a93a8d7859eddeeee994e89dbe750358bf.
```

## Semantic shard rerun

The E040 rerun selector is evidence based.  A shard is selected when its
manifest state is `COMPLETE_FAIL`, its result is not accepted, and its local
classification file contains an unresolved pole.  No node ID is embedded in
the selector.

The 26 selected shards all reran successfully through the analytic divisor
classifier:

```text
selected                         = 26;
accepted                         = 26;
fresh runtime certificates       = 26;
unresolved poles after rerun      = 0.
```

## Outer continuation

Two capped outer-controller slices were completed.  The second safe pause has
the following aggregate state:

```text
encountered nodes                = 185;
completed pass                   = 184;
completed fail                   = 0;
pending                          = 1;
pending node                     = P08_P08S05_Q08_N01;
pole classifications             = 315;
runtime-evaluated classifications = 65;
runtime-resolved classifications = 65;
unresolved classifications       = 0.
```

The extra 39 runtime rows beyond the repaired 26 are genuinely unseen adaptive
coordinates encountered during the continuation.  Their successful fresh
classification is the transfer test required by checkpoint 5331; it is not a
family-wide exemption.

## Claim boundary

The controller is paused, not complete.  Consequently the finite E040 row is
not accepted and its aggregate error is infinite by construction.  This
checkpoint does not establish the finite regulator integral, regulator-zero
limit, decay-angle integral, UV coefficient, local GR or full MTS.

The protected formalization-workbench digest remains
`0ec1bc6012136ffc6b28a1512aca6ce712b6decd2ff793310a9bd61775f3db1f`,
with modified-file count zero.  No generated `.pyc` remains and no GitHub
action occurred.

## Exact resume

Run another single-thread BelowNormal slice:

```text
.venv-score\Scripts\python.exe scripts\Y5_R2FR_5327_D2_midpoint_regulator_ladder_controller.py --mode run --epsilon-id E040 --max-runtime-hours 1
```

When traversal completes, require finite-row acceptance before executing
`--mode validate-target --epsilon-id E040`.  Checkpoint 5328 is allowed only
after that target validation passes.

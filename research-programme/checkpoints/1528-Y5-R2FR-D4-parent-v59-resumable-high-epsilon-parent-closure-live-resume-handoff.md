# 5512: D4 parent-v59 resumable high-epsilon parent closure live resume handoff

## Run state

- Started: `2026-09-03T12:39:47Z` (`2026-09-03T13:39:47+01:00` local).
- Runner: `scripts/Y5_R2FR_5512_D4_parent_v59_resumable_high_epsilon_parent_closure.py`.
- Runner SHA-256: `7a61ea3f91167e9f948715c2c0693eccdeffbf975ad2201cff04b9fb0a5835a4`.
- Unified execution session: `5040`.
- Numerical worker: PID `13512`, BelowNormal, affinity mask `1` (one logical core).
- Launcher shim: PID `9428`; it is not a second numerical worker.
- Source: frozen checkpoint 5511 frontier `190/2/0`, witnesses `69`, v59 audit rows `34`.
- Target: `R_E0S_E1S_E1S`.
- Target count: one atomic node; between-node budget `12600` seconds.

The strict dry-run passed all eight checkpoint-5511 artifact hashes, source
register, exact pending order, exact partition, signed parent-v59 revision,
both scoped proof-cache bindings, five certified low-epsilon leaves and the
single failed epsilon-pair parent witness.

At `2026-09-03T12:41:55Z`, the worker had accumulated `122.234375`
CPU-seconds, remained BelowNormal on one logical core and had committed zero
checkpoint-5512 records. The inherited frontier therefore remained exactly
`190/2/0`; the pre-evaluation state SHA-256 was
`6c30795524b937b838c6c4730b49bc6eff77581fe71dfc36b48699ee1dfb5596`.

## Resume protocol

1. Poll unified execution session `5040` before launching anything else.
2. If unavailable, inspect the matching Python process and
   `source-intake/functional_rg/5512/work-v1/E07__U051__RIGHT_CONNECTOR__CUBOID__6df3d70a73e4618b.json`.
3. Do not launch a duplicate while a matching process is active.
4. If one record exists, rerun the same command only to regenerate and validate
   reports; the expensive node replays from atomic state.
5. If the process stopped with zero records, checkpoint 5511 remains untouched
   and the same command safely restarts the target.

## Command

`./.venv-score/Scripts/python.exe -B scripts/Y5_R2FR_5512_D4_parent_v59_resumable_high_epsilon_parent_closure.py --target-node-evaluations 1 --max-runtime-seconds 12600`

## Claim discipline

This is a bounded numerical sibling-closure calculation only. Local GR,
Newtonian recovery, Maxwell recovery and full MTS viability remain unclaimed.

## Atomic record one

`R_E0S_E1S_E1S` records `REFINED_X2` after `517.1741068999982` seconds. The
only failed lower is the collision-Jacobian interval at `0.0`; relative-root
and selected-global-root lowers remain positive at `0.9945257922830719` and
`3.2196863886779425`. The source-width rule creates exact children
`R_E0S_E1S_E1S_X0S` and `R_E0S_E1S_E1S_X1S`.

The durable state is `190/3/0`, witnesses `70`, one checkpoint-5512 record,
zero v59 triggers and exact partition error `0.0`. State SHA-256 after record
one is `e967078d0b3e3030ed597fb81250c08f3e8d8d7759054b5913504f7caed7449d`.
All `19/19` interim validation gates pass. Resume with the same command but
set `--target-node-evaluations 2`; the next exact target is
`R_E0S_E1S_E1S_X0S`.

The record-two continuation started at `2026-09-03T12:51:01Z` in unified
session `84167`. Its numerical worker is PID `28300`, BelowNormal with affinity
mask `1`; launcher PID `16432` is non-numerical. Poll session `84167` before
any recovery or relaunch.

## Atomic record two

`R_E0S_E1S_E1S_X0S` records `REFINED_X2` after `437.783756499994`
seconds. Again only the collision-Jacobian interval reaches zero; the two
chart-root lowers remain positive at `0.9945257922830769` and
`3.219686388677946`. The durable frontier is `190/4/0`, witnesses `71`, with
zero unresolved nodes. State SHA-256 is
`7bd9145a8901c232087fda8af4042359c223be7cb4483208826b0af8bd25bff8`.
Resume with `--target-node-evaluations 3`; next target is
`R_E0S_E1S_E1S_X0S_X0S`.

## Atomic record three

`R_E0S_E1S_E1S_X0S_X0S` records `REFINED_T2` after
`402.296269199927` seconds. The collision-Jacobian lower is again the only
zero; relative-root and selected-global-root lowers are
`0.9967065956665725` and `3.2212930514484697`. The exact t children leave
frontier `190/5/0`, witnesses `72`, zero unresolved and state SHA-256
`ceec96d70526ac20ced855cfaa8282fa3d5050368a370aae09868ec690cc6d1b`.
Resume with `--target-node-evaluations 4`; next target is
`R_E0S_E1S_E1S_X0S_X0S_T0S`.

## Atomic record four

`R_E0S_E1S_E1S_X0S_X0S_T0S` records `REFINED_X2` after
`397.858467999962` seconds. Its chart-root lowers remain positive at
`0.9967071872818571` and `3.2212930514484697`; the exact x split leaves
frontier `190/6/0`, witnesses `73`, and state SHA-256
`737da0badb1cdb0519263b66126d2907ad64eb6ec630699dce84c267b1858d68`.

The first four records now reproduce the derived finite-cover sequence
`x, x, t, x`. Resume with `--target-node-evaluations 8`; each subsequent node
is committed atomically and the between-node runtime guard remains `12600`
seconds. Next target is `R_E0S_E1S_E1S_X0S_X0S_T0S_X0S`.

The records-five-through-eight continuation started at
`2026-09-03T13:19:24Z` in unified session `49963`. Numerical worker PID
`26868` is BelowNormal on affinity mask `1`; launcher PID `29552` is
non-numerical. Poll session `49963` before any recovery or relaunch.

At the four-hour continuation check, PID `26868` remained responsive and had
accumulated approximately `13461` CPU-seconds. Five records were durable,
frontier remained `191/5/0`, and record six was still evaluating on one
BelowNormal logical core. Do not interrupt or duplicate it.

## Atomic record six

`R_E0S_E1S_E1S_X0S_X0S_T0S_X1S` passes after
`14537.3579721` seconds. Its denominator and collision-Jacobian lowers are
`1.9203844576531e-08` and `0.74963827195303`; relative-root and selected-root
lowers are `0.958515778338702` and `0.310103322579824`. The invocation then
stops at its between-node runtime guard, leaving durable frontier `192/4/0`,
witnesses `73`, zero unresolved and state SHA-256
`a1979f705c2d0974cbca2840fbe4a84aa096b7fd8ac3ec973d1bfaa09d07e9c7`.
Resume with `--target-node-evaluations 7`; next target is
`R_E0S_E1S_E1S_X0S_X0S_T1S`.

## Atomic record seven

`R_E0S_E1S_E1S_X0S_X0S_T1S` passes after `68.0062279000413`
seconds. Its denominator and collision-Jacobian lowers are
`8.1757891692264e-05` and `0.883162995983218`. The durable frontier is
`193/3/0`, witnesses remain `73`, and state SHA-256 is
`2feb82c1836b5660114acd7e26077593a67df7d83782de6b6935083513f68033`.
Resume with `--target-node-evaluations 8`; next target is
`R_E0S_E1S_E1S_X0S_X1S`.

The record-eight continuation started at `2026-09-03T18:17:06Z` in unified
session `72217`. Numerical worker PID `21492` is BelowNormal on affinity mask
`1`; poll session `72217` before any recovery or relaunch.

## Atomic record five

The first source-scale leaf,
`R_E0S_E1S_E1S_X0S_X0S_T0S_X0S`, is `ACCEPTED` after
`2991.25705620006` seconds. Its denominator and collision-Jacobian lowers are
`1.81504713356609e-07` and `0.460697431506174`; relative-root and selected-root
lowers are `0.944043609382134` and `0.310163042546397`. The durable frontier is
`191/5/0`, with state SHA-256
`755b910fe1af5d8720ed17139910970403d79563857e67a9779b05915c3a29f9`.
The same worker is evaluating record six; do not relaunch it.

## Atomic record eight

`R_E0S_E1S_E1S_X0S_X1S` passes after `6678.03848420002` seconds by
one live parent-v59 trigger, one exact split and one exact aggregate, with no
cache hit. The durable frontier is `194/2/0`, zero unresolved, and state
SHA-256 is
`21d0a0e6bd4a1ad6b23ba57a6f01a43c8c568d09673275d70d299e18f736ecde`.
The only remaining high-epsilon node is `R_E0S_E1S_E1S_X1S`.

The runner's resumable record ceiling was raised from `8` to `16`; no physics,
source, evaluator, split or validation rule changed. The revised runner
SHA-256 is
`6d78c6f752a48e94e6a3ad0d643243ed31d4abb54534457779c41bbc2b62a7f9`.
AST validation and a strict nine-record dry-run both pass. Resume with
`--target-node-evaluations 9`.

The record-nine continuation started at `2026-09-03T20:13:17Z` in unified
session `93575`. Numerical worker PID `26976` is BelowNormal on affinity mask
`1`; launcher PID `2444` is non-numerical. Poll session `93575` before any
recovery or relaunch.

## Completed outcome

Record nine, `R_E0S_E1S_E1S_X1S`, passes after `16392.9466164`
seconds with four parent-v59 triggers, four exact splits, eight live terminal
passes, zero cache hits and four exact aggregates. Across all nine records,
the derived sequence is four refinements followed by five accepted leaves.

Those five leaves and checkpoint 5511's five low-epsilon leaves are pairwise
interior-disjoint and exactly close `R_E0S_E1S`. The ten-leaf union has
rational volume error `0.0`, regular-path upper
`3.6712041095475463e+22`, denominator lower `1.9057482833921196e-08`,
relative-root lower `0.9440436093821337`, selected-global-root lower
`0.3097903003001753` and collision-Jacobian lower
`0.010244978531048046`.

Final frontier is `195/1/0`, witnesses `73`, zero unresolved. All `19/19`
validation gates pass and all `138/138` registered sources exist. The strict
post-run dry-run passes. No checkpoint-5512 worker remains active; next target
is the sole broad sibling `R_E1S`.

Frozen SHA-256 bindings:

- runner: `6d78c6f752a48e94e6a3ad0d643243ed31d4abb54534457779c41bbc2b62a7f9`;
- state: `c3c637a87677d0b3c6e97899ac3e357f8f4e170b5b7b3f45eb26338291dc8ead`;
- result: `696b07b6e843025c69c00c4a465d79bf3b86a0f340b1486eefb229e6c5a585b2`;
- validation: `b9927138a21a53ebd6df175b773fd5f79d5f030f9a46c410ae0e3e18da0e1e09`;
- source register: `5d6c85e41920f478bb68dcc72987ae4868881201f2216ad2c15b3cc4a813ea53`;
- node audit: `1419ca1b8d101c8a425edb7dd7236dc6a9f9477e42dcb852dc35fffab05d4af9`;
- parent-union audit: `f573439f5172244f311c06838c4d6704c90bfc76ba2a972c56c1989d4d358434`;
- v59 audit: `0c2c6fd0ad20895c769cc3721833360c4f06148eeeed4e7862a53b4f40801845`.

At `2026-09-04T00:14:45Z`, record nine was still active. PID `26976` had
accumulated approximately `13004.5` CPU-seconds and remained BelowNormal on
affinity mask `1`. Records one through eight were durable at frontier
`194/2/0`; do not duplicate the live worker.

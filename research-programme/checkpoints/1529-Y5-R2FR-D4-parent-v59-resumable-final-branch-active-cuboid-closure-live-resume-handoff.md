# 5513: D4 parent-v59 final-branch active-cuboid closure live resume handoff

## Completed active cuboid: 2026-09-07 08:50:48+01:00

The final record 45 was accepted. The complete active cuboid is certified:
**218 accepted / 0 pending / 0 unresolved**, 95 refinement witnesses, three
certified nested unions and exact partition-volume error zero. The 23/23
validation rows pass. State and terminal marker agree. The full nested chain
is certified. Record 45 took 11023.311143900006 node seconds.

- State SHA: `7ab2c0b74444f4bfd3d828c0dcf36409fd771d4963ef55012fdbe734e7c2c6e6`.
- Result SHA: `fc13d197f267b3c379ce825cd89e61eda7018f49a80e4afc5722bb4be72bd232`.
- Validation SHA: `e35cf6fdb93830039a9304d9d0d08dc901d1843f4044dab10969d5420b0314ba`.

The certified region has positive lower bounds: collision Jacobian
0.010244978531048046, amplitude denominator 1.5645726337737403e-9,
relative root 0.9413782923495447, selected global root 0.3097899495622827.
Its regular-path upper bound is 1.139554820420109e23. These are regional
certificate bounds, not measured gravitational residuals or global claims.
Full outer-parent enclosure, event-local W3, all-operator local GR and full
MTS flags remain false. **Do not launch record 46: next main target is
OUTER_TRANSPLANT.**

The companion queue terminated after a JSON check-boolean serialization
error. The corrected pilot2 passed preflight, then exposed a fluid-surface
collocation failure; pilot3 reproduced it and localized the residual to
r/R approximately 0.99998031. All failures/snapshots are preserved.
The same fluid equations are now implemented with two regular-endpoint
solutions matched inside the star, instead of pushing a singular endpoint
through a global collocation solve. `coupled-O4-matched1` is the first test
of that numerical formulation. Inspect CURRENT_LOCAL_RESUME and its case
outputs before any successor. Earlier live-worker/queue notes are historical.

## Next-safe-gap reservation: 2026-09-07, O4 coupled implementation

Record 45 remains live, PID 22300; do not duplicate or interrupt it.
The full O4-responsive reference is implemented, compiled and dry-run checked,
but numerical validation is **pending**. The prior 31/31 result is algebra,
not validation of the new coupled star.

A non-numerical supervisor is queued: PID 38144, run
`runs/O4-coupled-pilot1-20260907`, WAITING_FOR_MAIN_45 at 08:16:07+01:00.
It will validate main record 45, then hold the 5513 worker lock while running
the zero-coupling coarse/fine companion pair. **Do not launch D4 46 or another
companion until this supervisor is terminal and its output is inspected.**
It does not launch a D4 successor. One numerical core / BelowNormal throughout.

See `DERIVATION-20260907-O4-coupled-reference-and-weak-kinetic-overlap.md` and
`scripts/parent_O4_coupled_radiation_20260907.py`. The exact new weak delta-K
overlap removes the need for a numerical third metric derivative without
discarding the curvature variation. Independent forced-fluid finite elements
test the collocation result. Signed/half-step probes follow only after the
zero-coupling pair passes. All broad physical claims remain false.

## Latest handoff: 2026-09-07, O4 Hilbert source validated

Record **44** accepted `R_E1S_E1S_E1S_E1S_X0S_X1S` at
`05:22:30+01:00`, in `5432.126889900013` node seconds. The saved frontier
is **217 accepted / 1 pending / 0 unresolved**. All **23/23** main checks
pass; 95 refinement witnesses, two certified nested unions and zero exact
partition error remain. No complete-cuboid or broader physical flag is promoted.

Record-44 hashes:
- State: `4d2e9d67e7e70a9f119a5351a29944e1616a7aefe4a2eb86db04d030b70f90ca`.
- Result: `7c4dceffc14cd4a5491de02b6206c049b32fd7b985a0d53c45a26bb026875b4a`.
- Validation: `9f6ff2fe4cb16ce23641690c93918c90b4072d778718691642de185539d6795b`.

At the safe gap the new `parent_O4_hilbert_source_20260907.py` ran:
**31/31 PASS**, with independent action variations and time-dependent
stress/flux/Ward checks. See
`DERIVATION-20260907-O4-Hilbert-source-and-responsive-matter.md`.
The scalar-only K0 substitution is explicitly rejected by the full source.
This fills the source formulas and derives a conditional derivative-jet
bound; it is not a solved O4 star or a full preparation theorem.
The sharper EOS/interface issue and the correct general-gamma surface
condition are derived for the next coupled implementation.

Result:
`source-intake/local-preparation/20260907/O4-Hilbert-source-initial.json`,
SHA `35a1b3f686f798f22cf16d0106e1e0ade52b2740e6beea60db1923aafbb809ca`.
Executed script SHA:
`9f715865d317493ef9de1ef9d4a2106b9c607826359068bb8d1768397b5e3226`.
Current and historical source hashes agree. The main state was preserved.

Active successor: `runs/5513-node45-20260907`, target **45**, path
`R_E1S_E1S_E1S_E1S_X1S`. Hidden launch `05:45:24+01:00`, running
`05:45:28`; numerical PID **22300**, shim **29556**, supervisor **39696**,
one core and BelowNormal. At `05:46:42` it was live at `72.5625` CPU
seconds; error log empty. Verify the actual process and terminal marker,
state hash and gates before any successor. A single pending region is not
a guarantee of one remaining operation: it can still refine.

Do not rerun completed companion tests or reset the live atomic job.
All earlier handoffs below are preserved as history. No GitHub action or
original-workbench edit was made.

## Latest handoff: 2026-09-07, after the coupled reference test

Record **43** completed at `03:14:47+01:00`, accepting
`R_E1S_E1S_E1S_E1S_X0S_X0S` in `17749.27666199999` node seconds.
The authoritative frontier is **216 accepted / 2 pending / 0 unresolved**.
All **23/23** main validation rows pass, with 95 refinement witnesses,
two certified nested unions and zero exact partition-volume error.
The 146 source paths exist and the original-workbench count gate remains
`before=8760;after=8760`. Broad local-GR/MTS/complete-cuboid flags stay false.

Saved record-43 hashes:
- State: `565ee775558e7019d00b3a2bde749f0ffb5c2d5a28816f06d4792087b13442f6`.
- Result: `c9e09e283f3090de43922d056a52085e5069de840c5c9681a3c0d9712fbfbb6a`.
- Validation: `880aa726e902501bd541fe26359594275973c000cf55cc3c135a9c291f4b85ae`.

Before launching 44, both pending companions were actually run. The final
causal-fluid/metric/radiation pack passes **21/21**, and the final radial
default-path regression passes **13/13**. The first failure, its exact
source versions and later corrections are preserved; see
`DERIVATION-20260906-coupled-fluid-radiation.md` for the new Green identity,
actual numbers, immutable result hashes and the remaining physical scope.
The naive lapse-value overlap remains a cancellation-limited diagnostic;
the independent first-derivative evaluation meets the unchanged threshold.
This reference solve does not derive a full-parent preparation rate.

Active successor: `runs/5513-node44-20260907`, target count **44**, path
`R_E1S_E1S_E1S_E1S_X0S_X1S`. Hidden launch `03:50:11+01:00`,
running `03:50:15`; numerical PID **38052**, shim **39636**, supervisor
**4604**, one core and BelowNormal. At `03:50:30` the numerical worker
was live at `10.484375` CPU seconds and the error log was empty.
Do not duplicate it. Inspect terminal marker/hash/main gates before
launching 45, using the Sept7 run directory rather than Sept6.
The next substantive physics target is the same-action retained O4
metric/matter variation, not a scalar-only K0 substitution.
All preceding companion state/source/archive checks pass; no GitHub action.

The following earlier handoffs are retained as history and are superseded
by this section for process ownership, completion counts and pending tests.

## Current continuation - remaining high-epsilon branch, 2026-09-05/06

### Latest sequential-batch position

| Record | Path | Outcome | Node seconds | Frontier |
| --- | --- | --- | ---: | --- |
| 21 | `R_E1S_E1S` | `REFINED_EPSILON2` | 575.6718799000082 | 205/2/0 |
| 22 | `R_E1S_E1S_E0S` | `REFINED_X2` | 602.5366974000062 | 205/3/0 |
| 23 | `R_E1S_E1S_E0S_X0S` | `REFINED_X2` | 495.38509710000653 | 205/4/0 |
| 24 | `R_E1S_E1S_E0S_X0S_X0S` | `REFINED_T2` | 371.14778739999747 | 205/5/0 |
| 25 | `R_E1S_E1S_E0S_X0S_X0S_T0S` | `REFINED_X2` | 362.41474489998654 | 205/6/0 |
| 26 | `R_E1S_E1S_E0S_X0S_X0S_T0S_X0S` | `ACCEPTED` | 3195.113129000005 | 206/5/0 |
| 27 | `R_E1S_E1S_E0S_X0S_X0S_T0S_X1S` | `ACCEPTED` | 13742.745301100003 | 207/4/0 |
| 28 | `R_E1S_E1S_E0S_X0S_X0S_T1S` | `ACCEPTED` | 95.89557140000397 | 208/3/0 |
| 29 | `R_E1S_E1S_E0S_X0S_X1S` | `ACCEPTED` | 5898.799598400001 | 209/2/0 |
| 30 | `R_E1S_E1S_E0S_X1S` | `ACCEPTED` | 11879.9163901 | 210/1/0 |
| 31 | `R_E1S_E1S_E1S` | `REFINED_EPSILON2` | 514.3710813000071 | 210/2/0 |
| 32 | `R_E1S_E1S_E1S_E0S` | `REFINED_X2` | 522.8598117999936 | 210/3/0 |
| 33 | `R_E1S_E1S_E1S_E0S_X0S` | `REFINED_X2` | 432.5621186999924 | 210/4/0 |
| 34 | `R_E1S_E1S_E1S_E0S_X0S_X0S` | `REFINED_T2` | 345.6521126000007 | 210/5/0 |
| 35 | `R_E1S_E1S_E1S_E0S_X0S_X0S_T0S` | `REFINED_X2` | 342.1709708999988 | 210/6/0 |
| 36 | `R_E1S_E1S_E1S_E0S_X0S_X0S_T0S_X0S` | `ACCEPTED` | 2611.0456061000004 | 211/5/0 |
| 37 | `R_E1S_E1S_E1S_E0S_X0S_X0S_T0S_X1S` | `ACCEPTED` | 13113.79162270001 | 212/4/0 |
| 38 | `R_E1S_E1S_E1S_E0S_X0S_X0S_T1S` | `ACCEPTED` | 104.43662910000421 | 213/3/0 |
| 39 | `R_E1S_E1S_E1S_E0S_X0S_X1S` | `ACCEPTED` | 7033.113149000012 | 214/2/0 |
| 40 | `R_E1S_E1S_E1S_E0S_X1S` | `ACCEPTED` | 16626.018586299993 | 215/1/0 |
| 41 | `R_E1S_E1S_E1S_E1S` | `REFINED_X2` | 523.5733076000179 | 215/2/0 |
| 42 | `R_E1S_E1S_E1S_E1S_X0S` | `REFINED_X2` | 396.5427282000019 | 215/3/0 |

Each completion marker was matched to the authoritative state hash, record
count and passing `23/23` validation table before launching its successor.
Only one numerical worker ran at a time. The five splits narrow the uncertified
region; the subsequent accepted leaves supply new positive-bound certificates,
not just successful refinement/plumbing checks. They are not GR claims.

Latest saved hashes (record 42):
- State: `3bef068fc32eba5b3869e5942a6fa27b85a9a35cd5610d2ed23872b93fc2825e`.
- Result: `7c94a9ee8f744ef68d5b032e655cbe40f8619497bb3438945aa9bd9f7f8753d8`.
- Validation: `f9ff55970230b6e191ca96aafffc75ab4c434d26655278f8307dcb1b2abb7ffb`.

Active run: `runs/5513-node43-20260906/`; target count `43`, path
`R_E1S_E1S_E1S_E1S_X0S_X0S`. Hidden launch at `2026-09-06T22:16:41+01:00`,
running status at `22:16:45`. Numerical PID `3708`, shim `13324`, supervisor
`30912`; one core, BelowNormal. Latest verification at
`2026-09-07T02:09:59+01:00`: numerical CPU `13412.8125` seconds, no reported
worker error. All earlier radial and metric-source companion tests completed
before this launch; the later coupled-fluid pilot/regression remain pending.
The bounded launcher passed its unchanged-runner, input-hash and
duplicate-worker preflight. The four-hour reply handoff does not kill or
restart this unfinished atomic calculation.
This supersedes the earlier process and next-target notes below. Inspect the
run's status, completion marker, logs and actual process before any relaunch.
There are `95` refinement witnesses, two certified nested unions, zero total
partition-volume error and `146/146` existing source paths. No Python cache
was created. The runner's formalization snapshot remains unchanged at `8760`
files before/after. The numerical runner and proof gates were not altered.

Record 42 completed at `2026-09-06T21:54:12+01:00`, exit zero, with all
23 checks passing. It derives a second exact x split because the coarse
collision-Jacobian enclosure reaches zero; relative-root and selected-root
lowers remain `0.9945427532054276` and `3.2196941402294916`. The exact
total partition, both nested certificates and 215 accepted regions survive.

Between records 42 and 43, the radial-overlap companion completed twelve
bound/continuum solves on consistent regular GR stellar backgrounds at
two resolutions/tails. The three packs pass 12/12, 12/12 and 13/13 checks.
The last includes the derived nonconstant-`K_0` on-shell subtraction identity.
Positive finite reference densities are not a full parent rate. The newly
derived exterior metric cubic source passes its own 11/11 checks; metric
backreaction enters at the same amplitude order and must be combined with
the contact source, including interference. See
`DERIVATION-20260906-parent-radiative-overlap.md`, especially section 6.
All result/source/runner hashes were verified; v1 runners and initial
results are retained, the main state was untouched, and all broad gates
remain false.

A later companion is now pending **before record 44**:
`scripts/parent_coupled_fluid_radiation_20260906.py`, with derivation in
`DERIVATION-20260906-coupled-fluid-radiation.md`. It replaces a frozen
material interior by the derived forced conservation/Einstein response and
adds the full metric/contact overlap. Compilation and dry-run pass; the
coupled numerical pilot is not executed while 43 is live. Verify 43's
terminal state, then run the radial default regression and coupled pilot
(`--alpha 0.005 --tag pilot`) before continuing the D4 sequence. Preserve
failures and inspect all reference convergence/constraint checks. The
pre-extension radial runner is archived as `radial-overlap-runner-v2.py`.
The exact regression arguments are `--alphas 0.04 --tag callback-regression`.
At the 2026-09-07 handoff, both intended result JSONs remain absent. Final
source compilation and dry-run pass; no numerical success is inferred.
The existing run folder retains its 20260906 date; a newly launched run 44
should use the actual launch date after the tests, not rename the old run.

Record 41 completed at `2026-09-06T21:43:47+01:00`, exit zero, with all
23 validation rows passing. The coarse collision-Jacobian enclosure reaches
zero while relative-root and selected-root lowers remain
`0.9945427532054226` and `3.2196941402294876`. It therefore derives an exact
x split, not a new accepted leaf or proof of a physical singularity. The
two children replace the parent in the stack; all prior certificates and
the exact total partition remain intact.

Record 40 completed at `2026-09-06T21:07:18+01:00`, exit zero. Its
denominator, relative-root, selected-root and collision-Jacobian lower bounds
are `2.0511825134496592e-08`, `0.9527825299460665`, `0.3097899495622827`
and `0.2948672387836614`. Its regular-path upper is
`1.7573094183928355e+22`, a finite enclosure rather than physical smallness.
The full active cuboid and all broader physical gates remain open.

Record 37 completed at `2026-09-06T13:35:41+01:00`, exit zero. Its own
denominator, relative-root, selected-root and collision-Jacobian lower bounds
are `1.9787812113973668e-08`, `0.9584956604884839`, `0.3101029714875339`
and `0.7496976459912822`. Its integrated regular-path upper bound is
`3.3774445117072384e+17`, a finite enclosure, not a physical smallness claim.
Live v59 passes now total `29`; triggers/splits/cache/aggregates remain
`12/12/0/12`. Both certified nested unions and exact total partition survive.

Record 38 completed at `2026-09-06T13:52:58+01:00`, exit zero, with all
23 validation rows passing. Its denominator, relative-root, selected-root
and collision-Jacobian lower bounds are `8.11914246347395e-05`,
`0.9533953681950565`, `0.30998637474794477` and `0.8828148396872721`.
Its integrated regular-path upper bound is `671389347725.1554`.
Live v59 passes increase to `30`; the internal split counters are unchanged.
The frontier is now `213/3/0`, with no complete-active-cuboid or broader claim.

Record 39 completed at `2026-09-06T15:58:18+01:00`, exit zero, with all
23 checks passing. Its denominator, relative-root, selected-root and
collision-Jacobian lower bounds are `2.6180290237215246e-08`,
`0.9540759846782179`, `0.30997271335516485` and `0.7315523418902248`.
Its integrated regular-path upper bound is `2.3510587580697744e+17`.
One internal adaptive split raises triggers/splits/cache/aggregates to
`13/13/0/13`, with `32` live parent passes. The frontier is `214/2/0`;
both certified nested unions and zero total partition error are preserved.

Between records 39 and 40, the static-parent companion
`DERIVATION-20260906-parent-trapped-energy-bound.md` and its script passed
16/16 checks without changing the main numerical state. Its new result is
a geometry/kinetic-coefficient bound on below-threshold energy excited by
localized data, not a proof of zero occupation or full nonlinear preparation.
Reference quadratures are not D4 interval certificates or measured parent
parameters. The numerical owner and all broad claim gates are unchanged.

Between records 40 and 41, the nonlinear-transfer companion passed its
final compilation/dry-run and 28/28 checks. Its initial nonradiating-source
quadrature failure is retained in a separate JSON; smoothing both endpoints
corrected it without loosening a gate. An exact spectral-moment identity and
independent radial overlap/current controls also pass. The script reconstructs
real controlled historical `c_2` rows, not a numeric parent decay rate.
The exact radial curved-background Wronskian formula is now derived; the
actual parent eigenmode and its outgoing overlap remain the next physics
calculation. Main state/source hashes and all broad claim gates are preserved.

Between records 37 and 38, the independent companion
`DERIVATION-20260906-local-dispersive-preparation.md` and its script were
validated (16/16 checks, approximately 1.02 numerical seconds, main state
unchanged). It derives a conditional free-field local-decay route and an
explicit parent-remainder transfer bound, not full parent preparation.
The already-derived selected two-derivative local GR/Newton/Maxwell branch
is retained; broader all-operator/local-preparation flags are not promoted.

Record 26's accepted leaf has amplitude-denominator lower bound
`1.8153394312591552e-07`, relative-root lower `0.9440290403928252`, selected-
global-root lower `0.31016278720875445`, and collision-Jacobian lower
`0.4625538617193929`. Its parent revision is the unchanged v59 proof-carrying
adaptive x/t cover. The run completed at `2026-09-05T22:09:46+01:00`, exit
zero, with an empty error log. It used one live parent pass, giving `19`
cumulative live passes; v59 triggers/splits/cache hits/aggregates stay `8/8/0/8`.
This certifies only that subregion. The active cuboid, full outer enclosure,
event-local W3, local GR and full MTS remain open.

Records 27 and 28 completed at `2026-09-06T02:23:22+01:00` and `02:28:14`
local, respectively; both exit codes were zero. Their markers and passing
validation tables were checked before each next invocation. Record 27's
denominator, relative-root, selected-root and collision-Jacobian lower bounds
are `4.293737448574776e-09`, `0.9585006754134998`, `0.3101030672913443`,
and `0.7496493147155993`. Record 28's corresponding lower bounds are
`8.133262647512358e-05`, `0.9533955422715236`, `0.3099864705157335`,
and `0.8829013616709418`. These are positive certificates for their own
regions, not a closure of the remaining branch or a calibrated physical bound.
Cumulative live parent passes are now `21`; triggers/splits/cache hits/
aggregates remain `8/8/0/8`. Accepted paths are unique and positive, total
partition-volume error is zero, and both previously certified nested unions
remain intact. Full-outer, event-local W3, local-GR and full-MTS flags stay false.

Record 27's state hash, also retained as record 28's input hash, is
`f602675f1f3ae84c2b73ed652cdd29bf8feec47c3dd00ff7465d6b8a45b4549f`;
result hash `492be5aa1501aab96e1334240c3ebc2a897e5760936a8be444323aef17802466`;
validation hash `0e56c7d4dad67889f5d0b2878d8c4fa79475f749d5bc57a603955dcc484015ea`.
Run directories `5513-node27-20260905` and `5513-node28-20260906` preserve
their individual completion logs. Neither calculation was duplicated after a
long observation wait; process identity was checked before taking further action.

Record 29 completed at `2026-09-06T04:08:57+01:00`, exit zero. The node
took `5898.799598400001` seconds; its whole invocation was about 1 h 40 m.
The accepted denominator lower bound is `2.6739877392970034e-08`, relative-
root lower `0.9540761593793682`, selected-root lower `0.30997280911873304`,
and collision-Jacobian lower `0.731508477266036`. Its integrated regular-path
absolute upper bound is `2.2901582155877533e+17`: finite, not a claim of
physical smallness. One new internal v59 adaptive split was required; the
cumulative triggers/splits/cache hits/aggregates are now `9/9/0/9`, with
`23` live parent passes. No outer subdivision or discarded failure was hidden.

The marker, saved hash, exact record count and `23/23` passing validation rows
were checked before record 30's preflight and launch. All `146` source paths
exist, all accepted bounds are positive, paths are unique, and total partition
error remains zero. The runner reports the formalization snapshot unchanged
(`8760` before/after); no Python cache exists. The two previously certified
nested unions remain intact, but the active cuboid and all broader claims
remain open. The two pending paths are not a two-calculation completion promise.

Record 30 completed at `2026-09-06T07:43:11+01:00`, exit zero, with
denominator lower `2.3412334679660946e-08`, relative-root lower
`0.9527827046253218`, selected-root lower `0.3097900452693874`, and
collision-Jacobian lower `0.3481896124161985`. Its integrated regular-path
absolute upper bound is `1.6475514305988113e+22`, finite rather than small.
Cumulative live parent passes reached `27`; v59 triggers/splits/cache hits/
aggregates reached `12/12/0/12`. This did not close the active cuboid.

The remaining sibling `R_E1S_E1S_E1S` failed its coarse Jacobian enclosure
and was split in epsilon by record 31, completed at `08:07:54` local. Record
32 then split its first child in x, completed at `08:20:46`. The positive
root bounds were retained, but the zero-containing Jacobian intervals were
not promoted to positive certificates or interpreted as actual singularities.
All `23/23` checks passed after each commit; markers, state hashes and source
preservation were verified before the next bounded launch. The runner reports
the formalization snapshot unchanged (`8760` before/after), and no Python cache
exists. The three pending regions are not an estimate of remaining job count.

Records 33, 34 and 35 completed at `08:31:58`, `08:41:46` and `08:50:51`
local on 2026-09-06. Each retained the coarse zero-containing collision-
Jacobian interval as a refinement witness while the root factors stayed
positive. No new accepted leaf is claimed from these subdivisions. All three
completion markers, state hashes and passing `23/23` validation tables were
checked before launching the next invocation. The next candidate must pass
its own bound checks; earlier sibling certificates are not substituted for it.

Record 36 passed independently and completed at `2026-09-06T09:37:35+01:00`,
exit zero. Its amplitude-denominator, relative-root, selected-root and
collision-Jacobian lower bounds are `1.8155551236521217e-07`,
`0.944024205336257`, `0.3101626913864941`, and `0.46319701723480045`.
The integrated regular-path absolute upper bound is `2581959563864254.0`;
this is a finite enclosure, not a physical-smallness claim. One further live
parent pass brings the count to `28`; triggers/splits/cache hits/aggregates
stay `12/12/0/12`. No new outer split was required for this accepted leaf.

The completion marker, saved hash and passing `23/23` validation rows were
checked before record 37's preflight and launch. Earlier accepted leaves are
preserved with positive bounds and unique paths, total partition error remains
zero, and both certified nested unions remain intact. The formalization
snapshot is reported unchanged (`8760` before/after), no Python cache exists,
and all `146` source paths were checked during this continuation. Active-cuboid,
full-outer, event-local W3, local-GR and full-MTS claims remain unproved.

A roughly 3-5-hour planning range is reasonable for this neighbouring candidate,
not a completion guarantee; the runtime guard remains between nodes. The conversation
returns now, within its four-hour check-in cap, while this authorized single-
node job runs independently. No automatic follow-up or GitHub action was made.

### Earlier continuation evidence

Record twenty-one was recovered from the completed run, not restarted.
`runs/5513-node21-20260905/completion.marker` matches the authoritative
state hash and reports exit zero at `2026-09-05T18:03:34+01:00`; no matching
MTS process remained at the next goal check. Outcome: `REFINED_EPSILON2`
for `R_E1S_E1S`, numerical runtime `575.6718799000082` seconds.

The coarse enclosure could not exclude a zero collision Jacobian. Its
relative-root and selected-global-root bounds were positive, approximately
`0.9971347346572067` and `3.2216319899705064`. This does not prove an actual
zero or a physical singularity. The unresolved coarse attempt is retained as
a refinement witness, with exact children `R_E1S_E1S_E0S` and
`R_E1S_E1S_E1S`; neither child is certified by this split.

Durable state: `21` records, `205/2/0`, `84` refinement witnesses. All `23/23`
saved validation checks pass; accepted prefixes and exact partition remain
preserved, both completed nested unions remain certified, and the runner
reports the formalization snapshot unchanged (`8760` files before/after).
The active-cuboid, full-outer, event-local W3, local-GR and full-MTS claims
remain false.

Record-twenty-one hashes:
- State: `19265cb4790459b3874d2d14b7a4d30caec3a0fa48627197479e40c2dda3c359`.
- Result: `f9bcf4cb3537b08c9f76a986f715ade36bb5c1a5158fe77200fa56e3ee0f22d6`.
- Validation: `020d3320d244a5c92442c6137894e10286c242e8ae358e9550d30c277e5a7b9e`.

The bounded launcher passed `-ValidateOnly` for absolute target `22` and
run ID `5513-node22-20260905`. It was then started hidden at
`2026-09-05T20:22:59+01:00`, status `RUNNING` at `20:23:02` local.
Numerical PID `7564`, venv shim `10772`, supervisor `16720`. Both Python
processes were confirmed BelowNormal with affinity `1`; only `7564` computes.
No unrelated process was changed. Worker/startup error logs were empty.

Target: `R_E1S_E1S_E0S`, from the state hash above, using the unchanged
runner and its between-node `12600`-second guard. Inspect
`runs/5513-node22-20260905/status.json`, logs, completion marker and live
process before any recovery. One new record per invocation; a split can
increase the pending count. No GitHub action occurred.

## Historical background continuation - record twenty-one, 2026-09-05

Authorized by the user's continuation request. After verifying the successful
record-twenty result and completion marker, the bounded launcher passed its
`-ValidateOnly` input/hash/duplicate-worker preflight for absolute target `21`.
All `146` registered source paths exist. The numerical runner is unchanged.

Run directory: `runs/5513-node21-20260905/`. The hidden supervisor started
at `2026-09-05T17:52:09+01:00`; status became `RUNNING` at `17:52:12` local.
Numerical PID `8020`, venv shim PID `11728`, PowerShell supervisor PID `15536`.
The numerical worker and shim were confirmed BelowNormal, affinity mask `1`;
only PID `8020` computes. The unrelated RN task is untouched.

Target: `R_E1S_E1S`, using the twenty-record state hash below and unchanged
runner SHA-256 `7349a0db3653c8038f2b14018b996ff94181800093bb8818d78c170f5c2ec6ff`.
The invocation commits at most one new record before returning. Refinement
is a legitimate outcome and can create more pending children; one branch is
not a guarantee of one remaining computation.

Read `status.json`, `log.txt`, `error.txt` and `completion.marker` in the run
directory, plus `runs/5513-node21-20260905-launcher.stderr.txt` for startup
errors. Error logs were empty at startup. This detached job has no unified
execution session. Inspect the actual process and authoritative saved state
before recovery; never repeat an already committed record.

The earlier sibling coarse evaluation took `728.658251099987` seconds before
epsilon refinement. A check after approximately 30 minutes is reasonable,
but this is not a completion forecast for the branch. The runtime guard
remains `12600` seconds between nodes, not a hard timeout. No automatic
follow-up was scheduled. No GitHub action occurred.

## Historical saved result - record twenty accepted, 2026-09-05

Run `runs/5513-node20-20260905/` finished at `2026-09-05T15:57:16+01:00`
with exit code zero, empty error logs and a `PAUSED_RESUMABLE` completion
marker whose state hash matches the authoritative file. The old worker,
shim and supervisor are no longer active.

Accepted node: `R_E1S_E0S_E1S_X1S`; node runtime `13852.950303099999`
seconds (approximately 3 h 51 m), full invocation about 3 h 53 m.
Frontier: `205/1/0`, committed records `20`, refinement witnesses `83`.
All `23/23` validation gates pass and all `146` source paths were rechecked.
The runner reports the formalization snapshot unchanged (`8760` before/after);
no `scripts/__pycache__` exists. No numerical formulas or proof gates changed.

The larger nested union `R_E1S_E0S` is now certified under ten accepted
leaves with zero exact volume error and pairwise-disjoint interiors. Its
minimum amplitude-denominator bound is `1.1672233223868317e-08`, relative-root
bound `0.9440338966484806`, selected-global-root bound `0.3097901357249221`,
and collision-Jacobian bound `0.4019341479846927`. Its integrated regular-path
absolute upper bound is `2.9904202921298677e+22`. This is a finite bound, not
a smallness or phenomenological-viability claim.

There are now two certified nested unions. The complete partition, including
the pending region, still has zero volume error. The active cuboid itself
is not closed because `R_E1S_E1S` remains pending. Full outer enclosure,
event-local W3, local GR and full MTS remain unclaimed.
Cumulative v59 triggers/splits/cache hits/aggregates: `8/8/0/8`; live parent
passes: `18`.

Saved hashes:
- State: `9d1f45e08f3784d1fdd60d4967f8c2a517690185a29cd3534e180ac1566301db`.
- Result: `809186e7b8ea3b67d9a7ea5d43a93534268a6faf970f6d0b8b959d13c7ff0d08`.
- Validation: `5859ae9694688545ae366abde83a08c3449bbc8c92ec3894191ddbae74d7f464`.

## Historical background continuation - record twenty, 2026-09-05

Authorized by the user's continuation request. The existing bounded launcher
passed its non-numerical input/hash/duplicate-worker check and all `146`
registered source paths exist. No numerical formulas or proof gates changed.
The supervisor was started hidden at `2026-09-05T12:04:20+01:00`; status
became `RUNNING` at `12:04:23` local.

Run directory: `runs/5513-node20-20260905/`.
Numerical PID `7680`, venv shim PID `15196`, PowerShell supervisor PID `3628`.
All are BelowNormal with affinity mask `1`; only PID `7680` computes.
The unrelated RN task remains untouched. There is no unified execution session.

Target: `R_E1S_E0S_E1S_X1S`, absolute record count `20`, source state hash
`5b87a90ea92ea41d99e89587d3eb64bce9ab1f5a6437b42a6c894c74f57845e8`.
The unchanged runner SHA-256 is
`7349a0db3653c8038f2b14018b996ff94181800093bb8818d78c170f5c2ec6ff`.
One additional atomic record is authorized for this invocation, not an
unbounded continuation. A refinement outcome leaves its children pending.

Inspect `status.json`, `log.txt`, `error.txt` and `completion.marker` in the
run directory. Startup stderr is also retained in
`runs/5513-node20-20260905-launcher.stderr.txt`; both error logs were empty
at startup. The completion marker means the invocation stopped, not that the
active cuboid or MTS theory is certified. Check the process and authoritative
state before recovery; never repeat a node that has already committed.

Estimated runtime: approximately 4-5 hours (around 16:05-17:05 BST), with
possible contention or refinement overrun. The `12600`-second runtime guard
is between nodes and will not kill an unfinished evaluation. The conversation
is released while the job runs; no automatic follow-up was scheduled.
The saved nineteen-record result below remains authoritative until the next
atomic commit and validation. No GitHub action occurred.

## Historical saved result - record nineteen accepted, 2026-09-05

Run `runs/5513-node19-20260905/` finished at `2026-09-05T02:07:03+01:00`
with exit code zero, an empty error log and a `PAUSED_RESUMABLE` completion
marker. The worker, shim and supervisor from that run are no longer active.
The marker's state hash matches the authoritative numerical state.

Accepted path: `R_E1S_E0S_E1S_X0S_X1S`. Node runtime:
`7094.1971558000005` seconds; accepted-record time
`2026-09-05T01:06:51.370661+00:00`. Frontier is `204/2/0`, committed records
`19`, refinement witnesses `83`. All `23/23` validation rows pass; `146` source
paths are recorded. Accepted bounds are positive, paths are unique and exact
total partition-volume error is zero when the pending regions are included.
The runner reports the formalization snapshot unchanged (`8760` before/after),
and no `scripts/__pycache__` exists. Cumulative v59 triggers/splits/cache hits/
aggregates are `5/5/0/5`; live parent passes are `14`.

Exactly one nested union is certified. `R_E1S_E0S` currently contains nine
accepted leaves but retains a pending region, so it is not yet certified.
No active-cuboid, full-outer, event-local W3, local-GR or full-MTS claim follows.

Saved hashes:
- State: `5b87a90ea92ea41d99e89587d3eb64bce9ab1f5a6437b42a6c894c74f57845e8`.
- Result: `547a0d511052367653e539a6a3d0273e8adb0d059e8a7b2abf998a11d3232a69`.
- Validation: `7aecdca95ba5b21ed9cbaabaec804e4e32b6a47b9c89c46bf62287328ca29426`.

Next path: `R_E1S_E0S_E1S_X1S`, absolute target count `20`. The existing
`scripts/run_5513_bounded.ps1` passed `-ValidateOnly` for run ID
`5513-node20-20260905`, including this state hash, unchanged runner hash,
nineteen prior records and no matching worker. Acceptance without subdivision
would supply the tenth leaf of `R_E1S_E0S`; require its exact union audit
before calling that parent closed. The other pending region is `R_E1S_E1S`.
The earlier counterpart took roughly `16547` seconds (4 h 36 m), so allow
4-5 hours or more under contention. The runtime guard remains between nodes,
not a hard timeout. Keep one numerical worker, one core and BelowNormal.

## Historical background continuation - record nineteen, 2026-09-05

The user authorized the next node. `scripts/run_5513_bounded.ps1` passed its
non-numerical `-ValidateOnly` input check, including the unchanged numerical
runner hash, exact saved-state hash, 18 prior records, a clean pending
frontier and no matching active MTS worker. The numerical runner also retains
its own inherited-source and proof gates before evaluation.

The hidden PowerShell supervisor started at `2026-09-05T00:06:52+01:00`.
Run directory: `runs/5513-node19-20260905/`; status `RUNNING` was confirmed
at `00:06:59` local. Numerical worker PID `13728`, venv shim PID `12268`,
supervisor PID `8976`; all have affinity `1` and BelowNormal priority. Only
PID `13728` performs numerical work. This is a detached process, not a unified
execution session.

The target is `R_E1S_E0S_E1S_X0S_X1S`, absolute record count `19`, using
the record-eighteen state hash below and `--max-runtime-seconds 12600`.
The helper limits each invocation to one new committed record and prevents
duplicate helper launches with an exclusive lock. It records `PAUSED_RESUMABLE`
on a successful partial completion, or `FAILED` with an error. Job completion
is not checkpoint-wide certification.

Read `status.json`, `log.txt`, `error.txt` and `completion.marker` in the run
directory. Startup errors are also captured in
`runs/5513-node19-20260905-launcher.stderr.txt`. Before any recovery, inspect
the live process and the authoritative numerical state, even if a status file
still says running. Never repeat the node if record nineteen already committed.

Estimated duration is 2-3 hours based on the earlier counterpart's roughly
6714 seconds plus setup and contention. The between-node guard does not kill
an unfinished node. The conversation is released while this authorized job runs;
the next user check should read its actual result rather than start another job.

## Historical saved result - record eighteen accepted

Authorized after the 2026-09-04 cross-repo review. Strict source dry-run
passed with matching inherited hashes, exact source partition and positive
accepted bounds. The command began at `2026-09-04T23:54:20+01:00`:

`./.venv-score/Scripts/python.exe -B scripts/Y5_R2FR_5513_D4_parent_v59_resumable_final_branch_active_cuboid_closure.py --target-node-evaluations 18 --max-runtime-seconds 12600`

Session `54865` exited successfully after accepting
`R_E1S_E0S_E1S_X0S_X0S_T1S` at `2026-09-04T23:58:07+01:00`.
Node runtime: `85.79101470000023` seconds. Worker PID `6928` used BelowNormal
priority and affinity mask `1`; it and launcher PID `16548` were confirmed
gone after completion. No further worker was launched.

The durable state is now `18` records, `203/3/0`, and `83` refinement witnesses.
The new leaf's amplitude-denominator lower bound is `8.147470753116109e-05`,
relative-root lower `0.9533957487359181`, selected-root lower
`0.3099865610286224`, and collision-Jacobian lower `0.8829885582064088`.
It required no new v59 split and retained all earlier accepted witnesses.
All `23/23` validation gates pass; sources `146/146`; formalization snapshot
unchanged at `8760` files; no `scripts/__pycache__`. The exact total partition
has zero volume error. Only one nested union is complete; the active cuboid
and all broader claim flags remain false.

Saved hashes:
- State: `c9a5854dc0ea0af1e3b1c7a5ee70f16636d3f795a4fb64c6a2ba64e5b495324f`.
- Result: `7a1521d811ee8829eec622b9fdaacaa9b44b6f211a0513c9e8e9482bb4e45390`.
- Validation: `ffc5c0419614b79394ae66f85f97cb50f1431b65a15b02775aedc1f2234c9f42`.

Next path: `R_E1S_E0S_E1S_X0S_X1S`. Check for any matching live worker,
then resume the same script with `--target-node-evaluations 19` and
`--max-runtime-seconds 12600`. Its earlier low-epsilon counterpart took
about `6713.57` seconds; that is a rough planning reference, not a deadline.
The one-node target returns after its next committed result even if more
branches remain. Preserve the one-core BelowNormal limit.

## Historical saved state - record seventeen, 2026-09-04

This entry supersedes the historical process IDs and resume commands below.
At `2026-09-04T23:18:12+01:00`, the process inventory contained no Python
workers. The last node, `R_E1S_E0S_E1S_X0S_X0S_T0S_X1S`, was accepted
and committed at `2026-09-04T22:05:21+01:00`; reports were written by
`22:05:31` local. Its measured evaluation runtime was
`17721.106480699964` seconds, about 4 h 55 m.

There are `17` committed records (the last record's zero-based ordinal is
`16`), frontier `202/4/0`, and `83` refinement witnesses. The saved result
reports all `23/23` validation gates passing, positive bounds on all accepted
leaves, unique accepted paths, and zero partition-volume error when pending
regions are included. One nested union is certified. The final branch and
active cuboid are still incomplete; all broader claims remain false.

State: `source-intake/functional_rg/5513/work-v1/E07__U051__RIGHT_CONNECTOR__CUBOID__6df3d70a73e4618b.json`.
State SHA-256: `46e18605d7238a3bb942baa9e380698d5c0ef409a3f7fc5e3d6b7b96187b477d`.
Next path: `R_E1S_E0S_E1S_X0S_X0S_T1S`.

The user is coordinating a Codex update; no new numerical worker was launched
during this review. On continuation, first confirm there is no matching worker,
then use the existing state with an absolute target of `18` for one more node:

`./.venv-score/Scripts/python.exe -B scripts/Y5_R2FR_5513_D4_parent_v59_resumable_final_branch_active_cuboid_closure.py --target-node-evaluations 18 --max-runtime-seconds 12600`

The runtime guard operates between nodes. It does not interrupt or save a
partially evaluated node at four hours. Keep the one-core BelowNormal limit;
report any overrun while allowing the current node to commit. Pending branches
may subdivide, so their count is not an estimate of remaining evaluations.

## Run state

- Started: `2026-09-04T01:07:02Z` (`2026-09-04T02:07:02+01:00` local).
- Runner: `scripts/Y5_R2FR_5513_D4_parent_v59_resumable_final_branch_active_cuboid_closure.py`.
- Runner SHA-256: `7faa1c16a8b8e490ddbfdfd8de4b23c68874ea778ab835574f1a74c7c30699eb`.
- Unified execution session: `25975`.
- Numerical worker: PID `30540`, BelowNormal, affinity mask `1`.
- Launcher shim: PID `18292`; it is not a second numerical worker.
- Source: frozen checkpoint 5512 frontier `195/1/0`, witnesses `73`, v59 audit rows `55`.
- Target: sole pending root branch `R_E1S`.
- Target count: one atomic node; between-node budget `12600` seconds.

The strict dry-run passes all eight checkpoint-5512 artifact hashes, source
register, exact pending order and exact partition. It proves that the `195`
source accepted paths are unique, all required bounds are positive, the root
has exactly one refinement witness, parent v59 reconstructs at its signed
revision and both proof-cache bindings remain scoped.

Checkpoint 5513 adds an independent root-union gate. Emptying the stack is not
sufficient: active-cuboid certification additionally requires every accepted
leaf to be unique, positive-bound, pairwise interior-disjoint and an exact
rational-volume cover of `R`. Full outer and every broader local-GR/MTS flag
remain false even if this narrow gate closes.

At `2026-09-04T01:11:35Z`, the worker had accumulated about `196` CPU-seconds.
No checkpoint-5513 record had committed, so the inherited frontier remained
`195/1/0`. Pre-evaluation state SHA-256:
`4eb8f5a2cb4f140523e1e3320977b12edc3be06099c34e20a1bed3ec27fbfaee`.

## Resume protocol

1. Poll unified session `25975` before launching anything else.
2. If unavailable, inspect PID `30540` and
   `source-intake/functional_rg/5513/work-v1/E07__U051__RIGHT_CONNECTOR__CUBOID__6df3d70a73e4618b.json`.
3. Do not launch a duplicate while a matching process is active.
4. If a record exists, rerun only to regenerate/validate reports; the atomic
   state avoids repeating completed nodes.
5. If zero records and no process remain, checkpoint 5512 is untouched and the
   command can safely restart.

## Command

`./.venv-score/Scripts/python.exe -B scripts/Y5_R2FR_5513_D4_parent_v59_resumable_final_branch_active_cuboid_closure.py --target-node-evaluations 1 --max-runtime-seconds 12600`

## Claim discipline

This calculation can certify only one active outer cuboid. It cannot by itself
establish full outer coverage, event-local/combined `W3`, regulator removal,
all-operator local GR, Newtonian recovery, Maxwell recovery or full MTS.

## Atomic record one

`R_E1S` records `REFINED_EPSILON2` after `1177.5261103001` seconds. The
collision-Jacobian interval alone reaches zero; relative-root and
selected-global-root lowers remain positive at `0.9970813536728632` and
`3.221613679619237`. The exact epsilon children are `R_E1S_E0S` and
`R_E1S_E1S`.

The durable frontier is `195/2/0`, witnesses `74`, zero unresolved and exact
partition error `0.0`. Checkpoint 5512's nine records remain intact and the
adapter recovery key is absent. State SHA-256 is
`161d3e0c7c19ad85fbdeb1ba5208db4c47b765d058348f43dff729a81ce70557`.
Resume with `--target-node-evaluations 2`; next target is `R_E1S_E0S`.

## Atomic record two

`R_E1S_E0S` records `REFINED_EPSILON2` after `728.658251099987`
seconds. Again only the collision-Jacobian interval reaches zero; relative-root
and selected-global-root lowers remain positive at `0.9971561415613306` and
`3.2216385269433827`. The exact children are `R_E1S_E0S_E0S` and
`R_E1S_E0S_E1S`.

The durable frontier is `195/3/0`, witnesses `75`, zero unresolved and state
SHA-256 `f31df41712890b7df0d42f823c93021d3cc17c0e7f4245e39a70df9b93f60ee2`.
Resume with `--target-node-evaluations 8`; next target is `R_E1S_E0S_E0S`.

The records-three-through-eight continuation started at
`2026-09-04T01:45:09Z` in unified session `23617`. Numerical worker PID
`23216` is BelowNormal on affinity mask `1`; launcher PID `1928` is
non-numerical. Poll session `23617` before any recovery or relaunch.

The record-two continuation started at `2026-09-04T01:30:09Z` in unified
session `95281`. Numerical worker PID `3480` is BelowNormal on affinity mask
`1`; launcher PID `24652` is non-numerical. Poll session `95281` before any
recovery or relaunch.

## Records three through seven

Records three through six derive the exact refinement sequence `x, x, t, x`
below `R_E1S_E0S_E0S`; every failed coarse box has only a zero
collision-Jacobian interval while both chart-root lowers stay positive.
Record seven, `R_E1S_E0S_E0S_X0S_X0S_T0S_X0S`, passes after
`3773.91969570005` seconds. Its denominator and collision-Jacobian lowers are
`1.81511438486358e-07` and `0.461316892960348`.

At `2026-09-04T05:47:52Z`, seven records were durable at frontier `196/6/0`,
witnesses `79`, zero unresolved and state SHA-256
`0d098ff8d9f968b9219cea3dc226080cebdf2a6f9432c5baedc22a744fbe39f6`.
Record eight remained active in session `23617` on one BelowNormal core.

## Atomic record eight

`R_E1S_E0S_E0S_X0S_X0S_T0S_X1S` passes after
`14865.6276093001` seconds. Its denominator and collision-Jacobian lowers are
`1.89639197434878e-08` and `0.749642997047084`; both root lowers remain
positive. The durable frontier is `197/5/0`, witnesses `79`, zero unresolved,
and state SHA-256 is
`8a3244012387de73beafee5b7ba9183a40e6a3e80d09df0d232c9c5c5f0d5a11`.
Resume with `--target-node-evaluations 16`; next target is
`R_E1S_E0S_E0S_X0S_X0S_T1S`.

## Records nine and ten

`R_E1S_E0S_E0S_X0S_X0S_T1S` and `R_E1S_E0S_E0S_X0S_X1S`
both pass, after `80.47` and `6713.57` seconds respectively. The durable
frontier is `199/3/0`, witnesses `79`, zero unresolved and state SHA-256
`6b5405ff1fc28a9ebc830327f6c77b5fb8d19a70578a080694af42c88e8251ed`.

At the four-hour continuation check, record eleven remained active on worker
PID `3952`, BelowNormal with affinity mask `1`. Do not interrupt or duplicate
session `64750`.

The records-nine-through-sixteen continuation started at
`2026-09-04T07:33:40Z` in unified session `64750`. Numerical worker PID `3952`
is BelowNormal on affinity mask `1`; launcher PID `17364` is non-numerical.
Poll session `64750` before any recovery or relaunch.

## Atomic record eleven

`R_E1S_E0S_E0S_X1S` passes after `16547.2700151` seconds using four
live parent-v59 triggers, four exact splits, zero cache hits and four exact
aggregates. Its denominator and collision-Jacobian lowers are
`2.44590822930423e-08` and `0.45566733237234`. The durable frontier is
`200/2/0`, witnesses `79`, zero unresolved and state SHA-256
`249be01f8b7fce5130e77fe8a34038a8c9ef65949e553809d73465ef6453eda5`.

The runner now independently audits exact nested unions at
`R_E1S_E0S_E0S`, `R_E1S_E0S` and `R_E1S` before allowing the root flag. No
evaluator or physics rule changed. Revised runner SHA-256:
`7349a0db3653c8038f2b14018b996ff94181800093bb8818d78c170f5c2ec6ff`.
The revised strict dry-run passes. Resume with `--target-node-evaluations 16`;
next target is `R_E1S_E0S_E1S`.

## Records twelve through sixteen

Records twelve through fifteen derive `x, x, t, x` beneath
`R_E1S_E0S_E1S`; record sixteen's first terminal leaf passes after
`3768.15046430007` seconds. Frontier is `201/5/0`, witnesses `83`, zero
unresolved and state SHA-256
`11deff90623e9e09acf046ac5903b48d666d11fede8efede94770cb43e377370`.

The new nested audit proves `R_E1S_E0S_E0S` is an exact, pairwise-disjoint
five-leaf union with zero rational volume error. The two larger parents remain
correctly incomplete. All `23/23` validation gates pass. Resume with
`--target-node-evaluations 24`; next target is
`R_E1S_E0S_E1S_X0S_X0S_T0S_X1S`.

The records-seventeen-through-twenty-four continuation started at
`2026-09-04T16:08:10Z` in unified session `78489`. Numerical worker PID
`20952` is BelowNormal on affinity mask `1`; launcher PID `14208` is
non-numerical. Poll session `78489` before any recovery or relaunch.

The record-twelve continuation started at `2026-09-04T14:26:14Z` in unified
session `97935`. Numerical worker PID `31540` is BelowNormal on affinity mask
`1`; launcher PID `9812` is non-numerical. Poll session `97935` before any
recovery or relaunch.

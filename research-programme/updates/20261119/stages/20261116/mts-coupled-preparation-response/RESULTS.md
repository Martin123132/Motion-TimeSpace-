# Coupled background, preparation and live surroundings

Completed local manual stage, 16 November 2026. This extends the retained
background calculation; it does not replace the MTS action or start another
theory. Persistent goal remains paused. No publication or new fit.

## What changed physically in this calculation

The accepted coherent background now drives the **complete retained active
perturbation system**, including surrounding ordinary matter, radiation,
neutrinos, both scalar modes where present, and the metric. The original
native species equations own that response. The thermo/opacity response is
derived on the saved RECFAST branch, not set to zero.

A complete saved native state is matched ONCE at the common earliest time.
The 902 later preparation states are evolved from that state; they are not
independently reset. Both baseline and MTS reproduce all 934 original
diagnostic packets byte-for-byte when the new background hook is disabled.
This supplies a consistently transported preparation conditional on the
existing cosmological initial state, not a new derivation of its primordial
origin or of a galaxy's population.

Original bank, 33-by-902 query grid through epoch2924, physical k=5 Mpc^-1,
signed weights, masses, couplings, normalizations and 32/64 step choices are
unchanged. Algebra1e-10 and numerical2e-5 gates remain unchanged.
All comparisons here use the original conformal times.

## Pressure: include the preparation, not just its later increment

The full response is

    weighted delta Y(t) = weighted delta Y(0)
                         + weighted [delta Y(t)-delta Y(0)].

That identity was checked using saved arrays for both cases. Dropping the
first term would materially understate the MTS pressure change.

| MTS pressure quantity, retained normalized source units | Result |
|---|---:|
| Initial matched-preparation response | -4.185470119541198e-9 |
| Maximum later increment response | 1.790588974419825e-10 |
| Final later increment response | 1.4361031428824964e-10 |
| Final FULL response | -4.041859805252945e-9 |
| Maximum full response magnitude | 4.207386322074108e-9 |
| Maximum total changed prediction plus measured allowances | 4.446548102534776e-9 |
| Original unchanged allowance | 5.076162418225474e-9 |

**The full pressure check passes, using87.5966% of the allowance.** The
post-preparation increment alone uses only3.5274%; it is not the full result.
The allowance accounting includes the retained reported numerical budget,
saved history refinement, and both new coupled-step comparisons. These
are measured numerical allowances, not a rigorous continuum error bound.
The maxima of the individual terms need not occur at the same report.

Full density/current budgets also pass, using20.6416%/0.43814% of their
unchanged allowances. MTS full-response32/64 relative differences are
4.45743e-9,1.71363e-8,3.14600e-8 for density/current/pressure.
The largest increment-response relative difference is1.77840e-7,
against2e-5.

Do not erase the earlier failed derivative-only pressure substitution.
It was a different, inconsistent partial operation. This stage changes
the coupled background, perturbations, surroundings and preparation
together and tests the resulting sources.

## Exchange with the live surrounding system

The exact retained source identities and explicit old-background Euler
contacts are in DERIVATION.md and symbolic-result.json. The corrected
background removes those contacts by its equations; the old accounting
still contains them. The density work is separated into expansion,
own-current transport, own density, surrounding density, metric feedback
and approximation contact. Endpoint sources and integrated work are
computed separately.

MTS normalized full density/current exchange residuals:
3.760491892e-12 and5.891457451e-13, versus2e-5.
The change-only balances on their OWN small scales give
3.703884083e-9 and3.486230158e-12, also passing.

Omitting surrounding density work fails the MTS full balance
(0.105442 on the original source scale) and the response balance
(0.00115023 on its own scale), both against2e-5.
The baseline full-source omission test is less sensitive and passes;
we do not pretend that negative control detects an error in both cases.

The final MTS density increment response is1.1528131126e-8. Removal of
the old approximation contact contributes1.2102662970e-8 to that work
budget; smaller physical work terms compensate it. This is a correction
to the saved source representation, not a new astronomical signal.

## Fair baseline result and unresolved precision

Baseline source-scale preparation, pressure and exchange tests pass.
Its own pressure/current sources are identically zero by the retained
cold-source definition, not inferred zeros for all surrounding species.

Three new tiny-response relative tests remain failed:
- Increment refinement:1.87705e-19 /2.96878e-18 =0.0632263.
- Increment exchange:9.90999e-20 /2.96878e-18 =0.0333807.
- Full-preparation refinement:4.25059e-18 /6.73932e-18 =0.630714.

All exceed2e-5; small absolute size does not prove their convergence.
The four prior baseline background-relative failures also remain in
the inherited stage. Do not report an all-tests pass.

MTS passes29/29 coupled checks and12/12 full-preparation checks.
Baseline passes25/27 and11/12 respectively. Seven symbolic identities/
controls,36 paired preflight checks,22 scoring reproduction checks,
and44 initial consolidated verification checks pass.

## Evidence and implementation

- result.json: coupled increment and exchange tests, including failures.
- preparation-result.json and *-preparation-budget.npz: FULL matched source.
- score-cached-replay.json and preparation-replay.json: exact cached replays.
- verification-v2.json: source preservation, build, capture and provenance.
- closeout.json: final acceptance, cleanup and artifact hashes.
- *-coupled-32.npz / *-coupled-64.npz: both resolutions, no expensive rerun
  merely for replay.
- run_sized.py, native_context.py and private native/: implementation.
- prove_response.py: exact source/contact identities.
- replay_coupled.py --replay: replay the frozen original scoring inputs.
  The first scorer discovers input files dynamically; the later replay
  intentionally uses its saved inventory so adding the preparation audit
  cannot change that inventory. Scientific scoring statements are identical.

The first incremental native build failed because of stale Fortran module
dependencies. A private full39-unit build resolved it; originals were not
modified. Cold32 was intentionally saved before starting a separate64
worker; its owner-hold failure receipt is an orderly handover, not a
scientific rejection. The first consolidated validator hit a NumPy-boolean
JSON serialization error; verification-v2 corrects only serialization,
with no integration rerun or gate change. Those receipts remain.

Four auxiliary native dependencies were explicitly hashed at closeout,
rather than falsely labelled pre-run freezes. The exact native packet
reproduction is separately established. The original frozen source hashes
were rechecked individually.

## Scope and next physics

This is the retained finite-regime, selected-subsystem exchange calculation
with live surroundings, not a new all-species quantum stress theorem.
The existing hierarchy/thermodynamic approximations remain visible.
Quantum measure stays separate. No galaxy occupation is supplied.

Next, check the shared metric constraints and spatial-pressure equation
on these same corrected states. Carry the FULL preparation term, the
12.4% remaining pressure headroom, and the baseline precision failures
forward. See NEXT.md. Nothing is running after closeout.


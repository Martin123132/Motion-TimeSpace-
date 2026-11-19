# Real changing-metric transport: separate preparation and numerical defects

2026-11-10. Local continuation of the retained MTS scalar branch, not a new
theory or fit. Sources, mass/coupling, native history,399modes per model,
z=10 starting slice,Delta ln a=.001, and1e-10/2e-5 gates are unchanged.
The independent cold Euler control follows its own saved background.
Read closeout.json for the final verified inventory; no absent closeout is
an authorization to relaunch an unobserved worker.

## 1. Actual-background error certificate

The saved initial values and retained species coefficients define the exact
ODE for this conditional statement. Outward192-bit rational intervals prove
a strict three-coordinate Picard/first-exit enclosure on the whole interval.
The91-term second-adiabatic residual then gives

    integral |R_W|/W <=2.270e-24, all0<=k<=5/Mpc.

This is not a sampled maximum and does not reuse the inapplicable frozen-H
certificate. It controls the oscillator representation with the same exact
initial state, not its physical selection or floating-point evaluation.
The exact forced truncation bounds, source-polynomial bounds and float32
input allowances are separately stored in background-bound.json and
source-bound.json. Maximum forced allowance is5.281e-19 times the initial
carrier coefficient norm; maximum source-rounding allowance is0.109701 in
that coefficient norm. Neither is a fractional observable uncertainty.
Initial-state uncertainty, true history interpolation error and native model
error are excluded, not silently assumed measured to that precision.

## 2. Preserve what the original test found

The primary microscopic run passed its implemented numerical checks but
failed the native density/current comparison in7of399MTSmodes. Maximum
normalized density error was2.52719e-5 against the unchanged2e-5 gate.
Its pressure difference was0.127815 on the fixed density-source block.
Cold's maximum endpoint error was9.79900e-8 and passed.

4096to8192panels changed the original source block by3.721e-9. Background
17versus33saved-point and phase-order controls also passed. Direct physical
KG checks at k=.03,.1,1,5/Mpc and both real quadratures passed; tightening
rtol tenfold reduced maximum normalized field error from4.571e-8 to4.566e-9.
The pilot source readout reached a roughly2e-8 cancellation floor rather
than showing the same tenfold trend. Do not claim source convergence from
the field trend alone.

These controls were insufficient to catch low-k relative-phase loss. Their
passing flags are retained as scoped checks, not relabeled as an all-mode
accuracy theorem. The original result is never overwritten or promoted.

## 3. Derive the preparation correction, rather than fit pressure

The free sideband derivative used for the original preparation is not the
derivative of a metric-forced particular state. Directly from the physical
field equation, a flat constant-metric state without a free negative-frequency
homogeneous component satisfies

    F'=-i omega F-i[2mu^2/(omega+mu)]Psi B.

It gives Pi=r delta-r(1-r)Psi and the unit Newtonian phase force at k=0.
The changing-background leading dressing is

    D0=[C'(lambda0-H)-2mu^2Psi]/(lambda0+lambda_k), C=Psi+3Phi.

The exact response equation and its remaining D0' and W2-residual defects
are derived in DRESSING-DERIVATION.md. Eight symbolic identities pass.
Both preparations match the identical initial density/current to6.50e-16.
No mass, coupling or correction coefficient was fitted.

This is explicitly conditional preparation, not a derived formation state.
Its17point adiabatic indicator reaches1.566e-8; that diagnostic is not a
uniform bound. With the old phase evaluation, the pressure discrepancy
falls to7.443e-9 on the same energy block, but the same seven density cases
still fail. Therefore preparation does not explain the density defect.

## 4. Reject one hypothesis, then isolate the numerical cause

An independent integral of the saved averaged conservation equations gives
heavy density/current discrepancies1.281e-10/4.126e-6; cold gives
9.295e-8/9.800e-8. All399modes per model pass. This rejects blaming the
saved density history for the observed seven-mode mismatch on this test.
It is an internal consistency check, not independent observational evidence.

The small beat was computed accurately, but then added to a31906.603radian
carrier before taking trigonometric functions. At k=1e-5/Mpc an8.583e-15
beat became exactly zero in that sum. At the worst failing mode,
k=0.0004371444812611/Mpc, the1.64009952e-11 beat became1.81898940e-11.
Reading a small density perturbation beside a large phase transfer amplifies
this otherwise tiny angular rounding.

Evaluating the exact angle-addition identities without adding the angles
first fixes the representation. Binary64 arithmetic, equations and gates
are unchanged.80digit controls give repaired rotation errors below1.49e-16
at the six declared modes; old argument-addition errors reach1.49e-12.

Changing only the endpoint rotation while REUSING the original forcing
integral removes all seven density failures. The conditional dressed density
error falls from2.52862e-5 to1.961e-8; the undressed density error also falls
to2.658e-8 while retaining its pressure transient. This isolates two distinct
effects instead of attributing everything to a changed physical state.

## 5. Scope and retained evidence

The full separate-phase integral is complete in phase-full-result.json:

| Preparation/control | Maximum density error | Maximum current error | Pressure energy-block discrepancy | Density/current failures |
|---|---:|---:|---:|---:|
| Original free preparation, repaired rotation | 1.678e-8 | 4.104e-6 | 0.127815 | 0/399 |
| Conditional metric dressing, repaired rotation | 2.367e-9 | 4.126e-6 | 7.454e-9 | 0/399 |
| Physical cold Euler control | within9.800e-8 combined | within9.800e-8 combined | dust control | 0/399 |

4096to8192panel changes are3.724e-9 and2.487e-9 on the original and dressed
source blocks respectively. The unchanged2e-5 density/current gate passes
for every mode of both histories. This table is a saved-history interface
test, not a fit to observations or a percentage improvement of the theory.
The pressure column is normalized to the density-source scale, not pressure.

The added independent physical low-k regression is recorded separately in
direct-low-result.json. Both tolerances pass at the worst original failing
mode and both real quadratures. Its maximum source-block difference is
1.457e-5 at rtol2e-11 and1.398e-5 at rtol2e-12. The normalized field error
shrinks from4.096e-8 to4.022e-9, but the source readout does NOT improve
tenfold: its pressure component is also nonmonotone,1.345e-7 to4.296e-7.
This independent test supports the declared2e-5 gate, not a claim that the
whole physical calculation is independently accurate to the2.367e-9 native
density agreement. The difficult cancellation/readout remains visible.

Both original preparations and original failures are saved alongside the
repair. Supplemental process/output bindings are checked when sealing;
the earlier43entry validation remains unchanged.

Metrics are supplied histories, not a new self-consistent Einstein solution.
The conditional dressing does not select a local halo occupation. Native
averaging, source precision and genuinely coupled evolution remain separately
identified questions. Tiny analytical truncation bounds do not replace the
physical/numerical uncertainty budget.

The concrete advance is a certified changing-background transport envelope,
a derived metric-dependent preparation law, and an isolated/fixed low-k phase
representation defect. NEXT.md points toward the reduced action/source law
and coupled metric evolution, rather than further refining a resolved panel
integral or fitting away a physical discrepancy.

# Live forced preparation, with the missing radiation coupling identified

This stage builds on the sealed 95-state source bridge. The initial-state
construction and its evolutions completed. A new independent metric check
found a real failure of the retained late radiation approximation; that
failure is kept explicit, quantified and traced to a source term.

## 1. Initial response derived from the live operator

For Y'=A(t)Y and C=c(t)Y, the exact row laws C'=(c'+cA)Y and
C''=(c''+2c'A+cA'+cA^2)Y replace the old fluid's initial metric derivative.
The conditional D0 and D0+D1 states are solved with the same physical
initial density/current and all 91 retained rest states. Four general
row/metric identities pass; three additional radiation identities pass.

Both four-coordinate preparation systems have row-scaled condition number
1.0004094 and maximum normalized constraint residual 1.55e-16. The local
correction |D1/D0| is about 1.18453e-8 on these prepared states. It remains
a conditional forced-state construction, not a galactic formation law.

Operator coefficient derivatives were evaluated on known backgrounds,
not future species/metric trajectories. Five-point one-sided stencils
stay inside the original window. The final refinement changes initial
states by at most 8.993e-11 in the frozen state norm. First/second source-row
derivative changes are 2.726e-10/9.633e-6 in their declared natural scales,
within 2e-5. The second derivative is rounding-sensitive and is not claimed
exact; its refinement gets noisier as spacing shrinks. No evidence supports
continuing to halve these stencils blindly.

Both new states were evolved with 128 and 256 internal exponential steps.
Refinement differences are 2.1606684e-7 (D0) and 2.1047891e-7 (D01), within
the unchanged 2e-5 gate. D01 changes a small fast coordinate appreciably
in the old component normalization, but that must not be reported as a
comparable change in gravity. At the final endpoint, D01-versus-D0 changes
density, current and metric sources at floating-point-level relative
scales; the pressure/Rh difference is -5.3326e-14, or 5.8251e-16 of the
energy normalization. These are preparation comparisons, not a claim of
observable accuracy or evidence that D01 is universally superior.

## 2. Independent metric conservation check exposes a retained defect

The previous native metric observer evaluates the momentum-law expression.
That is insufficient to check the derivative of the actual algebraically
eliminated potential. This stage instead differentiates its source row and
uses the actual coupled RHS. Define Ephi=Phi'+H Psi-Q/(2k). The generalized
identity retains this term:

    Ec'+H Ec = ED+3H EQ/k+3EH Q/k+(2k^2+3S)Ephi.

Its algebra checks pass, but the physical Ephi gate does NOT pass for the
retained heavy/MTS implementation. The Hamiltonian constraint remains
small by algebraic construction and is not mistaken for conservation.

| Case | Initial normalized Ephi | Final normalized Ephi | Gate 2e-5 |
| --- | ---: | ---: | --- |
| Unchanged native heavy | 5.4508406e-4 | 5.4490873e-4 | fail |
| Unchanged native cold | 4.5572096e-8 | 4.5681292e-8 | pass |
| Canonical scalar | 5.4508405e-4 | 5.4490872e-4 | fail |

The new D0 and D01 evolutions preserve essentially the same final failure.
The scalar's own sampled energy/current residuals are at most about
1.43e-10/2.10e-9 in their declared rate normalizations. Changing preparation
does not remove the separate radiation-source problem. All of these are
short-window endpoint/stencil measurements, not uniform trajectory bounds.

## 3. The omitted term predicts the error without fitting

Native derivs constructs the radiation-streaming approximation using
baryons/CDM/massive-neutrino density DM BEFORE adding the MTS scalar stress.
The heavy matter-like scalar lives in the custom dark-energy component,
so it is absent from this approximation's gravitating source even though
it is added to the later metric and other-species equations.

With q_r=-4 zM/3, exact differentiation gives the radiation energy defect

    ED_r=R_r delta_r,s'+2R_r(Dtotal-DM)/(3H),

subject to the retained homogeneous radiation/clock equations. The
measured source-history, heavy, slow and radiation-feedback contributions
are saved separately. For the heavy/canonical cases, the predicted
identity matches the measured error to component-normalized residuals of
order 1e-14 or smaller. The near-zero cold case also passes the same 2e-5
gate (approximately 1.3e-6 at worst on the finest stencil).

Radiation contributes approximately 99.98965% of the heavy/canonical
total constraint-error source at the initial endpoint and 99.98971% at the
final endpoint. The omitted heavy density accounts for essentially all
of that radiation ENERGY defect; the smaller radiation momentum terms
are retained separately. Removing this term from the algebraic prediction
destroys agreement. That is a mechanism test, not a repaired forward run.

The source equations imply the leading stressed correction

    Delta q=-2 DS/(3kH),
    Delta delta_r=(4DS+6PS)/k^2,
    Delta delta_g=Delta delta_r-2 opacity DS/(k^2 H).

No new fitted coefficient is present. RADIATION-SOURCE-DERIVATION.md states
its approximation domain and the remaining coupling requirements. It has
NOT been inserted into the forward solver in this stage. A consistent
repair must update gravity AND radiation/baryon coupling, not just a
readout or a residual subtraction.

## Scope, preservation and next action

Preparation and integration checks pass; the heavy/canonical conservation
gate deliberately remains failed. Do not collapse those into one green
physics label. The prior short-window and historical-archive qualifications
remain in force. Original equations, DLLs, bank, grids and coefficients
are unchanged. No new fit, data acquisition, Galaxy edit or publishing.

One initial wrapper-name collision stopped an import before a worker
started; IMPORT-REPAIR.md records the fix. All generated calculation
receipts and packets remain available. Final validation and cleanup are
recorded separately. Next is the isolated, source-complete radiation
comparison described in NEXT.md, reusing the now-derived live initial
preparations rather than rebuilding them.

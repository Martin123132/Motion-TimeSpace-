# Derived general-k carrier and an explicit native metric source connection

Started10 November and completed11 November2026 as one manually authorized step. The existing theory and physical parameters are retained. No new galaxy/cosmology fit, native forward integration or automatic goal resumption was performed.

## Concrete derivations and implementation

1. `general_k_model.py` supplies the k-dependent quadratic carrier, physical density/current/pressure rows, harmonic coefficients, phase primitive and first generator correction. In particular the current, metric denominator and force column retain their separate k factors. It reproduces the accepted corrected k=1 implementation instead of replacing that work.
2. The synchronous-to-canonical map is now explicit:

       uN=uS+v*alpha,
       pN=wS-3*eta*v-mu^2*b*alpha.

   The exact background/shift/lapse defect terms accompanying this transformation are derived in DERIVATION.md and tested without assigning those defects zero.
3. `native_source_port.py` solves the current metric connection while OTHER species remain in their existing native synchronous variables:

       Phi=-(Dr+Dstar_h+3H*(Qr+Qh)/k)/(2k^2+3Sh).

   It returns the native scalar density/current, lapse and clock shift. Its pressure inverse is also explicit. The denominator contains only the replaced component's enthalpy because Dr,Qr are native, not already canonical. Transforming ALL species recovers the existing total-enthalpy denominator exactly. This is a coordinate/source connection, not a new gravity law or coupling.

## Checks against independent equations and saved work

- **15 exact symbolic identities pass:** ten chart/source/arbitrary-defect identities and five current-native metric/source identities. These include the scalar's two evolution-defect equations and the equivalence of native and total canonical constraints.
- Synthetic algebra controls use four wavenumbers0.2,1,5,12 and four conformal masses0.5,3,30,300, with64/128 phase grids. The primitive operator is assembled independently from the field equations and differentiated coordinate map. Maximum row discrepancy is4.47472e-12; product-rule map derivative discrepancy3.85233e-16.
- The k=1 synthetic coefficient regression differs by at most1.97192e-16. Five fixed saved MTS epochs, using the ORIGINAL source normalization and both declared H' controls, reproduce the accepted corrected geometry to2.71050e-20 under the test normalization. These are regressions, not new independent observations.
- Both baseline and MTS saved late metric records are checked, including captured, integrated, precision, negative and zero controls. The new native source connection is independently replayed using the known CDM component as a gauge/metric test; all50 checks pass, maximum5.21609e-16. This does not assign scalar pressure to dust or claim the late heavy block was replaced.
- A k=1 operator merely relabelled k=5 is rejected. A second negative control incorrectly uses the total-enthalpy denominator while leaving rest sources native; its saved-potential errors5.19287e-9 (cold) and2.15565e-8 (MTS) exceed the same1e-10 algebra gate. These are implementation controls, not observational discrepancies.

The accepted numerical suite consists of482 unchanged original comparisons,32 higher-precision angular-mean checks,16 phase-grid comparisons and50 native-port comparisons. Counts are structured comparisons of these calculations, not580 independent physics experiments. Numerical/algebra gates remain2e-5/1e-10.

## Precision issue found and resolved, without changing the formulas

The original double-precision run remains FAILED: two angular-mean checks at k=0.2,mu=300 gave4.57687e-10 and4.69530e-10, exceeding1e-10. The mean cancels much larger oscillatory entries; all other original checks passed.

An independently frozen precision check reevaluated ALL32 means using the primitive equations, at60 and90 decimal digits and both original phase grids. The maximum discrepancy with the unchanged analytic mean falls to6.87277e-17; the60/90-digit means agree to1.502e-56 and the64/128 grids to1.198e-86 under the reported normalization. This identifies arithmetic loss in the original mean evaluation, not a retuned model. These finite checks are not a continuum error enclosure.

Read `validation.json` for the failed original suite, `accepted-validation.json` for the explicit higher-precision replacement and `native-port-validation.json` for the separate source connection. The numerical model and frozen input hashes were unchanged during the precision repair.

Two pre-test implementation issues are also preserved: a draft parsing error and a failed input-freeze lookup using forward slashes against Windows-style sealed relative keys. See DRAFT-COMPILE-REPAIR.md and INPUT-PATH-REPAIR.md. Neither was a physical model result. No failed receipt or original test result was overwritten.

## Late-reference scope correction and next step

The late files have61 times in their ORIGINAL schedule, but only TWO captured endpoints in the accepted short interval, native indices8 and9, at k=5 near z=10. Earlier shorthand about61 times must not be read as61 within-interval captures. Current MTS/cold continuous dimensions remain93/91 with the retained heavy selector.

The next calculation is the matching/initial-state construction for replacing that averaged heavy pair with the derived canonical/current-state block. The existing averaged density/current pair is not silently relabelled as an unaveraged field and velocity, and no arbitrary phase or new occupation has been selected. The derived maps and actual defect equations now specify how the replacement must couple to the metric once that retained state is carried across.

All artifacts stay in this new private stage plus the resume bookmark. Native libraries, original research, Galaxy files, GitHub and other agents' work are unchanged. No continuing task-owned worker is authorized. Use `finish_verified.py` for this stage's accepted closeout; the frozen original checker correctly remains a failed double-precision record.

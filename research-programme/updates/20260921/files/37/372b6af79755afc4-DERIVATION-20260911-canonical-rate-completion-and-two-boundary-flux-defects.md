# Canonical rate-space completion and the two boundary flux defects

Private derivation and implementation, 11 September 2026. No evolution or local-GR claim.

## 1. Outcome

**An action-consistent frozen trial-space extension has been constructed and tested, not merely proposed.** Every original coordinate and momentum direction is retained. No initial scalar/momentum profile is refitted and no constraint row is deleted.

On the constructive GR-plus-scalar reference, the old finite representation produces max|C_t|=2.19207e-5 although the unprojected initial jet has C=C_t=0. Completing the canonical rate spaces reduces all C_t rows to 1.44674e-17. Independent higher-order integration gives 1.32699e-17. The imposed inner mass drive is recovered to about 2e-19.

On the saved MTS state, **with full time-link sources retained and natural spatial reactions used in both comparisons**, max|C_t| decreases from 1.88178e-4 to 7.71469e-6. All interior rows are below 1.80e-15; the remaining two boundary rows have an independently derived flux-trace explanation. This is not an MTS initial-data or evolution certificate: those two rows remain nonzero, and the imposed boundary drive needs compatible re-preparation after the boundary projection is repaired.

Predecessor: `DERIVATION-20260911-inverse-boundary-preparation-and-constructive-GR-reference.md`.

## 2. What is and is not held fixed

The branch remains kappa=1/10, Lambda=m_chi=b2=b3=0, P=0 initially. GR means GR with the canonical scalar. These are code-normalized finite/action tests, not observational fits.

- GR uses the preceding formula-defined first jet, reconstructed independently by dense integrating-factor-equivalent ODE solutions. Its mass agrees with the saved reference within the checked 1e-12 tolerance. The reference is used as a fixed affine initial-field offset, not interpolated into the old mass-face space. This isolates rate-space errors rather than mixing in new initial-field interpolation errors.
- MTS uses the unchanged physical fields of the preceding converged N16, outer-clock-normalized finite root. No failed GR iterate is used as physical data.
- Original bases and their frozen seed weights are retained. Added functions are frozen at these initial fields. This is not yet a field-adaptive nonlinear discretization or a proof on a neighborhood of the initial state.
- Both comparisons use the natural spatial boundary reactions. The prior MTS root used different, finite fitted reactions; its former tiny residual must not be compared directly with the new natural-reaction residual as though the problem were unchanged.
- Quadrature is split at all scalar/mass/reference knots. Frames are built at bulk order 12 and tested unchanged at order 16; full Gram link integration is checked at orders 8 and 12.

The general new evaluator reproduces the original MTS canonical evaluator at its original quadrature and original reactions before any extension is applied.

## 3. The defect is a projection defect, with signed channels

Write V_mu,V_chi for coordinate trial maps and W_P,W_pi for momentum maps. The symplectic pairings are

```text
M = <W_P,V_mu>,   S = <W_pi,V_chi>.
```

For fixed initial physical fields, each lapse basis function eta_j has four local canonical rate functions:

```text
s_j = kappa F^(3/2) pi w eta_j,
q_j = sqrt(F) pi eta_j/R^2,
E_j = eta_j H/(R sqrt(F)) - eta_j,R/(kappa sqrt(F))
      + eta_j mu/(kappa R^2 F^(3/2)),
T_j = (eta_j sqrt(F) R^2 w)_R,
H = pi^2/(2R^2)+R^2 w^2/2.
```

The old finite equations project these into different coordinate/momentum spaces. With d_mu,d_P,d_q,d_pi denoting finite rates minus these unprojected local rates, the GR C_t defect is exactly the sum of the tested covectors

```text
<eta_j, d_mu,R/(kappa sqrt(F))
          +(mu_R/(kappa R F^(3/2))+H/(R sqrt(F))) d_mu>,
-<eta_j, R^2 sqrt(F) w d_q,R>,
-<eta_j, sqrt(F) pi d_pi/R^2>,
-<eta_j, kappa F^(3/2) pi w d_P>.
```

For MTS the explicit differentiated Gram constraint is an additional retained channel; differences against local GR rates then include genuine Gram forcing and are **not all numerical errors**. The complete signed reconstruction is checked, including this channel. Its error is below 1.4e-18 on the saved cases.

The old GR reference defect is dominated by the mass-rate projection channel (2.18606e-5), not an unsolved radial mass constraint. Initial C itself is about 1.6e-20 in this quadrature.

## 4. Constructed phase-space extension

### Coordinate-rate completion

First normalize the original trial coordinates and momenta by invertible weighted QR transformations. No original mode is dropped. Let U be independent residuals of s_j, or q_j in the scalar sector, after projection off the original coordinate space V. Append U to both V and W. Since <U,V>=0 and <U,U>=I, the new pairing is triangular:

```text
< [W,U], [V,U] > = [[M,<W,U>],[0,I]].
```

This preserves invertibility of the old pairing and includes the required coordinate rates. Rank selection applies only to proposed additional rate residuals, at a recorded normalized tolerance of 1e-12. The GR scalar family has one redundant combination already in the original Hermite space; none of the original scalar modes is removed.

### Momentum-rate completion using continuous duals

Project E_j and T_j off the enlarged momentum space and call their independent residuals T. Momentum functions may be piecewise discontinuous, but coordinate functions must remain continuous. **We do not put discontinuous momentum rates into coordinate spaces.**

Take a reservoir B of continuous cell bubbles (four polynomial modes on every combined subcell). Define

```text
H0 = B - V M^(-1) <W,B>,
C = <T,H0>,
H = H0 C^dagger,   with C C^dagger = I.
```

Then <W,H>=0 and <T,H>=I, giving

```text
< [W,T], [V,H] > = [[M,0],[<T,V>,I]].
```

H is continuous because B and V are continuous. The new coordinates and momenta are genuine trial functions in the same canonical action; they are not additive forces or subtracted residuals. The bubble moment matrix has full numerical row rank in both tested sectors. Pairing block identities agree within 5.2e-15; the largest full pairing condition number is about 1.66.

For GR, the original phase dimensions 33 and 34 become 67 and 67. For MTS they become 67 and 68. These counts are coordinate counts per canonical pair, not a count of fundamental physical fields. The extra functions are discretization degrees of freedom.

The bulk Hamiltonian, including its physical P-squared boundary term, is evaluated independently. Complex directional derivatives in all four phase blocks agree with the enlarged canonical equations within 6.3e-16 on the GR reference. Full nonlinear Gram-action differentiation is not claimed; its complete previously derived P=0 time-link first variations are retained and replayed against the old implementation.

### A simpler sufficient GR completion

For the initial GR constraint-rate identity, coordinate-rate completion alone suffices in exact integration: s_j and q_j in the coordinate spaces make the remaining momentum projection errors orthogonal to their C_t test weights. Hence those errors need not vanish pointwise for C_t to vanish weakly.

The explicit ablation confirms this: the 50/50 coordinate-only phase frames give max|C_t|=1.48170e-17. Full momentum completion is useful for the MTS source identity and more accurate individual rates, but is not necessary to close this particular GR first-jet identity. No assertion is made that 50/50 is a globally minimal discretization.

Pointwise geometric momentum-rate discrepancies remain around 1e-8 in the full GR numerical construction, despite much smaller weak residuals. Do not replace these actual measured errors with a blanket claim that every rate is exact to roundoff. No interval conditioning/rounding certificate is supplied here.

## 5. Tests and results

| State and representation | Maximum absolute C_t | Maximum absolute interior C_t |
|---|---:|---:|
| GR reference, original spaces | 2.19207e-5 | 2.19207e-5 |
| GR reference, coordinate completion | 1.48170e-17 | 1.48170e-17 |
| GR reference, full completion | 1.44674e-17 | 1.44674e-17 |
| GR reference, same full frame, higher quadrature | 1.32699e-17 | 1.32699e-17 |
| MTS, original spaces with natural reactions | 1.88178e-4 | 1.65390e-5 |
| MTS, coordinate completion | 9.14054e-6 | 2.76898e-12 |
| MTS, full completion | 7.71469e-6 | 1.79499e-15 |
| MTS, same full frame, higher quadrature | 7.71469e-6 | 1.77399e-15 |

Interior excludes only the two endpoint lapse-test rows; **the full norm remains reported and is not a pass for MTS**. The same fixed completed frames also pass three unfitted positive interior lapse variations, with both endpoint lapse values unchanged: GR all-row maxima below 3.75e-17; MTS interior maxima below 1.80e-15. The MTS boundary rows remain nonzero in all three variations.

## 6. Derived location and meaning of the two remaining rows

Let u_h be the mass velocity produced by the finite canonical projection and s=kappa R^2 F q w the local bulk flux, with q now represented by the completed scalar coordinate space. Let Gchi_b be the full pulled-back Gram scalar force at the physical endpoint. All anchor orientations and endpoint Jacobians are retained.

The parent one-sided fluxes are

```text
u_parent,in  = s_in  + kappa sqrt(F_in)  q_in  Gchi_in /N_in,
u_parent,out = s_out - kappa sqrt(F_out) q_out Gchi_out/N_out.
```

The outer sign differs from the inner sign because the endpoint links have opposite orientation. These are not the GR-only flux law.

Integration by parts gives a boundary contribution [eta (u_h-s)/(kappa sqrt(F))]. Combining this with the existing full Gram joint-variation identity and the natural scalar reaction cancellations gives the following conditional trace identity when the bulk rate/test dualities are complete:

```text
C_t,in  = -(u_h,in-s_in)/(kappa sqrt(F_in)) + q_in Gchi_in/N_in
        = -(u_h,in-u_parent,in)/(kappa sqrt(F_in)),
C_t,out = +(u_h,out-s_out)/(kappa sqrt(F_out)) + q_out Gchi_out/N_out
        = +(u_h,out-u_parent,out)/(kappa sqrt(F_out)),
C_t,interior = 0.
```

The trace identity assumes the P=0 adjoint/Gram identities, regular spatial boundary reactions and exact relevant function-space pairings. It is not a general nonlinear continuum theorem. The entire finite residual vector is independently predicted by the two flux-trace gaps to 1.80e-15 in the full MTS test. Deliberately omitting the Gram endpoint force is detected.

Numerically, for full MTS completion:

```text
u_h,in      = 0.00033637899674630065
u_parent,in = 0.0003357524556197037
gap_in      = 6.26541126596972e-7

u_h,out      = 0.0008828107246721511
u_parent,out = 0.0008825359009400019
gap_out      = 2.748237321492002e-7

C_t,in  = -7.71468994776849e-6
C_t,out = +3.3490837576886277e-6
```

The previous imposed inner drive is 0.00033578281226508903. It is also different from the new parent trace, because the natural-reaction/enlarged jet changes the time links. Merely replacing the finite mass velocity with the old imposed number would not repair both mismatches.

The earlier endpoint result and the full current definitions remain in `DERIVATION-20260911-nonlinear-mass-elimination-and-boundary-flux-compatibility.md`; the time-link adjoint derivation is in `DERIVATION-20260911-coupled-initial-jet-and-exact-time-link-adjoint.md`.

## 7. Next concrete construction

The next target is now **a trace-preserving mass-flux projection derived from the actual Gram kernel**, followed by compatible inverse-boundary re-preparation. It is not another unconstrained fit of interior momenta or another search for a missing fundamental coupling.

For a finite parent-derived flux family F, the required projection Pi must satisfy both the existing weak moment relations and (Pi f)(R_b)=f(R_b) at both physical boundaries. Simply overwriting two coefficients, deleting two C_t rows or imposing u_parent from the GR law is forbidden. A viable route is a paired coordinate/momentum extension whose boundary evaluation functional is represented on that flux family, with continuous coordinate lifts. It must retain the full time-link dependence; freezing a flux family and then changing the geometric momentum rate without checking the changed Jacobians would be circular.

After the trace projection works, redo the declared inverse preparation (inner mass history drives q_in) and retain the natural outer clock. Require the full boundary rows, interior rows and meaningful spatial refinement to pass before higher time jets or evolution.

## 8. Saved implementation and guards

- `scripts/annular_canonical_reference_fields_20260911.py`
- `scripts/annular_canonical_rate_completion_20260911.py`
- `scripts/derive_annular_canonical_rate_completion_20260911.py`
- `scripts/verify_annular_canonical_rate_completion_20260911.py`
- `scripts/seal_annular_canonical_rate_completion_20260911.py`
- `source-intake/navier-stokes/20260911/annular-canonical-rate-completion-attempt01/status.json`
- `source-intake/navier-stokes/20260911/annular-canonical-rate-completion-control-attempt01/status.json`

All source archives and completed predecessor scripts remain immutable. The current initial fields and old failed runs are not overwritten. No GitHub, subagents, galaxy work, frozen workbench modifications or evolution. One BelowNormal, single-core Python at a time, with no owned worker left running at finalization.

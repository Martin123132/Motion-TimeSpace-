# Applied cubic clock and a two-sided boundary-compatible first jet

Private/local continuation, 12 September 2026. N16 only, with matched GR and
metric-Gram controls. No new evolution, public update, physical local-GR pass,
black-hole result or interval/continuum certificate.

## 1. Outcome

The previously proposed lapse correction has now been APPLIED. Its full
variational implementation requires two extra lapse equations, not simply
changing the displayed boundary derivatives. Those extra equations are solved
along with every old constraint, physical boundary drive and clock condition.

The first implementation removes the large boundary defect but exposes two
smaller numerical effects. We derive and construct a projection for the whole
interior nodal-source family, then use an explicitly integrated gravitational
action with its boundary term retained. In that NEW finite-quadrature branch,
both models pass the initial constraints, their first time derivatives and
the endpoint P_t condition under the unchanged final 1e-10 numerical gates.

This is a real small-case boundary preparation, not an evolved solution. In
particular the new finite action is not silently identified with the earlier
quadrature action, and its certificates must not be transferred to that old
action or to the earlier N128 construction.

## 2. Contract and the additional equations

Retain F=1-2mu/R, kappa=1/10, Lambda=m_chi=b2=b3=0 and the annulus
[5.875,6.125]. Both branches use the common prepared N16 scalar/free auxiliary
momentum, the original kinetic map pi=K_seed*xi, the same inner mass, physical
mass/scalar drives and natural outer clock. GR includes that same scalar;
it is not vacuum GR or the separate older smooth manufactured reference.

The action-derived classical free-P endpoint condition is P_b(t)=0, assuming
independently free endpoint P variations and no additional parent P-boundary
action. At the P=0 slice its first compatibility condition is P_t,b=0.
The regular endpoint bulk equation gives

    (N_R/N)_b = kappa E_b/R_b + mu_b/(R_b^2 F_b),
    E=pi^2/(2R^2)+R^2 chi_R^2/2.

For L=R_out-R_in, x=(R-R_in)/L, let

    Y_1=L(x^3-2x^2+x), Y_2=L(x^3-x^2),
    Delta_b=N_b*(required logarithmic derivative)_b-(N_R)_b,
    N=N_P1+Y_1 Delta_in+Y_2 Delta_out.

Both lapse endpoint VALUES are unchanged. The two derivative changes are
calculated from the current prepared fields, not fitted physical constants.
During the action variation, fields and lapse coefficients are independent;
the initial preparation formula is not differentiated as a hidden matter
dependence of N.

The lapse trial/variation span is the complete P1 space PLUS these two cubics.
All 17 old lapse rows remain, and two independent new rows are added. To keep
them well scaled, subtract the weighted P1 projection of Y and apply an
invertible QR normalization. This changes the basis, not its span or equations.

Two new dependent mass functions are constructed by integrating the normalized
extra lapse functions, subtracting the linear endpoint drift and normalizing.
They are continuous and zero at both endpoints. The existing 17 free mass-face
coefficients plus these two amplitudes solve ALL 19 initial constraints with
an analytic Jacobian. Original initial mass bubbles remain separately recorded;
no original canonical variation is removed. Local rate completion includes
all 19 lapse directions and the two mass lifts before the trace constructions.

The resulting mass Jacobian condition is about 4606.14, not a uniform
invertibility proof. The final mass canonical pairing is 77-dimensional and
has condition about 1.664. Physical fields, matrices and source coefficients
are saved; a small residual is not treated as a rank certificate.

## 3. What applying the clock correction alone accomplished

The enlarged, uncorrected controls have endpoint P_t of roughly
(+7.9e-4,-7.2e-4) in both branches. Applying the exact cubic preserves the
full finite constraint/drive gates and makes the strong endpoint formula zero.
Nevertheless, projected endpoint P_t remains about 1e-7 for MTS and 1e-9
for GR. These were not declared zero or hidden by a looser trace gate.

The independent decomposition on the corrected attempt02 writes

    P_t,endpoint = trace(projected bulk force)
                   + trace(projected nodal Gram force)
                   + trace(weak integration-by-parts defect).

It reconstructs the measured endpoints within 4.9e-19. For MTS's inner
endpoint, the primary components are approximately

    bulk: 2.49e-13, nodal: -1.05799e-7, weak-IBP: -9.70820e-10.

For GR there is no nodal Gram component; its remaining defect is numerical
weak-IBP work. Merely making the new mass/lapse polynomials evaluate more
coherently does NOT cure that term. That unsuccessful cure remains in
attempt03 instead of being presented as progress it did not make.

## 4. Constructed momentum trace projection for ALL nodal sources

Let V,W denote the existing mass coordinate and momentum maps, with
M=<W,V>. For the 15 INTERIOR node evaluation covectors, set

    L_j=V(R_j)^T, E_b=W(R_b), D=E_b M^(-T) L.

The desired endpoint trace of a pure interior nodal distribution is zero.
The current finite projection does not enforce that. We construct two new
continuous coordinate functions H with interior nodal values -D^T, zero
endpoint values and <W,H>=0. Nodal hats give the prescribed values; the
existing continuous cell-bubble reservoir supplies the orthogonal correction.

Normalize H=H_raw A by an invertible QR map. Construct paired momentum
functions T with

    <T,V>=0, <T,H>=I, T(endpoint)=A^(-T).

Endpoint hats plus bubble moments supply T. Full ranks are checked without
deleting old modes or nodal-source directions. The new pairing is block
diagonal, diag(M,I). For an arbitrary interior nodal load g,

    old endpoint response = D g,
    added endpoint response = A^(-T)(-A^T D g) = -D g.

Thus the entire nodal family has zero projected endpoint momentum trace while
every old weak covector is retained. This is NOT fitting the actual Gram load
to a cancellation coefficient. The construction does not inspect its source
amplitudes. GR receives the same construction, although its Gram load is zero.

Afterwards the existing kernel mass-flux trace completion is rebuilt using
the new actual P_t and time Jacobians. Its new coordinate functions vanish at
interior nodes, where the Gram mass forces act. Their bulk force vanishes by
the retained moment relations in the exact weak integral, so the two trace
constructions are compatible conditionally. Actual rates/J are recomputed;
floating-point transparency is not assumed.

An independent solve on the FINAL full frame tests all 15 nodal source columns:
maximum endpoint trace errors are 5.32e-13 (GR) and 2.82e-13 (MTS). All 16
parent cell-kernel directions also remain; their mass-flux trace errors are
below 1.6e-17. No source mode, original canonical direction or boundary row
is discarded. This fixes the MTS-specific projection effect but leaves the
shared weak-IBP defect in the OLD finite action (attempt04).

## 5. An explicit alternative finite quadrature of the SAME continuum action

The old zero-P gravitational Hamiltonian density is

    H_g,old = -N mu_R/(kappa sqrtF).

With U=sqrtF and ANY fixed reference U_ref,

    H_g,new = -N(U+1/U-2U_ref)/(2kappa)
              -R N_R(U-U_ref)/kappa,
    B_g,new = [R N(U-U_ref)/kappa]_in^out.

Their continuum integrals are exactly equal: H_g,new-H_g,old is minus the
radial derivative of the written boundary primitive. Changing U_ref only
adds an analytically null integral of (RN)_R. We use U_ref=sqrt(2/3) solely
for numerical conditioning; it is neither a model parameter nor a sourced
physical coupling. It is held fixed in every variation.

The scalar, P-linear/P-squared weak bulk terms, physical P-squared boundary,
outer clock and port reactions are unchanged. The Gram time-link action,
including its full Jacobians/current, is unchanged. The added gravitational
boundary is retained before varying: it cancels the natural mass boundary
reaction at P=0 and gives the correct remaining bulk mass covector.

At fixed finite quadrature Q the two actions need not be identical. Their
explicit difference is

    H_new-H_old = [R N(U-U_ref)]/kappa
                         -Q[partial_R(R N(U-U_ref))]/kappa.

We record this difference, rather than subtracting an unexplained force from
an old Euler row. On the final fields it is about -6.00e-16 for GR and
-2.26e-15 for MTS; the separately evaluated boundary-defect expression agrees.
A tiny action-value difference alone would not bound its derivatives.
Complex-step tests independently check the NEW action's mass and extra-cubic
lapse derivatives. This is a new finite-quadrature branch with its own tests.

The new weak gravitational constraint is

    C_g[eta] = Q[eta(U+1/U-2U_ref)/(2kappa)
                         +eta_R R(U-U_ref)/kappa]
                  -[eta R(U-U_ref)/kappa].

Its mass derivative is

    delta C_g[eta] = Q[(eta mu/(kappa R^2 F^(3/2))
                          -eta_R/(kappa sqrtF)) delta mu]
                       +[eta delta mu/(kappa sqrtF)].

Matter and Gram terms are retained in the full constraint/Jacobian and Cdot.
There is no numerical differentiation of an inferred cancellation force.
The new mass Euler calculation no longer obtains a small P_t by subtracting
large nearly cancelling coordinate-gradient and boundary terms.

## 6. Final paired result and unchanged acceptance gates

Attempt07, N16 only:

| Quantity | Matched GR+scalar | MTS metric-Gram |
|---|---:|---:|
| Primary max of all 19 C rows | 8.7534e-14 | 6.9624e-14 |
| Higher-quadrature max C | 1.4194e-13 | 9.9156e-14 |
| Primary max of all 19 Cdot rows | 1.5266e-16 | 6.0253e-12 |
| Higher-quadrature max Cdot | 2.0817e-17 | 2.8387e-12 |
| Primary max endpoint P_t magnitude | 2.2987e-13 | 1.0962e-13 |
| Higher-quadrature max endpoint P_t magnitude | 4.2616e-13 | 4.4442e-13 |
| Primary inner mass-drive gap | 0 | -5.1457e-14 |
| Outer clock-value gap | 0 | 0 |

The original 17 constraints, two added rows, both full parent mass-flux traces,
outer scalar drive and endpoint P_t all pass their declared 1e-10 gates.
Higher quadrature changes the reported numbers but does not break a gate.
Sampled F remains above 0.65957 and N above 0.81206, not interval bounds.

The strict inner mass Newton stop at 2e-14 stalled in the integrated-action
experiments. The final run uses the SAME 2e-13 INNER solve tolerance for BOTH
branches. The final physical/numerical acceptance gates remain 1e-10 and the
P_t gate is not relaxed. The larger C residuals are reported in the table;
they are not still described as 2e-14 solves. This adjustment is solver
precision management, not evidence that the strict attempt converged.

The final independent control passes 21 checks, including action identities,
actual action derivatives, the 19-row mass Jacobian, fixed-frame replay and
full-family trace testing. The mass Jacobian directional errors are at most
1.37e-12. These controls support this finite first jet, not a general existence,
well-posedness, positivity or full local-GR theorem.

## 7. The next clock-rate condition is also derived

Assuming the classical endpoint P=P_t=0 and the same no-extra-P-boundary
contract, time differentiation gives

    partial_R(N_t/N)_b = kappa E_t,b/R_b + mu_t,b/(R_b^2 F_b^2),
    E_t=pi*pi_t/R^2 + R^2 chi_R*(chi_t)_R.

For the declared constant outer clock,

    (N_t/N)_out = -mu_t,out/(R_out F_out).

Let that last value be r. A constructive candidate is

    N_t = r N + Y_1 a_in + Y_2 a_out,
    a_b = N_b*[required partial_R(N_t/N)]_b.

It preserves the clock-rate condition and supplies the two required boundary
gradient rates. The two candidate amplitudes are approximately
(0.00421284,0.00503170) for GR and (0.00410655,0.00538835) for MTS in fixture
units. These are saved as UNAPPLIED next-lapse-rate candidates, not full
second jets. No assumption about missing scalar accelerations or mass-drive
second derivatives is silently supplied by this construction.

**Next target:** assemble the full next-time-jet equations on these frozen
small-case frames, including nonlinear history covectors, time-boundary work,
clock rate and both physical-drive compatibility conditions. Test the same
system with GR. Only authorize a short trajectory when those gates and the
history/time-domain contract hold. Do not return to automatic N256 refinement
or reuse an old failed-state evolution.

## 8. Preserved attempts and evidence

- attempt01: stopped on a 1.60e-12 numerical primitive-origin drift; corrected
  by subtracting BOTH endpoint primitive values, not raising that trace tolerance.
- attempt02: applied the full cubic and solved 19 rows; exposed nodal and weak-IBP defects.
- attempt03: coherent local polynomial representation; did not cure weak-IBP.
- attempt04: full-family nodal trace construction; shared old-action weak-IBP remains.
- attempt05: integrated gravity with reference 1; strict inner solves stalled in both branches.
- attempt06: conditioning reference sqrt(2/3); strict GR inner solve stalled, MTS completed.
- attempt07: same common inner tolerance in both branches; complete paired first-jet gates.

All seven runs and executed sources are retained under
source-intake/navier-stokes/20260912/annular-cubic-lapse-boundary-attemptNN.
The earlier paths/results are not overwritten. No failed attempt is an
approved physical seed.

Key local sources (relative to post-checkpoint-work):

- `DERIVATION-20260912-nonlinear-history-Euler-equations.md`
- `DERIVATION-20260912-bounded-N128-and-nonlinear-continuation.md`
- `scripts/annular_cubic_lapse_boundary_polynomial_20260912.py`
- `scripts/annular_cubic_lapse_nodal_trace_20260912.py`
- `scripts/annular_cubic_lapse_reference_gravity_20260912.py`
- `scripts/annular_cubic_lapse_final_boundary_20260912.py`
- `scripts/derive_annular_cubic_lapse_final_boundary_20260912.py`
- `scripts/diagnose_annular_cubic_Ptrace_20260912.py`
- `scripts/verify_annular_cubic_final_boundary_20260912.py`
- `source-intake/navier-stokes/20260912/annular-cubic-Ptrace-diagnosis-attempt01.json`
- `source-intake/navier-stokes/20260912/annular-cubic-lapse-boundary-attempt07/status.json`
- `source-intake/navier-stokes/20260912/annular-cubic-boundary-control-attempt01/status.json`

One BelowNormal single-core Python at a time, no subagents or GitHub action.
The combined final seal records hashes, source-path checks, a resume snapshot
and an mtime scan of the frozen workbench since 2026-09-12T12:03:18Z. No files
outside post-checkpoint-work are intentionally modified.

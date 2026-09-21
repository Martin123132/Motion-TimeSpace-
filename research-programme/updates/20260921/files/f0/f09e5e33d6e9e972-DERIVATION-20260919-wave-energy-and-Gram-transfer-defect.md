# Full scalar wave-error energy and the Gram transfer defect

Private continuation, 19 September 2026. This stage evaluates the kinetic-plus-potential hierarchy diagnostic proposed in the preceding sealed result. All original scalar modes, the source constraint, live geometry and both reference/MTS branches are retained. No action, coupling, trajectory or source boundary condition is changed.

## Result in plain language

Adding potential energy does **not** cancel the observed final MTS error-energy growth. About97.47% of its instantaneous total rate is accounted for by the **Gram stiffness-transfer work**, the difference between how the two grids turn the same coarse field into a Gram force. The ordinary gradient-transfer and changing-geometry terms are also retained.

This identifies a specific finite-system consistency problem to investigate. It does NOT establish a physical instability, long-time growth, a failed underlying theory or a resolved GR limit. Two stable discrete wave systems can accumulate phase/representation error between them. Conversely, calling this endpoint growth merely kinetic/potential exchange would miss the measured residual.

The raw error norm is dominated by an initial representation mismatch common to both branches. A second exact diagnostic separates that initial field/velocity difference, its linear continuation, the subsequently accumulated difference, and their cross term. It does not erase the initial mismatch or replace the original test.

The earlier **12.5718%** impulse and approximately **13.58%** instantaneous reduced-force hierarchy discrepancies remain unchanged. These are normalized annular calculations through T=4e-5, not a full .004 interval, physical-SI fit, complete GR/Newton limit or empirical acceptance test. Coarse/fine endpoints have unequal saved time resolutions, so the comparison is not isolated spatial truncation error.

## 1. Stiffness from the existing action, not a replacement force

Let D be the existing reference P2 gradient evaluation and B the existing lifted Gram operator. The unchanged scalar potential is

    U(u) = (1/2) (D u)^T diag(a) D u
         + (1/2) (B u)^T diag(w) B u,
    K = D^T diag(a) D + B^T diag(w) B,

where a=quadrature_weight*coefficient/J and w is the original sampled coefficient/J divided by the original Gram spacing. All rows are retained. Reference has no Gram rows; its ordinary-gradient energy/force is nonzero and provides the relevant comparator.

For each actual saved initial/final state, both grids independently reproduce the action's potential and scalar force as

    F = -K u + G,
    G = V Q^T diag(omega) (Phi v + V Q u),

where Q is the actual source-map motion operator, omega the temporal quadrature weight, v the scalar velocity and V the source velocity. G is a retained kinetic source term, not an additional fitted coupling.

### Positivity and the pinned source

All actual spatial and present Gram weights are positive. A zero gradient quadratic form requires a constant on each connected P2 half-interval. The original zero source value pins both constants, so the ideal discrete gradient form is positive definite on the retained scalar space; adding the nonnegative Gram form does not remove this property. No eigenvalues/modes were clipped.

A simple sufficient comparison is

    u^T M u <= C u^T K u,
    C = (L_max^2/2) max(omega/quadrature_weight)
                       / min(a/quadrature_weight).

On each side, u(anchor)=0 gives the elementary integral inequality integral(u^2)<=L_side^2/2 integral((u')^2). Constant-coefficient P2 mass and gradient polynomial integrals are integrated exactly in ideal arithmetic by the existing Gaussian rule. Applying the sampled weight extrema proves the stated discrete comparison in that arithmetic. Floating evaluations were checked on the actual displacement and two independent nodal probes, not claimed as an interval-arithmetic proof. Sampled C is about1.0167132 here; this is not a uniform continuum or full source/gravity-Hessian coercivity certificate.

## 2. Exact hierarchy energy balance

I is the fixed reference nodal interpolation from coarse H to fine h. The grids are not nested as function spaces. Define

    e = u_h - I u_H,
    d = v_h - I v_H = dot(e),
    E_wave = (1/2) d^T M_h d + (1/2) e^T K_h e,
    R_wave = M_h dot(d) + K_h e.

Then

    dot(E_wave) = d^T R_wave
               + (1/2) d^T dot(M_h) d
               + (1/2) e^T dot(K_h) e.

The -d^T K_h e conservative kinetic work cancels the corresponding potential exchange, but it does NOT cancel d^T R_wave. All mass and stiffness geometry rates are retained. This is scalar hierarchy-error energy, **not** the complete source-plus-gravity Hamiltonian.

### Seven residual channels

Use the actual inverse relation p=Mv+bV+r, canonical force F=dot(p), source acceleration A=dot(V), and the induced covector comparison T=M_h I M_H^(-1). The retained scalar acceleration law is

    M dot(v) = -K u + G - dot(b)V - bA - dot(M)v - dot(r).

It gives

    R_wave = [T K_H u_H - K_h I u_H]
           + [G_h - T G_H]
           + [-dot(b_h)V_h + T dot(b_H)V_H]
           + [-b_h A_h + T b_H A_H]
           + [-dot(M_h)v_h + T dot(M_H)v_H]
           + [-dot(r_h) + T dot(r_H)].

The first bracket splits into ordinary-gradient and Gram stiffness-transfer loads, giving seven channels in total. T is an induced-velocity comparison, not raw nodal interpolation of momentum covectors, nor an asserted symplectic map.

## 3. Actual endpoint comparison

The complete saved canonical direction and both inverse-residual derivatives come from the previous sealed run. State, velocity, scalar force and mass consistency are verified before reuse. Fine live geometry is recomputed at symmetric full-state tangent probes of2e-7,1e-7,5e-8,2.5e-8. No trajectory is evolved.

The displacement tangent is formed as e±epsilon*d before evaluating energy, rather than subtracting two almost equal independently perturbed nodal arrays; this reduces cancellation loss in the intended tangent test. Geometry is still recomputed from each full perturbed state. These are finite-difference estimates, not certified derivatives or a convergence theorem.

### Energies at T=4e-5

| Quantity | Reference | MTS |
|---|---:|---:|
| Kinetic error energy | 3.31746e-16 | 8.54327e-15 |
| Ordinary-gradient error energy | 1.32837938e-10 | 1.32839791e-10 |
| Gram error energy | 0 | 5.00537e-19 |
| Total error energy | 1.32838270e-10 | 1.32848334e-10 |
| Initial total error energy | 1.32839134e-10 | 1.32839134e-10 |
| Fractional change from initial | -6.50835e-6 | +6.92575e-5 |

The small Gram energy does not imply small Gram force-transfer work. They are different quantities, one quadratic in the displacement error and the other pairing velocity error with a consistency residual.

### Rates at the finest probe

| Work/rate | Reference | MTS |
|---|---:|---:|
| Ordinary-gradient stiffness transfer | -6.37256e-11 | +8.75081e-12 |
| Gram stiffness transfer | 0 | +4.05935591e-10 |
| Kinetic source force | -4.35332e-15 | -1.84061e-15 |
| Cross transport | -7.85156e-16 | -2.78527e-15 |
| Source acceleration | -2.34500e-16 | +7.11495e-16 |
| Mass transport | +5.25409e-18 | +1.08997e-16 |
| Inverse-residual derivative | +7.50304e-21 | +1.02133e-20 |
| Changing-mass contribution | -2.57475e-18 | -5.44546e-17 |
| Changing-stiffness contribution | +1.79503e-12 | +1.79507e-12 |
| **Total scalar error-energy rate** | **-6.19359543e-11** | **+4.16477609e-10** |
| Localized absolute rate bound | 1.84091e-10 | 6.68679e-10 |

For MTS, conservative kinetic work is -1.43636902e-11 and potential exchange is +1.43636902e-11. These cancel each other, not the positive Gram transfer work. The ratio4.05935591e-10/4.16477609e-10=0.97468767 explains the97.47% statement. It is a signed decomposition of this endpoint diagnostic, not a probabilistic causal attribution.

Across all probes, maximum direct/composed energy-rate discrepancy is5.75e-19(reference) and4.14e-19(MTS); maximum residual-load reconstruction discrepancy is6.64e-15 and9.32e-15 respectively. The errors are NOT monotone under probe refinement. Pass tolerances are stored explicitly and are larger than observed errors; no small-channel sign or many-digit physical interpretation is justified by them.

## 4. Separate the initial representation floor without hiding cross terms

Both initial displacement and initial velocity discrepancies are nonzero: their maximum nodal magnitudes are about1.35643e-8 and4.42713e-8. Ignoring the initial velocity would be incorrect.

Let e0,d0 denote these exact saved initial differences. Define a diagnostic first-order baseline and increment

    e_b(t) = e0 + t d0,    d_b = d0,
    e_i = e-e_b,           d_i = d-d0.

The baseline is NOT a new physical solution. No evolved state or original error measure is changed. Exact polarization gives

    E_wave = E_b + E_i + E_cross,
    E_cross = d0^T M_h d_i + e_b^T K_h e_i.

E_b and E_i are nonnegative; E_cross can have either sign. The complete differentiated identity, including dot(M), dot(K), dot(e_b)=d0 and the increment acceleration, is evaluated. Independent dense fixtures reject dropping the cross terms.

| Finest-probe quantity | Reference | MTS |
|---|---:|---:|
| Baseline energy E_b | 1.32840221e-10 | 1.32840221e-10 |
| Increment energy E_i | 4.61541e-16 | 7.68449e-15 |
| Cross energy | -2.41244e-15 | +4.29285e-16 |
| Baseline rate | +2.71634e-11 | +2.71634e-11 |
| Increment rate | +2.30754e-11 | +3.84169e-10 |
| Cross rate | -1.12175e-10 | +5.14473e-12 |

Thus the reference's negative raw total rate is NOT evidence that its subsequently accumulated error is zero or decreasing: its cross term matters. MTS has a larger growing increment in this chosen comparison, but an increment relative to a linear baseline can grow even for stable oscillatory systems. Neither sign is a standalone stability/instability certificate. Initial-floor subtraction must not be used to improve the reported12.5718% impulse discrepancy artificially.

## 5. Next derivation target: weak Gram-force consistency

The concrete remaining load is

    S_G = T K_G,H u_H - K_G,h I u_H,
    K_G,a = B_a^T W_a B_a.

For the actual velocity test d, define the coarse dual test

    eta_H = M_H^(-1) I^T M_h d.

By mass symmetry,

    d^T S_G = (B_H eta_H)^T W_H (B_H u_H)
            - (B_h d)^T W_h (B_h I u_H).

This exact weak-form identity gives a sharper next question than another long time integration: which mismatch between the coarse/fine Gram trial and test factors produces the measured4.05936e-10 work, and can that residual be bounded with a constant that remains controlled under refinement? eta_H is a mass-adjoint test, not an asserted orthogonal projection: M_H need not equal I^T M_h I.

Next calculate this weak transfer pairing on the saved states, separate source-adjacent from remaining Gram rows, and derive/check a consistency bound without deleting the source trace or replacing the physical action. The displayed weak identity is derived here; its dedicated actual-row decomposition and refinement bound have NOT yet been evaluated. Reducing an error norm, switching a comparison map or observing one decreasing endpoint is not by itself a local-GR proof.

## Evidence / limitations

Successful new implementation checks:146 (25 independent wave-energy algebra,86 actual action/energy/tangent checks,35 initial-jet/polarization checks). These are implementation checks, not146 independent confirmations of MTS. No failed execution occurred in this stage; all43 historical failed executions remain in the inherited chain.

- Previous seal: `source-intake/navier-stokes/20260914/annular-compensated-canonical-driver-final-integrity.json`
- Independent algebra: `source-intake/navier-stokes/20260914/annular-wave-error-energy-algebra-attempt01/status.json`
- Actual energy calculation: `source-intake/navier-stokes/20260914/annular-live-wave-error-energy-attempt01/status.json`
- Initial-jet calculation: `source-intake/navier-stokes/20260914/annular-wave-initial-jet-split-attempt01/status.json`
- Unchanged parent action: `scripts/annular_quadratic_source_fitted_action_20260915.py`
- New factored energy helper: `scripts/annular_wave_error_energy_20260919.py`
- Actual runner: `scripts/derive_annular_live_wave_error_energy_20260919.py`
- Polarization runner: `scripts/derive_annular_wave_initial_jet_split_20260919.py`

Private post-checkpoint-work only; no GitHub or subagents. One actual single-core BelowNormal computation at a time. The integrity seal verifies all inherited/new evidence and sourced nonclaim tables, compiles the new sources without bytecode, and checks the protected workbench by mtime since14:03:20UTC. That is not a pre-turn whole-tree hash baseline. This stage does not establish the full GR limit or resolve the continuum force mismatch.

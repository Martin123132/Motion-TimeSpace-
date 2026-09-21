# Source impulse and a force-controlling energy norm

Private continuation of `DERIVATION-20260919-variable-geometry-Gram-consistency.md`. This is an additional dynamical test, not a replacement of the instantaneous source-force requirement. The earlier 13.58% MTS endpoint force discrepancy remains an unresolved result. This note does not establish the full GR limit. All quantities in this experiment are normalized annular-model quantities, not calibrated SI observables.

## 1. Exact source impulse, with no time averaging in the evolution

For the retained source action write p_total=p_wave+p_material and f_total=f_wave+f_material. Here f means the raw coordinate derivative of the Lagrangian, not the reduced physical force. The canonical Euler equation gives

    F_radiation = f_wave - d p_wave/dt
                = d p_material/dt - f_material.

This is a dynamical identity. It does not require deleting Gram terms, setting the source motion to zero, or replacing the solved equations by averaged equations. For a differentiable test weight w, on [0,t_end], subtract the initial momenta before integrating by parts:

    I_wave[w] = integral w f_wave
                - w(t_end) [p_wave(t_end)-p_wave(0)]
                + integral w' [p_wave-p_wave(0)],

    I_material[w] = w(t_end) [p_material(t_end)-p_material(0)]
                    - integral w' [p_material-p_material(0)]
                    - integral w f_material.

The initial subtraction is algebraically exact even when w(0) is nonzero. It reduces avoidable cancellation from a constant momentum offset. The difference of these two numerical constructions is independently compared with the quadrature form of the total canonical balance defect. The validator retains the additional reconstruction terms: integral w (f_wave+f_material-f_total), minus the weighted endpoint change of p_wave+p_material-p_total, plus its w'-weighted integral. These source-covector split and momentum-inverse residuals must not silently be equated to zero. Agreement of that identity is an implementation check, not proof of continuum convergence.

The finite-element test reconstructs actual saved fully coupled trajectories; it does not integrate a modified source law. Three weights w=(t/T)^k, k=0,1,2, and four prefixes T/4,T/2,3T/4,T are tested at T=4e-5. Using a finite family of weights is not a proof of convergence against all smooth test functions. A small net impulse can coexist with a substantial instantaneous error or rapid oscillations.

An exact negative control makes that last distinction unavoidable: take F_epsilon(t)=sin(t/epsilon), epsilon_n=T/(2*pi*n+pi/2). Then F_epsilon_n(T)=1 for every n, but |integral w F_epsilon_n|<=epsilon_n*(2||w||_infinity+||w'||_L1) -> 0 for any fixed differentiable weight. Even genuine weak convergence would not by itself recover the old endpoint-force requirement.

## 2. Conditional weak-force convergence criterion

Let delta p and delta f be finite-versus-continuum material momentum and material raw force differences. For exact dynamics,

    |integral w (F_h-F)|
      <= |w(t_end)| |delta p(t_end)| + |w(0)| |delta p(0)|
         + ||w'||_L1 ||delta p||_infinity
         + ||w||_infinity ||delta f||_L1.

If either evolution has an Euler defect, add the absolute weighted integral of the difference of those defects. Consequently uniform material-momentum convergence and L1 material-force convergence, together with vanishing Euler defects, imply weak radiation-force convergence on the same interval. This is a sufficient conditional theorem; it does not assume those hypotheses have already been proved for the nonlinear parent.

The material relations are explicit:

    chi = sqrt(N^2-v^2/U^2),
    p_material = m v/(U^2 chi),
    f_material = -m (N N_R+v^2 U_R/U^3)/chi.

For E=sqrt(m^2+U^2 P^2) and v=N U^2 P/E, these give p_material=P and f_material=-E N_R-N U U_R P^2/E, the unchanged characteristic material force. The symbolic validator checks this for signed real P, not just outward-moving matter.

There is also an explicit sufficient state/geometry condition. On a common admissible rectangular box with N_min>0, U_min>0, |v|<=V<N_min U_min, N<=N_max, |N_R|<=L_N and |U_R|<=L_U, set

    chi_0 = sqrt(N_min^2-V^2/U_min^2),
    B_0 = N_max L_N + V^2 L_U/U_min^3.

The momentum Lipschitz constants for (v,N,U) can be taken as

    L_pv = m N_max^2/(U_min^2 chi_0^3),
    L_pN = m V N_max/(U_min^2 chi_0^3),
    L_pU = 2m V/(U_min^3 chi_0) + m V^3/(U_min^5 chi_0^3).

The material-force constants for (v,N,U,N_R,U_R) can be taken as

    L_fv = m [2 V L_U/(U_min^3 chi_0) + B_0 V/(U_min^2 chi_0^3)],
    L_fN = m [L_N/chi_0 + B_0 N_max/chi_0^3],
    L_fU = m [3 V^2 L_U/(U_min^4 chi_0) + B_0 V^2/(U_min^3 chi_0^3)],
    L_fNR = m N_max/chi_0,
    L_fUR = m V^2/(U_min^3 chi_0).

Multiply these by the corresponding state/geometry differences to bound delta p and delta f. The box condition matters: two individually timelike endpoint states alone do not justify applying a mean-value bound along a path that leaves the timelike domain. Values and gradients are evaluated at each moving source position; comparing them at one fixed radius would omit the source-position error. A clock floor, bounded gradients and the required convergence remain hypotheses, not new parent-owned constants.

## 3. Discrete, auditable error budget

The comparison uses 17 common times for both finite trajectories and the independent characteristic oracle. On a prefix, positive composite Simpson weights a_j define

    M[p,f] = w_end (p_end-p_0)
             - sum_j a_j [w'_j (p_j-p_0)+w_j f_j].

Let delta p_shift=(p_h-p_h0)-(p-p0). The exact finite-data difference is bounded by

    |M_h-M| <= |w_end delta p_shift_end|
               + sum_j a_j [|w'_j delta p_shift_j|+|w_j delta f_j|].

There is an exact telescope

    I_wave_h - I_augmented_continuum
      = (I_wave_h-M_h_common) + (M_h_common-M_continuum_common)
        + (M_continuum_common-I_augmented_continuum).

Both outer terms are computed, not discarded. This yields a bound for the difference of the finite numerical functionals. It is NOT a continuous-time supremum bound or a rigorous enclosure of the unknown exact solution. Separate diagnostics report:

- quadrature subsampling of the SAME saved path;
- actual evolved time-step halving at each spatial resolution;
- spatial comparison with the best available time controls;
- continuum degree384/512 and actual maximum-step T/8 versus T/16 controls;
- raw-term cancellation and independent momentum-balance residuals.

The continuum oracle augments the unchanged characteristic ODE with passive integrals of the radiation force. These integrals do not feed back into the physical equations. Accepted augmented states are saved. Both branches receive the same test; the zero-Gram reference is not presumed exact.

## 4. A derived energy bound for the explicit Gram drive

At fixed geometry and source position let M be the positive scalar mass, K=K_regular+K_Gram the full retained scalar stiffness, B the inherited lifted Gram map, W its positive weight and W_b its source derivative. Let X be the source-transport cross map and T=M^-1 X. The same explicit drive audited previously is the quadratic functional

    J_G(u) = -1/2 (Bu)^T W_b (Bu) + (BTu)^T W(Bu).

Its exact gradient is

    g(u) = -B^T W_b Bu + X^T M^-1 B^T W Bu + B^T W BTu.

The X^T term is required; omitting it changes the functional derivative. Define

    L_E(u) = sqrt(g(u)^T K^-1 g(u)),
    omega_max^2 = lambda_max(K,M),
    beta = max_i |(W_b)_i|/W_i,
    a_0 = max_quadrature |c| R^2/C = max_quadrature |c|/(N U),

where c=partial_b R and C=R^2 N U. With the same positive quadrature used to assemble the action, T is the weighted L2 projection of -c u_R. Projection contractivity gives

    ||Tu||_M <= a_0 ||u||_Kregular <= a_0 ||u||_K,
    ||BTu||_W <= omega_max a_0 ||u||_K.

Thus, with H=beta/2+omega_max a_0,

    |J_G(e)| <= H ||e||_K^2,
    |J_G(u+e)-J_G(u)|
      <= L_E(u) ||e||_K + H ||e||_K^2.

This is a frozen-geometry, field-only estimate. All scalar modes and Gram rows remain; no frequency clipping is used. It identifies a real sufficient force-control condition: BOTH products on the right must tend to zero. Merely asserting ||e||_K -> 0 is insufficient when L_E or H grows with mesh refinement. Dynamic metric/source errors require additional control. The measured spatial and temporal hierarchical errors are not the unknown continuum error.

## 5. Execution record and results

All seven new workers/validators completed: two main saved-trajectory reconstructions (44 checks each), two coarse-time controls (20 each), the independent continuum oracle (12), the energy bound (24), and the comparison/algebra validator (216). Total: 380 successful implementation checks. There were no new failed executions. These are software/algebra/evidence checks, not 380 independent tests of the physics. The previous 40 failed executions remain preserved. No public push or protected-workbench edit is part of this stage.

### 5.1 Actual integrated forces

For the unweighted full-prefix impulse, the tight continuum value is -1.0757930998401473e-12. Its degree384->512 change is 3.5114716778e-16, while actual maximum-step halving changes it by 3.1418928838e-23. These are empirical refinements, not rigorous uncertainty bounds.

| Branch | Base vertices | Evolved steps | Radiation impulse | Relative difference from tight continuum |
|---|---:|---:|---:|---:|
| Reference | 257 | 16 | -1.0229095827122e-12 | 4.9158% |
| Reference | 257 | 32 | -1.0229484784585e-12 | 4.9122% |
| Reference | 513 | 32 | -1.0737502758124e-12 | 0.18989% |
| Reference | 513 | 64 | -1.0737611313801e-12 | 0.18888% |
| MTS | 257 | 16 | -1.0637427233260e-12 | 1.1201% |
| MTS | 257 | 32 | -1.0642565809523e-12 | 1.0724% |
| MTS | 513 | 64 | -1.2110608024856e-12 | 12.5738% |
| MTS | 513 | 128 | -1.2110400129155e-12 | 12.5718% |

The important adverse result is that the fine MTS discrepancy does NOT disappear when integrated over the tested interval. The fine-grid impulse error is 1.3524691308e-13, whereas actual time-step halving changes that impulse by only 2.0789570040e-17. Reference spatial refinement improves the same diagnostic substantially. The apparently better coarse MTS impulse is therefore not evidence of a resolved limit. Conversely, two spatial levels do not prove divergence or rejection of the underlying continuum theory.

At the fine MTS resolution, the full-prefix weighted errors are 8.9637% for k=1 and 7.9691% for k=2. The unweighted prefix errors are 58.5566%, 26.1828%, 17.2692%, 12.5718% at T/4,T/2,3T/4,T. Early impulses are much smaller, so the large early percentage must be read alongside its absolute difference, not as a statement that the entire gravitational model is wrong by that percentage. The fine reference's corresponding unweighted prefix errors are 2.7567%, 0.3060%, 0.4699%, 0.1889%; its full-prefix k=1,2 errors are 0.1014%, 0.0646%.

The largest same-path quadrature difference among the twelve fine MTS moments is 3.8637e-18; for the fine reference it is 1.4343e-19. Coarse weighted quadratures are NOT all this well resolved: the worst coarse16 MTS difference is 1.9247e-15 and is comparable to that particular moment's discrepancy. All 96 matched moments and 72 actual time/spatial comparisons are retained, not just the favorable unweighted endpoint.

The unweighted fine MTS impulse subtracts raw terms with total absolute scale 5.5854e-8 to obtain approximately 1.2110e-12. Independent material-momentum construction differs by 8.7383e-20; its total canonical quadrature defect is 1.1449e-19, with the inverse/split correction explicitly retained. Thus the measured 1.3525e-13 discrepancy is not explained by those recorded closure residuals. The common-node material telescope gives 1.3524852391e-13, nearly saturating its finite-data bound. It is not a rigorous bound on an uncomputed exact continuum trajectory.

### 5.2 Energy-control result

All 1072 scalar modes remain in the fine test. The MTS maximum scalar angular frequency is 3.2396241e6, a_0=1.30357617, beta=1.67472746, and H=4.22309767e6. The independently differentiated gradient passes the directional checks.

| Fixed-fine-geometry comparison | Energy norm of field difference | Dual force gain | Derived energy bound | Measured Gram-force change magnitude |
|---|---:|---:|---:|---:|
| MTS embedded257 -> actual513 | 1.6299680e-5 | 523.930156 | 9.6618849e-3 | 2.9701554e-8 |
| MTS 64 -> 128 evolved steps | 3.2882018e-13 | 523.930106 | 1.7227879e-10 | 1.7207286e-10 |

The time-step bound is sharp to about 0.12%. The spatial global-energy bound is far too loose to certify anything useful: most of that energy difference is not aligned with the source-force functional, and the maximum-frequency quadratic estimate is conservative. This is a limitation of that bound, not a newly measured physical force of 9.66e-3. The previous localized five-term Gram bound remains available and much stronger for the spatial hierarchy; it is not superseded by this coarse global bound. The zero-Gram reference gives exactly zero for this particular Gram-functional change and bound, while retaining a nonzero ordinary spatial field error.

## 6. Decision and next derivation

This stage closes a tempting but unsupported escape route: the current source-force mismatch cannot simply be declared a fast oscillation that averages away on the tested interval. It also gives a verified sufficient force-control law and a sharp temporal error estimate. It does not establish spatial convergence of the live branch, the full original interval, a parent-derived physical coupling, or full local GR.

The next useful derivation is error transport in the source-force functional itself, using its exact gradient/adjoint and localized Gram split, including geometry and initial-data defects. Qualify that estimate against the existing actual temporal refinements before another expensive spatial run. A generic energy norm, a further time-step reduction alone, or promoting the good coarse-grid impulse would not address the demonstrated spatial sensitivity. Preserve both the unfavorable MTS result and the successful reference control.

Evidence:

- `source-intake/navier-stokes/20260914/annular-P2-source-impulse-comparison-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-P2-source-impulse-comparison-attempt01/matched-impulses.csv`
- `source-intake/navier-stokes/20260914/annular-continuum-source-impulse-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-P2-Gram-energy-error-bound-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-P2-Gram-trajectory-defect-attempt01/status.json`

Primary implementations:

- `scripts/run_annular_P2_saved_impulse_20260919.py`
- `scripts/run_annular_P2_saved_coarse_impulse_20260919.py`
- `scripts/run_annular_continuum_impulse_20260919.py`
- `scripts/derive_annular_P2_Gram_energy_error_bound_20260919.py`
- `scripts/compare_annular_source_impulse_20260919.py`

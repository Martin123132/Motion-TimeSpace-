# Causal coupled defect correction of the finite moving action

Private local checkpoint. This is a numerical derivation and test on the original finite prescribed-background action, not a full GR limit. No original GR-oracle failure is upgraded. No force term, matter coupling, action, initial data or physical acceptance gate is fitted or replaced.

## 1. What is constructed

The preceding checkpoint, `DERIVATION-20260916-moving-force-attribution-and-adjoint.md`, qualified the complete finite field/source/clock Jacobian and force derivative. It also explained the observed short-run force discrepancy by initial preparation and accumulated omitted-mode response. Explaining an already observed discrepancy is not yet a useful forward correction.

Here the predictor receives only the reduced states and their derivatives, the original initial state computed by its existing function, and the fixed model. It receives no future full states, future full forces, observed discrepancies or fitted correction coefficients. Both branch predictions and refinement controls are saved and hashed before a separate validator opens the reference trajectories. The underlying test has already been studied: this is input-isolated algorithm validation, NOT blind discovery or a new empirical test.

## 2. Derived correction, including initial preparation

Write the unchanged original first-order equations as zdot=F(z), with z=(u,b,v,V,clock). Let r(t) be the reconstructed lifted reduced path. Define J(t)=DF(r(t)) and d(t)=F(r(t))-rdot(t). Solve

```text
etadot = J eta + d,
eta(0) = z_original(0) - r(0),
c(t) = r(t) + eta(t).
```

This is a linear inhomogeneous initial-value problem with known coefficients, not a fit to the full trajectory. It is the first Newton correction to the differential equation residual, with the initial condition corrected at the same time. Field positions, source position, all their rates, and the clock are corrected together. The reported force is the original action's force evaluated on c, not a subtracted observed error.

In exact arithmetic/integration,

```text
cdot = F(r) + J eta,
F(c)-cdot = N(r,eta) = F(r+eta)-F(r)-DF(r)eta.
```

If F is twice continuously differentiable along the segment r+s eta, then componentwise Taylor's formula gives

```text
N(r,eta) = integral_0^1 (1-s) D2F(r+s eta)[eta,eta] ds.
```

Thus a Hessian bound H on a specified admissible tube would imply |N| <= H |eta|^2/2 in a specified norm. This checkpoint does not supply such a certified tube bound. Measuring N and its half-amplitude scaling is only a finite-path diagnostic, not that theorem's missing uniform hypothesis.

## 3. Numerical reconstruction is not hidden

The implementation reconstructs r and eta with centered cubic Hermite polynomials. For the reconstructed correction eta_h, let

```text
rho = eta_h_dot - [DF(r) eta_h + F(r)-rdot].
F(r+eta_h) - (rdot+eta_h_dot) = N(r,eta_h) - rho.
```

The saved output contains N, rho and the total residual separately, including interior midpoints. Small algebraic closure of this identity is an implementation check, not a bound on rho. Nonlinear remainder scaling and force errors are also distinct: stiffness may amplify an acceleration norm without a comparable force error.

The coordinate rows of the original F are the velocities. Accordingly the exact correction restores position/rate consistency automatically. The clock row is retained: it is driven by corrected source motion even though the clock does not feed back into this prescribed-background action. A clock change below rounding precision must not be sold as an observed improvement.

For completeness, if z is the exact original solution and e=z-(r+eta_h), then

```text
edot = F(r+eta_h+e)-F(r+eta_h) + N-rho,
e(0) = 0, apart from rounding.
```

A certified Lipschitz bound L on a containing tube would give |e(t)| <= integral_0^t exp(L(t-s)) |N(s)-rho(s)| ds. The current sampled residuals and standard/tight comparisons are not substitutes for that uniform bound. No such continuum or all-time certificate is claimed.

## 4. Fixed experiment and source separation

Original locally refined action, base129, source splits8, n=286, state size575, background mass0, source anchor6.03; both reference and MTS branches; T=.005. This remains 1/80 of the old T=.4 GR-oracle test. The reference branch here is the finite reference action, not the continuum GR oracle.

- `scripts/prepare_annular_causal_inputs_20260916.py` extracts only reduced arrays from the old mixed container; its lazy NPZ reads never load future full arrays. Original initial data come from the old initial-data function. The output pack has a strict four-key schema.
- `scripts/run_annular_causal_correction_20260916.py` reads only that pack and its configuration, integrates the coupled correction, and saves prediction manifests. It uses the already qualified `scripts/annular_full_force_linearization_20260916.py`.
- `scripts/run_annular_causal_correction_20260916_v2.py` supplies an actual integration-step refinement. The first tighter-tolerance run accepted the same steps as the standard run, so it is retained as a tolerance check, not mislabelled as evidence from a finer step sequence. This additional run limits steps to a quarter of each Hermite interval, instead of the original half-interval first step. This decision preceded opening the future full trajectories.
- `scripts/validate_annular_causal_correction_20260916.py` requires completed, hash-matching standard/tight predictions before opening the future full trajectories. It independently checks selected corrected states against the original variational acceleration implementation.

Planned before execution: 321-knot and161-knot paths; standard relative/absolute tolerances2e-8/1e-14, tight2e-10/1e-16; both branches treated identically. Existing isolated force budget2e-7 and numerical force-control tolerance2e-10 remain unchanged. Component controls (coordinate-representation errors, not continuum physical-field norms): field1e-9, source1e-11, field rate1e-6, source rate1e-9, clock1e-11. These new numerical component controls do not replace the original GR gates. All outcomes, including failures or rounding-limited components, are recorded.

## 5. Results

All predictions were completed and hash-sealed before the validator opened future full trajectories. The standard and tighter-tolerance runs used8000 RHS evaluations per fine case and produced identical outputs. The separate quarter-interval step control used16520 evaluations per branch. Its actual maximum step was3.90625e-6. All eight cases pass the predetermined component controls, the2e-10 numerical force control and the2e-7 isolated reduction budget at all321 comparison times.

| Branch | Uncorrected maximum force discrepancy | Corrected,161-knot path | Corrected,321-knot path and finer integration |
| --- | ---: | ---: | ---: |
| Reference | 3.31638582e-8 | 8.00953596e-13 | 1.46517726e-15 |
| MTS | 4.08634577e-8 | 2.22873992e-11 | 3.97967758e-15 |

The baseline is the original restricted-action force versus the saved original full trajectory. The corrected force is evaluated from the unchanged full action on the independently predicted corrected state. Both the restricted-action baseline and the original-force-at-uncorrected-state baseline are retained in the machine-readable report; these are not silently interchanged.

These tiny fine-path differences are numerical agreement with the saved finite replay, NOT certified absolute physical accuracy. The prior replay controls reported up to2.224e-12 variation, and no new continuum oracle is involved. The robust statement is that even the coarser path improves the sampled MTS discrepancy by about1833 times, and the largest observed path-refinement change is2.22874290e-11, below the fixed2e-10 control. The actual integration-step refinement changes force by at most6.162e-16/reference and8.606e-16/MTS, measured in ordinary floating point.

Fine-path, finer-integration coordinate-representation errors against the saved full states are:

| Component | Reference | MTS |
| --- | ---: | ---: |
| Field coordinates | 3.904e-18 | 3.470e-18 |
| Source position | 2.665e-15 | 8.882e-15 |
| Field rates | 1.248e-15 | 3.310e-15 |
| Source rate | 2.103e-15 | 5.413e-15 |
| Clock | 1.735e-18 | 1.735e-18 |

All five components improve in this comparison, rather than force improving at the expense of field or source motion. The corrected clock and several other components are rounding-limited; they are not independently verified physics at these scales. Original-action accelerations and forces at nine selected corrected states also agree with the separate variational implementation. Energy drift is at most1.388e-17 in these numerical units. Energy drift is a diagnostic, not a symplecticity or long-time stability theorem.

### What the residual diagnostic does NOT establish

The identity F(r+eta_h)-(rdot+eta_h_dot)=N-rho closes algebraically within5.55e-17. However, midpoint reconstruction residuals are much larger than this identity's rounding error: fine-path maxima are about1.061e-9/reference and9.760e-9/MTS in the acceleration component, and the coarser MTS maximum is1.554e-7. They remain explicitly saved. Fine measured nonlinear residual maxima are4.158e-12/reference and1.839e-11/MTS; no uniform bound follows.

Crucially, halving eta does NOT give a clean measured1/4 norm ratio: the finer-step values are0.723/reference and0.344/MTS. Therefore this direct floating-point subtraction does not empirically resolve clean quadratic scaling at the actual perturbation amplitude. Cancellation/rounding is a possible contributor, not a proved explanation. The exact Taylor identity remains conditional on the stated smoothness; these numerical values must not be used to certify a Hessian bound or second-order asymptotic regime. The successful saved-trajectory prediction does not erase this unresolved residual-precision limitation.

Successful current implementation checks: input isolation5, standard correction21, tolerance control13, actual step refinement13, separate validation50; total102. These are implementation/control checks, not102 independent physical validations. No numerical attempt failed; the unchanged-step tolerance control is retained, not deleted. All21 inherited failed attempts remain preserved through the previous seal.

Evidence:

- `source-intake/navier-stokes/20260914/annular-causal-inputs-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-causal-standard-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-causal-standard-attempt01/predictions-sealed.json`
- `source-intake/navier-stokes/20260914/annular-causal-tight-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-causal-tight-step-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-causal-tight-step-attempt01/predictions-sealed.json`
- `source-intake/navier-stokes/20260914/annular-causal-validation-attempt01/status.json`
- Prior integrity: `source-intake/navier-stokes/20260914/annular-force-response-final-integrity.json`
- Current integrity (complete only when its state says so): `source-intake/navier-stokes/20260914/annular-causal-correction-final-integrity.json`

## 6. Next scientific target

This correction uses the full-state Jacobian and is not a demonstrated speedup over simply evolving the full finite action. Its purpose here is to derive and isolate the response to reduction error, not to create a new physical coupling. The source trace, fixed versus jointly refined Gram stencil and genuine continuum comparison remain separate issues.

If this removes the reduced/full numerical discrepancy, stop polishing this short comparison. Return to the original moving-source GR-oracle/joint-refinement test, preserve the original initial data and full force observable, and distinguish finite spatial/trace error from time-integration/reduction error. A correction toward the original finite action cannot repair a genuine disagreement of that action with the continuum oracle. If the predictor fails the fixed numerical controls, preserve the failure and identify its source before extending the horizon.

Decision: the predetermined sampled finite-action controls pass, so take the first route. Specifically return to `DERIVATION-20260916-boundary-capacity-and-local-source-refinement.md` and its full T=.4 comparisons. The fine513/4 MTS final absolute force discrepancy there is2.60123896e-6 against2e-7, while its field and source/clock gates pass; the fine reference endpoint passes but its nine-time maximum3.99473e-7 does not. These are different grids/horizons from this predictor experiment, so no numerical subtraction of today's errors from those old failures is legitimate.

The next bounded target is an action-preserving, paired refinement test that separately controls bulk resolution and the source trace layer, without statically relaxing away its inertia or initial memory. Compare the complete moving force history with the same independently resolved GR references and unchanged gates. Use the original full-action evolution unless a reduction is separately qualified on that actual grid and horizon; today's short near-full-dimensional correction is not permission to assume a cheap reduced long run. A trend consistent with convergence is evidence to investigate, not a proof of the parent GR limit. Do not spend the next checkpoint merely refining the near-roundoff agreement reported here.

Work remains private in post-checkpoint-work. No GitHub, subagents, edits to the protected workbench, discarded failures, new damping or force fitting. All numerical jobs have finished; integrity sealing is the final administrative step.

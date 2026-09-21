# Live canonical exponential step: exact split, short nonlinear qualification

Private continuation of `DERIVATION-20260919-joint-source-refinement-and-inertial-force-scale.md`. This changes the numerical integrator, not the annular action, matter coupling, canonical momenta, initial preparation, Gram term or physical force definition. It does not establish the full GR limit.

Headline: the live short evolution now has independent numerical controls, and the exact indexed implementation is about7.55–9.80times faster on the tested RHS evaluations. Source-cell refinement reduces the reference force discrepancy by78%, but does not materially reduce the MTS discrepancy. The evaluated Schur split shows that the explicit source-inertia correction is only2.56% of the latter's remaining discrepancy; the next target is the bulk/Gram-dependent drive, with all terms retained. All these results concern4e-5, not the earlier full.004 interval.

## 1. Exact nonlinear equation, not a frozen-geometry replacement

Let z=(u,b,p,p_b) collect the existing canonical state at all fifteen material labels. The original live solver defines z'=F(z): at every evaluation it inverts the canonical momenta and solves the radial metric constraints, then evaluates all scalar and source covectors. The baseline and MTS branches use the same procedure; the latter retains its full finite Gram term.

At the initial state, freeze a scalar mass/stiffness pencil separately at each material label:

    K V = M V Omega^2,    V^T M V = identity.

All554 scalar modes per label are retained. Negative or zero scalar eigenvalues cause an explicit failure; they are not clipped. The source block is intentionally zero in the frozen operator, not in the live equation.

For increments relative to the unchanged initial canonical state z0, first use canonical modal coordinates q=V^T M delta-u and pi=V^T delta-p. For numerically balanced rotation coordinates set x=Omega q and y=pi. This last scaling is invertible but is NOT called a canonical transformation. Source increments delta-b and delta-p_b are left unchanged. Write the complete linear transformation as T and w=T(z-z0).

    A(x,y)=(Omega y,-Omega x),    A(source increments)=0,
    R(w)=T F(z0+T^-1 w)-A w,
    w'=A w+R(w),    w(0)=0.

This is an exact change of variables for the finite-dimensional live equation. Even eigensolver error only changes the chosen splitting if the same invertible numerical transform and operator are used in both terms; it is not permission to drop R. In floating point, round-trip and independent physical-pencil tests quantify the remaining implementation errors. Source motion, moving mesh, metric response, kinetic cross terms and Gram force are all in the retained live evaluation. No metric or source velocity is held fixed there.

Using increments avoids repeatedly rotating a large background state and subtracting it to recover a tiny change. This is arithmetic preparation, not a change to initial data.

## 2. Rotation and entire phi-function

For each scalar pair let theta=h*omega and J(x,y)=(y,-x). Then:

    exp(h A)=cos(theta) identity + sin(theta) J,
    phi1(h A)=sinc(theta) identity + (1-cos(theta))/theta J,
    phi1(z)=(exp(z)-1)/z.

Here sinc(theta)=sin(theta)/theta. The off-diagonal coefficient is evaluated as theta*sinc(theta/2)^2/2 to avoid small-angle cancellation. At zero frequency the exponential and phi1 are both identity, so the source block receives its full nonlinear update. The implementation's numpy sinc convention includes the required factors of pi.

The rotation preserves the frozen scalar energy norm. This fact does NOT assert conservation of the live coupled energy by the nonlinear numerical method.

## 3. Explicit exponential midpoint

    a=exp(h A/2) w + (h/2) phi1(h A/2) R(w),
    w_new=exp(h A) w + h phi1(h A) R(a).

Both nonlinear evaluations rebuild the live constrained geometry. The identical initial R(0) can be reused across time-refinement runs. Subsequent stages never replace it with that initial value.

For a fixed spatial discretization and sufficiently smooth R, let F_tilde(w)=A w+R(w). The stage is w+h F_tilde/2+O(h^2). Expanding the update gives

    w_new=w+h F_tilde+(h^2/2)(A+R')F_tilde+O(h^3),

which matches the exact solution through second order. For constant R the step is exact; for R=0 all scalar modes propagate exactly. For A=0 it is ordinary explicit midpoint, so the complete method is not advertised as unconditionally stable or symplectic. This is a classical fixed-system consistency statement, not a mesh-uniform stiff-order theorem.

Methodological source: Hochbruck and Ostermann, *Explicit exponential Runge-Kutta methods for semilinear parabolic problems*, SIAM J. Numer. Anal.43 (2005), DOI10.1137/040611434, https://epubs.siam.org/doi/10.1137/040611434 ; author-hosted manuscript https://na.math.kit.edu/download/papers/rkexp.pdf (accessed2026-09-18). The paper establishes the exponential-RK framework and distinguishes classical from stiff order. Its parabolic assumptions are NOT imported as a theorem for this oscillatory constrained system. The initial attempt to fetch https://na.math.kit.edu/download/papers/acta-final.pdf timed out; no result is attributed to that unavailable fetch.

## 4. What can still restrict the step

The frozen rotation has operator norm1, and phi1 is its time average, also of norm at most1. If the exact remainder is L-Lipschitz on the domain containing the true/numerical states and stages, comparing two numerical steps gives

    ||delta w_new|| <= (1+h L+h^2 L^2/2) ||delta w||.

Thus the explicit restriction moves to the remainder; it does not disappear. Large changing metric coefficients, moving-source transport, or source/field coupling can still make L large. No numerical value for a rigorous L has yet been established.

For any differentiable reconstructed trajectory w_hat, define the continuous defect d=w_hat'-A w_hat-R(w_hat). Variation of constants and Gronwall imply, conditionally on the same Lipschitz domain,

    ||w_hat(t)-w(t)|| <= exp(L t) [||w_hat(0)-w(0)|| + integral_0^t exp(-L s)||d(s)|| ds].

If the physical reduced-force functional has a known Lipschitz bound C_force in this norm, its state-induced error is bounded by C_force times this bound, plus independent force-readout error. Neither L, C_force nor a continuous defect enclosure is supplied by a few endpoint differences. This explains why time refinement must check the actual reduced source force as well as a state norm; a good field norm alone cannot certify force convergence.

## 5. Predeclared live pilot

Both branches: base257, source-cap4e-5,554 scalar nodes,15 material labels, unchanged analytic preparation, duration4e-5 in the existing normalized units. This is one percent of the earlier .004 interval. Use4,8,16 equal steps, saving every accepted endpoint. Compare the last two endpoint force values against a2e-9 temporal diagnostic budget and the frozen scalar energy-norm difference against1e-6. These are short pilot diagnostics, not a replacement for the existing absolute2e-7 AND peak-relative0.5% continuum-force gates.

At every final state, recompute the original reduced wave force via the live canonical tangent, not the raw source covector. Check canonical inversion, radial constraints, timelike motion, positive material Jacobian, scalar/source Euler residuals and the moving-current Noether identity. These instantaneous identities do not by themselves prove an accurate trajectory.

Implementation sources: `scripts/annular_P2_live_exponential_20260919.py`, `scripts/verify_annular_P2_live_exponential_20260919.py`, `scripts/verify_annular_P2_live_exponential_v2_20260919.py`, `scripts/run_annular_P2_live_exponential_20260919.py`.

## 6. Results and limits

Both live pilots completed,22 implementation checks each. The manufactured solver control has18 passing checks, including a nonlinear, noncommuting source-coupled comparison against independent DOP853. Errors for10/20/40 steps are7.1158863983e-7,1.7870673378e-7,4.4778456408e-8. Ratios approximately3.98 and3.99 support the derived classical second order on that fixture only.

The first validator execution is retained as failed: binary64 scipy matrix exponentiation disagreed by3.2621e-11 at rotation angle100000, above the2e-11 gate. The corrected validator uses an independent60-digit augmented matrix exponential and retains the same thresholds; it passes without changing the rotation implementation. This repairs the validation reference, not the physical model.

No full continuum-force, unrestricted GR, PPN, observational or black-hole conclusion follows from this solver qualification. Old failed scientific gates remain failed until independently retested. Physical quantities here use the existing normalized annular test units, not newly inferred SI parameters or observational error bars.

### Live time refinement

| Branch |4-step endpoint force|8-step endpoint force|16-step endpoint force|8-to16 force change|
|---|---:|---:|---:|---:|
|reference|-5.1852601368e-8|-5.1803363719e-8|-5.1791149984e-8|1.2213734906e-11|
|MTS|-5.0981727821e-8|-4.1463287725e-8|-4.1366603630e-8|9.6684095192e-11|

The reference state-norm difference ratio is4.00284 and force-difference ratio4.03133, consistent with classical second order over these steps. MTS4-to8 force difference9.5184400963e-9 FAILS the declared2e-9 temporal budget and is retained as a failed coarse temporal diagnostic, despite all instantaneous constraints passing. MTS8-to16 passes that budget; its state-norm difference is4.6072729489e-11 relative to initial frozen field energy. Its successive ratios78.25/98.45 are NOT evidence of second-order asymptotics. The coarse MTS step spans almost one fastest frozen period (maximum angle6.18216); it must not be selected merely because its force looks closer to the continuum.

The exact live RHS is reconstructed at initial and perturbed states to relative errors of order1e-15. The MTS independent physical-pencil action error is3.3091e-13, and its canonical increment round trip2.9680e-15. Source flow is nonzero throughout. Endpoint canonical/radial and scalar/source Euler/current checks pass on all six runs. These are instantaneous consistency checks, not an integration error bound.

Wall time for all three refinements and diagnostics is3642.9seconds reference and3656.8seconds MTS, run concurrently on two single-core BelowNormal workers. Fine16-step evolution itself is1588.1/1550.1seconds. RHS counters in the pilot count the split's live evaluations, not extra direct-check or tangent/constraint diagnostic solves. No full .004 trajectory was launched.

### Independent continuum comparison at4e-5

The separately discretized continuum384/512 endpoints give forces-5.3732253913e-8/-5.3795549953e-8, differing6.3296040830e-11. Their waveform/source-position refinement checks also pass. Both finite branches use the same512 reference, original preparation and physical radii.

| Quantity at the16-step endpoint |reference|MTS|
|---|---:|---:|
|Waveform relative energy-norm error|0.000293374086|0.000293385500|
|Absolute reduced-force discrepancy|2.0043999692e-9|1.2428946324e-8|
|Error divided by prior full-window force peak|0.0371103%|0.230115%|
|Error divided by the force at THIS early time|3.72596%|23.1040%|
|Maximum source-position discrepancy|1.7764e-15|1.7764e-15|
|Maximum velocity discrepancy|1.7313e-12|1.1882e-11|
|Maximum clock-rate discrepancy|9.7766e-13|1.5392e-10|

The inherited absolute2e-7 AND0.5%-of-prior-peak force target is2.7005981227e-8; both endpoints pass it, together with the waveform, source and clock smoke targets and the empirical time diagnostic. This is not a full-interval force pass. The early force is small, so that inherited target is relatively permissive here: particularly, the23.1% instantaneous MTS discrepancy must not be hidden behind the peak-scaled pass. It also exceeds the8-to16 temporal change by roughly129times. This suggests that reducing this step alone will not remove the discrepancy, but is not a rigorous error decomposition or proof that the entire remainder is spatial error.

Source: `source-intake/navier-stokes/20260914/annular-P2-live-exponential-short-continuum-attempt01/status.json`. Independent comparator: `scripts/compare_annular_P2_live_exponential_short_20260919.py`.

### Direct physical-space algorithm control

Independent DOP853 controls at the first fine endpoint2.5e-6 are complete. They use the original physical canonical RHS with no modal split. The stronger control explicitly halves the maximum RK step as well as tightening tolerance: merely changing tolerances can leave an already accepted RK step unchanged, so a zero difference in such a case is not meaningful time-refinement evidence. The first reference tolerance-only run is retained and reused rather than erased or repeated from scratch.

|First fine endpoint control|reference|MTS|
|---|---:|---:|
|RK step-refinement relative field change|6.4266e-15|1.0229e-14|
|RK step-refinement force change|8.5609e-16|7.0633e-14|
|Exponential versus refined RK relative field change|5.5499e-13|4.2917e-11|
|Exponential versus refined RK force change|6.6567e-14|3.8328e-10|

Both pass the predeclared independent short-control budget. This first-step agreement is not presented as an independent integration over the entire4e-5 pilot; the stronger test below supplies that separately.

Sources: `scripts/verify_annular_P2_live_exponential_direct_20260919.py` and `scripts/verify_annular_P2_live_exponential_direct_v2_20260919.py`.

## 7. Next mathematical/numerical target

After the direct algorithm control, compare spatial/source-cell refinement at this fixed evolved endpoint with the same time controls and both branches. Use the existing conforming force-lift/Schur decomposition to distinguish finite source projection, bulk discretization, Gram contribution and time error. Then extend the evolved interval in measured stages. Do not silently replace the reduced source force by pressure or alter the initial preparation. The new solver makes those tests possible; it does not complete the unrestricted local-GR bridge.

No full-window speedup has been demonstrated: extrapolating the fine pilot alone would still imply tens of hours, and is not a justified runtime prediction. Do not launch that extrapolated job. Read-only inspection identifies a concrete exact-algebra optimization to test first: `scripts/annular_live_P2_canonical_v2_20260918.py` currently forms all N nodal values at every quadrature sample in P2Material.samples and P2Density.update, then selects just the three local P2 nodes. With label interpolation W and local indices j(q,a), the required contraction is only

    local_value(q,a)=sum_label W(q,label)*u(label,j(q,a)),    a=0,1,2.

This avoids the Q-by-N dense temporary without deleting any physical mode or changing quadrature. The same indexed contraction applies to momenta-inverted rates; the source component is evaluated separately. This optimization is now implemented and qualified at the saved states, as detailed below. Its observed stage speedup is not a guarantee about an entire future simulation. Preserve the current executed sources and evidence.

## 8. Exact indexed evaluation and batched material cuts

`scripts/annular_P2_indexed_live_geometry_20260919.py` implements that contraction and batches the material-cut construction. The original density construction independently finds the intersecting reference edges for every physical quadrature radius, inverts their material labels and sorts the cuts between-0.5 and+0.5. The new version collects the SAME strict edge intersections in bounded2048-row blocks, evaluates the same eight inverse-node iterations on the flattened list, and sorts the cuts per radius. Duplicate cuts yield zero-width pairs, which are discarded; adjacent distinct pairs below the original1e-13 width threshold are discarded exactly as before. NaNs only pad the rectangular cut-workspace and are excluded before any quadrature point is emitted. The Legendre nodes, weights, material weight, ordering of physical quadrature points and full Gram/source contributions are retained.

The identity is distributivity and pointwise batching, not a coarser integral or dropped field sector. Floating-point association can change. Therefore `scripts/verify_annular_P2_indexed_live_geometry_20260919.py` compares original and optimized label quadrature, all density terms, live canonical rates/covectors, geometry, radial constraints, reduced source force and current identities on saved initial and evolved257 states in BOTH branches, plus arbitrary real/complex indexed-contraction fixtures.

All36 checks pass. Observed whole-RHS timings in seconds, with another single-core worker active:

|State|Original|Indexed|Observed speed ratio|
|---|---:|---:|---:|
|reference initial|46.1012|4.70188|9.80|
|reference evolved|46.1196|4.77242|9.66|
|MTS initial|46.0674|6.09913|7.55|
|MTS evolved|45.9307|5.59360|8.21|

Largest rate change2.1684e-19; largest covector change1.1103e-16. The true evolved reduced-force change is2.3202e-17 in reference and0 at reported precision in MTS. These are numerical saved-state checks, not a statement of bitwise equality for every future state. The avoided dense-sample allocation and indexed-gather sizes are recorded analytically in the evidence; no process-wide peak-memory improvement is claimed from those formulas.

Evidence: `source-intake/navier-stokes/20260914/annular-P2-indexed-live-geometry-attempt01/status.json`. No earlier executed implementation or sealed trajectory was overwritten. The fast implementation is opt-in through the new system class; inherited initial preparation remains unchanged.

### Stronger whole-pilot independent control

`scripts/verify_annular_P2_indexed_full_pilot_20260919.py` uses the qualified indexed physical RHS, WITHOUT the modal split, for an independent integration over all4e-5. Each branch uses DOP853 first with maximum step5e-6, then2.5e-6 and tighter tolerances, retaining17 times matched to the exponential trajectory. It also compares the true endpoint reduced forces, not raw covectors. Both runs completed. Reference passes: RK force change1.6697e-16 and exponential-versus-RK force change4.0661e-12. MTS's exponential-versus-tight-RK difference is2.6557e-11, but its coarse-to-tight RK force difference4.0054770405e-10 FAILS the stricter2e-10 independent-control budget. The corresponding scientific flag remains FALSE; instantaneous constraints and code checks passing do not erase that miss.

The additional MTS control in `scripts/refine_annular_P2_indexed_MTS_RK_20260919.py` reduces the step to1.25e-6 and tightens tolerances. It completed385 physical RHS evaluations in1832seconds. The further RK endpoint force change is1.1540502711e-12, below the unchanged2e-10 control budget; the exponential-versus-further-RK force change is2.7710728894e-11, below2e-9. Corresponding endpoint relative field changes are1.1819583011e-13 and1.3011255593e-11. Canonical, radial, current and Euler checks pass. The refined independent-control flag is TRUE; the earlier failed coarse flag remains FALSE in its original evidence. The further-refined force is-4.1338892901e-8.

The further force check is at the endpoint only; the previous17 matched-time field/source comparisons are retained rather than mislabelled as newly refined at every time. No acceptance threshold is relaxed. The original miss was a numerical precision issue, not an inference that MTS is physically ruled out. These checks do not retest the old .004 window, supply spatial convergence, or bound force error at every time. Source: `source-intake/navier-stokes/20260914/annular-P2-indexed-full-pilot-control-MTS-attempt02/status.json`.

## 9. First evolved source-cell refinement

After the reference whole-pilot control passed, `scripts/run_annular_P2_evolved_source_halving_20260919.py` evolves the saved source-cap2e-5 initial state with16 and32 exponential steps, preserving the bulk257 mesh and all original preparation. It also checks original versus indexed RHS on this finer grid. Both time controls, constraints, current identities and scoped endpoint gates pass; no force is corrected or replaced.

Reference results at4e-5:

- Cap4e-5 independently integrated RK force:-5.1787083928e-8; error against continuum:2.0084660258e-9.
- Cap2e-5,32-step force:-5.3351803930e-8; error:4.4374602378e-10, or0.825% of the instantaneous continuum force.
- Error ratio finer/coarser:0.22094, approximately78% smaller. The16-to32-step force change is6.7577e-12, so the observed improvement is much larger than that temporal diagnostic.
- Actual evolved Schur projection inertia drops from4.3669554584e-8 to2.1836092042e-8, consistent with the derived leading source-cell scale halving.
- Source-touching conforming-lift work drops from-3.2323571102e-9 to-2.6142982576e-11. Other bulk work remains: total lift work changes from-1.8530940422e-9 to+1.3531202758e-9, with a pressure-trace discrepancy of opposite sign on the finer grid. Hence the total error still includes cancellation; it is not a no-cancellation bound or proof of asymptotic order.
- The exact on-shell Schur-force identity closes below5.3e-16. The conforming-lift identity residual is2.7128e-11 on both grids, explicitly retained rather than advertised as exact to machine precision.

These are only two source-cell resolutions at fixed bulk resolution and a very short time. After its independent numerical precision prerequisite passed, MTS received the matched comparison through `scripts/run_annular_P2_evolved_source_halving_v2_20260919.py`, completing in542seconds under a900second runtime allowance. All modes, original preparation and physical force are retained.

|MTS quantity at4e-5|Cap4e-5 independent RK|Cap2e-5,32 exponential steps|
|---|---:|---:|
|Reduced force|-4.1338892901e-8|-4.1231634653e-8|
|Absolute continuum discrepancy|1.2456657053e-8|1.2563915300e-8|
|Source projection inertia Q|4.3669548175e-8|2.1836090654e-8|
|Pressure trace|-5.0000929451e-10|-2.6220339764e-10|
|Conforming bulk-lift work|-1.2718627938e-8|-1.1629600456e-8|
|Combined Gram work|-2.8147382975e-8|-2.9366958835e-8|
|Source-touching lift work|-1.4385159427e-8|-1.3296130418e-8|

MTS does NOT exhibit the reference branch's large force improvement. The discrepancy remains about23.35% of the instantaneous continuum force. The finer/coarser error ratio1.00861 alone is not evidence of deterioration: its absolute change1.0726e-10 is smaller than the finer-grid16-to32 temporal difference1.3506880000e-10. This temporal difference passes the predeclared2e-9 diagnostic but is not a rigorous error bound. The relative time-refinement field change is3.3111e-11. The waveform error remains0.000293385497; source/velocity/clock and instantaneous consistency checks pass. Schur identity residuals are below5.8e-16; lift identity residuals remain2.7128e-11. Both branches pass the inherited peak-scaled endpoint target, but that relatively permissive short-endpoint target is not enough to call either full-interval convergence or MTS superiority.

The halved Q confirms that the intended local source refinement happened. It did not remove the MTS residual, and its source-touching and Gram work remain appreciable. This directs the next test toward the resolved bulk/Gram dynamics and induced source trace, not repeated source-cell halving on its own. These data do not isolate a single term as the cause or justify deleting the Gram action.

Sources: `source-intake/navier-stokes/20260914/annular-P2-evolved-source-halving-reference-attempt01/status.json` and `source-intake/navier-stokes/20260914/annular-P2-evolved-source-halving-MTS-attempt02/status.json`.

## 10. Exact force-error split: what local projection can and cannot explain

Using the already derived on-shell force F=(I J-Q G)/(I+Q), with I>0 and Q>=0, define

    Pi=-Q(J+G)/(I+Q),    F=J+Pi.

For a continuum comparator F_star and measured numerical identity residual epsilon=F_measured-J-Pi,

    F_measured-F_star=(J-F_star)+Pi+epsilon,
    max(0,|J-F_star|-|Pi|-|epsilon|) <= |F_measured-F_star|
        <= |J-F_star|+|Pi|+|epsilon|.

This is an algebraic decomposition with triangle bounds, not a new force law. On the saved states, `scripts/derive_annular_P2_evolved_force_error_split_20260919.py` verifies the independently evaluated Schur force, signed decomposition and bounds; exact-rational fixtures and omitted-projection negative controls are included. All21 checks pass and the four rows are saved in `source-intake/navier-stokes/20260914/annular-P2-evolved-force-error-split-attempt01/saved-force-error-split.csv`. Source run hashes are reverified. The floating-point evaluations are not interval-certified inequalities for the unknown continuum solution; continuum discretization and time errors remain separate.

At the source-refined reference endpoint, J-F_star=1.2180e-10 and Pi=3.2194e-10. At the source-refined MTS endpoint, J-F_star=1.2241977645e-8 while Pi=3.2193743644e-10, only2.56% of its observed discrepancy. Its reverse-triangle lower value is1.1920039991e-8, conditional on these saved values. Thus the explicit source-inertia correction alone cannot account for most of this MTS discrepancy. Holding J,G,I fixed and setting Q to zero would still leave the1.2242e-8 drive gap. That counterfactual is NOT an actual evolved Q-to-zero limit: changing the discretization can change J,G,I and the whole trajectory.

This provides a concrete next target rather than another missing-input inventory: resolve the remaining drive J=f_b-r_b-a^T M^-1(f_u-r_u) under matched bulk-and-source refinement, retain its full Gram contribution, and use the force-lift ledger to determine which terms change. First qualify the finer-grid spectra/cost and time error with the indexed solver; then run paired short evolutions. Extend the interval only after this distinction is under control. Do not retune the physical force, choose the coarser MTS step because it agrees better, or treat this calculation as an empirical theory comparison.

## 11. Checkpoint scope

Completed: exact all-mode live split, classical second-order derivation, independent short physical-RHS controls for both branches, qualified exact-algebra performance improvement, paired evolved source-cell refinement, and an evaluated force-error decomposition. No owned job remains required for this checkpoint. The old.004 interval, joint spatial convergence, unrestricted GR limit and observational claims remain open. All work stays private in post-checkpoint-work; no GitHub action, subagent or protected-workbench edit is part of this stage.

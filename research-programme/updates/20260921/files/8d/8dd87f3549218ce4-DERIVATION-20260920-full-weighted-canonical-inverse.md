# Full weighted canonical inverse with candidate radial gravity

Private checkpoint, 20 September 2026. This extends `DERIVATION-20260920-candidate-canonical-momenta-and-live-response.md`. Source seal: `source-intake/navier-stokes/20260914/annular-candidate-canonical-response-final-integrity.json`.

## 1. What is being solved

At the coherent initial field/source coordinates q, solve simultaneously

\[
 p(q,v,y)=p_{\rm target},\qquad R(y,q,v)=0,\qquad y=(\mu,\log N).
\]

There are **16425 velocity and momentum components**: 1094 field variables and one source variable on each of 15 material interpolation nodes. The target is the preceding action-owned, material-weighted momentum vector. The original unweighted collocation momenta are not substituted.

The reference and both MTS Gram extensions are treated alike. Known initial velocities are used to manufacture perturbed starting guesses and assess recovery; they are not supplied to the inverse routine or used to construct its preconditioner. The preconditioner is assembled at the first perturbed trial and its newly solved metric.

The candidate's gravity action, normalized coupling, matter action and boundaries are unchanged. Coordinates are fixed throughout. This is not a trajectory or a derivation of the complete covariant parent action.

## 2. Full fixed-metric Hessian, without a dense full matrix

With the velocity sampling operator T from the preceding material-weighted action, the wave momentum and its fixed-metric derivative are

\[
 p_{\rm wave}=T^T W_k T v,\qquad H_{\rm wave}=T^T W_kT,
\]

where W_k contains positive radial/material quadrature weights and k=r^2/(N sqrt(F)). Each row of T samples the three local P2 field functions and the moving-source transport term, with all 15 material cardinal functions. For the proper-clock source term,

\[
 H_{\rm dust}=T_b^T W_bT_b,\qquad
 W_b={\rm radial\ weight}\,\sigma\,\frac{m_sN^2}{Fs^3}.
\]

The actual full preconditioner is H_0=H_wave+H_dust at the first perturbed iterate. Its matrix is stored sparsely. No directions are removed, replaced by four probes, or assigned a fitted inertia.

Reorder variables by field node, then material index, putting the 15 source variables last:

\[
 H_0=\begin{pmatrix} A&B\\B^T&D\end{pmatrix}.
\]

P2 functions overlap only within an element, whose free field indices differ by at most two. Dense coupling among the 15 material coefficients therefore gives the 16410-dimensional field block a half-bandwidth of 2(15)+14=44. The source block is only 15 by 15. The source coupling is not assumed spatially local.

After diagonal scaling, factor the banded field block and form

\[
 S=D-B^TA^{-1}B.
\]

The full solve is

\[
 x_b=S^{-1}(r_b-B^TA^{-1}r_f),\qquad
 x_f=A^{-1}(r_f-Bx_b).
\]

Positive field Cholesky pivots and source-Schur eigenvalues are checked. A tiny floating-point assembly asymmetry is measured before symmetric averaging for this preconditioner only; the momentum map, action, target and radial equations are not modified by that averaging. One-norm condition estimates are reported as estimates, not rigorous upper bounds.

This establishes a usable fixed-metric preconditioner on the tested numerical states. It does not establish positivity of the entire metric-eliminated inertia.

## 3. The nonlinear inverse includes live gravity

For each trial velocity the implementation:

1. Recomputes the full averaged physical temporal-square density and source velocities.
2. Solves the candidate's nonlinear radial mass/lapse equations, including the fixed inner mass and outer N/sqrt(F)=1 condition.
3. Recomputes all material-weighted canonical momenta at that solved geometry.
4. Applies H_0^{-1} to the entire momentum residual and takes a damped correction.

In symbols,

\[
 y_k=y(q,v_k),\qquad
 v_{k+1}=v_k-\eta_kH_0^{-1}[p(q,v_k,y_k)-p_{\rm target}].
\]

This is a preconditioned nonlinear iteration, not an assertion that the fixed-metric Hessian equals the live Jacobian. The latter contains the previously derived p_y y_v response. Gravity is re-solved at every proposed step; a line search rejects non-timelike trials or a nondecreasing scaled residual.

Both stopping gates must hold: relative diagonally scaled full-momentum residual below 2e-11 and largest preconditioned component correction below 2e-10. The final radial residual must be below 2e-12. For manufactured roundtrips the independently known maximum velocity error must also be below 2e-9. A small unweighted residual alone is not sufficient.

## 4. Controls that distinguish a real solve from replaying known data

- Every one of the 16425 initial velocity components is perturbed. Two independent broad starting perturbations target the same saved momentum vector.
- The inverse routine receives only the target, trial velocities, momentum map and preconditioner; it does not receive the known answer.
- Independent complex differentiation at the perturbed fixed metric tests the full assembled Hessian on a dense all-component direction.
- Three dense all-component manufactured linear systems test the full block-banded/Schur inverse against its assembled matrix.
- At the finer radial/material quadrature, a further target is shifted by H_0 delta v using a separately specified broad perturbation. Its solution is not known in advance; all momentum and radial equations must still be satisfied, and the resulting velocity must differ nontrivially from the original.
- The two numerical quadrature settings are (radial degree, material order)=(18,20) and (22,28). Roundtrip targets at each setting come from their own preceding quadrature. Agreement of recovered velocities therefore tests numerical roundtrip consistency, not independent physical convergence with a fixed external target.

## 5. Numerical results

`source-intake/navier-stokes/20260914/annular-candidate-full-canonical-inverse-attempt01/status.json` records **107 passed implementation/control checks and 15 completed nonlinear solves**. The worker finished in approximately 3791 seconds (63.2 minutes), on one core. No execution failed, no mode was deleted, and no numerical gate was relaxed.

The 15 solves comprise twelve known-state roundtrips (two starts for each of three branches at each of two quadratures) and three new momentum targets at the finer quadrature. Every case required four accepted corrections, with five residual evaluations including the initial state. There were no rejected line-search trials. Full iteration histories are retained: 75 rows.

| Quantity across the completed tests | Measured maximum or range |
|---|---:|
| Maximum velocity error over every component of the twelve roundtrips | 5.78e-13 |
| Final diagonally scaled relative full-momentum residual | 4.44e-12 |
| Largest final preconditioned component correction | 5.77e-13 |
| Final radial integral residual | 5.60e-17 |
| Manufactured full linear-system recovery error, relative | 9.41e-14 |
| Full linear-system equation residual, relative | 4.22e-16 |
| Independent complex fixed-metric Jacobian discrepancy, relative | 3.95e-15 |
| Difference between coarse/fine roundtrip velocities | 5.04e-16 |
| Raw fixed-metric matrix one-norm condition estimate | approximately 1.67e7 |
| Diagonally scaled fixed-metric matrix condition estimate | approximately 3.83e3 |

The field block has 16410 components and half-bandwidth 44; its smallest scaled Cholesky pivot is approximately 0.35672818. The 15-dimensional source Schur matrix has smallest scaled eigenvalue approximately 0.08059330. All six complete preconditioners retain every component. Measured preconditioner assembly asymmetry is below 8.48e-17 relative before symmetric averaging. The conditioning is nontrivial, but the full linear controls and nonlinear recovery tests pass without truncation or regularizing away weak directions.

The three changed targets produce new solved velocities, differing from the original by approximately 0.000411940614 in the largest component. Their full momentum and gravity residuals also pass. The targets were specified through a preconditioner-weighted perturbation, not generated by feeding a known answer through the nonlinear map. These are additional self-consistent initial-data solutions at the same coordinates, not new time-evolved states or observations.

Across all final solutions, sampled F stays above 0.73025048 and the sampled source speed ratio |V|/(N sqrt(F)) stays below 0.03963586. These are numerical chart checks, not interval-certified continuum bounds. Both MTS extensions agree on this tested initial configuration; that does not establish equivalence on general fields or remove the earlier evolved-force discrepancies.

**Closed here:** a full-component, material-weighted numerical canonical inverse in the tested fixed-coordinate initial neighborhood, with live radial geometry at every trial. **Not closed:** a global inverse theorem, positivity of every mode of the metric-eliminated inertia, matching force/current evolution, physical spatial convergence, or full GR. All evidence rows remain valid_for_claim=false. The inherited 55 failed executions are preserved; there is no new failed attempt.

## 6. Resource and evidence discipline

One actual single-core BelowNormal worker is used. Fixed-coordinate quadrature caching is capped at 512 MiB of counted sample arrays; uncached samples are rebuilt in a streaming tail. This cache cap is not a cap on the entire process: sparse matrices, factors and transient working arrays require additional memory.

Executed scripts, target files and earlier reports are not edited. Iteration histories, trial rejection records, sparse matrices, factors, seeds, recovered states and residuals are retained. No GitHub action, subagents, sibling-workbench change, or long evolution is part of the stage.

Implementation: `scripts/annular_candidate_full_inverse_20260920.py` and `scripts/derive_annular_candidate_full_inverse_20260920.py`.

## 7. What follows if the numerical inverse qualifies

The next dynamical ingredient is the **matching material-weighted coordinate covector**, p_dot=partial L/partial q at fixed metric, justified by the stationary gravity+boundary action. It must include moving-coordinate transport, candidate Gram terms, proper-clock source terms, and metric gradients at moving sampling points. Existing frozen-background force formulas are useful inputs, not permission to bypass this full action derivative.

Derive and independently check those force components, then combine them with this inverse for a very short canonical evolution. Re-solve gravity at every evaluation; test reference and both candidates with equal time-step controls. Temporal-current/general-shift consistency and spatial convergence remain separate obligations.

A successful fixed-coordinate inverse is an advance toward that evolution, not a proof of global existence/uniqueness, all-mode reduced-inertia positivity, full GR, or repair of the old physical-force discrepancies. All physical claim flags remain false.

### Explicit next force identities, not yet numerically qualified

At one material label use reference coordinate xi, field Q(xi), nodal-rate interpolant nu(xi), source velocity V, and the existing source-fitted map r=R(xi;b,z). Write J=R_xi, d=R_b, with d independent of b in this affine source map, and define

\[
 k=\frac{r^2}{N\sqrt F},\quad C=r^2N\sqrt F,\quad
 K=Jk,\quad G=C/J,\quad m=-dQ_\xi/J,\quad W=\nu+Vm.
\]

The wave Lagrangian per label is integral(K W^2/2-G Q_xi^2/2) dxi minus sum_i G_i a_i, with a_i=1/2 sum_f P_fi(HQ)_f^2. H and P are fixed reference-space operators for the stated candidate. Holding the continuous metric profile fixed while varying b gives

\[
 K_b=d_\xi k+Jk_r d,\qquad
 G_b=C_r d/J-Cd_\xi/J^2,\qquad
 m_b=-m d_\xi/J,
\]

where k_r=k(2/r-ell_r-F_r/(2F)) and C_r=C(2/r+ell_r+F_r/(2F)). Direct differentiation therefore supplies

\[
 (L_{\rm wave})_b=\int d\xi\left(\tfrac12K_bW^2+KWV m_b
                    -\tfrac12G_bQ_\xi^2\right)-\sum_i(G_b)_i a_i,
\]

and the proper-clock contribution at r=b is

\[
 (L_{\rm dust})_b=-\frac{m_s}{s}\left(NN_r+\frac{V^2F_r}{2F^2}\right).
\]

For a field basis phi_j, at fixed nodal rates and source variables,

\[
 (L_{\rm wave})_{q_j}=
 -\int d\xi\left(KWV\frac dJ+GQ_\xi\right)(\phi_j)_\xi
 -\left[H^T\operatorname{diag}(P G)Hq\right]_j.
\]

Here P G denotes the sampler applied to nodal G_i, not a new coupling. To obtain the material-nodal covectors, integrate each per-label covector against w(z)L_a(z), exactly as for the new momenta. The radial metric is stationary for the retained action, so its implicit variation cancels in this first derivative only under the same boundary/envelope conditions already tested. These formulas follow by differentiation of the stated pulled-back candidate action; they have **not** been implemented or independently checked against the full candidate coordinate variation in this checkpoint. That independent test, rather than copying a frozen force or introducing a fitted term, is the next task.

The force implementation must preserve the preceding cancellation-safe preparation of Hq from exact-source embeddings and high-precision local derivative atoms. Reapplying a large Gram stencil to prematurely rounded common nodal coordinates is not an equivalent numerical route. The good velocity-inverse residuals do not certify the accuracy of that higher-derivative force calculation; its arithmetic and quadrature checks must be performed separately.

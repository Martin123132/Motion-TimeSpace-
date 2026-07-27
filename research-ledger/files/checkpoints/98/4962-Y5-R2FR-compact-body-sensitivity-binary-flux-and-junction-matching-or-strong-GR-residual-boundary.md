# 4962 - Compact-body sensitivity, binary flux and junction matching

Date: 2026-07-13.

Marker: MTS_4962_COMPACT_BODY_SENSITIVITY_FLUX_JUNCTION.

Status: private analytic and source-executed checkpoint. The selected
integrated-H, exact-Diff, metric-only and reflection-even branch now has a
compact-body theorem at leading two-derivative point-particle order. The first
motion-scalar sensitivity and scalar charge vanish, no independent vector
charge exists, stellar junctions close, and conservative binding and tensor
radiation use the same M_R residue. Three hash-locked realistic EOS families
exclude a perturbative scalar zero mode throughout nine stable models by more
than seventeen orders in the sufficient density margin.

This is a material extension of the 4960 weak-local theorem. It is not an
all-operator compact-GR or full-MTS claim. The parity-even Weyl-cubic
coefficient, finite higher-curvature matching, CFF coefficient and
disconnected nonlinear scalar branches remain explicit strong-field
residuals.

## 1. Exact branch being tested

The retained parent contains one public Lorentzian metric, exact Diff/BRST,
ordinary visible matter and a reflection-even motion scalar. At the local
two-derivative order,

    S_2 = integral sqrt(-g) [
            M_R^2 (R-2 Lambda)/2
            - Z (nabla psi)^2/2
            - m_gap^2 psi^2/2
          ] + S_SM[g,Phi,A].

The visible matter action contains no direct psi argument at fixed metric.
The effective action obeys

    Gamma[g,Phi,A,psi] = Gamma[g,Phi,A,-psi].

Checkpoint 4943 independently establishes the homogeneous interior scalar
equation, regular field and flux junctions, and zero asymptotic scalar flux.
Checkpoint 4960 establishes that the leading metric source residue is one
rank-one universal direction. Checkpoint 4961 declares H and Diff as parent
data rather than pretending that the current scalar creates them.

## 2. Compact-body first-sensitivity theorem

Let

    x_inf = psi_inf/M_R

and let m_A(x_inf) be the ADM mass of a stationary compact solution with fixed
baryon number, entropy and conserved visible charges. Assume the solution is
on a unique regular branch continuously connected to psi=0. Reflection maps
the solution at x_inf to one at -x_inf without changing the metric ADM charge.
Therefore

    m_A(-x_inf) = m_A(x_inf).

Its regular local expansion contains only even powers,

    m_A(x_inf)
      = m_A(0) + m_A,2 x_inf^2/2 + m_A,4 x_inf^4/24 + ...

and hence

    alpha_A
      := d ln m_A/dx_inf evaluated at zero
      = 0,

    Q_A
      := -d m_A/dpsi_inf evaluated at zero
      = 0.

This is not a weak-compactness expansion. It follows from the exact branch
symmetry and regularity. It agrees independently with the 4943 Gauss-flux
result

    Q_A = surface integral n_mu K_eff^munu nabla_nu psi = 0.

For two bodies A and B on the same branch, the leading scalar dipole factor is

    (alpha_A-alpha_B)^2 = 0.

The second sensitivity

    beta_A = d alpha_A/dx_inf evaluated at zero

need not vanish. It can govern scalar-pair effects or a bifurcation if the
quadratic operator develops a zero mode. It is retained rather than silently
set to zero.

## 3. No perturbative scalarization zero mode

On a static compact background, let u be a linear scalar perturbation with
zero asymptotic boundary value. The 4943 quadratic packet gives a spatial
operator whose integrated zero-mode equation is

    integral_Sigma N sqrt(gamma) [
      B_eff^ij D_i u D_j u + m_eff^2 u^2
    ] = boundary terms.

The regular stellar interface contributes no boundary term because

    [u] = 0,
    [n_i B_eff^ij D_j u] = 0.

The asymptotic term vanishes. If B_eff is positive and m_eff^2 is
nonnegative, the integrand is nonnegative and the only decaying solution is
u=0. In the massless case, the asymptotic value removes the constant mode.
Thus no perturbative branch bifurcation is available while the quadratic
form stays positive.

The 4883 BSK24, SLY4 and DD2 models were re-read from their locked LALSuite
tables. Their largest central density is

    rho_c,max = 2.2800188119234442e18 kg m^-3.

The conservative 4943 sufficient instability threshold is

    rho_critical = 4.246023114199768e35 kg m^-3.

Therefore

    max rho_c/rho_critical = 5.3697748471940454e-18,

or 17.2700 orders below the threshold. All nine stable EOS rows pass. The
largest inherited fixed-mass tidal contact cap remains

    3.0387186566321415e-17.

This excludes a perturbative zero mode in the tested strict-EFT corridor. It
does not prove that a disconnected, large-amplitude solution cannot exist
for a nonconvex completion outside that corridor.

## 4. Vector sensitivity

The selected lead branch contains no independent public vector or aether
field and no vector pole. A compact-body vector sensitivity is therefore
absent by field content, rather than fitted small.

The old 4864-4871 unit-flow sensitivity calculation remains a valid
correspondence-extension result. It is not imported into this metric-only
theorem and cannot be used to weaken or strengthen the selected branch.

## 5. Metric, scalar and electromagnetic junctions

After integrating out the regular internal body fields, Diff invariance gives
the worldline EFT

    S_A = -m_A integral ds
          + lambda_A/2 integral E_mn E^mn ds
          + dissipative and higher-multipole operators.

The first term is universal metric coupling. The finite-size coefficients
carry ordinary EOS dependence and higher-curvature corrections; they are not
new long-range charges.

At Einstein-Hilbert order the metric junction is

    [K_ab] - h_ab [K] = -S_ab/M_R^2.

For an ordinary stellar surface with no distributional surface stress,

    [h_ab] = 0,
    [K_ab] = 0.

The interior and exterior therefore use one ADM mass and one M_R residue.
The scalar junctions are

    [psi] = 0,
    [n_mu K_eff^munu nabla_nu psi] = 0.

For the Maxwell-CFF action define

    D^munu = F^munu - 4 c_IR C^munurhosigma F_rhosigma.

Then, in the absence of magnetic surface charge,

    [n_mu D^munu] = j_Sigma^nu,
    [n_mu dualF^munu] = 0.

The same c_IR occurs in propagation, junction response and Hilbert stress.
There is no independent compact-body electromagnetic gravity coefficient.

The R2 and C2 terms are treated on the analytic strict-EFT branch. Order
reduction and the local metric map retain the GR-connected solution and
exclude independent heavy/runaway junction data. This statement is
conditional on perturbative Wilson coefficients and is not a
nonperturbative quadratic-gravity theorem.

## 6. Conservative and radiative residue equality

The conservative massless-pole exchange scales as

    C_cons = 1/M_R^2 = 8 pi G_N.

The far-zone tensor amplitude carries

    h_TT proportional to Q_double_dot/(M_R^2 R),

while the wave stress carries M_R^2. Consequently

    C_rad = M_R^2 (1/M_R^2)^2 = 1/M_R^2 = C_cons.

If the graviton coordinate is rescaled by any nonzero a, the kinetic residue
becomes M_R^2/a^2 and the source vertex becomes 1/a. Their radiative product
is still

    (M_R^2/a^2) (a/M_R^2)^2 = 1/M_R^2.

No separate radiation value of G can be inserted. On the two-derivative
branch, on-shell stress conservation removes mass monopole and dipole tensor
radiation, leaving

    P_T = G_N/(5 c^5)
          average[Q_triple_dot,ij Q_triple_dot,ij].

The scalar dipole is zero and no vector channel exists. Thus conservative
binding, wave generation and wave energy flux all inherit the same one-time
Newton calibration.

## 7. What is promoted

Inside the declared stable selected parent:

    leading two-derivative compact point-particle GR = established;
    first compact scalar sensitivity                = zero;
    ordinary compact scalar charge                  = zero;
    leading scalar dipole flux                       = zero;
    compact vector sensitivity                       = absent;
    metric and scalar junction matching              = derived;
    conservative and tensor-radiative G_N            = identical;
    realistic-EOS perturbative zero mode              = excluded.

This is stronger than the 4960 test-body result. It reaches self-gravitating
objects at the leading point-particle and tensor-radiation order without
borrowing the old aether response or adding a compact-body coupling.

## 8. Finite strong-field residual boundary

The all-operator compact claim remains false for specific, finite reasons.

1. The parity-even C3 coefficient is observationally bounded by the 4923
   GW250114 recast, but its robust horizon-control proxy is about 0.040 and
   does not satisfy the declared one-percent compact gate.
2. The conditional 4929 fixed-point trajectory gives an extraordinarily
   small ell_plus near 1.8e-36 m, but the full interacting parent flow and
   transition-scale ownership remain incomplete. That number is not promoted
   as a full-parent prediction.
3. The R2 and C2 realistic-EOS contact response is tiny under inherited
   strict-EFT caps, but the finite Wilson coefficients are not yet
   parent-predicted or measured.
4. The physical CFF coefficient still requires threshold matching or one
   source-backed calibration.
5. The perturbative scalar zero mode is excluded, but a disconnected
   nonperturbative reflection-breaking branch has not been globally ruled
   out.
6. The theorem applies to the selected Lorentz-invariant reflection-even
   state, not every cosmological or coherent-flow MTS state.
7. Integrated H, Diff, visible ontology and the numerical value of G remain
   explicit parent or one-time calibrated content as decided at 4961.

## 9. Decision

    selected two-derivative compact point-particle GR  = true conditionally;
    zero leading scalar dipole on selected branch      = true;
    same conservative and radiative G_N                = true;
    realistic-EOS perturbative scalar stability        = true;
    all-operator compact GR                             = false;
    pure motion-scalar origin of gravity                = false;
    full MTS                                            = false.

The project has therefore crossed a genuine boundary: compact-body
sensitivity and binary radiation no longer form an unanalysed gap. The
remaining compact problem is higher-operator and global-branch control, not a
missing leading source coupling.

## 10. Artifacts

- post-checkpoint-work/scripts/Y5_R2FR_4962_compact_body_sensitivity_binary_flux_and_junction.py
- post-checkpoint-work/source-intake/functional_rg/4962/compact_body_matching_results.json
- post-checkpoint-work/source-intake/functional_rg/4962/compact_body_sensitivity_and_no_dipole.csv
- post-checkpoint-work/source-intake/functional_rg/4962/junction_and_worldline_matching.csv
- post-checkpoint-work/source-intake/functional_rg/4962/conservative_radiative_residue_match.csv
- post-checkpoint-work/source-intake/functional_rg/4962/realistic_EOS_scalar_stability_transfer.csv
- post-checkpoint-work/source-intake/functional_rg/4962/strong_field_residual_boundary.csv
- post-checkpoint-work/source-intake/functional_rg/4962/compact_body_strong_GR_decision.csv
- post-checkpoint-work/source-intake/functional_rg/4962/PROVENANCE.md
- post-checkpoint-work/scripts/Y5_R2FR_4962_compact_body_sensitivity_binary_flux_and_junction_validation.py
- post-checkpoint-work/source-intake/mts_residuals/P8_Y5_BRR545_4962_VALIDATION.csv

## 11. Next target

4963-Y5-R2FR-strong-field-C3-Wilson-selection-and-global-scalar-branch-exclusion-or-compact-GR-finite-residual.md

The next step should not reopen weak coupling or repeat sensitivity algebra.
It should attack the two residuals capable of changing the compact verdict:
select or source-bound the physical C3 Wilson coefficient, and derive a
global convexity/no-disconnected-branch theorem or execute a nonlinear
scalarized-star search. No GitHub action is authorized.

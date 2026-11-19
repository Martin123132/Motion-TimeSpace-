# Checked current, common-metric source and exchange

16 November 2026. A bounded bridge to existing source owners, not a replacement
action or a new cosmological fit. Preserve all saved fixtures and gates.

## 1. Existing results we reuse, rather than re-claim

4916 owns the common metric and the four-dimensional densitized-source map.
4904 already gives the opposite gauge/matter Lorentz forces on their equations.
MTS-ACTION-AND-SOURCE-PULLBACK.md and its METRIC-VARIATION.md explain the
Euler chain terms when source coordinates depend on the metric. Those scalar
results are already verified on saved histories; we do not rerun or present
them as new derivations.

The concrete new interface is between the just-checked action current and a
metric variation of that SAME regulated matter action. Its moving chiral
projector cannot be held fixed during metric variation.

The internal-gauge current j is not the cosmological momentum source Q_s.
A neutral field can have zero gauge current and nonzero density, momentum and
stress. The retained bath must not be erased from gravity because it is neutral.

## 2. Normalize the parent exchange equations explicitly

Use the Lorentzian owner convention

    delta S_m = integral sqrt(-g) [-T_m,munu delta g^munu/2
                   + j_a^mu delta A^a_mu + Euler terms].

A gauge-covariant diffeomorphism uses delta A_mu=xi^nu F_numu.
After integrations by parts and the local Lorentz identity for spinors,

    nabla_mu T_m^mu_nu = F^a_numu j_a^mu + E_cov,nu.

E_cov contains the full matter/Higgs Euler terms and any required integrated
spin terms; it is not set to zero on arbitrary test fields. On their equations
the Lorentz force remains. The gauge action gives
nabla T_gauge = F E_A. Its field equation E_A+j=0 supplies the opposite force.
Thus combined conservation follows from a shared action, not from assigning
an equal-and-opposite number by hand. Random off-shell gauge fixtures are
not solutions of E_A+j=0, and we do not claim force cancellation on them.

With E_g=2 delta S/(sqrt(-g) delta g_cov), integration of the metric Lie
variation gives ONE divergence of E_g with the corresponding Euler contacts.
The factor2 in 4904's schematic off-shell line cannot be reused literally
with this explicit normalization unless its right side is also rescaled.
We fix the normalization by the displayed variation, leaving old records
untouched. Its on-shell conservation statement is unaffected.

For a dimensionless link U=exp(a A_connection), the leading smooth-field
variation gives J_link=a^3 j_connection. Our y=6Y convention means
A_connection,Y=(g_Y/6) B_canonical; the color and weak factors similarly use
their already calibrated gauge couplings. Canonical source conversion follows
by that chain rule. No new MTS charge, gauge coupling or mass is fitted here.
The a=1 tiny fixtures do not establish a continuum limit.

## 3. Concrete constant-metric diagnostic, frozen before testing

The old regulator is flat. It has no unique metric extension supplied by the
fermion-measure theorem. We therefore declare a minimal CONSTANT-background
diagnostic family, not a parent-derived curved-lattice completion:

    G = inverse Euclidean metric, positive definite,
    e = positive symmetric square root of G,
    v = det(G)^(-1/2),
    K_mu=(T_mu-T_mu^dagger)/2, Delta_mu=T_mu-I,
    D_W(G)=sum_mu,a gamma_a e_a^mu K_mu
                   + sum_mu,nu G^munu Delta_mu^dagger Delta_nu/2.

It is gauge covariant and gamma5-Hermitian. At G=I it reduces exactly to the
retained Wilson operator. Keep its mass, lattice, boundary signs, couplings
and raw field probes unchanged. All scalar kinetic terms contract their
saved forward differences with the SAME G; all sectors carry the SAME v.
The independent barred Yukawa tensors use the completed Dirac-adjoint
convention with fixed frame spin matrices.

This family is a stated regulator choice. Higher-curvature operators,
nonconstant coframes/spin connections and other finite-cutoff counterterms
are not selected or bounded by this test.

## 4. Derive both metric and gauge responses from that action

For a symmetric inverse-metric direction B, the coframe response solves

    e delta e + delta e e = B,
    delta v = -v Tr(G^-1 B)/2.

The Wilson derivative follows by differentiating the displayed kinetic and
Wilson contractions. Carry it through the same Frechet derivative of
sign(H_W) used in the checked current.

Writing psi=P(G,U)eta with independent barred rows, the exact ambient-coordinate
chain is

    delta_g S|eta = delta_g S|psi + E_psi delta_g P eta.

The second term is computed and retained. This resembles the older scalar
source-pullback formula, but P is a NON-INVERTIBLE projector, not that older
invertible coordinate map. In particular E_psi P=0 does not imply
E_psi(delta P)eta=0. A separate witness checks this distinction. Do not claim
on-shell equality of these two responses merely by analogy with the scalar map.

Define an INTEGRATED Euclidean response tensor

    R_munu = partial S_E/partial G^munu,
    T_E,munu = -2 R_munu/v.

This is a declared variational convention, not a direct physical Lorentzian
energy reading. For Hcal=vG, the 4916 chain algebra applies:

    partial S_E/partial Hcal^munu
        = -[T_E,munu - Ginv_munu Tr(G T_E)/2]/2.

Test that chain with direct Hcal-path perturbations, not just the trace
identity fed back into itself. For each sector the volume, coframe, Wilson
and projector terms must all be included. The bath contribution is separately
checked against its explicit quadratic action.

The new mixed-source check is

    partial_B J_act(link,a)
        = partial_(link,a) [partial_B S_E].

The left side varies the independently computed link current with the metric;
the right side varies the analytic metric response with the link. Check both
finite-difference steps and both action totals. This is an integrability test
of the finite diagnostic action, not a proof of local diffeomorphism symmetry
for a fixed lattice.

## 5. Exchange readouts on the saved inputs

A small-plaquette principal-log curvature and the saved action current give
the connection-normalized diagnostic f_nu=sum_mu,a F^a_numu J^a_mu.
Check its gauge covariance and the direct action derivative under the link
variation delta U_mu=xi^nu F_numu U_mu. This tests the current normalization
in the force/work coupling. It does NOT replace a local stress-divergence
calculation or assume the gauge fixture is on shell.

For the neutral real motion/bath action, define Lorentzian
L_int=sum_j g_j psi X_j. Its stress contribution is g_munu L_int.
The free-sector divergences exchange -g_j X_j dpsi and -g_j psi dX_j.
The interaction-stress derivative closes their sum. On saved lattice edges,
use the exact midpoint product rule

    Delta(psi X)=X_mid Delta psi + psi_mid Delta X.

This is an algebraic exchange audit, not a claim that a discrete difference
is a continuum covariant derivative. Dropping the interaction-stress term
must fail. The common-metric bath response is nonzero although its gauge
force is zero. Euclidean action/stress signs follow the convention above,
rather than being conflated with the Lorentzian exchange signs.

## 6. Acceptance and scope

Three saved synthetic fixtures; original1e-10 normalized identity gate and
1e-6 failure-control floor. Preserve the old source bank, physical grids,
couplings and cosmological history. Use trace, trace-free stretch and shear
directions, with the already-used0.005/0.0025 finite-difference steps.
Check the full10-component integrated source map and explicit bath addition.
Use the first fixture for independent finite differences and mixed responses;
replay the exact cached inputs. Retain any failed run.

This is not a new variable-metric field evolution, a gauge-measure
construction, or a fit to observations. Quantum measure terms stay outside
the calculation. After this bridge, return to a specific retained physical
source/evolution question rather than enlarging the regulator indefinitely.

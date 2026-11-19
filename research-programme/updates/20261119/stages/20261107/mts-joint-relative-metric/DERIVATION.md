# Close relative phase, metric and matter together

Private continuation of the retained MTS canonical-field branch, 2026-11-07.
Parent: ../mts-relative-phase-perturbations-20261107/closeout.json,
SHA2560ed0dc3b0b30e452a9e241057d21ffa6497e16298eace03d5b58ee13a4acab5f.
No field, interaction, parameter, initial mode or observed dataset is added.

## 1. The issue solved here

The parent's exact relative scalar is y=(delta,W). Its affine map is

    y=T z+V u, u=(Psi,Phi_N).

When u is prescribed, its equation for z contains u_N. In a gravitational
calculation u is NOT independent: both metric channels are linear functions
of the current matter state. Treating u_N as a slow external signal would
silently weaken the problem.

Let r be all retained other matter/gauge coordinates and w=(y,r). Write

    u=L_h y+L_r r=L w,  w_N=G w.

G is the full retained coupled generator for the selected metric branch.
It includes both scalar fields, CDM/baryons, radiation, the G192 massive
hierarchy, native pressure/closure terms and the quadrature enthalpy defect.
The row L is derived from the same GR or spatial-Poisson constraints.

The transformation can be closed algebraically, without guessing u_N.

## 2. Exact closed transformation

Define M=I-V L_h and partition the new state as zeta=(z,r).
Solving the first displayed equation gives

    y=M^-1 T z+M^-1 V L_r r
    w=S zeta
    S=[[M^-1 T, M^-1 V L_r],[0,I]]
    R=S^-1=[[T^-1(I-V L_h), -T^-1 V L_r],[0,I]].

Multiplying the blocks proves RS=SR=I whenever T and M are invertible:
the upper-right product cancels as
T^-1 V L_r-T^-1 V L_r, and the diagonal products are identities.
This keeps the response of the other matter; r has not been set to zero.

The exact transformed generator is

    zeta_N=B zeta
    B=R G S+R_N S=S^-1(G S-S_N).

For the upper two rows,

    R_h,N=-T^-1 T_N R_h-T^-1(V_N L+V L_N).

All other rows of R_N vanish. T_N and V_N are the parent's analytic
derivatives, including alpha_N, mu_N, b_N and theta_N. L_N is the
derivative of the actual metric row. Equivalently u_N=(L_N+LG)w:
it is determined by the coupled equations, not assumed negligible.

The initial mode and readouts must transform as

    zeta0=R0 w0,   w1=S1 zeta1,   observable=O S zeta.

Neither endpoint is reset. For the baseline, no heavy relative coordinate
is defined or divided by zero: S=R=I for this additional transformation.

## 3. The two actual metric rows

Use N=ln(a), CONFORMAL Hubble rate H, k>0, omega=am,
alpha=k^2/(omega H), mu=omega/H, eta=H_N/H, b=rho_h/(2H^2).
The parent's T and V are explicit functions of alpha,mu,b and theta.
This alpha is not the older gauge displacement.

For the heavy component, c=cos(2theta), s=sin(2theta):

    D_h=rho_h[1,0]
    P_h=rho_h[-c,2s/alpha]
    Q_h=(H/k)rho_h[-alpha s/2,1-c]
    ell_D,h=-D_h-3P_h-(k/H)Q_h
    ell_Q,h=-2Q_h+(k/H)P_h.

With total quadrature enthalpy Wq and defect DeltaW=Wq-Wbackground,
the total GR rows are

    L_Psi=-D/(2k^2)-3H Q/(2k^3)-shear/k^2
    L_PhiN=-[ell_D+3H(eta Q+ell_Q)/k+3Wq L_Psi]/(2k^2+3Wq).

For spatial Poisson they are

    L_Psi=-D/(2k^2)
    L_PhiN=-[ell_D+3DeltaW L_Psi]/(2k^2+3Wq).

The heavy self row L_h has zero shear, but shear remains in L_r.
The total ell_Q includes the actual native pressure, radiation shear and
the derivative of the retained quadrature defect. Its native implementation
is reused from ../mts-cold-adapted-metric-gain-20261107/cold_math.py,
not redefined to force an ideal-fluid conservation identity.

## 4. A phase-uniform inverse bound on the saved cold interval

This bound uses the SAME parent-frozen interval
a=[0.36273334952836184,0.46575884027469494], length L=0.25 e-fold.
Let alpha in [alpha_min,alpha_max], mu>=mu_min, and H<=Hmax.
The parent already proves T invertible. For the new inverse use

    ||V L_h||_2 <= ||V||_F ||L_h||_F =: lambda.

The parent's explicit V gives the entrywise bounds

    |V11| <= (alpha_max/2+3)/(2mu_min)
    |V12| <= (3alpha_max/(4mu_min)+3)/(2mu_min)
    |V21| <= (alpha_max^2/4+4.5alpha_max/2)/(2mu_min)
    |V22| <= (3alpha_max^2/(8mu_min)+1.5alpha_max)/(2mu_min).

The Frobenius norm of these four positive entries bounds ||V||.
For the positive retained branch rho_h<=3H^2, |eta|<=2.
Define the following uniform bounds:

    d=3Hmax^2
    p=d sqrt(1+4/alpha_min^2)
    q=d(Hmax/k)sqrt(alpha_max^2/4+4)
    ell=d+3p+d sqrt(alpha_max^2/4+4).

They bound the norms of D_h, P_h, Q_h and ell_D,h respectively.
Use 2k^2+3Wq>=2k^2, 3Wq/(2k^2+3Wq)<=1.
Positivity of the canonical/thermal matter also gives
0<=Wbackground<=6H^2. Since |DeltaW|<=Wq+Wbackground,

    3|DeltaW|/(2k^2+3Wq) <= 1+9Hmax^2/k^2.

Thus we do NOT need to set the defect to zero or assign an external
perturbation history to bound the heavy inverse. Let

    psi_P=d/(2k^2)
    phi_P=ell/(2k^2)+(1+9Hmax^2/k^2)psi_P
    psi_GR=psi_P+3Hmax q/(2k^3)
    phi_GR=(ell+3p+12Hmax q/k)/(2k^2)+psi_GR.

Then ||L_h||_F<=sqrt(psi_branch^2+phi_branch^2).
The GR estimate uses
3H/k(|eta|q+||ell_Q,h||)<=12Hq/k+3p.

The positive background identity eta<=1 implies
Hmax=H_upper(N0)exp(L), with the unchanged algebra padding.
The inherited alpha interval and mu minimum already cover all phases.
No sampled maximum supplies this continuum inequality.

For lambda<1, the Neumann bound gives

    sigma_min(M)>=1-lambda
    ||M^-1||_2<=1/(1-lambda)
    ||M^-1-I||_2<=lambda/(1-lambda).

The worst evaluated bound is lambda=2.4644982227e-11 (half k, GR).
Consequently the extra metric-feedback inverse is well conditioned
throughout this interval under the retained positive-branch assumptions.
This number measures a COORDINATE-INVERSION correction, not the strength
of gravity or the size of gravitational growth.

The inequalities are analytic; their numerical endpoints inherit the
parent's qualified background tube. They are not a new directed-rounding
formal certificate of the entire background computation.

## 5. Check the construction against the native coupled system

Use the original native contexts and saved coefficient packets, in the
already resolved EARLY domain, for all half/balanced/double wavenumbers
and both MTS/heavy and baseline/cold. This is distinct from the late
cold interval where the inverse is bounded without assigning a phase.
Do not transplant an early native trajectory into the late interval.

The existing cold-adapted physical-energy map is P_e. Replace only the
heavy full-frequency pair by the parent's relative pair using J. If v
is the normalized native state, then w=J P_e v, with generator

    G=J[P_e G_native P_e^-1+(P_e)_N P_e^-1]J^-1+J_N J^-1.

J_N is derived from the original scalar equations. The retained native
rows supply L; the two separate metric branches supply their own G.
The remaining matter and the G192 tail are transformed with the original
weights and derivatives. Tail-to-core forcing is multiplied by R as well;
it is not dropped because it is outside the two scalar coordinates.

native_joint.py builds B and its physical readouts. run_native.py then
compares its action on full states against PoissonDriver.evaluate, which
calls the retained native implementation independently. The tests include
the entire G192 tail and the actual native pressure/closure branches.

L_N is evaluated by a symmetric fourth-order difference of the same
time-local native rows, at widths .04/max(mu,1), half and quarter.
The independent finite difference of R checks the analytic product rule
for R_N. The fine-width comparison is a numerical derivative qualification,
not a symbolic proof of every thermal-row derivative. All errors are
judged against the pre-existing gates, not a relaxed threshold.

612 full native-vector checks cover both models and metric branches.
Separately, the native contexts replay their owned prefix preparation and
verify the saved seed exactly. This is not a new cosmological initial mode.

## 6. Preserve the existing prepared histories, not just random probes

check_histories.py transports 13 existing epochs, including the initial
and final epochs, from each of the twelve saved GR/Poisson histories
(two models, three wavenumbers, two branches). It stores the relative/
joint cores and reconstructed D,Q,shear,Psi,Phi_N in small new packets.

These are the existing retained preparations, not a newly assumed
adiabatic mode. Source archives are hash-checked before use and again
by audit_joint.py. No new background or late perturbation ODE is run.
The native context's internal initial-prefix replay is recorded explicitly.

## 7. What this now enables

We have an exact, invertible closed matter/metric coordinate map; gravity
no longer has to be supplied as an independent perturbation history.
The retained source/readout predictions survive this change of variables.

The next construction is the correlated phase mean and remainder of B,
including gravitational growth and all other matter, on the frozen cold
background. Averaging G, S and S_N separately is not justified: their
phase correlations and the rational metric denominator must be retained.
Carry the owned early preparation through a controlled joint transfer,
rather than inventing a late cold initial mode. Compare GR and spatial
Poisson using the same preparation, windows and tolerances.

The present inverse bound is not itself a bound on that joint averaging
remainder or on a late observational prediction. It removes the implicit
metric-source obstacle so that calculation can now be made explicitly.

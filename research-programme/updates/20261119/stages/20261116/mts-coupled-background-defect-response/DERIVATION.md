# One coherent background correction

16 November 2026. Continue the retained exchange diagnostic, not a new
theory or cosmological fit. Masses, populations, source conventions, the
bank and the physical reporting grid are unchanged.

## 1. The system being corrected

Native conformal time tau is in Mpc, c=1. The physical background equations
retained by the previous stages are

    a'=a H,
    b_j'=v_j,
    v_j'=-2H v_j-M_j b_j,   M_j=(a m_j)^2,
    3H^2=R_other(a)+sum_j(v_j^2+M_j b_j^2)/2.

R_other uses the ACTUAL retained matter/radiation/massive-neutrino formula,
not an independent massless approximation. Include the slow scalar in
both cases and the populated heavy scalar in MTS. In the saved independent
background interpolants, a'=r a, b_j'=v_j+f_bj and
v_j'=-2H v_j-M_j b_j+f_vj. These defects are measured and retained.

The original common metric and positive quadratic normal-mode action are
unchanged. The fields are already in the diagonal basis: do not insert a
second copy of their old mixing potential.

## 2. Linear response, with a stable scale coordinate

Use alpha=delta a/a, B_j=delta b_j and V_j=delta v_j. Then

    delta R=R_other,N alpha
             +sum_j[v_j V_j+M_j b_j B_j+M_j b_j^2 alpha],
    delta H=delta R/(6H),
    alpha'=(H-r)alpha+delta H+(H-r),
    B_j'=V_j-f_bj,
    V_j'=-2H V_j-M_j B_j-2v_j delta H-2M_j b_j alpha-f_vj.

R_other,N is the derivative with respect to ln(a), derived from the same
retained density expression. The extra (H-r)alpha term is required by the
relative coordinate; the previous absolute delta-a equation remains valid.

All corrections start at zero at ONE earliest common preparation anchor
per cosmology, not at every shifted preparation node. Integrate to the end
of the already-saved33-report domain and sample all original33x902 queries.
This is a local anchored background repair, not a recalibration of the
entire early-universe history or a new formation prescription.

## 3. Exact nonlinear correction and independent control

For q=1+alpha, a_star=a q, b_star=b+B and v_star=v+V, evaluate

    delta R=R_other(a q)-R_other(a)
       +sum_j[v_j V_j+V_j^2/2
               +M_j(b_j B_j+B_j^2/2)
               +M_j(q^2-1)(b_j+B_j)^2/2],
    H_star=sqrt(H^2+delta R/3),
    delta H=delta R/[3(H_star+H)],
    alpha'=q(H_star-r),
    B_j'=V_j-f_bj,
    V_j'=-2H V_j-2delta H(v_j+V_j)
          -M_j B_j-M_j(q^2-1)(b_j+B_j)-f_vj.

Use stable algebraic differences for R_other, retaining the original
piecewise neutrino function and rejecting unsupported regimes. No defect
amplitude is fitted.

Independently integrate the autonomous absolute system in section1 from
the same initial data. Compare reconstructed corrected scale/fields,
their Friedmann rate, the linear approximation and32/64 refinements.
The correction and absolute formulations are distinct numerical
representations of the same retained equations; agreement is a numerical
test, not a new observational success. Original1e-10/2e-5 criteria and
1e-10/1e-12 solver settings are retained.

## 4. Source/metric response without an inconsistent promotion

At fixed saved heavy perturbations u,w and fixed native COMOVING k,

    D=v w+M b u, Q=k v u, P=v w-M b u,
    Y=(a/R0)(D,Q,P).

Derive the exact readout change using the corrected a,b,v,M and the linear
variation given in the previous NEXT.md. This is a background-only
sensitivity, NOT a complete updated prediction. The inherited note's
wording about a fixed physical wave number is interpreted as fixed native
comoving k; physical k/a changes with a.

At fixed eta_k and surrounding D_o, the constraint changes by

    delta z=[delta D/(2k)-z delta H]/(H+delta H),
    delta eta_k'=delta Q/2.

These terms are diagnostic feedback sources, not a licence to hold the
environment or perturbations fixed in the physical theory. A full response
must also carry delta D_o,delta Q_o, prepared-state changes and the effect
of changed clocks on matching. Their absence cannot be hidden by selecting
a favourable pressure residual. Quantum measure stays separate.

The immediate scientific acceptance is a tested coherent background
correction and its source-response interface. No source replacement or
closure of the previous pressure budget is claimed from a frozen-state
sensitivity alone.


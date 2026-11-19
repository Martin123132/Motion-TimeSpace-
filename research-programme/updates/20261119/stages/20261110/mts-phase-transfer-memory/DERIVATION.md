# Finite-support source transfer and its retarded continuation

This calculation extends the retained coupled real-scalar branch. It neither changes the historical signed temporal projection nor replaces the action with a new late fluid. Read the previous live-coupling stage at `../mts-coupled-phase-stress-20261110` first.

## 1. Exact transfer for the actual saved discrete weights

Let t_0<...<t_N be the original 902 saved times, w_i the original a225-w6-d8 extraction weights, S=sum(w_i), and C_j=sum_{i<=j}w_i for j=0,...,N-1. For any sampled source Y:

    P[Y] = sum_i w_i Y(t_i)
    S Y(t_N) = P[Y] + sum_j C_j [Y(t_{j+1})-Y(t_j)]
             = P[Y] + integral_(t_0)^(t_N) C(t) Y'(t) dt.

C(t)=C_j on each saved interval. This follows by telescoping, without assuming positive weights, a smooth averaging kernel, periodicity, stationarity or a dust limit. S is explicitly carried; the original weights are not renormalized. In this packet S=1 numerically, sum(abs(w))=1.7024412255970143 and 429 weights are negative.

The rightmost endpoint is chosen to make the support wholly in its past. It is NOT a relabeling of the original central matching scale. A symmetric extraction around the old center contains samples later than that center; it cannot be described as an instantaneous causal initial condition there without additional transport information.

The discrete difference formula is an algebraic check only. The substantive test integrates Y' from the retained field/matter equations and compares the predicted endpoint with the saved native result. It does not define Y' by subtracting the measured endpoint discrepancy.

## 2. Source equations supplying the memory

Use the same native scalar normalization as the previous stage, k=1 Mpc^-1 in the frozen tests, beta=a/rho0 with the original matching-density normalization rho0, and r=dln(a_thermal)/dtau from the actual native thermal interpolant. H is the native Friedmann rate. They are distinguished at finite numerical resolution.

For one retained real scalar:

    D=v*w+mu2*b*u; P=v*w-mu2*b*u; Q=k*v*u; mu2=(a*m)^2
    E_f=r*b_N-v; E_b=r*v_N+2H*v+mu2*b
    Y_D=beta*D; Y_Q=beta*Q; Y_P=beta*P

Differentiation using the original Klein–Gordon perturbation equation yields:

    Y_D' = (r-H)Y_D -3H Y_P -k Y_Q -beta*k*z*v^2
           + beta*E_b*w + beta*mu2*E_f*u
           + 2beta*(r-H)*mu2*b*u
    Y_Q' = (r-2H)Y_Q +k Y_P +beta*k*E_b*u.

The three last terms in the density law and last term in the current law account for the already-existing representation defects; they are not new physical forces. The pressure derivative is obtained directly from the product, without fitting pressure:

    w'=-2H*w-(k^2+mu2)u-k*z*v
    Y_P'=beta*[r*P+r*v_N*w+v*w'
               -2r*mu2*b*u-mu2*r*b_N*u-mu2*b*w].

For the baseline dust control, the native synchronous CDM current and pressure are zero. Since its rescaled density R_c is proportional to a^-1, beta*R_c is constant and:

    Y_c'= -beta*R_c*k*z.

The retained slow scalar is checked in BOTH cosmologies as well. No heavy scalar or scalar pressure law is invented for the baseline dust control.

Each source-equation term is integrated against the SAME C(t). The resulting ledger separates pressure work, gravitational work, current transport, dilution and numerical representation terms. The memory is accumulated physical evolution on a known trajectory, not a compensating stress added to the action.

## 3. Metric conditions for an instantaneous interface

Hold every other native state fixed at the endpoint. On the retained flat branch:

    z=(D_total/(2k)+eta_k)/H; eta_k'=Q_total/2
    delta_z=delta_D/(2kH); delta_eta_k'=delta_Q/2
    delta_Phi=-(delta_D+3H*delta_Q/k)/(2k^2).

Thus preserving both D and Q preserves these metric constraints at an instantaneous source replacement. Matching a single combination such as D+3H Q/k is not sufficient to preserve eta_k'. Pressure also matters for subsequent density/current evolution even though it is not a separate argument to this native stress port.

The derived boundary memory transports all three scalar sources to the endpoint. Merely inserting P[Y_D],P[Y_Q] there creates a different instantaneous source. That observation is NOT an exclusion of a consistently coarse-grained cosmology: such a description must coarse-grain its metric and other species consistently too. It is specifically an obstruction to an unadjusted mixed-description handoff.

## 4. Exact retarded continuation available from the action

The next construction need not invent a local pressure fit. Collect the real scalar perturbations in x=(u_s,w_s,u_h,w_h), omitting the heavy pair in the baseline. Define

    z_rest=(D_rest/(2k)+eta_k)/H,
    z=z_rest+sum_j(v_j*w_j+mu_j^2*b_j*u_j)/(2kH).

Eliminating this live scalar density feedback in the KG equation gives a linear system x'=A(t)x+B(t)z_rest:

    A_(u_j,w_l)=delta_jl; A_(u_j,u_l)=0
    A_(w_j,u_l)=-(k^2+mu_j^2)delta_jl-v_j*mu_l^2*b_l/(2H)
    A_(w_j,w_l)=-2H*delta_jl-v_j*v_l/(2H)
    B_(u_j)=0; B_(w_j)=-k*v_j.

The metric variable eta_k remains in the other-species/rest system, where Q feeds its evolution. It must not be frozen or removed in a fully coupled reduced implementation. The density self-feedback above is already included in A, not forgotten as an external force.

Let T(t,s) be the fundamental matrix of A. The standard variation-of-constants identity then yields the exact source response

    Source(t)=C_source(t)T(t,t0)x0
              + integral_(t0)^t C_source(t)T(t,s)B(s)z_rest(s) ds.

For each scalar, C_D=(mu2*b,v), C_P=(-mu2*b,v), C_Q=(k*v,0) in its pair of columns. Multiplication by beta produces the historically normalized sources. This is an application of a standard mathematical identity to the retained equations, not a new mathematical theorem. Its coefficients are action/background-owned and have not been fitted to pressure or galaxy observations.

Consequently the frozen projected pair obeys

    (P[Y_D],P[Y_Q])^T = L_projection*x0 + known_history_term,

where L_projection=sum_i w_i beta_i C_DQ(t_i)T(t_i,t0). If the relevant physical block of L_projection is nonsingular and adequately conditioned, two projected source numbers together with the specified driving history CAN recover that block's coherent state. This must be calculated, not denied merely because phase was averaged and not assumed merely because two numbers are present. A singular/ill-conditioned block instead requires retained phase information or a controlled memory description.

This stage proves the block algebra and evaluates the finite-support boundary memory. It does NOT yet evaluate T or prove this projection map's rank/conditioning. No positive ensemble, primordial occupation or independent galaxy population follows from the formal retarded identity.

## 5. Numerical meaning

The native reference support is widened to precisely original indices1991..2892, without changing the original 4253 samples. All its saved source/metric observations reproduce exactly. It remains a fixed-regime native owner. Primitive states between saved nodes use cubic Hermite interpolation with native derivatives; Gaussian integration orders4/8 and retained-history strides1/2 are compared. At every quadrature evaluation, the retained source implementation forms the metric from that interpolated physical state, rather than fitting the memory to the desired endpoint.

This is a known-history equation/transfer consistency test, not a held-out prediction or a new complete late cosmology. The numerical refinements are sensitivity evidence, not rigorous global error bounds. Baseline and MTS use the unchanged2e-5 numerical and1e-10 algebra acceptance gates. The same bank, action, masses, normalization, background, source convention and output grid remain in use.

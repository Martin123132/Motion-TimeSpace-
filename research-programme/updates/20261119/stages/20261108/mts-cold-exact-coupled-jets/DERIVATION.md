# Exact cold relative-phase coupling derivatives

This is a continuation of the retained MTS cold-background calculation, not a new theory or a new late-time initial condition. The parent is `../mts-cold-clock-thermal-generator-20261108/closeout.json`, SHA256 `6bfd07ec9fd838fdc0146e9bea5a1e67d41bbbf774c475b37e26c7c3e524c813`. Earlier equations, source histories, native matter options and physical comparison gates are retained.

## 1. Variables and physical directional derivative

Use N=ln(a), conformal Hubble rate H in Mpc^-1, physical conformal clock tau in Mpc, comoving k in Mpc^-1, U=a m_s phi_s, V=phi_s', heavy conformal density rho, and c=cos(2theta), s=sin(2theta). The saved background fixes the external density R and enthalpy W. The source laws give

    H² = [R + (U²+V²)/2 + rho]/3
    U_N = U + a m_s V/H
    V_N = -2V - a m_s U/H
    rho_N = (-1+3c)rho
    tau_N = 1/H
    theta_N = mu - 3s/2,  mu=a m_h/H.

For a coefficient Q(N,U,V,rho,tau,theta), its derivative is its explicit N derivative plus the chain rule along all five rates above. The slow part holds theta fixed but retains rho_N=(-1+3c)rho; the phase part holds the slow state fixed. Their sum is the total physical derivative. Dropping the cosine term in rho_N would change the operator.

`source_laws.py:metric_arguments` and `tangent.py` implement this directional chain rule. `coupled_jets.py:evaluate` now obtains the complete physical metric readout and both endpoint-map derivatives this way. No finite-difference jet enters the new generator. Previous fourth-order jets are independent comparison data, not new inputs.

## 2. Finite-source derivatives, including the quadrature defect

For each retained finite Fermi quadrature term, write t=v² and r for its conformal density contribution. The source dispersion relation implies

    t_N = -2t(1-t)
    r_N = -(1+t)r
    r_NN = (1+4t-t²)r.

Its enthalpy contribution w=r(1+t/3) therefore obeys

    w_N = -r(1+2t-t²/3)
    w_NN = r(1+7t-11t²/3+t³).

The four polynomial identities are checked symbolically. Summation uses the SAME saved positive finite Fermi quadrature, not a replacement continuum integral. The native five-node perturbation quadrature is distinct and kept distinct.

Let delta_c and delta_r be the tiny cold and radiation normalization differences already exposed by the parent high-precision audit. With Q=(4/3)sum_j r_j for the native five-node source and W_m for the external massive enthalpy,

    Delta = delta_c/a + 4 delta_r/(3a²) + Q - W_m
    Delta_N = -delta_c/a - 8 delta_r/(3a²) + Q_N - W_m,N
    Delta_NN = delta_c/a + 16 delta_r/(3a²) + Q_NN - W_m,NN.

The exact full GR momentum readout retains Delta and the parent's baryon-pressure term. The spatial-Poisson readout already contains Delta_N, so differentiating that branch requires Delta_NN. Setting any of these terms to zero would silently change the retained implementation. The source-law derivatives are independently checked against 70-digit differentiation of the previously qualified source formulas.

## 3. The thermal clock is not the physical clock

The native thermal source is a saved cubic interpolation in a log-table-time coordinate t, with P(t)=a/table_time, Q(t)=cs² or opacity, and log-table spacing h_t. Define D=h_t P+P_t. The retained source gives

    Q_N = P Q_t / D
    Q_NN = P[(P_t Q_t+P Q_tt)D - P Q_t(h_t P_t+P_tt)]/D³.

These parent-derived jets are used unchanged. This is the derivative of the retained thermal history, not a new calculation of MTS recombination. The independent test moves N by a complex increment, solves the local cubic scale-inversion equation and evaluates Q at that independently obtained table coordinate. It does not reuse Q_N to construct the comparison. The expansion is local within a cell; parent one-sided second-derivative conventions apply at joins.

## 4. Exact physical coupled generator

In the physical perturbation coordinates y, let L be the complete metric readout, F its injection and G the free generator:

    y_N = (G + F L)y.

L includes the other matter sectors; it is not a heavy-only gravitational closure. Let T=I+P_micro be the retained heavy periodic map extended by the identity, and let W be the physical affine metric map, with only its two heavy rows nonzero. W equals h times the earlier relative affine map, h=sqrt(rho)H/k. The changing physical weight is already included through gamma=h_N/h in G.

The coupled coordinate relation is

    y = T z + W L y
    S = (I-W L)^-1 T,     y=S z
    R = T^-1(I-W L),      z=R y.

Parent whole-tube inverse tests justify these inverses on the saved branch. Direct differentiation gives

    A = R(G+F L)S + R_N S.

The new `coupled_jets.py` obtains R_N from the exact source laws, including changing h, thermal scale readout and Delta_NN. The baseline has no heavy coordinate map and simply retains G+FL.

## 5. Cancel the rapid micromotion algebraically

The previous formula is exact, but constructing its large terms separately is needlessly cancellation-sensitive. Differentiate R, use RS=I and S=T+WLS, and rearrange without commuting any matrices:

    A = T^-1(G T - T_N) + T^-1 K S
    K = (G W - W_N + F)L - W(L_N + L G + L F L).

This follows directly by substituting R_N=-T^-1 T_N R-T^-1(W_N L+W L_N). It is an identity of the coupled system, not an additional averaging assumption.

G has an isolated two-row heavy block before metric coupling. Thus T^-1(GT-T_N) leaves the other free rows unchanged; its heavy block is the earlier exactly derived normal-form generator plus gamma I. `stable_coupled.py:assemble` evaluates that cancellation first and only then adds the full metric correction. It retains both the GR and spatial-Poisson branches, every external metric column and the same physical weight.

The identity is checked against the direct pullback at all saved epoch/phase cases and all 256 original midpoint phase nodes. A separate 70-digit calculation evaluates the direct pullback and compares both double-precision implementations. Independent complex-step derivatives use the earlier unsimplified momentum expression and direct map inversion rather than the new automatic-differentiation path.

## 6. Retained phase averaging

At each retained wave family's saved midpoint, keep theta_j=pi*j/256 and omega(theta)=mu-3sin(2theta)/2. The time-weighted phase mean is

    Abar = integral[A(theta)/omega(theta)] / integral[1/omega(theta)]
    C_theta = (A-Abar)/omega,   mean_theta(C)=0.

`average_exact.py` recomputes the same sampled mean and periodic primitive from the exact-jet, cancellation-factored generator. It compares against the saved operator, mean and primitive. Baseline phase independence is tested directly rather than assuming a zero numerical error. All original numerical gates remain ALGEBRA=1e-10 and GATE=2e-5.

## 7. Meaning of this result and next calculation

This stage replaces a numerical differentiation step with source-derived equations and makes the rapid cancellation explicit. It qualifies the coefficient implementation and preserves the saved midpoint result. Extremely small residuals in the 70-digit derivative checks measure arithmetic consistency of those formulas, not accuracy against the universe.

The finite thermal source, original UFA/full-hierarchy choices, G192 closure, earlier native representation tests and inherited background uncertainty remain explicit assumptions. Coefficient qualification uses the inherited core plus first two massive-tail levels; the parent's full G192 checks and free-source envelope are reused, not relabelled as a new full G192 evolution.

Next, differentiate the FACTORED coupled expression across the inherited (U,V,rho,tau) tube. Preserve correlations in L_N, W_N and the scalar flow instead of adding independent maxima before cancellation. Combine that enclosure with the existing skew-streaming/dissipative-collision structure and physical averaging remainder. Then transport the original prepared mode with both physical endpoint maps, carrying source replacement, phase averaging and global integration errors separately. No new late initial mode is needed.

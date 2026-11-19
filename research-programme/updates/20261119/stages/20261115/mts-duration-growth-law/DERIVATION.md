# Elapsed-time growth from the retained coupled equations

## Scope and inherited inputs

This continues the retained MTS action's existing cold/heavy conditional weak-field calculation; it does not introduce another theory. Mode k=5, the original902 signed preparation nodes, physical normalization, native source bank, background interpolation, source grids and2e-5/1e-10 gates are unchanged. Time below is elapsed native conformal time, not years or a new redshift variable.

The sealed inputs are the coupled equations in ../mts-live-metric-state-20261112/metric_math.py, the one-sided source integration in ../mts-corner-safe-source-evolution-20261115/source_history.py, and both completed histories in ../mts-next-eight-epoch-extension-20261115. Exact source paths and SHA256 values are in frozen-inputs.json.

For each preparation node, let X be the own-field plus metric state, F=(D_other,Q_other), and K=F''. The source history and original quadratic control share their initial state, F0,F1,K0. Their difference obeys exactly within this retained numerical system:

    DeltaX' = A(t_i+s) DeltaX + B(t_i+s) R_i(s), DeltaX(0)=0,
    R_i(s) = integral_0^s (s-v) [Khat(t_i+v)-K_i(0)] dv,
    DeltaO(T) = sum_i w_i C_i(T) DeltaX_i(T).

A,B,C are already fixed by the retained equations. The sum uses signed weights; replacing them with absolute weights changes the prediction. Absolute weights are used only in numerical uncertainty estimates. Neither reference corrections nor observed data determine the coefficients below.

## One-sided local law

If the source is smooth on the initial side, write Khat(t_i+s)-K_i(0)=K1*s+K2*s^2/2+O(s^3). Initial represented mismatch is checked explicitly and is exactly zero at every retained node. If a mismatch e0 existed, the leading state term would instead include B0*e0*s^3/6; it is not silently discarded.

With A=A0+A1*s+..., B=B0+B1*s+..., C=C0+C1*s+...:

    R(s) = K1*s^3/6 + K2*s^4/24 + O(s^5),
    DeltaX(s) = X4*s^4 + X5*s^5 + O(s^6),
    X4 = B0*K1/24,
    X5 = A0*B0*K1/120 + B1*K1/30 + B0*K2/120,
    O4 = C0*X4,
    O5 = C0*X5 + C1*X4.

These coefficients follow by matching powers in the differential equation, not by fitting two endpoint ratios. growth_math.py evaluates the source derivatives from each first-cell polynomial and A,B,C derivatives from the retained background. K1/K2 are derivatives of that numerical source representation; this calculation does not independently prove their continuum-physical accuracy.

For the heavy state X=(u,w,eta), with b the background field, v its conformal derivative, M2 the conformal mass squared, H the conformal Hubble value and beta=a/density0:

    B_D=(0,-v/(2H),0), B_Q=(0,0,1/2),
    C_D=beta*(M2*b,v,0),
    C_Q=beta*(k*v,0,0),
    C_P=beta*(-M2*b,v,0).

Consequently, per node:

    (O4)_D = (O4)_P = -beta*v^2*(K1)_D/(48H),
    (O4)_Q = 0,
    (O5)_Q = k*(O4)_D/5.

The density source first drives w; u requires another integration. That is the origin of the extra power in current, rather than an empirically fitted fifth-order exponent. The cold density coefficient is -cold_normalization*(K1)_D/(48H); cold current and pressure remain exactly zero.

The first-cell common validity ranges are recorded in each result. Many nodes cross interpolation corners well before either saved endpoint, so this Taylor law alone must not be treated as a global power law.

## Exact handling of corners in the represented source

Let c_j be a source-curvature corner and J_j=Khat(c_j+)-Khat(c_j-). For any nonnegative integer p, piecewise integration by parts gives

    integral_0^T (T-v)^p/p! [Khat(v)-K0] dv
      = e0*T^(p+1)/(p+1)!
        + integral_0^T (T-v)^(p+1)/(p+1)! Khat'_piecewise(v) dv
        + sum_(0<c_j<T) J_j*(T-c_j)^(p+1)/(p+1)!.

For p=2 this is I0=integral R(s)ds; p=3 gives I1=integral(T-s)R(s)ds. A curvature jump thus contributes a shifted cubic term to the leading directly driven state, not a single global fourth power. The equality is verified against independent Gaussian integration on saved segments. Some jumps belong to the numerical representation; they are not automatically new physical discontinuities.

A first kernel approximation is

    DeltaX(T) approximately B0*I0 + A0*B0*I1 + B1*(T*I0-I1).

It uses the full piecewise source, but approximates the changing transfer coefficients. Its MTS mismatch is retained in results; it is not promoted just because the moments are exact.

## Time-dependent response expansion

To retain the changing background and source corners without fitting a power, define

    Y0(T) = integral_0^T B(s) R(s) ds,
    Y(n+1)(T) = integral_0^T A(s) Yn(s) ds,
    DeltaX(T) = sum_(n=0 to infinity) Yn(T).

This is the Volterra/time-ordered response expansion of the same linear equation. With locally bounded A and integrable B R, it converges on every finite retained interval. Each extra interaction supplies an additional integral. For a smooth cubic remainder, Yn=O(T^(n+4)); sparse readouts can delay the first nonzero observable further. The physical A,B,C and signed projection remain unaltered.

For any consistent state norm, define L(T)=integral_0^T ||A(s)||ds and Hf(T)=integral_0^T ||B(s)R(s)||ds. A conservative analytic remainder inequality is

    ||DeltaX-sum_(n=0 to N)Yn|| <= Hf(T)*exp(L(T))*L(T)^(N+1)/(N+1)!.

This states the mathematical condition; sampled norms in the next-window contract are planning indicators, not certified upper bounds on L or unknown future sources. No future pass follows just from this inequality.

We evaluate Y0 through Y8 with the same DOP853 accuracy and original physical32/64 maximum steps, at the same17 saved reports. The initial difference remains zero at the original preparation origin; the expansion is not reset at the short-window boundary. Reference comparison uses the separately saved direct difference evolution, avoiding subtraction of large nearly equal full states.

## Interpretation

The local order is derived. A universal pure T^4/T^5 extrapolation is rejected at the unchanged correction gate for MTS over these windows. The time-dependent, corner-aware response expansion succeeds against both saved histories. This is a conditional numerical consistency and mechanism result, not new galaxy or cosmological observation evidence. It gives a defensible next test: double the current elapsed horizon, acquiring its missing source values and independent readouts before scoring.

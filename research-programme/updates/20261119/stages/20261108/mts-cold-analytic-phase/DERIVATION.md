# Analytic phase control of the retained cold relative system

## 1. The finite harmonic source, not an empirical Fourier fit
Fix a physical slow state sigma=(N,phi_s,v_s,rho_h,tau). Set z=exp(2 i theta),
c=(z+z^-1)/2 and s=(z-z^-1)/(2i). H,alpha,mu,rho_h and external thermal inputs are fixed on this fibre.
The heavy stress dictionaries already derived from the canonical action are

    D_h=rho_h delta
    P_h=rho_h(-c delta+2s W/alpha)
    Q_h=(H/k)rho_h[-alpha s delta/2+(1-c)W]
    Wq_h=rho_h(1-c), eta=eta0+b c.

These are Laurent polynomials of degree one. External canonical/fluid/thermal coordinates have no fast heavy phase; their connection coefficients are at most linear in eta. The gauge enthalpy defect is external: the heavy velocity squared cancels from Wq-W. Its derivative must be cancelled algebraically, not differentiated as two unrelated large numbers.
Consequently the free coupled generator G0 and metric injection F have harmonic degree at most one. This includes the slow scalar and all retained fluid/neutrino species. The remote G192 streaming is constant on a phase fibre, not discarded.

The solved metric denominator is

    d_phys=2k^2+3[Wq_ext+rho_h(1-c)] = d0(1-epsilon_d c)
    d0=2k^2+3(Wq_ext+rho_h), epsilon_d=3rho_h/d0.

Both GR and spatial-Poisson metric rows have L=P/d with d=d_phys/d0 and numerator P of degree at most two. For GR this follows from eta Q_h and Wq Psi, both degree two. For spatial Poisson it follows from the retained enthalpy defect and the same denominator. No Poisson substitution is made in the GR row.
The periodic source maps T=I+P_micro and V are degree one; their physical derivatives T_N and V_N have degree at most two. These statements follow directly from relative_math.py and forced_map.py, not from a decay fit.

Eight equally spaced real phase points uniquely recover these coefficients because 8>2*2. Collocation evaluates the exact finite algebraic representation; the excluded Fourier modes and independent phases test arithmetic/source consistency. They are not the proof of finite degree. Numerical evaluation/slow-jet error remains separate from the analytic truncation theorem.

## 2. Differentiate source coefficients before dividing
Write physical slow flow f=f0+c fc and omega=theta_N=mu-3s/2. Then

    L_theta=(P_theta-L d_theta)/d
    D_sigma L f=[P_0+c P_c-L(d_0+c d_c)]/d
    L_N=omega L_theta+D_sigma L f.

The subscripts 0,c here denote directional derivatives along f0,fc, not Fourier modes; d0 above is a different, explicitly named normalization.
This retains the rational phase dependence when differentiating. The implementation differentiates the finite coefficients with the inherited fourth-order slow differences, and checks widths .001 and .0005. Those finite differences are qualified approximations to slow derivatives, not symbolic exact derivatives or background-error certificates. Phase derivatives themselves are analytic.

With heavy selector J and lift J^T,

    M=I-V L J^T
    S=I+J^T M^-1[(T-I)J+V L]
    R=I+J^T[(T^-1-I)J-T^-1 V L]
    R_N,heavy=-T^-1[T_N R_heavy+V_N L+V L_N].

The exact retained physical normalization is D=diag(h,h,1,...), h=sqrt(rho_h)H/k on the heavy slots. It gives

    A=D[R(G0+F L)S+R_N S]D^-1+gamma P_h
    gamma=eta0-1/2+(3/2+b)c.

The numerical source adapter evaluates precisely this expression. Baseline has no heavy phase or heavy maps; it is checked independently on its own saved background.

## 3. An explicit rational denominator
Let t=det T and m=det(d I-V P_heavy). Then one valid common denominator for A is

    Q=d^2 t^2 m.

Degree bookkeeping gives: d degree1, t degree2, m degree6 or less; R numerator degree4, S numerator degree6, R_N numerator degree8. Thus Q degree<=12 and A Q degree<=15. The physical gamma connection is included in that count.
The independently reconstructed A Q is checked for forbidden harmonics beyond15. No empirical cutoff determines this degree.

## 4. Weighted Fourier algebra and the omitted analytic tail
Use ||F||_r=sum_j ||F_j||_2 r^|j|, bounded in code with coefficient Frobenius norms. It is submultiplicative; ||I||_r=1. For ||X||_r<1,

    ||(I-X)^-1||_r <= 1/(1-||X||_r).

Use r=16. Scalar d, T, and M obey the contraction bounds without searching for complex roots. In particular

    L_r <= P_r/(d_constant-d_tail,r)
    S_r <= 1+(P_micro,r+V_r L_r)/(1-V_r L_heavy,r)
    R_r <= 1+(P_micro,r+V_r L_r)/(1-P_micro,r)
    (R_N)_r <= (T_N,r R_r+V_N,r L_r+V_r L_N,r)/(1-P_micro,r).

Therefore

    A_r <= cond(D)[R_r(G0,r+F_r L_r)+(R_N)_r]S_r+gamma_r.

The full remote tail is included conservatively by its banded row/column norm bound 2 max(kv/H)+3/2. This is only a tail regularity estimate: use the previous logarithmic norm, not this large A_r, for physical growth control.

For any analytic coefficient family obeying this bound,

    sum_|j|>=m ||A_j|| <= r^-m A_r.

Hence the exact256-point trigonometric interpolation error is at most 2 A_r r^-128. This bound is derived from the source denominators and finite numerators; it is not extrapolated from an FFT noise floor.

The physical-clock mean uses w=1/omega, w_r<=1/(mu-3r/2), and exact mean(w)=1/sqrt(mu^2-9/4). For256 nodes, both numerator and denominator quadrature errors must be included:

    clock_alias=w_r r^-256
    ||Abar_256-Abar|| <= 2 A_r clock_alias/[mean(w)-clock_alias].

For zero-angle-mean C with C_theta=(A-Abar)/omega, C_r<=A_r w_r. In addition to the interpolation tail of C, integrating sampled forcing has an alias error bounded conservatively by

    4 A_r w_r r^-128 + (1/2) mean_error w_r.

These very small exact-arithmetic analytic truncation bounds do NOT imply corresponding numerical precision. Native arithmetic, coefficient extraction, finite differences and background replacement are much larger independent error channels. No source has been computed to140 decimal places.

## 5. Pole-free inverses throughout the inherited cold tube
Reuse the previously derived alpha interval, mu minimum and H maximum, including the saved background tube. Canonical positive densities imply rho_h<=3H^2, |eta0|<=2, 0<=b<=3/2. Positive quadrature implies Wq_ext>=0. Consequently epsilon_d<=9H_max^2/(2k^2). The source-map polynomial formulas give explicit r-weighted coefficient upper bounds for P_micro,V, not sampled maxima.

For the GR heavy metric row, set Jq=H Q_h/k. Bound its weighted norm by

    ||Jq||_r <= rho_max H_max^2/k^2 [alpha_max r/2+1+r].

Use the exact rearrangement

    Phi_N=-Psi-[D_free+3 eta Jq+3 H Q_free/k-2k^2 Psi]/d_phys

and H Q_free/k=-2Jq+P_h. This avoids needing an upper bound on arbitrary positive quadrature enthalpy. For spatial Poisson, retain the defect and use

    Phi_N=-Psi-[D_free-(2k^2+3W_true)Psi]/d_phys,

where W_true,r<=H_max^2(6+3r), from positive-energy canonical matter and its heavy harmonic. These give uniform upper bounds for ||V L_heavy||_r. All T, M, d and clock contraction inequalities must stay below1. The baseline has no such heavy inverse.

This theorem excludes phase poles throughout the inherited cold tube. It does not bound every slow derivative or establish a uniform A_r/remainder supremum on that tube; endpoints are validations of the derived analytic family, not substitutes for that remaining step.

## 6. Source perturbations and the next physical transport step
Coefficient errors must pass through the same inverses, not be labelled Fourier tails. If ||delta d||_r=e_d<d_margin and ||delta P||_r=e_P, then

    ||delta L||_r <= (e_P+L_r e_d)/(d_margin-e_d).

Similarly, a T perturbation e_T gives inverse change <=e_T/[(1-p)(1-p-e_T)], and feedback change is bounded by e_V Lh_r+V_r e_Lh+e_V e_Lh. These formulas provide a direct route for the saved background/jet uncertainty.
Next derive/control the slow-state coefficient and remainder envelopes on the whole cold interval, preserving the saved uncertainty tube and physical endpoint maps. Then transport the retained original preparation in a common physical frame for GR/spatial-Poisson comparison. No late initial perturbation is chosen here.

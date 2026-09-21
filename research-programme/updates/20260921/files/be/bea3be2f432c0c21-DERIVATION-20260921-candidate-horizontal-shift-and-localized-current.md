# Candidate horizontal-shift variation and the localized Legendre current

Private continuation. Keep the zero-shift action, exact proper clock, common P2 space and full Gram factors unchanged. The off-diagonal prescription is inherited explicitly from `DERIVATION-20260918-moving-P2-current-and-live-evolution.md`, not inferred uniquely from diagonal data. This checkpoint applies it to the current common-space/material-Galerkin candidate.

## 1. The inherited finite nonzero-shift action

Use ds^2=-N^2 dt^2+(dr+beta dt)^2/F+r^2 dOmega^2 and

    c=beta/(N^2 F-beta^2), C=r^2*(N^2 F-beta^2)/(N sqrt(F)),
    T_r=c(T,r), T(s,b(s))=s, J_T=partial_s T at fixed r.

Retain the source-fitted physical mesh on the leaf s, with node speeds W_i=d_i V. Transport every nodal field history by u_i^sharp(s)=u_i(T(s,r_i(s))) and transport C by Cbar=J_T*C(T,r). Then

    d_s u_i^sharp=u_i,t(T_i)*(J_T+c_i W_i).

Evaluate the same finite wave kinetic/gradient and Gram action with these histories/coefficient densities. The source term is -m sqrt(N_b^2-(V+beta_b)^2/F_b). At beta=0 this is exactly the retained action. D and S remain the actual fixed common-space operators; no old uniform-grid stencil is substituted.

For the finite-variation test choose a time-independent connection c=epsilon*h(r). This gives the exact leaf, not a first-order approximation,

    T=s+epsilon*(H(r)-H(b(s))), H'=h,
    J_T=1-epsilon*h(b)*V,
    beta=2*c*N^2*F/(1+sqrt(1+4*c^2*N^2*F)).

The metric in this test is a local jet through the archived metric and its archived time derivative, and the field histories are quadratic jets through the full archived coefficients/rates/accelerations. These tests probe an action derivative, not an independently evolved new spacetime. All retained spatial coefficients are used.

## 2. Raw first variation and source clock

At zero shift put I(r)=integral_b^r delta c. For a general time-dependent variation,

    delta u_i=v_i I_i,
    delta v_i=a_i I_i+v_i*(I_t|r+W_i delta c_i),
    delta Cbar=C_t I+C I_t|r,
    I_t|r=integral_b^r delta c_t - V delta c_b.

For temporally compact variations, integration by parts gives the inherited wave shift covector

    K_wave(R)=-sum_i Eold_i v_i I_(b,r_i)(R)
              -integral C(r)*partial_t Z(r)*I_(b,r)(R) dr,

where Eold=pdot-L_q, I_(a,b)(R)=sign(b-a)*1_(min(a,b)<R<max(a,b)), and Z=delta L_wave/dC is a physical-radius distribution. Temporal boundary work is sum_i p_i v_i I_i+integral C Z I dr and must be retained for noncompact variations. The dust shift covector gives the energy current j_d=m*N^2*V/s delta(r-b), with s=sqrt(N^2-V^2/F). The complete energy current is J_horizontal=K_wave+j_d, and its mass-current conversion at beta=0 is kappa*sqrt(F)/N.

The regular coefficient covector is Z_reg=-[r^4*T_field^2/C^2+g^2]/2, while a Gram atom is Z_i=-load_i/J_i, load=S^T((D u)^2/2). Distinguish the source clock s, leaf parameter s in the inherited notation, map Jacobian J_i and time Jacobian J_T.

## 3. Moving distributions, not a static stencil

At fixed physical radius, partial_t Z contains regular derivatives, all moving P2-face deltas, and moving Gram-atom delta primes. In the current implementation:

    edge contribution to C Z_t = W*(e_right-e_left),
    atom bulk contribution = -gamma*(S^T((D u)*(D v)))_i
                             -V*gamma_b,i*load_i,
    local atom current = W_i*h_i*delta(R-r_i), h_i=gamma_i*load_i.

The material average of the last expression uses the actual inverse-label Jacobian. The source anchor has distinct one-sided spatial Jacobians. Ordinary faces cannot be discarded.

The direct computation uses left primitives below each source and minus right tails above it, then adds the local moving-atom current. It does not define this current from the measured mass tangent or from the localized Legendre current.

## 4. The exact comparison exposes the material-projection question

Use E=L_q-pdot, the opposite sign to Eold. Define the nodally localized residual work

    C_R = integral w(z) [sum_i 1_(r_i(z)<R)*v_i(z)*E_i(z)
                        +1_(b(z)<R)*V(z)*E_b(z)] dz.

E_i(z),E_b(z) are the per-material-layer action residuals, not values reconstructed by assuming the Galerkin residual vanishes pointwise. They include the full Gram force and the exact source inertia. From H_wave=-integral C Z, the whole-layer Noether identity, and the source clock identity, derive

    J_horizontal(R)=Q_R-d_t H_R-C_R.

The previous finite-action Legendre construction instead gives

    J_Legendre(R)=Q_R-d_t H_R-P_R,
    P_R=v^T M_R M^-1 E_Galerkin.

Therefore the explicit compatibility criterion is

    J_horizontal-J_Legendre=P_R-C_R.                 (1)

This is not license to set either residual to zero. A material Galerkin equation only sets integrals against its retained cardinal functions to zero. A sharp physical cut can take a nodal velocity outside that label space. In particular, even if E_Galerkin=0, the cut work C_R requires calculation.

At cuts outside the entire source support, its source mask is constant in z. For field nodes whose entire material extent lies on one side of R, the velocity times mask remains a retained degree14 polynomial. Under the exact Galerkin equations, any surviving C_R can therefore come only from nodes whose material extent crosses the cut. This follows from polynomial test-space orthogonality, not from a numerical observation. For the archived acceleration the uncut/global residual work must also be retained.

If the radial constraints and the compatible inner condition hold, the same propagation argument gives R_horizontal=mu_t+(kappa*sqrt(F)/N)*J_horizontal=-(kappa*sqrt(F)/N)*C_R. Thus the right question for this prescribed extension is a calculable residual/projection term, not an arbitrary fitted flux.

## 5. Predeclared experiment

Reuse reference and both common-space MTS variants, both archived Richardson tangents and both localized quadrature orders8/12, all16,425 components, and exactly the previous five source-free physical cuts plus empty/whole cuts. Evaluate both archived accelerations and the previous fixed-background action accelerations M^-1 B. Recompute per-layer weak Euler work, direct regular/face/atom horizontal current, and compare equation(1) to the independently saved localized current. Test whole-layer Noether accounting without assuming layerwise equations.

Predeclared energy-unit tolerances:2e-11 for the independent horizontal/Legendre/projection identity,2e-11 for current equality as a separate scientific question, and2e-11 for order8/12 differences. Preserve any failed equality test rather than replace the extension. Raw versus finite nonzero-shift action derivatives use a two-step centered Richardson comparison, separated into wave, Gram and dust sectors, with tolerance2e-12+2e-7*abs(raw sector derivative), tightened to an absolute term2e-18 for the separately evaluated tiny Gram sector. The three material-label spot tests use full spatial coefficients; they are not a complete material/time convergence proof.

No new parent uniqueness, arbitrary-coordinate covariance, empirical fit or full time evolution is inferred merely from equality of two finite-action currents. The constructive target is to calculate the actual inherited shift response, quantify any projection term, and determine the next equation from that result.

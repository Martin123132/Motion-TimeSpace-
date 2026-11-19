# Cosmological exchange balance on the retained histories

16 November 2026. Reuse the 33-report window through epoch2924, the original
902 signed preparation nodes, both 32/64 runs, and full/quadratic/difference
histories. This is an exchange diagnostic, not another evolution or a fit.

## Existing ownership and the concrete new comparison

The canonical off-shell scalar source identities already exist in
../mts-action-source-pullback-20261107/DERIVATION.md. The live own-field/metric
equations are owned by ../mts-live-metric-state-20261112/metric_math.py.
The latest surrounding sources are the saved corner-aware histories, not
new closures. We now evaluate their work and the approximation mismatch in
ONE balance on the completed cosmological window, rather than claim those
earlier identities as new.

Stage49's positive quadratic motion/bath action is diagonalized by a constant
orthogonal map into light and heavy eigenmodes. The saved heavy history
already contains that quadratic mixing in its mass and state. Do not add
another g psi X interaction stress in this basis. Its geometric work is
not a direct charged-matter coupling. The finite lattice gauge-current
fixtures are not cosmological stress or source data. Quantum measure terms
are entirely outside this calculation.

## Clock, state and stress

Use native conformal time tau in Mpc, c=1. Retain separately
r=(ln a)' from the saved clock and H from the retained Friedmann readout.
Let b,v be the heavy background, u,w its perturbation, M=(a m_h)^2 and
eta_k the live metric state. Define

    D=v w+M b u,  Q=k v u,  P=v w-M b u,
    z=[(D+D_o)/(2k)+eta_k]/H,
    u'=w+e_u,
    w'=-(M+k^2)u-2H w-k v z+e_w,
    eta_k'=(Q+Q_o)/2+e_eta.

The background defects are f_b=b'-v and f_v=v'+2H v+M b; M'=2rM.
For beta=a/R0, the saved heavy outputs are Y=beta(D,Q,P). Direct product
differentiation gives the GEOMETRIC-clock balance

    Y_D'+3r Y_P+k Y_Q+W = B_D+E_D,
    Y_Q'+r Y_Q-k Y_P   = B_Q+E_Q,
    W=beta k v^2 z,
    B_D=beta[4(r-H)v w+f_v w+M f_b u],
    B_Q=beta[2(r-H)Q+k f_v u],
    E_D=beta[v e_w+M b e_u],  E_Q=beta k v e_u.

These are identities for the retained canonical stress, including its
off-shell/background-representation contacts. In particular setting r=H
or setting the independently interpolated b'=v discards known terms.
They do not declare those canonical variables to be exact continuum
solutions or silently replace the off-shell metric-chain construction.

For the cold control, R_c=C_c/a, D=R_c delta_c, Q=P=0,
delta_c'=-kz+e_c, and Y_D=N_c delta_c. Its corresponding balance is

    Y_D'+N_c k z=N_c e_c.

Cold dust current and pressure vanish in this retained frame; other
baseline sectors do not thereby have zero stress.

## Surrounding-source work and approximation error

The heavy work splits WITHOUT a new parameter:

    W_self=beta v^2 D/(2H),
    W_other_density=beta v^2 D_o/(2H),
    W_eta=beta k v^2 eta_k/H.

Replace beta v^2 by N_c for cold. Q_o enters eta_k' and hence future work;
its absence as a separate instantaneous term in W is not its deletion.
This split depends on the saved perturbative gauge and is not an invariant
assignment of microscopic energy transfer between species.

Write X'=A X+B S with S=(D_o,Q_o). For the original quadratic source S_q
and the corner-aware source S_f=S_q+R, the quadratic trajectory viewed
against the full-source equation has

    e_approx = -B R.

Thus e_w=+v R_D/(2H), e_eta=-R_Q/2 in the heavy case, and
e_c=+R_D/(2H), e_eta=-R_Q/2 for cold. The energy contact is precisely
the difference W_full-W_quadratic at the SAME state. The current-source
error still changes the evolved metric and cannot be discarded.
The separately saved difference state obeys X_delta'=A X_delta+B R;
it is not obtained by noisy subtraction of the two large histories.

## A bounded time-integrated check, without rerunning the history

Reconstruct a diagnostic quintic Hermite state between unchanged reports,
using their states and equation-owned first/second derivatives. Derive
S' from the same frozen integrated curvature cells. Retain the reconstruction
residual e_rec=X_Hermite'-(A X_Hermite+B S), rather than call interpolation
an exact trajectory. This is distinct from e_approx.

Integrate the flux/work, background contacts and e_rec projection with
Gauss-Legendre orders8/16. Compare their sum with actual saved endpoint
stress changes. Report both the balance with contacts and the raw result
with e_rec omitted, against the ORIGINAL saved observable scales and2e-5
gate. Quadrature refinement is a numerical working allowance, not a
rigorous continuum error bound. No interpolation is used to overwrite any
saved state or source grid.

Use all902 nodes with their original signed weights, and retain their
separate local clocks. Weighted geometric factors must be summed nodewise,
not replaced by one averaged H. Reuse native boundary packets for an
independent source/first-derivative comparison at all33 right-edge epochs.

The surrounding native data here close D_o,Q_o forcing, not the complete
pressure/shear evolution of every other species. Therefore this stage
tests the own-subsystem exchange with its environment, not an invented
all-species stress-conservation certificate. Existing full-model sources
remain the authority for any later extension.


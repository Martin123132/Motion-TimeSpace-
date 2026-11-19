# Explicit coupled memory operator for the next test

This derives the next interface; it is not a claim that the coupled integration has been executed. It builds on the retained LIVE-FEEDBACK-LIFT.md and this stage's conditional memory equation. The perturbation system must first be verified linear at fixed homogeneous background. Homogeneous variables are not perturbation-error coordinates and must not be replaced by a correction vector.

Let X denote the original two heavy normal coordinates and r the other perturbations. Write the existing linear parent equations and rest-source readout as

    X'=A X+G L r,
    r'=C X+D r,
    zeta=L r.

All matrices depend on the retained homogeneous background and time. They represent the existing source coupling, not new free coefficients. Set X=T y+h L r, using the same phase-coordinate map as the conditional test. Define

    C_tilde=C T,
    D_tilde=D+C h L,
    Y=L C_tilde,
    W=L'+L D_tilde.

Then r'=C_tilde y+D_tilde r and zeta'=Y y+W r. Substitution into the differentiated coordinate map yields the exact coupled operator on Z=(y,r):

    A_lift = [ T^-1(A T-T'-h Y),  T^-1((A h+G-h')L-h W) ]
             [ C_tilde,           D_tilde                  ].

Let B be the prior effective 2x2 generator and b the effective third-column coefficient before the common -T^-1 h zeta' response is applied. Its corresponding current-state approximation is

    B_lift = [ B-T^-1 h Y,  b L-T^-1 h W ]
             [ C_tilde,     D_tilde       ].

Their difference is particularly useful:

    R_lift = [ T^-1(A T-T')-B,  (T^-1(A h+G-h')-b)L ]
             [ 0,               0                        ].

The explicit zeta' feedback cancels from the remainder because it is retained in both operators. This does not permit deleting that feedback from either evolution. The remaining source-column term is the coupled counterpart of the conditional g; it is not optional.

The forward memory test becomes

    Z0'=B_lift Z0,
    Delta'=B_lift Delta+R_lift Z0, Delta(t0)=0,
    Z1=Z0+Delta,
    E1'=A_lift E1+R_lift Delta, E1(t0)=0.

Even though R_lift has zero rest rows, Delta_r generally becomes nonzero through C_tilde Delta_y. Replacing it by zero would again freeze feedback and would not implement this coupled construction. Initial perturbation data remain the retained parent data; no new occupation or initial correction is fitted.

## Matrix-free implementation contract

1. Keep a single independently evolving homogeneous background. Construct perturbation-only exact and effective operators using the retained current-state native interface and phase map. Test F(0)=0 and superposition at fixed background before treating native calls as matrix-vector products.
2. The existing current metric constraint must determine zeta from r and zeta' from the current parent equations, not a saved future trajectory. Derivatives of L and the map use that same current background and the already checked derivative procedure.
3. Implement R_lift Z as the difference of those two current-state operator actions. Do not evaluate the native nonlinear background equations on Delta as though it were a second universe. Apply the perturbation operators at the common background instead.
4. Integrate Z0 and Delta with zero correction initially. The independently evaluated exact native trajectory is a comparator only. Test changes to that comparator leave both forward RHS blocks unchanged.
5. Use the retained source and signed-pressure readouts on Z1, fixed initial normalization, grids and gates, alongside the actual CDM baseline and step/derivative checks. Only a successful live test would support transferring the conditional result to the parent evolution.

If the retained native representation is affine rather than homogeneous in a particular coordinate, derive and retain its forcing explicitly instead of asserting F(0)=0. This algebra does not settle background averaging, general nonlinear dynamics, state preparation or observational inference; it supplies the specific unfit coupling/memory calculation needed next.

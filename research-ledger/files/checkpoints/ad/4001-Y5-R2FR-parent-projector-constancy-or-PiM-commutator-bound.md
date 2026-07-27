# 4001 - Parent Projector Constancy Or PiM Commutator Bound

Timestamp: `2026-07-01T19:19:44+00:00`

## Result

`Pi_M` is no longer a fuzzy projector word. It has one clean zero route and one explicit failure vector.

Zero route:

`Pi_M:C_H(A_ext)->C_M(A_ext)` is a parent-selected fixed chain-map on the physical Hilbert current complex, on the same annulus, same `tau`, same `e_obs`, same reference, and before readout.

Then

`d(Pi_M J_H)=Pi_M dJ_H + [d,Pi_M]J_H`, and `[d,Pi_M]J_H=0`.

## Constancy Conditions

`D_A Pi_M=0` requires the parent branch to fix `A_ext`, `W_source`, linked surfaces, orientation, `tau`, `e_obs`/Hodge data, reference subtraction, and the `M_H_ref` denominator before any scoring.

A topological/absolute-charge `Pi_M` can be stress-silent. A Hodge, Green, domain, or fitted/readout implementation cannot be used silently; its variation stress or operator bound must be retained.

## Quotient Route

If `Y=(M_H_ref,sigma^a)=Ybar(q(Phi))` and `v_X in ker(Dq)`, then `D_XY=0`, so `C_M` and `C_shape` vanish. This is only a partial projector/source-connection zero unless `H_tau`, `H_ref`, frame, units, and domain/reference clauses are also locked.

## Bound If Closure Fails

`Delta_PiM_4001 = |C_M|+|C_shape|+|C_curl|+|C_domain|+|C_ref|+|C_frame|+|C_units|+|I_commutator_abs|+|projector_stress|+|R_eq_guard|`.

The evaluator refuses both a post-readout mask and a closed wrong current. A closed topological current is not enough unless it is the observed Hilbert/Newton source with the same denominator.

## Evaluator Results

- `CASE4001_0_fixed_chainmap_zero`: status `CONDITIONAL_ZERO_CLAUSES_UNSIGNED`, Delta `0.000000000000e+00`, zero=True, no_readout=True, Hilbert_guard=True, claim=False
- `CASE4001_1_quotient_descent_partial`: status `PARTIAL_ZERO_HTAU_HREF_STILL_OPEN`, Delta `3.000000000000e-06`, zero=False, no_readout=True, Hilbert_guard=True, claim=False
- `CASE4001_2_domain_projector_drift`: status `PROJECTOR_DOMAIN_DRIFT_NONZERO`, Delta `9.000000000000e-05`, zero=False, no_readout=True, Hilbert_guard=True, claim=False
- `CASE4001_3_reference_frame_leak`: status `REFERENCE_FRAME_UNITS_NONZERO`, Delta `1.600000000000e-05`, zero=False, no_readout=True, Hilbert_guard=True, claim=False
- `CASE4001_4_closed_wrong_current_refused`: status `CLOSED_WRONG_CURRENT_NOT_NEWTON_SOURCE`, Delta `0.000000000000e+00`, zero=False, no_readout=True, Hilbert_guard=False, claim=False
- `CASE4001_5_readout_mask_refused`: status `POST_READOUT_PIM_MASK_FORBIDDEN`, Delta `0.000000000000e+00`, zero=False, no_readout=False, Hilbert_guard=True, claim=False
- `CASE4001_6_missing_parent_rows`: status `MISSING_PIM_COMPONENT_VECTOR`, Delta `MISSING`, zero=False, no_readout=True, Hilbert_guard=True, claim=False

## Verdict

This is progress but not a local-GR/Newton claim: the algebraic projector zero branch is sharp, yet current MTS still needs parent signatures or source-backed values for the component vector.

## Next Target

The next best move is `H_tau/H_ref`: prove integrability and source-blind reference lock, or carry `C_curl`, `C_ref`, `C_frame`, and `C_units` as explicit bounds.

- `4002-Y5-R2FR-Htau-Href-integrability-reference-lock-or-curl-bound.md`
- `scripts/Y5_R2FR_4002_Htau_Href_integrability_reference_lock_or_curl_bound.py`

## Source Count

- source needles found: `19/19`
